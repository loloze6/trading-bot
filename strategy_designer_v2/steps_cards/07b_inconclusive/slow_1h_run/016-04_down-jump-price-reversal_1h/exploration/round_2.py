import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            c=df["close"].values.astype(float); n=len(c)
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            for t in range(72,n,72):
                rec={"coin":coin,"w":w,"year":yr[t]}
                for h in (24,72):
                    rec[f"f{h}"]=c[t+h]/c[t]-1 if t+h<n else np.nan
                rr=r[t-71:t+1]
                past=c[t]/c[t-72]-1
                loss=np.sort(-rr[rr<0])[::-1]
                rec["past"]=past
                rec["top3"]=loss[:3].sum() if len(loss) else 0
                rec["lossshare"]=rec["top3"]/loss.sum() if len(loss) else np.nan
                rec["vol"]=np.nanstd(rr)
                rows.append(rec)
    d=pd.DataFrame(rows)
    # coin mean over all grid bars
    for h in (24,72):
        d[f"x{h}"]=d[f"f{h}"]-d.groupby("coin")[f"f{h}"].transform("mean")
    f=d[d.past<0].copy()
    f["top3v"]=f.top3/f.vol
    out={}
    def multi(g,xs,y):
        g=g.dropna(subset=xs+[y])
        X=np.c_[np.ones(len(g)),g[xs].values]
        b,*_=np.linalg.lstsq(X,g[y].values,rcond=None)
        e=g[y].values-X@b; s2=e@e/(len(g)-X.shape[1])
        se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        return pd.DataFrame({"b":b,"t":b/se,"n":len(g)},index=["c"]+xs)
    for y in ("x24","x72"):
        out[f"top3+past->{y}"]=multi(f,["top3","past"],y)
        out[f"lossshare+past->{y}"]=multi(f,["lossshare","past"],y)
    def reg(g,x,y):
        g=g.dropna(subset=[x,y]); s=stats.linregress(g[x],g[y]); return (len(g),s.slope,s.slope/s.stderr)
    out["simple"]=pd.DataFrame({f"{x}->{y}":reg(f,x,y) for x in ["lossshare","top3v"] for y in ["x24","x72"]},index=["n","slope","t"]).T
    f["fall_q"]=pd.qcut(f.past,3,labels=["big","mid","small"])
    out["by fall tercile lossshare->x72"]=pd.DataFrame({k:reg(g,"lossshare","x72") for k,g in f.groupby("fall_q",observed=True)},index=["n","slope","t"]).T
    out["by fall tercile top3->x72"]=pd.DataFrame({k:reg(g,"top3","x72") for k,g in f.groupby("fall_q",observed=True)},index=["n","slope","t"]).T
    big=f[f.fall_q=="big"]
    out["big fall: lossshare tercile"]=big.groupby(pd.qcut(big.lossshare.rank(method="first"),3,labels=False))[["x24","x72","past","lossshare"]].agg(["mean","count"])
    out["all fallen: lossshare tercile"]=f.groupby(pd.qcut(f.lossshare.rank(method="first"),3,labels=False))[["x24","x72","past"]].mean()
    out["by coin lossshare+past x72"]=pd.DataFrame({k:multi(g,["lossshare","past"],"x72").loc["lossshare",["b","t","n"]] for k,g in f.groupby("coin")}).T
    out["by year lossshare+past x72"]=pd.DataFrame({k:multi(g,["lossshare","past"],"x72").loc["lossshare",["b","t","n"]] for k,g in f.groupby("year")}).T
    return out
