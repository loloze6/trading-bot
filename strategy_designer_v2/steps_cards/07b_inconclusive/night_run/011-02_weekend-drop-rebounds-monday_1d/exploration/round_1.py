import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            d=b[["timestamp","close","volume","forecast","regime"]].copy()
            d["ts"]=pd.to_datetime(d["timestamp"],utc=True,errors="coerce") if not np.issubdtype(d["timestamp"].dtype,np.number) else pd.to_datetime(d["timestamp"],unit="ms",utc=True)
            d["dow"]=d.ts.dt.dayofweek; d["year"]=d.ts.dt.year
            r=d.close.pct_change(); d["r1"]=r
            d["z"]=r/r.rolling(20).std()
            r2=d.close.pct_change(2); d["z2"]=r2/(r.rolling(20).std()*np.sqrt(2))
            d["vr"]=d.volume/d.volume.rolling(20).mean()
            for h in [1,2,3,5]:
                d[f"f{h}"]=d.close.shift(-h)/d.close-1
            d["coin"]=coin; d["w"]=w; d["pos"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # coin mean h-bar return on grid
    for h in [1,2,3,5]:
        m=D[D.pos%h==0].groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"]=D[f"f{h}"]-D.coin.map(m)
    def summ(g,col="x2",zc="z"):
        g=g.dropna(subset=[col,zc])
        dn=g[g[zc]<0]; up=g[g[zc]>0]
        p=(-dn[zc])*dn[col]
        sl=stats.linregress(g[zc],g[col]) if len(g)>5 else None
        return pd.Series({"n_drop":len(dn),"mean_x_drop":dn[col].mean(),"t_drop":stats.ttest_1samp(dn[col],0).statistic,
                          "t_prod_drop":stats.ttest_1samp(p,0).statistic,"mean_x_rise":up[col].mean(),"t_rise":stats.ttest_1samp(up[col],0).statistic,
                          "slope_all":sl.slope if sl else np.nan,"t_slope":(sl.slope/sl.stderr) if sl else np.nan})
    out={}
    out["by_dow_x2"]=D.groupby("dow").apply(summ)
    S=D[D.dow==6]
    out["sun_by_h"]=pd.DataFrame({h:summ(S,f"x{h}") for h in [1,2,3,5]}).T
    out["sun_by_coin"]=S.groupby("coin").apply(summ)
    out["sun_by_year"]=S.groupby("year").apply(summ)
    out["sun_weekend2d_z2"]=summ(S,"x2","z2")
    S2=S.dropna(subset=["vr","z","x2"]); S2=S2[S2.z<0].copy()
    S2["vt"]=pd.qcut(S2.vr,3,labels=["lowvol","mid","highvol"])
    out["sun_drop_by_volterc"]=S2.groupby("vt").apply(lambda g: pd.Series({"n":len(g),"mean_x2":g.x2.mean(),"t":stats.ttest_1samp(g.x2,0).statistic,"t_prod":stats.ttest_1samp(-g.z*g.x2,0).statistic}))
    S2["zt"]=pd.qcut(S2.z,4,labels=["deepest","q2","q3","shallow"])
    out["sun_drop_by_depth"]=S2.groupby("zt").apply(lambda g: pd.Series({"n":len(g),"mean_x2":g.x2.mean(),"t":stats.ttest_1samp(g.x2,0).statistic}))
    M=S[(S.forecast>0)].dropna(subset=["x2"])
    M=M.assign(p=M.forecast/10*M.x2)
    out["main_by_coin"]=M.groupby("coin").p.agg(["count","mean",lambda s: stats.ttest_1samp(s,0).statistic])
    out["main_by_year"]=M.groupby("year").p.agg(["count","mean",lambda s: stats.ttest_1samp(s,0).statistic])
    out["main_all"]=pd.Series({"n":len(M),"t":stats.ttest_1samp(M.p,0).statistic})
    return out
