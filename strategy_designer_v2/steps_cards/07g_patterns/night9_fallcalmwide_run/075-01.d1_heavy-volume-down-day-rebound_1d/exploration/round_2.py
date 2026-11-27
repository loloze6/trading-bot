def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            nxt=c.shift(-1)/c-1
            vr=v/v.shift(1).rolling(20,min_periods=20).mean()
            vol20=r.rolling(20,min_periods=15).std()
            vol30=r.rolling(30,min_periods=25).std()
            agit=vol30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            tr60=c/c.shift(60)-1
            pos=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            df=pd.DataFrame({"coin":coin,"w":w,"r":r,"nxt":nxt,"vr":vr,"z":r/vol20,"tr60":tr60,
                             "agit":agit,"pos":pos,"vol20":vol20,
                             "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                             "yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["ex"]=d["nxt"]-d.groupby("coin")["nxt"].transform("mean")
    d=d.dropna(subset=["nxt","r","vr","tr60"])
    d["exs"]=d["ex"]/d["vol20"]
    def agg(g):
        x=g["ex"]
        return pd.Series({"n":len(x),"mean_ex%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    def slope_day(g,xcol,ycol="ex"):
        s=g.groupby("day")[[xcol,ycol]].sum()
        res=stats.linregress(s[xcol],s[ycol])
        return pd.Series({"days":len(s),"slope":res.slope,"t":res.slope/res.stderr})
    out={}
    up=d[d.r>0].copy()
    up["lightness"]=-np.log(up["vr"])
    out["up_slope_ex_on_lightness"]=slope_day(up,"lightness")
    out["up_light_by_year"]=up[up.vr<1].groupby("yr").apply(agg)
    d["trend"]=pd.cut(d["tr60"],[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    d["ag"]=np.where(d["agit"]>0.5,"agit","calm")
    upd=d[d.r>0].copy()
    out["up_by_trend_agit"]=upd.groupby(["trend","ag"]).apply(agg)
    fu=upd[upd.trend=="falling"].copy()
    fu["zq"]=pd.qcut(fu["z"],4,labels=["smallup","2","3","bigup"])
    out["falling_up_by_size"]=fu.groupby("zq").apply(agg)
    out["falling_up_slope_on_z"]=slope_day(fu,"z")
    out["falling_up_by_year"]=fu.groupby("yr").apply(agg)
    fu["posq"]=pd.qcut(fu["pos"],3,labels=["low","mid","high"])
    out["falling_up_by_closepos"]=fu.groupby("posq").apply(agg)
    # light volume up days graded within rising/choppy/falling
    upd["vrq"]=pd.qcut(np.log(upd["vr"]),3,labels=["light","mid","heavy"])
    out["up_trend_x_vol"]=upd.groupby(["trend","vrq"]).apply(agg)
    hd=d[(d.r<0)&(d.vr>1)]
    out["heavydown_by_trend_agit"]=hd.groupby(["trend","ag"]).apply(agg)
    return out
