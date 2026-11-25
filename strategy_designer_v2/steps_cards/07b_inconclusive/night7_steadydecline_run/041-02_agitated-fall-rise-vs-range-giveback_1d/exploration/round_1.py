def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w,df in wins.items():
            c=df["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        drift=pd.concat(allr).mean()
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float); h=df["high"].astype(float); l=df["low"].astype(float)
            rng=(h-l).shift(1).rolling(30,min_periods=30).mean()
            mv=(c-c.shift(1))/rng
            r1=c.shift(-1)/c-1
            r2=c.shift(-2)/c-1
            r3=c.shift(-3)/c-1
            r1b=c.shift(-2)/c.shift(-1)-1
            ret60=c/c.shift(60)-1
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(df["timestamp"]).dt.year,
                "inprof":(df["regime"]=="unknown"),"mv":mv,"r1":r1-drift,"r2":r2-2*drift,"r3":r3-3*drift,
                "r1b":r1b-drift,"fc":df["forecast"].astype(float),"ret60":ret60,"day":df["timestamp"]})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["mv","r1"])
    out={}
    P=D[D.inprof]
    out["n in profile / all"]=f"{len(P)} / {len(D)}"
    def tab(X,key):
        g=X.groupby(key)
        return pd.DataFrame({"n":g.r1.size(),"mean_r1%":g.r1.mean()*100,"t":g.r1.apply(lambda s: s.mean()/s.std(ddof=1)*np.sqrt(len(s)) if len(s)>2 else np.nan),
                             "mean_r2%":g.r2.mean()*100,"mean_r1b%":g.r1b.mean()*100})
    bins=[-np.inf,-1.5,-1,-0.5,-0.2,0,0.2,0.5,1,1.5,np.inf]
    P=P.assign(b=pd.cut(P.mv,bins))
    out["profile: next-day excess by scaled move"]=tab(P,"b")
    O=D[~D.inprof].assign(b=lambda x: pd.cut(x.mv,bins))
    out["outside profile: by scaled move"]=tab(O,"b")
    U=P[P.mv>0].copy()
    U["q"]=pd.qcut(U.mv,4,labels=False)
    out["profile up-days quartiles"]=tab(U,"q")
    out["profile up-days by coin"]=tab(U,"coin")
    out["profile up-days by year"]=tab(U,"year")
    U["fall60"]=pd.qcut(U.ret60,3,labels=False,duplicates="drop")
    out["profile up-days by 60d return tercile"]=tab(U.dropna(subset=["fall60"]),"fall60")
    out["profile up-days: corr mv vs r1"]=stats.spearmanr(U.mv,U.r1).correlation
    Dn=P[P.mv<0].copy(); Dn["q"]=pd.qcut(Dn.mv,4,labels=False)
    out["profile down-days quartiles"]=tab(Dn,"q")
    out["all profile days: up vs down sign"]=tab(P.assign(s=np.sign(P.mv)),"s")
    return out
