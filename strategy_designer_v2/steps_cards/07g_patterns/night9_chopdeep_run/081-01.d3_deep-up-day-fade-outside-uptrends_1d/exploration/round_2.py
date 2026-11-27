def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        allr=pd.concat([w.sort_values("timestamp")["close"].pct_change().dropna() for w in ws.values()])
        drift=allr.mean(); drift2=pd.concat([ (w.sort_values("timestamp")["close"].shift(-2)/w.sort_values("timestamp")["close"]-1).dropna() for w in ws.values()]).mean()
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"ts":b["timestamp"]}); d["coin"]=coin; d["w"]=w
            sd=r.rolling(20,min_periods=15).std()
            d["r1"]=r; d["rz"]=r/sd
            d["depth"]=(c.rolling(20,min_periods=15).max()/c-1)/sd
            d["tr60"]=c/c.shift(60)-1
            d["un"]=c.shift(-1)/c-1-drift
            d["un2"]=c.shift(-2)/c-1-drift2
            sd30=r.rolling(30,min_periods=20).std()
            d["agit"]=sd30/sd30.expanding(min_periods=30).median()
            d["prevup"]=(r.shift(1)>0).astype(float)
            d["pos"]=b["postRebalance_current_allocation"]
            d["idx"]=np.arange(len(b))
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["un","depth","r1","rz"])
    D["day"]=pd.to_datetime(D["ts"]).dt.floor("D")
    D["trend"]=np.where(D["tr60"]>0.1,"rising",np.where(D["tr60"]<-0.1,"falling",np.where(D["tr60"].isna(),"na","choppy")))
    def summ(g,col="un"):
        g=g.dropna(subset=[col]); x=g[col]
        if len(x)<10: return pd.Series({"n":len(x)})
        s=g.groupby("day")[col].sum(); k=g.groupby("day").size()
        se=np.sqrt(len(s)/(len(s)-1)*(((s-x.mean()*k)**2).sum()))/len(x)
        return pd.Series({"n":len(x),"days":len(s),"mean_%":100*x.mean(),"t":x.mean()/se})
    out={}
    U=D[D.r1>0].copy()
    U["dq"]=pd.qcut(U.depth.rank(method="first"),3,labels=False)
    U["zq"]=pd.qcut(U.rz.rank(method="first"),3,labels=False)
    out["up_depth3_x_upsize3"]=U.groupby(["dq","zq"]).apply(summ)
    out["up_depth3_2day"]=U.groupby("dq").apply(lambda g:summ(g,"un2"))
    U2=U.dropna(subset=["agit"]); U2["ag"]=np.where(U2.agit>1,"agit","calm")
    out["up_nonrising_depth3_by_agit"]=U2[U2.trend.isin(["choppy","falling"])].groupby(["ag","dq"]).apply(summ)
    out["up_depth3_by_prevup"]=U.groupby(["prevup","dq"]).apply(summ)
    # big down days rebound
    Dn=D[D.r1<=0].copy()
    Dn["zq"]=pd.qcut(Dn.rz.rank(method="first"),5,labels=False)
    Dn2=Dn[Dn.trend!="na"]
    out["down_size5_by_trend"]=Dn2.groupby(["trend","zq"]).apply(summ)
    # middle up size: all up days by rz quintile and trend
    U["zq5"]=pd.qcut(U.rz.rank(method="first"),5,labels=False)
    out["up_size5_by_trend"]=U[U.trend!="na"].groupby(["trend","zq5"]).apply(summ)
    # coin-level consistency of deep-up fade
    deep=U[U.dq==2]
    out["deepup_by_coin"]=deep.groupby("coin").apply(summ)
    return out
