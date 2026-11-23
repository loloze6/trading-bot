def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change(); s20=r.rolling(20).std()
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"win":w,"ts":ts,"wd":ts.dt.weekday,"year":ts.dt.year,
                "z1":r/s20,"z2":(c/c.shift(2)-1)/s20,
                "g1":(c.shift(-1)/c-1)/s20,"g2":(c.shift(-2)/c-1)/s20,"g3":(c.shift(-3)/c-1)/s20,
                "v":(b["volume"].astype(float)/b["volume"].astype(float).rolling(20).mean())})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    out={}
    # Fama-MacBeth: per-date cross-coin slope, t over dates (removes cross-coin correlation)
    def fm(g,x,y):
        sl=[]
        for _,q in g.groupby("ts"):
            q=q[[x,y]].dropna()
            if len(q)>=5 and q[x].std()>0: sl.append(np.polyfit(q[x],q[y],1)[0])
        sl=np.array(sl)
        return sl.mean(), sl.mean()/sl.std(ddof=1)*np.sqrt(len(sl)), len(sl)
    # pooled per-coin-mean: average signed product per date then t over dates
    def dm(g,x,y):
        q=g[[x,y,"ts"]].dropna(); q["p"]=np.sign(q[x])*q[y]
        m=q.groupby("ts")["p"].mean()
        return m.mean(), m.mean()/m.std(ddof=1)*np.sqrt(len(m)), len(m)
    t=[]
    for wd in range(7):
        g=d[d.wd==wd]
        for h in ["g1","g2","g3"]:
            a=fm(g,"z1",h); b=dm(g,"z1",h)
            t.append((wd,h,round(a[0],4),round(a[1],2),round(b[0],4),round(b[1],2),a[2]))
    out["by weekday: FM slope,t ; date-mean sign(z1)*fwd, t ; n dates"]=pd.DataFrame(t,columns=["wd","h","fm_slope","fm_t","dm","dm_t","n"])
    # Sunday decomposition: Saturday move vs Sunday move, jointly
    g=d[d.wd==6].copy(); g["zsat"]=g.z2*1.0-g.z1  # approx Saturday's z (returns small)
    q=g[["z1","zsat","g2","g1"]].dropna()
    X=np.column_stack([np.ones(len(q)),q.z1,q.zsat])
    for y in ["g1","g2"]:
        beta,res,_,_=np.linalg.lstsq(X,q[y],rcond=None)
        e=q[y]-X@beta; s2=e.var(ddof=3); cov=s2*np.linalg.inv(X.T@X)
        out["Sun joint "+y+": beta(z1 Sun), t, beta(zSat), t"]=pd.Series([beta[1],beta[1]/np.sqrt(cov[1,1]),beta[2],beta[2]/np.sqrt(cov[2,2]),len(q)],index=["bSun","tSun","bSat","tSat","n"]).round(4)
    # Friday continuation and Saturday reversal by year, and by coin sign-consistency
    for wd,h,nm in [(4,"g1","Fri->Sat"),(5,"g1","Sat->Sun"),(6,"g1","Sun->Mon"),(0,"g1","Mon->Tue")]:
        g=d[d.wd==wd].dropna(subset=["z1",h]).copy(); g["p"]=np.sign(g.z1)*g[h]
        out[nm+" signed fwd by year"]=g.groupby("year")["p"].agg(["mean","count"]).round(3)
        pc=g.groupby("coin").apply(lambda q: np.polyfit(q.z1,q[h],1)[0])
        out[nm+" coins with positive slope / total"]=f"{(pc>0).sum()}/{len(pc)}"
    # Friday continuation graded by |z1| and by volume
    g=d[d.wd==4].dropna(subset=["z1","g1","v"]).copy(); g["p"]=np.sign(g.z1)*g.g1
    g["zq"]=pd.qcut(g.z1.abs(),4,labels=False); g["vq"]=pd.qcut(g.v,4,labels=False)
    out["Fri by |z1| q"]=g.groupby("zq")["p"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))]).round(3)
    out["Fri by vol q"]=g.groupby("vq")["p"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))]).round(3)
    # book: daily return by weekday
    br=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd.copy(); x["wd"]=pd.to_datetime(x["day"]).dt.weekday; br.append(x)
    br=pd.concat(br)
    out["book ret by weekday"]=br.groupby("wd")["book_return"].agg(["mean","std","count"]).round(5)
    return out
