def explore(data):
    import pandas as pd, numpy as np
    out = {}
    # book daily returns: per window, mean across coins per day
    coins = list(data["days"].keys())
    wins = sorted(set(w for c in coins for w in data["days"][c]), key=lambda s:int(s[1:]))
    chain=[]; wl=[]
    percoin_dd = {}
    for w in wins:
        frames=[]
        for c in coins:
            if w in data["days"][c]:
                d=data["days"][c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        df=pd.concat(frames)
        g=df.groupby("day").agg(b=("book_return","mean"),h=("coin_return","mean")).dropna().sort_index()
        g["w"]=w; chain.append(g)
    ch=pd.concat(chain).reset_index(drop=True)
    eq=(1+ch.b).cumprod(); peak=eq.cummax(); dd=eq/peak-1
    ch["dd"]=dd
    out["max_dd"]=float(dd.min())
    out["yearly"]=float(eq.iloc[-1]**(365/len(ch))-1)
    # dd by window: deepest point and window return
    ww=ch.groupby("w").agg(book=("b",lambda x:(1+x).prod()-1),hold=("h",lambda x:(1+x).prod()-1),mindd=("dd","min"),days=("b","size"))
    # within-window own drawdown
    def wdd(x):
        e=(1+x).cumprod(); return float((e/e.cummax()-1).min())
    ww["own_dd"]=ch.groupby("w").b.apply(wdd)
    out["windows"]=ww.reindex(wins)
    # deepest drawdown episode: start/end positions
    trough=int(dd.idxmin()); start=int(eq[:trough+1].idxmax())
    out["episode"]=pd.Series({"start_w":ch.w[start],"trough_w":ch.w[trough],"days":trough-start,"hold_ret_in_episode":float((1+ch.h[start+1:trough+1]).prod()-1)})
    # trades features
    rows=[]
    for c in coins:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            cl=b.close
            r24=cl/cl.shift(24)-1
            mabs=r24.abs().rolling(720,min_periods=200).mean()
            f=r24/mabs
            r30=cl/cl.shift(720)-1
            r7=cl/cl.shift(168)-1
            vol=cl.pct_change().rolling(168).std(); volL=cl.pct_change().rolling(1440,min_periods=500).std()
            hi30=cl.rolling(720,min_periods=200).max(); dfh=cl/hi30-1
            fwd=cl.shift(-72)/cl-1
            t=data["trades"][c].get(w)
            if t is None or len(t)==0: continue
            ts=pd.to_datetime(b.timestamp)
            for _,tr in t.iterrows():
                et=pd.to_datetime(tr.entry_time)
                i=ts.searchsorted(et)
                if i>=len(b): continue
                rows.append(dict(coin=c,w=w,pnl=tr.net_profit_loss_percent,dur=tr.duration_minutes/60,
                                 f=f[i],r30=r30[i],r7=r7[i],volr=vol[i]/volL[i] if volL[i] else np.nan,dfh=dfh[i],
                                 ef=tr.entry_forecast))
    T=pd.DataFrame(rows)
    out["trades_summary"]=pd.Series({"n":len(T),"mean_pnl":T.pnl.mean(),"win":(T.pnl>0).mean(),"mean_dur_h":T.dur.mean(),"p5":T.pnl.quantile(.05)})
    for col in ["f","r30","r7","volr","dfh","ef"]:
        q=pd.qcut(T[col],5,duplicates="drop")
        out["by_"+col]=T.groupby(q).pnl.agg(["count","mean","std",lambda x:(x<-10).mean()])
    out["by_coin"]=T.groupby("coin").pnl.agg(["count","mean","std","min"])
    return out
