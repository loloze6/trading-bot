def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; coins = list(bars.keys())
    B = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            b["coin"]=c; b["wn"]=int(w[1:])
            b["pos"]=np.arange(len(b))
            rng=(b["high"]-b["low"])/b["close"]
            b["rr"]=rng/rng.rolling(30).mean()
            b["ma100"]=b["close"]/b["close"].rolling(100,min_periods=50).mean()-1
            b["ma50"]=b["close"]/b["close"].rolling(50,min_periods=30).mean()-1
            b["ret60"]=b["close"]/b["close"].shift(60)-1
            b["f10"]=b["close"].shift(-10)/b["close"]-1
            b["nr"]=b["close"].shift(-1)/b["close"]-1
            b["gain"]=b["postRebalance_current_allocation"]*b["nr"]
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            B.append(b)
    B=pd.concat(B,ignore_index=True)
    mu=B[B["pos"]%10==0].groupby("coin")["f10"].mean()
    B["x10"]=B["f10"]-B["coin"].map(mu)
    G=B[B["pos"]%10==0].dropna(subset=["x10"])
    def summ(s):
        s=s.dropna(); n=len(s)
        return pd.Series({"n":n,"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
    for f in ["ma100","ma50","ret60"]:
        G2=G.dropna(subset=[f]).copy()
        G2["side"]=np.where(G2[f]>0,"up","down")
        G2["act"]=np.where(G2["forecast"]>0,"signal","no signal")
        out[f"x10 by {f} side x signal"]=G2.groupby(["side","act"])["x10"].apply(summ).unstack().round(4)
        out[f"share of {f} known on active grid"]=round(G2.shape[0]/G.shape[0],3)
    # within up-side, graded by rr?
    G2=G.dropna(subset=["ma50"]); A=G2[(G2["forecast"]>0)&(G2["ma50"]>0)].copy()
    A["rrq"]=pd.qcut(A["rr"],3,labels=["lo","mid","hi"])
    out["signal & ma50 up: by rr tercile"]=A.groupby("rrq")["x10"].apply(summ).unstack().round(4)
    A=G2[(G2["forecast"]>0)&(G2["ma50"]<=0)].copy()
    A["rrq"]=pd.qcut(A["rr"],3,labels=["lo","mid","hi"])
    out["signal & ma50 down: by rr tercile"]=A.groupby("rrq")["x10"].apply(summ).unstack().round(4)
    # pseudo-books (before cost), NaN filter -> keep position
    def book(mask):
        g=B["gain"].where(mask,0.0)
        df=pd.DataFrame({"wn":B["wn"],"day":B["day"],"g":g}).dropna()
        P=df.groupby(["wn","day"])["g"].mean().reset_index().sort_values(["wn","day"])
        v=(1+P["g"]).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(P))-1
        sh=P["g"].mean()/P["g"].std()*np.sqrt(365)
        inpos=(B["postRebalance_current_allocation"].abs()>0)&mask
        return pd.Series({"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"sharpe":sh,"share in pos":inpos.mean()})
    res={"full":book(pd.Series(True,index=B.index))}
    for f in ["ma100","ma50","ret60"]:
        res[f"out when {f}<=0"]=book(~(B[f]<=0))
    out["pseudo books before cost"]=pd.DataFrame(res).T.round(4)
    # by year: gain on ma50 down vs up days
    B["yr"]=B["day"].dt.year
    B["ma50s"]=np.where(B["ma50"].isna(),"na",np.where(B["ma50"]>0,"up","down"))
    out["mean daily pos gain by ma50 side"]=B.groupby("ma50s")["gain"].agg(["mean","count"]).round(5)
    out["mean daily pos gain by year x ma50 side"]=B.groupby(["yr","ma50s"])["gain"].mean().unstack().round(5)
    return out
