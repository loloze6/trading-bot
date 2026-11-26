def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H=7
    rows=[]; drows=[]
    for coin, ws in data["bars"].items():
        g7=[]
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            fwd=c.shift(-H)/c-1
            r7=c/c.shift(7)-1
            r30=c/c.shift(30)-1
            s30=r1.rolling(30).std(); s90=r1.rolling(90,min_periods=40).std()
            er=(c-c.shift(30)).abs()/(c.diff().abs().rolling(30).sum())
            fc=b["forecast"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"fwd":fwd,"r7":r7,"r30":r30,"z7":r7/s30,"vr":s30/s90,
                            "er":er,"fc":fc,"r1":r1,"next1":r1.shift(-1),"wd":ts.dt.weekday,
                            "year":ts.dt.year,"r1z":r1/s30.shift(1)})
            d["grid"]=(np.arange(len(d))%H==0)
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    drift=A[A.grid].groupby("coin")["fwd"].mean()
    A["ex"]=A["fwd"]-A["coin"].map(drift)
    G=A[A.grid].dropna(subset=["ex","z7","er","r30","vr"])
    out={}
    act=G[G.fc!=0].copy()
    act["dirx"]=np.sign(act.fc)*act.ex
    act["fq"]=pd.qcut(act.fc.abs(),4,labels=False)
    out["active by |fc| quartile"]=act.groupby("fq")["dirx"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["active by year"]=act.groupby("year")["dirx"].agg(["mean","count"])
    out["active by coin"]=act.groupby("coin")["dirx"].agg(["mean","count"])
    # general: continuation of z7 sign across regimes
    G["side"]=np.sign(G.r7)*G.ex
    G["erb"]=pd.cut(G.er,[0,0.15,0.3,0.5,1.01])
    G["align"]=np.where(np.sign(G.r7)==np.sign(G.r30),"aligned","opposed")
    G["zb"]=pd.qcut(G.z7.abs(),3,labels=["small","mid","large"])
    f=lambda x: pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/x.std()*np.sqrt(len(x))})
    out["dir of r7 cont by er,align"]=G.groupby(["erb","align"])["side"].apply(f).unstack()
    out["dir of r7 cont by |z7| tercile,align"]=G.groupby(["zb","align"])["side"].apply(f).unstack()
    G["vrb"]=pd.qcut(G.vr,3,labels=["calm","mid","wide"])
    out["dir cont by vr,align"]=G.groupby(["vrb","align"])["side"].apply(f).unstack()
    # daily: next day after large daily moves
    D=A.dropna(subset=["r1z","next1"]).copy()
    D["zb"]=pd.cut(D.r1z,[-99,-2,-1,0,1,2,99])
    out["next day ret by today z"]=D.groupby("zb")["next1"].apply(f).unstack()
    out["coin ret by weekday"]=D.groupby("wd")["r1"].apply(f).unstack()
    # book daily
    bd=[]
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; bd.append(dd)
    B=pd.concat(bd)
    B["wd"]=pd.to_datetime(B["day"]).dt.weekday
    out["book ret by weekday"]=B.dropna(subset=["book_return"]).groupby("wd")["book_return"].apply(f).unstack()
    out["book by window"]=B.groupby("w")[["book_return","coin_return"]].mean()
    return out
