import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(b)
            cs=pd.Series(c)
            r28=(cs/cs.shift(28)-1).values
            lo=cs.rolling(60,min_periods=20).min(); hi=cs.rolling(60,min_periods=20).max()
            pos60=((cs-lo)/(hi-lo)).values
            lr=np.log(cs).diff()
            vol20=(lr.rolling(20).std()*np.sqrt(365)).values
            f=b["forecast"].fillna(0).values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            for i in range(0,n,10):
                rec={"coin":coin,"w":w,"yr":yr[i],"f":f[i],"r28":r28[i],"pos60":pos60[i],"vol20":vol20[i]}
                for h in (5,10):
                    rec[f"r{h}"]=c[i+h]/c[i]-1 if i+h<n else np.nan
                rows.append(rec)
    d=pd.DataFrame(rows)
    for h in (5,10):
        d[f"u{h}"]=d[f"r{h}"]-d.groupby("coin")[f"r{h}"].transform("mean")
    def slope(g,y="u10",x="f"):
        g=g[[x,y]].dropna()
        if len(g)<10 or g[x].std()==0: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        r=stats.linregress(g[x],g[y]); return pd.Series({"n":len(g),"slope":r.slope,"t":r.slope/r.stderr})
    out={}
    out["u5_by_coin"]=d.groupby("coin").apply(lambda g: slope(g,"u5"))
    out["u5_by_year"]=d.groupby("yr").apply(lambda g: slope(g,"u5"))
    dd=d.dropna(subset=["r28"]).copy()
    dd["q"]=pd.qcut(dd.r28.rank(method="first"),5,labels=False)
    out["r28_quint"]=dd.groupby("q").agg(n=("u10","count"),r28=("r28","mean"),u5=("u5","mean"),u10=("u10","mean"))
    dp=d.dropna(subset=["pos60"]).copy()
    dp["q"]=pd.qcut(dp.pos60.rank(method="first"),5,labels=False)
    out["pos60_quint"]=dp.groupby("q").agg(n=("u10","count"),pos=("pos60","mean"),u5=("u5","mean"),u10=("u10","mean"))
    dv=d.dropna(subset=["vol20"]).copy()
    dv["vq"]=dv.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["slope_by_volterc"]=dv.groupby("vq").apply(slope)
    out["slope_raw_r28_by_volterc"]=dv.groupby("vq").apply(lambda g: slope(g,"u10","r28"))
    return out
