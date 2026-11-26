def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    wins = sorted({w for c in days for w in days[c]}, key=lambda s: int(s[1:]))
    # book daily returns, chained in window order
    rows = []
    for w in wins:
        frames = []
        for c in days:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        if not frames: continue
        d = pd.concat(frames)
        g = d.groupby("day").agg(book=("book_return","mean"), hold=("coin_return","mean")).dropna().reset_index()
        g["w"]=w; rows.append(g)
    B = pd.concat(rows).reset_index(drop=True)
    B["val"]=(1+B["book"]).cumprod()
    B["peak"]=B["val"].cummax(); B["dd"]=B["val"]/B["peak"]-1
    # find top drawdown episodes
    eps=[]; inep=False
    for i,r in B.iterrows():
        if r.dd<0 and not inep: inep=True; s=i-1 if i>0 else i
        if inep and r.dd==0:
            seg=B.loc[s:i]; eps.append((s,seg.dd.idxmin(),i,seg.dd.min())); inep=False
    if inep: seg=B.loc[s:]; eps.append((s,seg.dd.idxmin(),B.index[-1],seg.dd.min()))
    eps=sorted(eps,key=lambda e:e[3])[:5]
    er=[]
    for s,t,e,m in eps:
        seg=B.loc[s+1:t]
        er.append({"window":B.loc[t,"w"],"depth":m,"days_to_trough":len(seg),"book_sum":seg.book.sum(),"hold_sum":seg.hold.sum(),"worst_day":seg.book.min(),"share_from_worst3":seg.book.nsmallest(3).sum()/seg.book.sum()})
    out["drawdowns"]=pd.DataFrame(er)
    out["book_overall"]=pd.Series({"mean":B.book.mean(),"sd":B.book.std(),"maxdd":B.dd.min(),"n":len(B)})
    # per-case analysis
    cases=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            nxt=cl.shift(-1)/cl-1
            sd20=r.rolling(20).std()
            z=r/sd20
            r5=cl/cl.shift(5)-1; r20=cl/cl.shift(20)-1
            prevdown=(r.shift(1)<0).astype(float)
            vol_ratio=sd20/r.rolling(60,min_periods=40).std()
            rng=(cl-b["low"])/(b["high"]-b["low"])
            alloc=b["postRebalance_current_allocation"]
            df=pd.DataFrame({"coin":c,"w":w,"f":b["forecast"],"z":z,"nxt":nxt,"r":r,"r5_prior":r5.shift(1),"r20":r20,"prevdown":prevdown,"volratio":vol_ratio,"closeloc":rng,"alloc":alloc,"inprof":b["regime"]!="chop","gain":alloc*nxt})
            cases.append(df)
    C=pd.concat(cases).dropna(subset=["nxt"])
    drift=C.groupby("coin")["nxt"].mean()
    C["ex"]=C["nxt"]-C["coin"].map(drift)
    S=C[C.f>0].copy()
    out["n_cases"]=len(S)
    def summ(g):
        return pd.Series({"n":len(g),"mean_ex":g.ex.mean(),"t":g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,"mean_gain":g.gain.mean(),"p5_gain":g.gain.quantile(0.05),"worst_gain":g.gain.min()})
    S["fq"]=pd.qcut(S.f.rank(method="first"),4,labels=["q1","q2","q3","q4"])
    out["by_forecast_q"]=S.groupby("fq").apply(summ)
    out["by_prevdown"]=S.groupby("prevdown").apply(summ)
    S["r5b"]=pd.qcut(S.r5_prior.rank(method="first"),3,labels=["deep","mid","up"])
    out["by_prior5d"]=S.groupby("r5b").apply(summ)
    S["vrb"]=pd.qcut(S.volratio.rank(method="first"),3,labels=["low","mid","high"])
    out["by_volratio"]=S.groupby("vrb").apply(summ)
    S["clb"]=pd.cut(S.closeloc,[-0.01,0.2,0.5,1.01],labels=["at_low","mid","upper"])
    out["by_closeloc"]=S.groupby("clb").apply(summ)
    S["r20b"]=pd.qcut(S.r20.rank(method="first"),3,labels=["deep","mid","shallow"])
    out["by_r20"]=S.groupby("r20b").apply(summ)
    # conditions without signal, in profile
    NS=C[(C.f<=0)&C.inprof]
    NS2=NS.copy(); NS2["clb"]=pd.cut(NS2.closeloc,[-0.01,0.2,0.5,1.01],labels=["at_low","mid","upper"])
    out["nosignal_inprofile_by_closeloc"]=NS2.groupby("clb").apply(lambda g: pd.Series({"n":len(g),"mean_ex":g.ex.mean()}))
    # holding: gain on bars held beyond the signal bar
    H=C[(C.alloc>0)]
    H["sig"]=H.f>0
    out["held_bars_by_signal"]=H.groupby("sig").apply(lambda g: pd.Series({"n":len(g),"mean_gain":g.gain.mean(),"sum_gain":g.gain.sum()}))
    out["by_window_gain"]=C.groupby("w").gain.sum().reindex(wins)
    return out
