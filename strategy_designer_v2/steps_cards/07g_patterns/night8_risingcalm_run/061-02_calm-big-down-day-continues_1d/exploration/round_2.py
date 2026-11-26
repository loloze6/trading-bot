def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd=r1.rolling(30,min_periods=20).std()
            z=r1/sd
            calm=(b["regime"]!="chop")
            tr60=c/c.shift(60)-1
            clv=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            n=len(b)
            for h in (3,5,10):
                f=c.shift(-h)/c-1
                f1=c.shift(-h-1)/c.shift(-1)-1
                for i in range(0,n-h-1,h):
                    rows.append(dict(coin=coin,w=w,h=h,z=z.iat[i],calm=bool(calm.iat[i]),
                        tr=tr60.iat[i],clv=clv.iat[i],yr=ts.iat[i].year,day=ts.iat[i].normalize(),
                        f=f.iat[i],f1=f1.iat[i],fc=b["forecast"].iat[i]))
    d=pd.DataFrame(rows).dropna(subset=["f","z"])
    for col in ("f","f1"):
        d[col]=d[col]-d.groupby(["coin","h"])[col].transform("mean")
    out={}
    def clt(v,day):
        s=pd.Series(v.values,index=day.values).groupby(level=0).sum()
        G=len(s); m=v.mean()
        se=np.sqrt((s-s.mean()*0).pow(2).sum()*G/(G-1))/len(v) if G>1 else np.nan
        # deviations from mean summed per day
        dev=pd.Series((v-m).values,index=day.values).groupby(level=0).sum()
        se=np.sqrt((dev**2).sum()*G/(G-1))/len(v)
        return m/se,G
    def follow(g,col="f"):
        v=g[col]*np.sign(g["z"])
        t,G=clt(v,g["day"])
        sl=stats.linregress(g["z"],g[col])
        return pd.Series({"n":len(g),"days":G,"follow%":v.mean()*100,"t_cl":t,"slope%perz":sl.slope*100,"t_slope":sl.slope/sl.stderr})
    for h in (3,5,10):
        x=d[d.h==h]
        out[f"h{h} follow-through by calm"]=x.groupby("calm").apply(follow)
    x=d[(d.h==5)&(d.calm)].copy()
    x["az"]=pd.qcut(x["z"].abs(),4,labels=False)
    out["h5 calm follow by |z| quartile"]=x.groupby("az").apply(follow)
    out["h5 calm follow by |z|q, skip day1 (f1)"]=x.groupby("az").apply(lambda g: follow(g,"f1"))
    out["h5 calm follow by window"]=x.groupby("w").apply(follow)
    out["h5 calm follow by coin"]=x.groupby("coin").apply(follow)
    out["h5 calm follow by year"]=x.groupby("yr").apply(follow)
    x["trb"]=pd.cut(x["tr"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    out["h5 calm follow by trend"]=x.groupby("trb",observed=True).apply(follow)
    out["h5 calm follow by z sign"]=x.groupby(np.sign(x["z"])).apply(follow)
    # close location as signal in calm: (clv-0.5) graded
    xc=x.dropna(subset=["clv"]).copy()
    xc["cq"]=pd.qcut(xc["clv"],4,labels=False)
    out["h5 calm excess by clv quartile"]=xc.groupby("cq").apply(lambda g: pd.Series({"n":len(g),"mean%":g.f.mean()*100,"t_cl":clt(g.f,g.day)[0]}))
    out["h5 calm clv vs z partial"]=pd.Series(dict(zip(["b_z","b_clv"],np.linalg.lstsq(np.c_[np.ones(len(xc)),xc.z,xc.clv-0.5],xc.f,rcond=None)[0][1:]*100)))
    # agitated h5 by sign
    xa=d[(d.h==5)&(~d.calm)]
    out["h5 agitated follow by z sign"]=xa.groupby(np.sign(xa["z"])).apply(follow)
    return out
