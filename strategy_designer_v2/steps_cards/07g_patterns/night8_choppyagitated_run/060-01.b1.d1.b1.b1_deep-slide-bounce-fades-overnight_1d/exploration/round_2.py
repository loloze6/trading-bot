def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"r1":r1,"vol":vol,"s1":r1/vol,
                "f5":(c.shift(1)/c.shift(6)-1)/vol.shift(1),
                "fwd1":c.shift(-1)/c-1,"fwd2":c.shift(-2)/c-1,
                "pos":np.arange(len(b)),"regime":b["regime"].values,
                "clpos":((c-b["low"])/(b["high"]-b["low"])).values,
                "upw":((b["high"]-np.maximum(b["open"],c))/(b["high"]-b["low"])).values,
                "year":pd.to_datetime(b["timestamp"]).dt.year.values})
            d["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D").values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    cm=D.groupby("coin")["r1"].mean()
    D["x1"]=D["fwd1"]-D["coin"].map(cm)
    D["x2"]=D["fwd2"]-2*D["coin"].map(cm)
    D["sx1"]=D["x1"]/D["vol"]
    D["prof"]=D["regime"].isin(["mean_reversion","unknown"])
    def reg(g,x,y="sx1"):
        g=g.dropna(subset=[x,y])
        if len(g)<30: return pd.Series({"n":len(g)})
        xc=g[x]-g[x].mean()
        b=(xc*g[y]).sum()/(xc**2).sum()
        e=g[y]-g[y].mean()-b*xc
        cl=(xc*e).groupby(g["day"]).sum()
        se=np.sqrt((cl**2).sum())/(xc**2).sum()
        return pd.Series({"n":len(g),"days":g["day"].nunique(),"slope":b,"t_cluster":b/se})
    def summ(g,col="x1"):
        g=g.dropna(subset=[col])
        s=g.groupby("day")[col].mean()
        return pd.Series({"n":len(g),"days":len(s),"mean%":100*g[col].mean(),"t_day":s.mean()/(s.std()/np.sqrt(len(s)))})
    P=D[D.prof]; O=D[~D.prof]
    out={}
    R=[]
    for nm,g in [("prof",P),("out",O),("prof_up",P[P.r1>0]),("prof_down",P[P.r1<=0]),("out_up",O[O.r1>0]),("out_down",O[O.r1<=0])]:
        for x in ["clpos","s1","upw"]:
            s=reg(g,x); s["set"]=nm; s["x"]=x; R.append(s)
    out["regressions_sx1"]=pd.DataFrame(R)
    U=P[(P.r1>0)&(P.f5<0)]
    out["case_regs"]=pd.DataFrame([reg(U,"s1").rename("s1"),reg(U,"f5").rename("f5"),reg(U,"clpos").rename("clpos")])
    Pu=P[P.r1>0]
    out["profup_by_clpos_q"]=Pu.assign(k=pd.qcut(Pu.clpos,4,labels=False)).groupby("k").apply(summ)
    out["profup_by_upwick_q"]=Pu.assign(k=pd.qcut(Pu.upw,4,labels=False,duplicates="drop")).groupby("k").apply(summ)
    out["profup_by_s1_q"]=Pu.assign(k=pd.qcut(Pu.s1,4,labels=False)).groupby("k").apply(summ)
    out["profup_s1q_x2grid"]=Pu[Pu.pos%2==0].assign(k=pd.qcut(Pu[Pu.pos%2==0].s1,4,labels=False)).groupby("k").apply(lambda g:summ(g,"x2"))
    out["prof_clpos_by_year"]=P.assign(k=(P.clpos>2/3)).groupby(["year","k"]).apply(summ)
    out["prof_clpos_by_coin_highthird"]=P[P.clpos>2/3].groupby("coin").apply(summ)
    return out
