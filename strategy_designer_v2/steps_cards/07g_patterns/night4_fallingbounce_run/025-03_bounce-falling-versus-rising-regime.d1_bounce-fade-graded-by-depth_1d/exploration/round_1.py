def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vol=r.rolling(20,min_periods=15).std()
            z=r/vol
            r5b=c/c.shift(5)-1
            r10b=c/c.shift(10)-1
            r30=c/c.shift(30)-1
            z5b=r5b/(vol*np.sqrt(5))
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"z5b":z5b,"r30":r30,"vol":vol,"f5":f5,"f1":f1,
                            "wd":ts.dt.dayofweek,"yr":ts.dt.year,"fc":b["forecast"],"pos":b["postRebalance_current_allocation"]})
            d["grid"]=(np.arange(len(d))%5==0)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[D.grid].dropna(subset=["f5","z"]).copy()
    out={}
    drift=G.groupby("coin")["f5"].mean()
    G["ab"]=G["f5"]-G["coin"].map(drift)
    G["zb"]=pd.cut(G["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    out["f5 by 1d z"]=G.groupby("zb")["ab"].agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    G["z5bb"]=pd.cut(G["z5b"],[-99,-1.5,-0.5,0.5,1.5,99])
    out["f5 by 5d z"]=G.groupby("z5bb")["ab"].agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    G["r30s"]=np.sign(G["r30"])
    out["f5 by 1dz x r30sign"]=G.groupby(["r30s",pd.cut(G["z"],[-99,-1,1,99])])["ab"].agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    G["volq"]=G.groupby("coin")["vol"].transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    out["f5 by vol tercile"]=G.groupby("volq")["ab"].agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    # corr of f5 with z5b and r30 vol-scaled
    G["r30z"]=G["r30"]/(G["vol"]*np.sqrt(30))
    res={}
    for v in ["z","z5b","r30z"]:
        g=G.dropna(subset=[v,"ab"]); rr,p=stats.pearsonr(g[v],g["ab"]); res[v]=(len(g),rr,rr*np.sqrt((len(g)-2)/(1-rr**2)))
    out["corr with f5 abnormal"]=pd.DataFrame(res,index=["n","r","t"]).T
    D1=D.dropna(subset=["f1"])
    out["f1 by weekday"]=D1.groupby("wd")["f1"].agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    out["f5 by coin x 1dz>1"]=G[G.z>1].groupby("coin")["ab"].agg(["count","mean"])
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    DD=pd.concat(dd)
    out["active pos share"]=float((D["pos"].abs()>1e-6).mean())
    out["book ret by coin"]=DD.groupby("coin")["book_return"].agg(["count","mean","std"])
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trades"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"]) if len(T) else "none"
    return out
