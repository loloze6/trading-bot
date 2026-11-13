def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float)
            r1=np.log(c).diff()
            vol=r1.rolling(20).std()
            sp=b["debug_info.components.sma_cross_down.last_history_value"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"wn":int(w[1:]),"r1":r1,"f1":r1.shift(-1),
                "f3":np.log(c.shift(-3))-np.log(c),"f10":np.log(c.shift(-10))-np.log(c),
                "z":r1/vol.shift(1),"sp":sp,"dsp":sp-sp.shift(10),"fc":b["forecast"].astype(float),
                "wd":ts.dt.dayofweek,"hr":ts.dt.hour,"yr":ts.dt.year,
                "dd":r1.rolling(3).sum()})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for k in ["f1","f3","f10"]:
        D[k+"x"]=D[k]-D.groupby("coin")[k].transform("mean")
    def s(g,col,ov=1):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)/ov) if len(x)>2 else np.nan,"up":(x>0).mean()})
    out={}
    out["timestamp hour values"]=D["hr"].value_counts()
    dn=D[(D.z<-0.5)]
    out["after down day (z<-0.5): f1x by coin"]=dn.groupby("coin").apply(lambda g:s(g,"f1x"))
    out["after down day: f1x by short/flat"]=dn.groupby(dn.fc<0).apply(lambda g:s(g,"f1x"))
    out["after down day: f1x early/late windows"]=dn.groupby(dn.wn>12).apply(lambda g:s(g,"f1x"))
    out["after down day: f3x by z bin"]=D.groupby(pd.cut(D.z,[-99,-1.5,-0.5,0.5,1.5,99])).apply(lambda g:s(g,"f3x",3))
    up=D[(D.z>0.5)]
    out["after up day: f1x by coin"]=up.groupby("coin").apply(lambda g:s(g,"f1x"))
    out["weekday f1x early/late windows"]=D.groupby(["wd",D.wn>12]).apply(lambda g:s(g,"f1x")).unstack()["t"] if False else D.groupby([D.wn>12,"wd"]).apply(lambda g:s(g,"f1x"))
    out["weekday 4 f1x by coin"]=D[D.wd==4].groupby("coin").apply(lambda g:s(g,"f1x"))
    out["weekday 2 f1x by coin"]=D[D.wd==2].groupby("coin").apply(lambda g:s(g,"f1x"))
    nz=D[(D.sp>-40)&(D.sp<=1)]
    out["near-cross below: f10x by spread 10d change sign"]=nz.groupby(nz.dsp>0).apply(lambda g:s(g,"f10x",10))
    out["near-cross below: f10x by coin"]=nz.groupby("coin").apply(lambda g:s(g,"f10x",10))
    out["near-cross below: f10x early/late"]=nz.groupby(nz.wn>12).apply(lambda g:s(g,"f10x",10))
    sh=D[D.fc<0]
    out["short regime: f10x by spread rising/falling"]=sh.groupby(sh.dsp>0).apply(lambda g:s(g,"f10x",10))
    out["all: f10x by spread 10d change sign"]=D.groupby([D.sp<0,D.dsp>0]).apply(lambda g:s(g,"f10x",10))
    return out
