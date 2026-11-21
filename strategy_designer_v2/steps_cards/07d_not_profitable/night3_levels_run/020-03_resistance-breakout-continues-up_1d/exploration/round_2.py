def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted(days[coins[0]].keys(), key=lambda w: int(w[1:]))
    chain = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy(); frames.append(d)
        g = pd.concat(frames).groupby("day")[["book_return","coin_return"]].mean().dropna().sort_index()
        g["win"]=w; chain.append(g)
    ch = pd.concat(chain).reset_index(drop=True)
    v=(1+ch.book_return).cumprod(); peak=v.cummax(); dd=v/peak-1
    tmin=int(dd.idxmin()); tpk=int(v[:tmin+1].idxmax())
    out["deepest_episode"]=pd.Series({"peak_win":ch.win[tpk],"trough_win":ch.win[tmin],"days":tmin-tpk,
        "book_sum":ch.book_return[tpk:tmin+1].sum(),"coin_sum":ch.coin_return[tpk:tmin+1].sum()})
    # within-window falls of pooled book
    rows=[]
    for w in wins:
        s=ch[ch.win==w]; vv=(1+s.book_return).cumprod(); cv=(1+s.coin_return).cumprod()
        rows.append((w,float((vv/vv.cummax()-1).min()),float(vv.iloc[-1]-1),float(cv.iloc[-1]-1)))
    out["window_falls"]=pd.DataFrame(rows,columns=["win","book_dd","book_ret","coin_ret"]).set_index("win").round(3)
    # failed breakouts and per-trade path
    rows=[]
    for c in coins:
        for w in wins:
            b=bars[c][w].reset_index(drop=True)
            cl=b.close.values; a=b.postRebalance_current_allocation.fillna(0).values
            pa=b.previous_allocation.fillna(0).values
            s=pd.Series(cl)
            ma50=s.rolling(50,min_periods=30).mean().values
            r30=s.pct_change(30).values
            for t in range(1,len(b)):
                if a[t]>0 and pa[t]<=0 and t+10<len(b):
                    lvl=cl[t-1]
                    back1=cl[t+1]<lvl; back2=min(cl[t+1],cl[t+2])<lvl
                    rows.append(dict(coin=c,win=w,r5=cl[t+5]/cl[t]-1,
                        r2_5=cl[t+5]/cl[t+2]-1, r2_10=cl[t+10]/cl[t+2]-1,
                        back2=back2, back1=back1,
                        below_ma=cl[t]<ma50[t] if ma50[t]==ma50[t] else np.nan,
                        r30=r30[t], alloc=a[t]))
    e=pd.DataFrame(rows)
    def summ(g,col):
        return pd.Series({"n":len(g),"mean":g[col].mean(),"t":stats.ttest_1samp(g[col],0).statistic if len(g)>2 else np.nan})
    out["after_day2_by_fellback"]=pd.DataFrame({k:summ(g,"r2_5") for k,g in e.groupby("back2")}).T.round(4)
    out["after_day2_10_by_fellback"]=pd.DataFrame({k:summ(g,"r2_10") for k,g in e.groupby("back2")}).T.round(4)
    out["r5_by_fellback_day1"]=pd.DataFrame({k:summ(g,"r5") for k,g in e.groupby("back1")}).T.round(4)
    e2=e.dropna(subset=["below_ma"])
    out["r5_by_below_ma50"]=pd.DataFrame({k:summ(g,"r5") for k,g in e2.groupby("below_ma")}).T.round(4)
    e3=e.dropna(subset=["r30"]); q=pd.qcut(e3.r30.rank(method="first"),5,labels=False)
    out["r5_by_r30_q"]=e3.groupby(q).agg(x=("r30","median"),r5=("r5","mean"),sd=("r5","std"),n=("r5","size")).round(4)
    # book daily return by coin's 30d trend state (all bars)
    rows=[]
    for c in coins:
        for w in wins:
            b=bars[c][w].reset_index(drop=True); s=b.close
            pos=b.postRebalance_current_allocation.fillna(0)
            g=pos*(s.shift(-1)/s-1)
            rows.append(pd.DataFrame({"g":g,"pos":pos,"r30":s.pct_change(30),"vol":s.pct_change().rolling(20).std()}))
    A=pd.concat(rows).dropna()
    A["q"]=pd.qcut(A.r30.rank(method="first"),5,labels=False)
    out["gain_by_r30"]=A.groupby("q").agg(r30=("r30","median"),gain=("g","mean"),gain_sd=("g","std"),pos=("pos","mean")).round(5)
    A["qv"]=pd.qcut(A.vol.rank(method="first"),5,labels=False)
    out["gain_by_vol"]=A.groupby("qv").agg(vol=("vol","median"),gain=("g","mean"),gain_sd=("g","std"),pos=("pos","mean")).round(5)
    return out
