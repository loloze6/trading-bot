def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            m=r.rolling(60,min_periods=20).mean(); s=r.rolling(60,min_periods=20).std()
            z=(r-m)/s
            v=b["volume"]; vz=np.log(v/v.rolling(20,min_periods=10).median())
            dd20=c/c.rolling(20,min_periods=10).max()-1
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),"r":r,"z":z,
                "n1":c.shift(-1)/c-1,"n2":c.shift(-2)/c-1,"reg":b["regime"].astype(str),"vz":vz,
                "dd20":dd20,"ddz":dd20/(s*np.sqrt(20)),
                "tr60":c/c.shift(60)-1,"vol30":r.rolling(30,min_periods=20).std()})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r"].mean(); D["mu"]=D["coin"].map(mu)
    D["x1"]=D["n1"]-D["mu"]; D["x2"]=D["n2"]-2*D["mu"]
    D["day"]=D["ts"].dt.floor("D")
    D["yr"]=D["ts"].dt.year
    medv=D.groupby("coin")["vol30"].median(); D["agit"]=D["vol30"]>D["coin"].map(medv)
    D["trend"]=np.select([D.tr60>0.10,D.tr60< -0.10],["rising","falling"],"choppy")
    D["grp"]=np.where(D.reg=="unknown","FA_reg",np.where(D.agit,"other_agit","other_calm"))
    def slope(g,xc,yc):
        g=g.dropna(subset=[xc,yc]); x=g[xc]-g[xc].mean(); y=g[yc]
        if len(g)<10 or (x*x).sum()==0: return pd.Series({"slope_bp":np.nan,"t_cl":np.nan,"n":len(g),"days":0})
        b=(x*y).sum()/(x*x).sum(); e=y-y.mean()-b*x
        sc=(x*e).groupby(g["day"]).sum(); se=np.sqrt((sc**2).sum())/(x*x).sum()
        return pd.Series({"slope_bp":b*1e4,"t_cl":b/se,"n":len(g),"days":g["day"].nunique()})
    out={}
    falls=D[D.r<0].copy(); falls["fz"]=-falls["z"]
    falls["vol_x_fall"]=falls["fz"]*np.exp(falls["vz"].clip(-2,2))
    falls["depth"]=-falls["ddz"]
    for xc in ["vz","depth","vol_x_fall","fz"]:
        out[f"falls slope x1 on {xc} by grp"]=falls.groupby("grp").apply(lambda g:slope(g,xc,"x1")).round(3)
    fa=falls[falls.grp=="FA_reg"]
    out["FA falls vz slope by year"]=fa.groupby("yr").apply(lambda g:slope(g,"vz","x1")).round(3)
    out["FA falls depth slope by year"]=fa.groupby("yr").apply(lambda g:slope(g,"depth","x1")).round(3)
    out["FA falls fz slope by year"]=fa.groupby("yr").apply(lambda g:slope(g,"fz","x1")).round(3)
    # all FA bars (any day) depth slope
    allfa=D[D.grp=="FA_reg"].copy(); allfa["depth"]=-allfa["ddz"]
    out["FA all days slope x1 on depth"]=slope(allfa,"depth","x1").round(3)
    out["FA all days slope x2 on depth"]=slope(allfa,"depth","x2").round(3)
    # joint: depth controlling fall size via residual
    g=fa.dropna(subset=["depth","fz","x1"]).copy()
    bb=np.polyfit(g["fz"],g["depth"],1); g["depth_res"]=g["depth"]-np.polyval(bb,g["fz"])
    bb2=np.polyfit(g["fz"],g["vz"].fillna(0),1); g["vz_res"]=g["vz"]-np.polyval(bb2,g["fz"])
    out["FA falls: depth beyond fall size"]=slope(g,"depth_res","x1").round(3)
    out["FA falls: volume beyond fall size"]=slope(g,"vz_res","x1").round(3)
    out["corr fz depth vz"]=g[["fz","depth","vz"]].corr().round(3)
    return out
