def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df[["timestamp","close"]].copy()
            ts=pd.to_datetime(d["timestamp"],utc=True)
            d["hour"]=ts.dt.hour.values; d["yr"]=ts.dt.year.values
            c=d["close"]
            d["r1"]=c.shift(-1)/c-1
            d["rp1"]=c/c.shift(1)-1
            d["tr72"]=c/c.shift(72)-1
            d["vol24"]=d["rp1"].rolling(24).std()
            d["pos"]=np.arange(len(d)); d["coin"]=coin; d["w"]=w
            for h in (4,12):
                d[f"f{h}"]=c.shift(-h)/c-1; d[f"p{h}"]=c/c.shift(h)-1
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    A["z72"]=A.groupby("coin")["tr72"].transform(lambda s:(s-s.mean())/s.std())
    A["exr1"]=A["r1"]-A.groupby("coin")["r1"].transform("mean")
    A["sc"]=A["rp1"]/A["vol24"]
    out={}
    def slope(g,x,y):
        g=g.dropna(subset=[x,y])
        if len(g)<50: return pd.Series({"slope_bp":np.nan,"t":np.nan,"n":len(g)})
        r=stats.linregress(g[x],g[y]); return pd.Series({"slope_bp":r.slope*1e4,"t":r.slope/r.stderr,"n":len(g)})
    H12=A[A["hour"]==12]
    out["h12 slope z72 by coin"]=H12.groupby("coin").apply(lambda g:slope(g,"z72","exr1"))
    out["h12 slope z72 by year"]=H12.groupby("yr").apply(lambda g:slope(g,"z72","exr1"))
    out["1h reversal slope (sc) by coin"]=A.groupby("coin").apply(lambda g:slope(g,"sc","exr1"))
    out["1h reversal slope (sc) by year"]=A.groupby("yr").apply(lambda g:slope(g,"sc","exr1"))
    out["1h reversal slope by hour"]=A.groupby("hour").apply(lambda g:slope(g,"sc","exr1"))
    for h in (4,12):
        G=A[A["pos"]%h==0].copy()
        G["x"]=G[f"p{h}"]/(G["vol24"]*np.sqrt(h))
        G["y"]=G[f"f{h}"]-G.groupby("coin")[f"f{h}"].transform("mean")
        out[f"{h}h past->next nonoverlap by coin"]=G.groupby("coin").apply(lambda g:slope(g,"x","y"))
    E=A[A["hour"].isin([20,21])]
    out["h20-21 excess by coin"]=E.groupby("coin")["exr1"].agg(lambda s:s.mean()*1e4).to_frame("bp").join(E.groupby("coin")["exr1"].agg(lambda s:s.mean()/(s.std()/np.sqrt(s.count()))).rename("t"))
    out["h20-21 excess by year"]=E.groupby("yr")["exr1"].agg(lambda s:s.mean()*1e4).to_frame("bp").join(E.groupby("yr")["exr1"].agg(lambda s:s.mean()/(s.std()/np.sqrt(s.count()))).rename("t"))
    return out
