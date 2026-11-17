def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,df in ws.items():
            allr.append(df["close"].astype(float).reset_index(drop=True).pct_change())
        mu=pd.concat(allr).mean()
        for w,df in ws.items():
            d=df.reset_index(drop=True)
            c=d["close"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(20,min_periods=15).std()
            z=r1/vol
            vr=d["volume"]/d["volume"].rolling(20,min_periods=15).mean()
            volrel=vol/vol.rolling(120,min_periods=40).mean()
            ts=pd.to_datetime(d["timestamp"])
            f1=c.shift(-1)/c-1-mu
            f2=c.shift(-2)/c-1-2*mu
            pos=d["postRebalance_current_allocation"].astype(float)
            rows.append(pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(d)),"z":z,"vr":vr,"volrel":volrel,
                "yr":ts.dt.year,"f1":f1,"f2":f2,"pos":pos}))
    A=pd.concat(rows,ignore_index=True)
    def summ(g,col="f1"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    B=A.dropna(subset=["z","f1","vr","volrel"]).copy()
    B["vrq"]=pd.qcut(B["vr"],3,labels=False)
    B["vlq"]=pd.qcut(B["volrel"],3,labels=False)
    falls=B[B["z"]<0].copy()
    falls["fq"]=pd.qcut(-falls["z"],4,labels=False)
    out={}
    out["falls: fall quartile x vol tercile"]=falls.groupby(["fq","vrq"]).apply(summ)
    out["falls: fall quartile x volregime"]=falls.groupby(["fq","vlq"]).apply(summ)
    big=falls[falls["fq"]==3]
    out["big falls: vrq x vlq"]=big.groupby(["vrq","vlq"]).apply(summ)
    hv=falls[falls["vrq"]==2]
    out["highvol falls by coin"]=hv.groupby("coin").apply(summ)
    out["highvol falls by year"]=hv.groupby("yr").apply(summ)
    # graded score: -z * vr
    falls["s"]=-falls["z"]*falls["vr"]
    falls["sq"]=pd.qcut(falls["s"],5,labels=False)
    out["falls by -z*vr quintile"]=falls.groupby("sq").apply(summ)
    falls["sv"]=-falls["z"]*falls["volrel"]
    falls["svq"]=pd.qcut(falls["sv"],5,labels=False)
    out["falls by -z*volrel quintile"]=falls.groupby("svq").apply(summ)
    hvf=falls[falls["vlq"]==2]
    out["highregime falls by coin"]=hvf.groupby("coin").apply(summ)
    # moderate rises
    rises=B[B["z"]>0].copy()
    rises["rq"]=pd.qcut(rises["z"],4,labels=False)
    out["rises: quartile x vol tercile"]=rises.groupby(["rq","vrq"]).apply(summ)
    out["rises: by coin (z in 0.5-1.5)"]=rises[(rises.z>0.5)&(rises.z<1.5)].groupby("coin").apply(summ)
    G2=falls[falls["i"]%2==0]
    out["falls f2 nonoverlap by vrq"]=G2.groupby("vrq").apply(lambda g:summ(g,"f2"))
    out["pos-weighted: share active on hv falls"]=pd.Series({"active share":(B["pos"]>0).mean(),"active hv":(B.loc[B.pos>0,"vrq"]==2).mean()})
    return out
