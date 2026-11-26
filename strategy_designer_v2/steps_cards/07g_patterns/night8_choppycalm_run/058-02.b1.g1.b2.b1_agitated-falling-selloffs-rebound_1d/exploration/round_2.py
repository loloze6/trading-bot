def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float); r=c.pct_change(); v=r.rolling(20).std()
            lr=np.log(c).diff()
            vol30=r.rolling(30).std()
            vp=vol30.rolling(200,min_periods=100).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            n=len(c); idx=np.arange(n)
            f5=c.shift(-5)/c-1; f3=c.shift(-3)/c-1; f2=c.shift(-2)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"z":r/v,"r":r,"nxt":c.shift(-1)/c-1,
                "f2":np.where(idx%2==0,f2,np.nan),"f3":np.where(idx%3==0,f3,np.nan),"f5":np.where(idx%5==0,f5,np.nan),
                "tr60":c/c.shift(60)-1,"vp":vp,
                "rp":(c-b["low"].rolling(20).min())/(b["high"].rolling(20).max()-b["low"].rolling(20).min()),
                "inprof":(b["regime"]=="unknown").values,"wd":ts.dt.weekday,"yr":ts.dt.year,
                "day":ts.dt.floor("D"),"pos":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for col in ["nxt","f2","f3","f5"]:
        D["ex_"+col]=D[col]-D.groupby("coin")[col].transform("mean")
    def st(g,col="ex_nxt"):
        x=g[["day",col]].dropna(); n=len(x)
        if n<3: return pd.Series({"n":n,"days":0,"mean%":np.nan,"t":np.nan})
        m=x[col].mean(); s=(x[col]-m).groupby(x["day"]).sum(); G=len(s)
        se=np.sqrt((s**2).sum()*G/(G-1))/n
        return pd.Series({"n":n,"days":G,"mean%":100*m,"t":m/se})
    out={}
    P=D[D.inprof].copy()
    U=P[P.r>0].copy()
    U["zq"]=pd.qcut(U["z"],5,labels=False)
    out["FA up days: z quintile next day"]=U.groupby("zq").apply(st).round(3)
    out["FA up days: z quintile 2d"]=U.groupby("zq").apply(lambda g:st(g,"ex_f2")).round(3)
    out["FA up days by coin"]=U.groupby("coin").apply(st).round(3)
    out["FA up days by year"]=U.groupby("yr").apply(st).round(3)
    out["FA up days zmean by q"]=U.groupby("zq")["z"].mean().round(2)
    # out-of-profile falling (calm) up days for contrast
    D["trb"]=pd.cut(D["tr60"],[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    D["ag"]=np.where(D.vp>0.5,"ag","calm")
    Up=D[(D.r>0)]
    out["up days next day by trend x agit"]=Up.groupby(["trb","ag"]).apply(st).round(3)
    # brief theme: choppy x agitation x range position, 3 days
    C=D[D.trb=="chop"].copy()
    C["rpq"]=pd.cut(C["rp"],[-.01,.2,.4,.6,.8,1.01],labels=False)
    out["chop: agit x rangepos 3d"]=C.groupby(["ag","rpq"]).apply(lambda g:st(g,"ex_f3")).round(3)
    out["Wed next day by year (all)"]=D[D.wd==2].groupby("yr").apply(st).round(3)
    out["Wed next day by coin"]=D[D.wd==2].groupby("coin").apply(st).round(3)
    return out
