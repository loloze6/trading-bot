def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,df in ws.items():
            c=df["close"].astype(float).values
            r=pd.Series(c).pct_change()
            allr.append(r)
        cm=pd.concat(allr).mean()
        for w,df in ws.items():
            d=pd.DataFrame()
            c=df["close"].astype(float).reset_index(drop=True)
            d["r1"]=c.pct_change()
            d["vol"]=d["r1"].rolling(24).std()
            d["z"]=d["r1"]/d["vol"]
            d["nx"]=c.shift(-1)/c-1-cm
            d["nx4"]=(c.shift(-4)/c-1)
            d["vol_rel"]=d["vol"]/d["vol"].rolling(24*30,min_periods=200).median()
            v=df["volume"].astype(float).reset_index(drop=True)
            d["vrel"]=v/v.rolling(24*7,min_periods=48).median()
            ts=pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            d["hour"]=ts.dt.hour; d["wd"]=ts.dt.weekday; d["year"]=ts.dt.year
            a=df["postRebalance_current_allocation"].astype(float).reset_index(drop=True)
            d["gross"]=a*(c.shift(-1)/c-1)
            d["coin"]=coin; d["win"]=w
            rows.append(d)
    D=pd.concat(rows,ignore_index=True).dropna(subset=["z","nx"])
    D=D[np.isfinite(D.z)]
    def slope(g):
        if len(g)<100: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        r=stats.linregress(-g.z.clip(-6,6),g.nx)
        return pd.Series({"n":len(g),"slope_bp":r.slope*1e4,"t":r.slope/r.stderr})
    out={}
    D["zb"]=pd.qcut(D.z,10,labels=False)
    out["by_z_decile"]=D.groupby("zb").agg(z=("z","mean"),nx_bp=("nx",lambda x:x.mean()*1e4),t=("nx",lambda x:x.mean()/x.std()*np.sqrt(len(x))),n=("nx","size"))
    out["by_hour"]=D.groupby("hour").apply(slope)
    out["by_coin"]=D.groupby("coin").apply(slope)
    out["by_year"]=D.groupby("year").apply(slope)
    out["by_wd"]=D.groupby("wd").apply(slope)
    D["vb"]=pd.qcut(D.vol_rel,5,labels=False)
    out["by_volrel_q"]=D.groupby("vb").apply(slope)
    D["vvb"]=pd.qcut(D.vrel,5,labels=False)
    out["by_volume_rel_q"]=D.groupby("vvb").apply(slope)
    out["vol_by_hour"]=D.groupby("hour").agg(vrel=("vrel","median"),absr_bp=("r1",lambda x:x.abs().mean()*1e4))
    out["gross_mean_bp_per_bar"]=D.gross.mean()*1e4
    out["gross_t"]=D.gross.mean()/D.gross.std()*np.sqrt(D.gross.count())
    return out
