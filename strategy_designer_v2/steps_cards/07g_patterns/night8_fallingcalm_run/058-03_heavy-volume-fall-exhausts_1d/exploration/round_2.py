def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); n=len(b)
            r1=c.pct_change()
            r60=c/c.shift(60)-1
            ts=pd.to_datetime(b["timestamp"])
            for L in [3,5,10]:
                b["r%d"%L]=c/c.shift(L)-1
            vol30=r1.rolling(30).std()
            fwd5=c.shift(-5)/c-1; fwd3=c.shift(-3)/c-1; fwd10=c.shift(-10)/c-1
            for i in range(0,n,5):
                if i+5>=n: continue
                rows.append(dict(coin=coin,w=w,reg=b["regime"].iloc[i],r3=b.r3.iloc[i],r5=b.r5.iloc[i],r10=b.r10.iloc[i],
                    r1=r1.iloc[i],r60=r60.iloc[i],vol30=vol30.iloc[i],fwd5=fwd5.iloc[i],fwd3=fwd3.iloc[i],
                    fwd10=fwd10.iloc[i] if i+10<n else np.nan,day=ts.iloc[i].normalize(),yr=ts.iloc[i].year))
    d=pd.DataFrame(rows)
    mu=d.fwd5.mean()
    d["fc"]=d.reg.isin(["mean_reversion","unknown"])
    d["z5"]=d.r5/(d.vol30*np.sqrt(5))
    out={}
    def reg(x,col,y="fwd5"):
        x=x[[col,y,"day"]].dropna()
        if len(x)<15: return pd.Series({"n":len(x)})
        s=stats.linregress(x[col],x[y])
        # signed-move style: direction = sign(col), unusual = (y-mu)*sign
        u=(x[y]-mu)*np.sign(x[col]); ud=u.groupby(x["day"]).sum()
        tday=ud.mean()/(ud.std()/np.sqrt(len(ud)))*1.0
        return pd.Series({"n":len(x),"slope":s.slope,"t":s.slope/s.stderr,"signed_unusual":u.mean(),"t_day":tday,"days":len(ud),
                          "dn_mean":x[y][x[col]<0].mean(),"up_mean":x[y][x[col]>0].mean(),"n_dn":(x[col]<0).sum()})
    fc=d[d.fc]
    t={}
    for col in ["r3","r5","r10","z5"]:
        for y in ["fwd3","fwd5","fwd10"]:
            t[(col,y)]=reg(fc,col,y)
    out["fallcalm momentum"]=pd.DataFrame(t).T
    out["fallcalm r5 by coin"]=pd.DataFrame({k:reg(g,"r5") for k,g in fc.groupby("coin")}).T
    out["fallcalm r5 by year"]=pd.DataFrame({k:reg(g,"r5") for k,g in fc.groupby("yr")}).T
    out["fallcalm r5 by window"]=pd.DataFrame({k:reg(g,"r5") for k,g in fc.groupby("w")}).T
    x=fc.dropna(subset=["z5","fwd5"]).copy(); x["q"]=pd.qcut(x.z5,5,labels=False)
    g=x.groupby("q")["fwd5"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["fallcalm z5 quintiles fwd5"]=g
    o=d.dropna(subset=["r60","vol30"]).copy()
    o["tb"]=pd.cut(o.r60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    out["r5 momentum by trend (all)"]=pd.DataFrame({str(k):reg(g,"r5") for k,g in o.groupby("tb")}).T
    out["r5 other than fallcalm"]=reg(d[~d.fc],"r5")
    # big daily move continuation, by profile flag
    d["z1"]=d.r1/d.vol30
    out["z1 all"]=reg(d,"z1")
    out["z1 fallcalm"]=reg(fc,"z1"); out["z1 other"]=reg(d[~d.fc],"z1")
    return out
