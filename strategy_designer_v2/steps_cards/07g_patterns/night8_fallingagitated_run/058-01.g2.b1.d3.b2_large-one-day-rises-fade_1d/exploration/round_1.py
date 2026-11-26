import numpy as np, pandas as pd

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=30).std()
            z1=r/sd
            r3=c/c.shift(3)-1
            z3=r3/(sd*np.sqrt(3))
            r10=c/c.shift(10)-1
            z10=r10/(sd*np.sqrt(10))
            clv=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            vol=b["volume"].astype(float); vr=vol/vol.rolling(20,min_periods=20).mean()
            f5=c.shift(-5)/c-1
            inprof=(b["regime"]!="chop")
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,len(b),5):
                rows.append(dict(coin=coin,w=w,i=i,z1=z1[i],z3=z3[i],z10=z10[i],clv=clv[i],vr=vr[i],
                                 f5=f5[i],inp=bool(inprof[i]),wd=ts[i].dayofweek,yr=ts[i].year,
                                 day=ts[i].normalize()))
    d=pd.DataFrame(rows).dropna(subset=["f5"])
    d["u"]=d["f5"]-d.groupby("coin")["f5"].transform("mean")
    out={}
    def tab(df,col,bins):
        df=df.dropna(subset=[col]).copy()
        df["b"]=pd.cut(df[col],bins)
        g=df.groupby(["inp","b"],observed=True)["u"]
        res=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
        return res.round(4)
    out["z1"]=tab(d,"z1",[-99,-2,-1,0,1,2,99])
    out["z3"]=tab(d,"z3",[-99,-1.5,-0.5,0.5,1.5,99])
    out["z10"]=tab(d,"z10",[-99,-1.5,-0.5,0.5,1.5,99])
    out["clv"]=tab(d,"clv",[-0.01,0.25,0.5,0.75,1.01])
    out["volratio"]=tab(d,"vr",[0,0.7,1,1.5,99])
    g=d.groupby(["inp","wd"])["u"]
    out["weekday"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))}).round(4)
    out["share_inprof"]=float(d["inp"].mean())
    bd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; bd.append(x)
    bd=pd.concat(bd)
    bk=bd.groupby(["w","day"])["book_return"].mean().dropna()
    out["book_by_window"]=bk.groupby(level=0).agg(["count","mean","sum"]).round(5)
    return out
