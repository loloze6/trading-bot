def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy().reset_index(drop=True)
            cl=b["close"]
            b["ret1"]=cl.shift(-1)/cl-1
            b["fwd10"]=cl.shift(-10)/cl-1
            b["trend"]=(b["regime"]=="trending")
            for L in (20,30,60):
                hi=cl.shift(1).rolling(L,min_periods=L).max()
                b[f"d{L}"]=cl/hi-1
            # bars since last trending bar
            idx=np.where(b["trend"].values,np.arange(len(b)),np.nan)
            last=pd.Series(idx).ffill()
            b["since"]=np.arange(len(b))-last
            b["coin"]=c; b["win"]=w; b["pos"]=np.arange(len(b))
            rows.append(b[["coin","win","pos","ret1","fwd10","trend","d20","d30","d60","since"]])
    B=pd.concat(rows)
    cm=B.groupby("coin")["ret1"].mean(); B["ex1"]=B["ret1"]-B["coin"].map(cm)
    G=B[B["pos"]%10==0].copy()
    cm10=G.groupby("coin")["fwd10"].mean(); G["ex10"]=G["fwd10"]-G["coin"].map(cm10)
    out={}
    def tstat(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    for L in (20,30,60):
        bins=[-10,-0.3,-0.2,-0.1,-0.05,0,10]
        out[f"daily excess by dist to {L}d high"]=B.groupby(pd.cut(B[f"d{L}"],bins))["ex1"].apply(tstat).unstack()
        out[f"10d grid excess by dist to {L}d high"]=G.groupby(pd.cut(G[f"d{L}"],bins))["ex10"].apply(tstat).unstack()
    nt=B[~B["trend"]]
    out["daily excess by days since last trending"]=nt.groupby(pd.cut(nt["since"],[0,5,10,20,40,80]))["ex1"].apply(tstat).unstack()
    out["trending daily excess"]=tstat(B.loc[B["trend"],"ex1"])
    out["above 60d high share of bars"]=(B["d60"]>0).mean()
    out["above 30d high share of bars"]=(B["d30"]>0).mean()
    return out
