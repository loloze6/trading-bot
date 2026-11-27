def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r0=c.pct_change()
            nx=c.shift(-1)/c-1
            nx2=c.shift(-2)/c-1
            nx3=c.shift(-3)/c-1
            dn=(r0<0).astype(int)
            # down run before today
            run=np.zeros(len(c),int); loss=np.full(len(c),np.nan)
            cnt=0; start=None
            for i in range(1,len(c)):
                # cnt = consecutive down closes ending at i-1
                run[i]=cnt
                if cnt>0: loss[i]=c[i-1]/c[i-1-cnt]-1
                if r0[i]<0: cnt+=1
                else: cnt=0
            vol20=r0.rolling(20).std()
            ret60=c/c.shift(60)-1
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r0":r0,"nx":nx,"u":nx-mu,"u2":nx2-2*mu,"u3":nx3-3*mu,"run":run,"loss":loss,
                "inprof":b["regime"].isin(["unknown","mean_reversion"]),"mr":b["regime"]=="mean_reversion",
                "pos":b["postRebalance_current_allocation"].astype(float),
                "fc":b["forecast"].astype(float),"vol20":vol20,"ret60":ret60,
                "rng":(b["high"]-b["low"])/c,"clpos":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,"yr":pd.to_datetime(b["timestamp"]).dt.year,
                "volz":b["volume"]/b["volume"].rolling(20).mean()})
            d["bp"]=d["pos"]*d["nx"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def ct(s,days):
        x=pd.DataFrame({"v":s.values,"d":days.values}).dropna()
        if len(x)<5: return (len(x),np.nan,np.nan,0)
        m=x.v.mean(); g=(x.v-m).groupby(x.d).sum(); n=len(x); Dn=len(g)
        se=np.sqrt((g**2).sum()*Dn/(Dn-1))/n
        return (n,m,m/se,Dn)
    def tab(groups,col="u"):
        out={}
        for k,sub in groups:
            n,m,t,dn=ct(sub[col],sub["day"]); out[k]={"n":n,"days":dn,"mean":m,"t":t}
        return pd.DataFrame(out).T
    res={}
    up=D[(D.r0>0)&(D.run>=2)]
    res["break by profile u"]=tab(up.groupby("inprof"))
    res["break inprof by run"]=tab(up[up.inprof].groupby(up[up.inprof].run.clip(upper=5)))
    res["break outprof by run"]=tab(up[~up.inprof].groupby(up[~up.inprof].run.clip(upper=5)))
    ip=up[up.inprof].copy(); ip["lq"]=pd.qcut(ip.loss,3,labels=False)
    res["inprof break by loss tercile u,u2"]=pd.concat([tab(ip.groupby("lq")),tab(ip.groupby("lq"),"u2").add_suffix("_2d")],axis=1)
    op=up[~up.inprof].copy(); op["lq"]=pd.qcut(op.loss,3,labels=False)
    res["outprof break by loss tercile"]=tab(op.groupby("lq"))
    # all bars: next day after r0 quintile by profile
    A=D.dropna(subset=["r0","u"]).copy()
    A["rz"]=A.r0/A.vol20; A["q"]=pd.qcut(A.rz,5,labels=False)
    res["all: next u by r0/vol20 quintile, inprof"]=tab(A[A.inprof].groupby("q"))
    res["all: next u by r0/vol20 quintile, out"]=tab(A[~A.inprof].groupby("q"))
    res["all: weekday u"]=tab(A.groupby("wd"))
    res["inprof: weekday u"]=tab(A[A.inprof].groupby("wd"))
    A["cq"]=pd.qcut(A.clpos,5,labels=False,duplicates="drop")
    res["all: close pos in range quintile"]=tab(A.groupby("cq"))
    A["vq"]=pd.qcut(A.volz,5,labels=False,duplicates="drop")
    res["all: rel volume quintile"]=tab(A.groupby("vq"))
    # book
    B=D[D.pos!=0]
    res["book by year"]=B.groupby("yr").agg(n=("bp","size"),mean=("bp","mean"))
    res["book by coin"]=B.groupby("coin").agg(n=("bp","size"),mean=("bp","mean"),sum=("bp","sum"))
    res["share inprof"]=float(D.inprof.mean())
    return res
