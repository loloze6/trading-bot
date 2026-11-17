def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            b["fwd7"]=c.shift(-7)/c-1
            b["past7"]=c/c.shift(7)-1
            b["past30"]=c/c.shift(30)-1
            b["vr"]=b["volume"]/b["volume"].rolling(20).mean()
            ts=pd.to_datetime(b["timestamp"])
            b["wd"]=ts.dt.weekday; b["yr"]=ts.dt.year
            b["r1"]=r.shift(-1)
            b["coin"]=coin; b["win"]=w; b["pos"]=np.arange(len(b))
            rows.append(b[["coin","win","pos","fwd7","past7","past30","vr","wd","yr","r1"]])
    A=pd.concat(rows)
    cm=A[A.pos%7==0].groupby("coin")["fwd7"].mean()
    A["ex7"]=A["fwd7"]-A["coin"].map(cm)
    d1m=A.dropna(subset=["r1"]).groupby("coin")["r1"].mean()
    A["ex1"]=A["r1"]-A["coin"].map(d1m)
    G=A[A.pos%7==0].dropna(subset=["ex7"])
    out={}
    def sl(d,col):
        d=d.dropna(subset=[col,"ex7"])
        if len(d)<30: return pd.Series({"slope":np.nan,"t":np.nan,"n":len(d)})
        x=(d[col]-d[col].mean())/d[col].std()
        res=stats.linregress(x,d["ex7"]); return pd.Series({"slope":res.slope,"t":res.slope/res.stderr,"n":len(d)})
    R=G[G.past30>0]
    out["rising30 past7 slope by coin"]=pd.DataFrame({c:sl(g,"past7") for c,g in R.groupby("coin")}).T
    out["rising30 past7 slope by year"]=pd.DataFrame({y:sl(g,"past7") for y,g in R.groupby("yr")}).T
    Rq=R.dropna(subset=["past7"]).copy()
    Rq["q"]=pd.qcut(Rq["past7"].rank(method="first"),5,labels=False)
    g=Rq.groupby("q")["ex7"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["rising30 past7 quint"]=g.drop(columns="std")
    # weekday robustness: Fri bar (wd4) and Thu (wd3) vs rest
    W=A.dropna(subset=["ex1"])
    def wt(d):
        a=d[d.wd.isin([3,4])]["ex1"]; b=d[~d.wd.isin([3,4])]["ex1"]
        t=stats.ttest_ind(a,b,equal_var=False)
        return pd.Series({"thufri":a.mean(),"rest":b.mean(),"t":t.statistic,"n":len(a)})
    out["thu/fri bar next-day by coin"]=pd.DataFrame({c:wt(g) for c,g in W.groupby("coin")}).T
    out["thu/fri bar next-day by year"]=pd.DataFrame({y:wt(g) for y,g in W.groupby("yr")}).T
    # graded weekday? by abs-weighted: next-day after wd by sign of today's move
    # volume ratio robustness
    out["vr slope by coin"]=pd.DataFrame({c:sl(g,"vr") for c,g in G.groupby("coin")}).T
    out["vr slope by year"]=pd.DataFrame({y:sl(g,"vr") for y,g in G.groupby("yr")}).T
    return out
