import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            c=df["close"].values.astype(float); n=len(c)
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            fc=df["forecast"].values.astype(float)
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            for t in range(0,n,72):
                rec={"coin":coin,"w":w,"t":t,"year":yr[t]}
                for h in (24,72,168):
                    rec[f"f{h}"]=c[t+h]/c[t]-1 if t+h<n else np.nan
                if t>=72:
                    past=c[t]/c[t-72]-1
                    rr=r[t-71:t+1]
                    loss=np.sort(-rr[rr<0])[::-1]
                    rec["past"]=past
                    rec["top3"]=loss[:3].sum() if len(loss) else 0
                    rec["share"]=rec["top3"]/abs(past) if past<0 else np.nan
                    rec["fc"]=fc[t]
                    rec["vol"]=np.nanstd(rr)
                rows.append(rec)
    d=pd.DataFrame(rows)
    for h in (24,72,168):
        d[f"x{h}"]=d[f"f{h}"]-d.groupby("coin")[f"f{h}"].transform("mean")
    f=d[(d.past<0)].dropna(subset=["x72"]).copy()
    out={}
    def reg(g,x,y):
        g=g.dropna(subset=[x,y])
        if len(g)<10: return (len(g),np.nan,np.nan)
        s=stats.linregress(g[x],g[y]); return (len(g),s.slope,s.slope/s.stderr)
    res={}
    for x in ["fc","share","past","top3"]:
        for y in ["x24","x72","x168"]:
            res[f"{x}->{y}"]=reg(f,x,y)
    out["regs"]=pd.DataFrame(res,index=["n","slope","t"]).T
    f["lshare"]=np.log(f.share.clip(lower=1e-6))
    # multiple regression share + past
    g=f.dropna(subset=["x72","lshare","past"])
    X=np.c_[np.ones(len(g)),g.lshare,g.past,g.vol]
    b,*_=np.linalg.lstsq(X,g.x72,rcond=None)
    e=g.x72-X@b; s2=e@e/(len(g)-4); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["multi lshare,past,vol"]=pd.DataFrame({"b":b,"t":b/se},index=["c","lshare","past","vol"])
    f["fall_q"]=pd.qcut(f.past,3,labels=["big","mid","small"])
    f["sh_q"]=f.groupby("fall_q",observed=True)["share"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["fallq x shareq mean x72"]=f.pivot_table(index="fall_q",columns="sh_q",values="x72",aggfunc="mean",observed=True)
    out["fallq x shareq count"]=f.pivot_table(index="fall_q",columns="sh_q",values="x72",aggfunc="count",observed=True)
    out["by coin share->x72"]=pd.DataFrame({k:reg(g2,"lshare","x72") for k,g2 in f.groupby("coin")},index=["n","slope","t"]).T
    out["by year share->x72"]=pd.DataFrame({k:reg(g2,"lshare","x72") for k,g2 in f.groupby("year")},index=["n","slope","t"]).T
    out["lshare->"]=pd.DataFrame({y:reg(f,"lshare",y) for y in ["x24","x72","x168"]},index=["n","slope","t"]).T
    out["share quintile x72"]=f.groupby(pd.qcut(f.share.rank(method="first"),5,labels=False))[["x72","past","share"]].mean()
    out["corr fc share"]=f[["fc","share","lshare","past"]].corr(method="spearman")
    return out
