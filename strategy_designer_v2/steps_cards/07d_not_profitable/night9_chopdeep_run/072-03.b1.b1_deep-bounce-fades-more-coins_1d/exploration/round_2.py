def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; trades=data["trades"]
    rows=[]
    for coin,ws in bars.items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); r1=c.pct_change()
            hi=c.rolling(20,min_periods=20).max(); sd=r1.rolling(20,min_periods=20).std()
            b["depth"]=(c/hi-1)/sd
            b["f10"]=c.shift(-10)/c-1
            b["ret20"]=c/c.shift(20)-1
            b["ret5"]=c/c.shift(5)-1
            b["up"]=r1>0
            vol30=r1.rolling(30,min_periods=30).std()
            b["vol30"]=vol30
            b["coin"]=coin; b["w"]=w; b["pos"]=np.arange(len(b))
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["nxt"]=c.shift(-1)/c-1
            rows.append(b)
    A=pd.concat(rows,ignore_index=True)
    drift=A[A.pos%10==0].groupby("coin")["f10"].mean()
    A["d10"]=A["f10"]-A["coin"].map(drift)
    A["choppy"]=A["regime"].isin(["mean_reversion","unknown"])
    A["sig"]=A["forecast"]<0
    G=A[(A.pos%10==0)&A.f10.notna()&A.choppy&A.up&A.depth.notna()].copy()
    out={}
    G["dq"]=pd.qcut(G["depth"],4,labels=["deep","q2","q3","shallow"])
    def summ(g):
        return pd.Series({"n":len(g),"d10":g.d10.mean(),"t":stats.ttest_1samp(g.d10,0).statistic if len(g)>2 else np.nan,"share_sig":g.sig.mean(),"mean_fc":g.forecast.mean(),"mean_depth":g.depth.mean()})
    out["choppy up grid: raw depth quartile"]=G.groupby("dq").apply(summ)
    out["choppy up grid: raw depth quartile x signal"]=G.groupby(["dq","sig"]).apply(summ)
    G["neg20"]=G.ret20<0
    out["choppy up grid: ret20<0 x signal"]=G.groupby(["neg20","sig"]).apply(summ)
    out["choppy up grid: ret20<0 x raw depth half"]=G.groupby(["neg20",G.depth<G.depth.median()]).apply(summ)
    # graded raw-depth measure: corr of depth with d10 within neg20
    cc={}
    for k,g in G.groupby("neg20"):
        r=stats.spearmanr(g.depth,g.d10); cc[str(k)]={"n":len(g),"spearman":r.correlation,"p":r.pvalue}
    r=stats.spearmanr(G.depth,G.d10); cc["all"]={"n":len(G),"spearman":r.correlation,"p":r.pvalue}
    out["spearman raw depth vs d10"]=pd.DataFrame(cc).T
    # forecast vs raw depth relation on signal bars
    S=A[A.sig&A.depth.notna()]
    out["signal bars: raw depth quartile counts"]=pd.qcut(S.depth,4).value_counts().sort_index().astype(str).to_frame("n") if len(S) else "none"
    out["corr forecast vs raw depth (signal bars)"]=float(np.corrcoef(S.forecast,S.depth)[0,1])
    # book daily gain from positions, split by state at bar
    P=A[A.postRebalance_current_allocation.abs()>1e-6].copy()
    P["g"]=P.postRebalance_current_allocation*P.nxt
    P["neg20"]=P.ret20<0
    out["position bars gain by ret20<0"]=P.groupby("neg20")["g"].agg(["mean","count","sum"])
    out["position bars gain by window"]=P.groupby("w")["g"].agg(["mean","count","sum"])
    P["dq"]=pd.qcut(P.depth,4,labels=["deep","q2","q3","shallow"])
    out["position bars gain by raw depth quartile"]=P.groupby("dq")["g"].agg(["mean","count","sum"])
    # trades
    T=[]
    for coin,ws in trades.items():
        for w,t in ws.items():
            if len(t)==0: continue
            t=t.copy(); t["coin"]=coin; T.append(t)
    T=pd.concat(T)
    out["trades summary"]=pd.DataFrame({"n":[len(T)],"mean_gross":[T.profit_loss_percent.mean()],"mean_net":[T.net_profit_loss_percent.mean()],"mean_days":[T.duration_minutes.mean()/1440],"win":[(T.net_profit_loss_percent>0).mean()]})
    T["dur_bin"]=pd.cut(T.duration_minutes/1440,[0,5,10,15,30,1000])
    out["trades by duration"]=T.groupby("dur_bin")["net_profit_loss_percent"].agg(["mean","count"])
    return out
