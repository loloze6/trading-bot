import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d=df.sort_values("timestamp").reset_index(drop=True)
            c=d["close"].astype(float)
            r=c.pct_change()
            vol=r.pow(2).shift(1).rolling(60,min_periods=20).mean().pow(0.5)
            ts=pd.to_datetime(d["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"pos":np.arange(len(d)),"z":r/vol,
                "f2":c.shift(-2)/c-1,"f3":c.shift(-3)/c-1,"wd":ts.dt.weekday,"year":ts.dt.year,
                "p7":c.shift(1)/c.shift(8)-1,"p7z":(c.shift(1)/c.shift(8)-1)/(vol*np.sqrt(7))}))
    A=pd.concat(rows,ignore_index=True)
    for h in [2,3]:
        m=A[A.pos%h==0].groupby("coin")[f"f{h}"].mean()
        A[f"ex{h}"]=A[f"f{h}"]-A["coin"].map(m)
    def reg(g,x,y):
        g=g.dropna(subset=[x,y])
        if len(g)<30: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        l=stats.linregress(g[x],g[y]); return pd.Series({"n":len(g),"slope":l.slope,"t":l.slope/l.stderr})
    out={}
    for h in [2,3]:
        G=A[A.pos%h==0].dropna(subset=["z",f"ex{h}","p7z"]).copy()
        G["trend"]=np.where(G.p7>0,"up","down")
        out[f"z_slope_by_trend_h{h}"]=G.groupby("trend").apply(lambda g: reg(g,"z",f"ex{h}"))
        G["tq"]=pd.qcut(G.p7z,5,labels=False)
        out[f"z_slope_by_p7z_quintile_h{h}"]=G.groupby("tq").apply(lambda g: reg(g,"z",f"ex{h}"))
        if h==2:
            G["zs"]=pd.cut(G.z,[-np.inf,-1,-0.3,0.3,1,np.inf])
            out["ex2_by_trend_zbin"]=G.groupby(["trend","zs"],observed=True)["ex2"].agg(["count","mean",lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
            out["z_slope_by_trend_year"]=G.groupby(["trend","year"]).apply(lambda g: reg(g,"z","ex2")).unstack(0)
            G["inter"]=G.z*G.p7z
            out["inter_slope"]=reg(G,"inter","ex2")
    return out
