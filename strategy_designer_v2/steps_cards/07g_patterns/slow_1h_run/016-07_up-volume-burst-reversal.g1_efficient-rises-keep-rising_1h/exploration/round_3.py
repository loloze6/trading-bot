def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r1=c.pct_change(); vol30=r1.rolling(720).std()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"yr":ts.dt.year,
                "z6":(c/c.shift(6)-1)/(vol30*np.sqrt(6)),
                "z12":(c/c.shift(12)-1)/(vol30*np.sqrt(12)),
                "z24":(c/c.shift(24)-1)/(vol30*np.sqrt(24)),
                "f12":c.shift(-12)/c-1,"f24":c.shift(-24)/c-1})
            rows.append(d.iloc[::24])
    D=pd.concat(rows).dropna()
    D["y"]=D["f24"]-D.groupby("coin")["f24"].transform("mean")
    D["y12"]=D["f12"]-D.groupby("coin")["f12"].transform("mean")
    def slope(x,xc,yc="y"):
        s=stats.linregress(x[xc],x[yc]); return pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(x)})
    out["slope next24 on z6/z12/z24 pooled"]=pd.DataFrame({k:slope(D,k) for k in ["z6","z12","z24"]}).T
    out["slope next12 on z6 pooled"]=slope(D,"z6","y12").to_frame().T
    out["slope next24 on z6 by coin"]=D.groupby("coin").apply(lambda x: slope(x,"z6"))
    out["slope next24 on z6 by year"]=D.groupby("yr").apply(lambda x: slope(x,"z6"))
    D["b"]=pd.cut(D["z6"],[-99,-2,-1,0,1,2,99])
    D["sz"]=np.sign(D["z6"])
    out["next24 ex: down vs up 6h moves, by coin"]=D.groupby(["coin","sz"])["y"].mean().unstack()
    return out
