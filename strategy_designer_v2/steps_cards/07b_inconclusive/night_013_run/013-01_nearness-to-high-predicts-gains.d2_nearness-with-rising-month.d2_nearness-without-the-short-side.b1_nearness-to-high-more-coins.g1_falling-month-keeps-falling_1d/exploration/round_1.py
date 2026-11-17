import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    H=[1,3,7,14,30]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].values
            n=len(c)
            r30=pd.Series(c).pct_change(30).values
            for h in H:
                for i in range(0,n-h,h if h!=7 else 7):
                    pass
            for i in range(0,n,7):
                rec={"coin":coin,"w":w,"year":pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "reg":df["regime"].iloc[i],"fc":df["forecast"].iloc[i],
                     "depth":df.get("debug_info.components.depth.last_history_value",pd.Series([np.nan]*n)).iloc[i],
                     "r30":r30[i]}
                for h in H:
                    rec[f"r{h}"]=c[i+h]/c[i]-1 if i+h<n else np.nan
                rows.append(rec)
    d=pd.DataFrame(rows)
    for h in H:
        d[f"x{h}"]=d[f"r{h}"]-d.groupby("coin")[f"r{h}"].transform("mean")
    m=d[d.reg=="mean_reversion"].copy()
    def slope(g,y="x7",x="fc"):
        g=g[[x,y]].dropna()
        if len(g)<10 or g[x].std()==0: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        r=stats.linregress(g[x],g[y])
        return pd.Series({"n":len(g),"slope":r.slope,"t":r.slope/r.stderr})
    out={}
    out["by_horizon"]=pd.DataFrame({f"h{h}":slope(m,y=f"x{h}") for h in H}).T
    out["by_horizon_rawdepth"]=pd.DataFrame({f"h{h}":slope(m,y=f"x{h}",x="depth") for h in H}).T
    out["by_year"]=m.groupby("year").apply(slope)
    out["by_coin"]=m.groupby("coin").apply(slope)
    m["fq"]=pd.qcut(m["fc"].rank(method="first"),5,labels=False)
    out["by_fc_quint"]=m.groupby("fq").agg(n=("x7","count"),fc=("fc","mean"),depth=("depth","mean"),x7=("x7","mean"),x7sd=("x7","std"))
    m["dq"]=pd.qcut(m["depth"].rank(method="first"),5,labels=False)
    out["by_depth_quint"]=m.groupby("dq").agg(n=("x7","count"),depth=("depth","mean"),x7=("x7","mean"),x14=("x14","mean"),x30=("x30","mean"))
    m["r30q"]=pd.qcut(m["r30"].rank(method="first"),3,labels=False)
    out["by_r30_tercile"]=m.groupby("r30q").apply(slope)
    out["by_r30_tercile_depth"]=m.groupby("r30q").apply(lambda g: slope(g,x="depth"))
    nm=d[d.reg!="mean_reversion"]
    out["all_regimes_raw_r7_vs_r30"]=pd.DataFrame({"mr":slope(m,y="x7",x="r30"),"other":slope(nm,y="x7",x="r30")}).T
    return out
