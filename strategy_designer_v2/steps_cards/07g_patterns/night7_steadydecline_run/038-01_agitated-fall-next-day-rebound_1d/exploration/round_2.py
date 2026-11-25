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
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),"r":r,"z":z,
                "r3":c/c.shift(3)-1,"r3z":(c/c.shift(3)-1)/(s*np.sqrt(3)),
                "n1":c.shift(-1)/c-1,"n2":c.shift(-2)/c-1,
                "reg":b["regime"].astype(str),"vz":vz,
                "tr60":c/c.shift(60)-1,"vol30":r.rolling(30,min_periods=20).std(),
                "dd20":c/c.rolling(20,min_periods=10).max()-1,
                "alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r"].mean(); D["mu"]=D["coin"].map(mu)
    D["x1"]=D["n1"]-D["mu"]; D["x2"]=D["n2"]-2*D["mu"]
    D["day"]=D["ts"].dt.floor("D")
    medv=D.groupby("coin")["vol30"].median(); D["agit"]=D["vol30"]>D["coin"].map(medv)
    D["trend"]=np.select([D.tr60>0.10,D.tr60< -0.10],["rising","falling"],"choppy")
    D.loc[D.tr60.isna(),"trend"]="na"
    D["prof"]=np.where(D.reg=="unknown","FA_reg",D.trend+"_"+np.where(D.agit,"agit","calm"))
    def tday(g,col):
        g=g.dropna(subset=[col]); dm=g.groupby("day")[col].mean(); n=len(dm)
        return pd.Series({"mean%":g[col].mean()*100,"t_day":dm.mean()/(dm.std()/np.sqrt(n)) if n>2 else np.nan,"cases":len(g),"days":n})
    def slope(g,xc,yc):
        g=g.dropna(subset=[xc,yc]); x=g[xc]-g[xc].mean(); y=g[yc]
        b=(x*y).sum()/(x*x).sum(); e=y-y.mean()-b*x
        sc=(x*e).groupby(g["day"]).sum(); se=np.sqrt((sc**2).sum())/(x*x).sum()
        return pd.Series({"slope_bp":b*1e4,"t_cl":b/se,"n":len(g),"days":g["day"].nunique()})
    out={}
    falls=D[(D.r<0)].copy(); falls["fz"]=-falls["z"].clip(upper=0)
    out["slope x1 on fall size by profile"]=falls.groupby("prof").apply(lambda g:slope(g,"fz","x1")).round(3)
    ups=D[(D.r>0)].copy(); ups["uz"]=ups["z"].clip(lower=0)
    out["slope x1 on up size by profile"]=ups.groupby("prof").apply(lambda g:slope(g,"uz","x1")).round(3)
    out["FA ups mean x1,x2"]=pd.DataFrame({h:tday(D[(D.prof=="FA_reg")&(D.r>0)],h) for h in ["x1","x2"]}).round(3)
    fa=falls[falls.prof=="FA_reg"].copy()
    fa["volb"]=pd.qcut(fa["vz"],3,labels=["lowvol","mid","highvol"])
    out["FA falls x1 by volume"]=fa.groupby("volb",observed=True).apply(lambda g:tday(g,"x1")).round(3)
    out["FA falls slope by volume tercile"]=fa.groupby("volb",observed=True).apply(lambda g:slope(g,"fz","x1")).round(3)
    fa["ddb"]=pd.qcut(fa["dd20"],3,labels=["deep","mid","shallow"])
    out["FA falls x1 by drawdown from 20d high"]=fa.groupby("ddb",observed=True).apply(lambda g:tday(g,"x1")).round(3)
    fa3=D[(D.prof=="FA_reg")&(D.r3<0)].copy(); fa3["f3"]=-fa3["r3z"]
    out["FA 3-day fall slope x1"]=slope(fa3,"f3","x1").round(3)
    out["FA 1d fall slope x2"]=slope(fa,"fz","x2").round(3)
    # book extremes
    bd=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items(): bd.append(dd.assign(coin=coin,w=w))
    B=pd.concat(bd); bk=B.groupby(["w","day"])["book_return"].mean().dropna()
    q=bk.quantile([0.01,0.99])
    out["book: top/bottom 1% days sum share"]=pd.Series({"n_top":(bk>=q[0.99]).sum(),"sum_top_bp":bk[bk>=q[0.99]].sum()*1e4,
        "n_bot":(bk<=q[0.01]).sum(),"sum_bot_bp":bk[bk<=q[0.01]].sum()*1e4,"total_bp":bk.sum()*1e4})
    return out
