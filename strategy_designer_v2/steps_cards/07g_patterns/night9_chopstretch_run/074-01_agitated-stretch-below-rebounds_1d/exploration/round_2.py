def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].astype(float); r=cl.pct_change(); sd=r.rolling(20).std()
            z=(cl/cl.rolling(20).mean()-1)/sd
            rng=(b["high"]-b["low"]); clpos=(cl-b["low"])/rng
            df=pd.DataFrame({"coin":c,"w":w,"pos":np.arange(len(b)),"z":z,
                "ag":(b["regime"]!="chop").astype(int),"tr":cl/cl.shift(60)-1,
                "sdz":r/sd,"clpos":clpos,"rngz":(rng/cl)/(rng/cl).rolling(20).mean(),
                "f1":cl.shift(-1)/cl-1,"f3":cl.shift(-3)/cl-1,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    for h in (1,3): A[f"u{h}"]=A[f"f{h}"]-A.groupby("coin")[f"f{h}"].transform("mean")
    A["tq"]=pd.cut(A.tr,[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    out={}
    def tab(G,col,by):
        g=G.groupby(by,observed=True)[col]
        return pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))}).round(4)
    def slope(G,x,y):
        G=G.dropna(subset=[x,y])
        d=G.groupby("day").apply(lambda s:None)
        res=stats.linregress(G[x],G[y])
        # day-clustered t
        X=G[x]-G[x].mean(); e=G[y]-G[y].mean()-res.slope*X
        s=(X*e).groupby(G["day"]).sum()
        se=np.sqrt((s**2).sum())/(X**2).sum()
        return pd.Series({"n":len(G),"days":G.day.nunique(),"slope":res.slope,"t_cl":res.slope/se})
    Ag=A[A.ag==1].dropna(subset=["clpos","u1"])
    out["agit u1 by clpos q x trend"]=tab(Ag.assign(cq=pd.qcut(Ag.clpos,5,duplicates="drop")),"u1",["tq","cq"])
    out["agit slope u1 on clpos"]=slope(Ag,"clpos","u1").round(5)
    out["calm slope u1 on clpos"]=slope(A[A.ag==0].dropna(subset=["clpos","u1"]),"clpos","u1").round(5)
    hi=Ag[Ag.clpos>0.8]
    out["agit high close u1 by window"]=tab(hi,"u1",["w"])
    out["agit high close u1 by coin"]=tab(hi,"u1",["coin"])
    out["agit high close u1 by year"]=tab(hi.assign(y=hi.day.dt.year),"u1",["y"])
    out["agit high close: wide vs narrow day"]=tab(hi.dropna(subset=["rngz"]).assign(rq=lambda x:pd.qcut(x.rngz,3)),"u1",["rq"])
    G3=A[(A.pos%3==0)&(A.ag==0)].dropna(subset=["z","u3"])
    out["calm u3 z<0 by trend"]=tab(G3[G3.z<0].assign(zq=lambda x:pd.cut(x.z,[-9,-2,-1,0])),"u3",["tq","zq"])
    out["calm slope u3 on z (z<0)"]=slope(G3[G3.z<0],"z","u3").round(5)
    out["calm u3 z<-1 by window"]=tab(G3[G3.z<-1],"u3",["w"])
    return out
