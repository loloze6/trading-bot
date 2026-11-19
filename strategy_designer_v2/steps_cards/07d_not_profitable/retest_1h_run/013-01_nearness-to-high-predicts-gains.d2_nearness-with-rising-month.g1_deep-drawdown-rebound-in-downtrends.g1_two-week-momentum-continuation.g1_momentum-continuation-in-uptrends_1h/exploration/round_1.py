def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted({w for c in coins for w in days[c].keys()}, key=lambda s: int(s[1:]))
    # book daily
    series = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day")[["book_return","coin_return"]].mean().sort_index()
        g["win"]=w
        series.append(g)
    s = pd.concat(series).reset_index(drop=True).dropna(subset=["book_return"])
    v = (1+s["book_return"]).cumprod(); peak=v.cummax(); dd=v/peak-1
    s["dd"]=dd.values
    # identify drawdown episodes deeper than 5%
    trough = dd.idxmin(); pk = v.loc[:trough].idxmax()
    out["deepest_dd"]=pd.Series({"depth":dd.min(),"peak_win":s.loc[pk,"win"],"trough_win":s.loc[trough,"win"],"days":trough-pk,
        "book_ret_in_fall":v.loc[trough]/v.loc[pk]-1,"coin_ret_in_fall":(1+s.loc[pk+1:trough,"coin_return"]).prod()-1})
    n=len(s); yr=v.iloc[-1]**(365/n)-1
    out["calmar_parts"]=pd.Series({"yearly":yr,"maxdd":dd.min(),"ndays":n})
    pw = s.groupby("win").agg(book=("book_return",lambda x:(1+x).prod()-1),coin=("coin_return",lambda x:(1+x).prod()-1),mindd=("dd","min"))
    out["per_window"]=pw
    # worst 20 days distribution vs coin
    s["bk"]=s["book_return"]
    worst = s.nsmallest(30,"bk")
    out["worst30_days"]=pd.Series({"mean_book":worst.bk.mean(),"mean_coin":worst.coin_return.mean(),"share_coin_neg":(worst.coin_return<0).mean(),"sum_book":worst.bk.sum(),"sum_all":s.bk.sum()})
    # grid analysis
    rows=[]
    for c in coins:
        for w,b in bars[c].items():
            cl=b["close"].values.astype(float); n=len(cl)
            al=b["postRebalance_current_allocation"].values.astype(float)
            hr=np.r_[np.diff(cl)/cl[:-1],np.nan]
            gain=al*hr
            hi=pd.Series(b["high"].values).rolling(336).max().values
            vol=pd.Series(np.r_[np.nan,np.diff(np.log(cl))]).rolling(168).std().values
            vol30=pd.Series(np.r_[np.nan,np.diff(np.log(cl))]).rolling(720).std().values
            reg=b["regime"].values
            for i in range(0,n-168,168):
                r14 = cl[i]/cl[i-336]-1 if i>=336 else np.nan
                r1d = cl[i]/cl[i-24]-1 if i>=24 else np.nan
                r60 = cl[i]/cl[i-1440]-1 if i>=1440 else np.nan
                rows.append(dict(coin=c,win=w,reg=reg[i],alloc=al[i],fwd=cl[i+168]/cl[i]-1,
                   pg=np.nansum(gain[i:i+168]),r14=r14,r1d=r1d,r60=r60,dist=cl[i]/hi[i]-1,vol=vol[i],volr=vol[i]/vol30[i]))
    g=pd.DataFrame(rows)
    a=g[g.alloc.abs()>1e-6].copy()
    out["n_grid_active"]=len(a)
    def tab(col,q=5):
        x=a.dropna(subset=[col]).copy()
        x["b"]=pd.qcut(x[col],q,labels=False,duplicates="drop")
        return x.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("pg","size"),pg=("pg","mean"),p10=("pg",lambda z:z.quantile(.1)),fwd=("fwd","mean"),alloc=("alloc","mean"))
    for col in ["r14","r60","dist","vol","volr","r1d"]:
        out["by_"+col]=tab(col)
    return out
