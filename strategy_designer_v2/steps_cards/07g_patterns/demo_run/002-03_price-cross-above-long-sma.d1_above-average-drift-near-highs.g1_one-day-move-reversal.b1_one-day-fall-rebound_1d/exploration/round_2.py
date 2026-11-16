def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            v=r.rolling(20,min_periods=15).std()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":c,"win":w,"wn":int(w[1:]),"z":r/v,"vol":v,
                "r20p":cl/cl.shift(20)-1,
                "f1":cl.shift(-1)/cl-1,"f5":cl.shift(-5)/cl-1,
                "wd":ts.dt.weekday,"yr":ts.dt.year,"i":np.arange(len(b))})
            d["volrank"]=v.rolling(120,min_periods=40).rank(pct=True)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in [1,5]:
        D["x%d"%h]=D["f%d"%h]-D["coin"].map(D.groupby("coin")["f%d"%h].mean())
    def tm(x):
        x=x.dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    F=D[(D.z<0)].dropna(subset=["volrank","x1"]).copy()
    F["pr"]=-F.z*F.x1
    F["vt"]=pd.cut(F.volrank,[0,1/3,2/3,1.01],labels=["low","mid","high"])
    F["half"]=np.where(F.wn<=12,"w1-12","w13-24")
    out["falls: mean(-z*x1) by vol tercile x half"]=F.groupby(["vt","half"])["pr"].apply(tm).unstack()
    out["falls high vol: mean(-z*x1) by coin"]=F[F.vt=="high"].groupby("coin")["pr"].apply(tm).unstack()
    # graded: corr of -z*volrank interaction
    F["zv"]=-F.z*F.volrank
    out["falls corr(-z*volrank,x1) vs corr(-z,x1)"]=pd.Series({"c_inter":np.corrcoef(F.zv,F.x1)[0,1],"c_plain":np.corrcoef(-F.z,F.x1)[0,1],"n":len(F)})
    # 5-day after big up day, multiple grid offsets
    res=[]
    for off in range(5):
        G=D[(D.i%5==off)].dropna(subset=["z","x5"]).copy()
        G["q"]=pd.qcut(G.z,5,labels=False)
        s=tm(G[G.q==4].x5); s["off"]=off; s["corr_z_x5"]=np.corrcoef(G.z,G.x5)[0,1]; res.append(s)
    out["5d excess after top z quintile, by grid offset"]=pd.DataFrame(res)
    G=D[D.i%5==0].dropna(subset=["z","x5"]).copy()
    G["q"]=pd.qcut(G.z,5,labels=False); G["half"]=np.where(G.wn<=12,"a","b")
    out["5d top z quintile by coin"]=G[G.q==4].groupby("coin")["x5"].apply(tm).unstack()
    out["5d top z quintile by half"]=G[G.q==4].groupby("half")["x5"].apply(tm).unstack()
    # up-day 1d reversal: slope among rises
    U=D[D.z>0].dropna(subset=["x1"]).copy()
    U["half"]=np.where(U.wn<=12,"a","b")
    out["rises: next-day excess by half"]=U.groupby("half")["x1"].apply(tm).unstack()
    out["rises: by coin"]=U.groupby("coin")["x1"].apply(tm).unstack()
    out["weekday by half"]=D.dropna(subset=["x1"]).assign(half=np.where(D.dropna(subset=["x1"]).wn<=12,"a","b")).groupby(["wd","half"])["x1"].apply(lambda x:tm(x)["t"]).unstack()
    out["weekday by year t"]=D.dropna(subset=["x1"]).groupby(["yr","wd"])["x1"].apply(lambda x:tm(x)["t"]).unstack().round(2)
    # falls in uptrend graded
    F["tr"]=pd.qcut(F.r20p,4,labels=False)
    out["falls: mean(-z*x1) by 20d trend quartile"]=F.dropna(subset=["tr"]).groupby("tr")["pr"].apply(tm).unstack()
    return out
