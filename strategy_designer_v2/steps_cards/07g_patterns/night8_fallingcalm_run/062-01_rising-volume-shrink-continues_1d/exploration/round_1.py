def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            n=len(b)
            fwd5=c.shift(-5)/c-1
            fwd1=c.shift(-1)/c-1
            r1=c/c.shift(1)-1
            r5=c/c.shift(5)-1
            r20=c/c.shift(20)-1
            sd20=r1.rolling(20).std()
            vr=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            vr10=np.log(v.rolling(10).mean()/v.shift(10).rolling(30).mean())
            rng=(b["high"]-b["low"])/c
            clpos=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(n),"fwd5":fwd5,"fwd1":fwd1,"r1":r1,"r5":r5,"r20":r20,
                "sd20":sd20,"vr":vr,"vr10":vr10,"rng":rng,"clpos":clpos,"fc":b["forecast"].astype(float),
                "reg":b["regime"].astype(str),"rec":b["debug_info.components.vol_dryup.last_history_value"],
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,"yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    D=pd.concat(rows)
    drift=D[D.pos%5==0].groupby("coin")["fwd5"].mean()
    D["ex5"]=D["fwd5"]-D["coin"].map(drift)
    D["sdn"]=D["sd20"]/D.groupby("coin")["sd20"].transform("median")
    D["z5"]=D["r5"]/(D["sd20"]*np.sqrt(5))
    G=D[(D.pos%5==0)].dropna(subset=["ex5"])
    out={}
    def tab(g,col,q=5):
        g=g.dropna(subset=[col])
        g=g.assign(b=pd.qcut(g[col],q,labels=False,duplicates="drop"))
        r=g.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("ex5","size"),mean=("ex5","mean"),sd=("ex5","std"))
        r["t"]=r["mean"]/(r["sd"]/np.sqrt(r["n"]))
        return r.drop(columns="sd").round(4)
    def slope(g,col):
        g=g.dropna(subset=[col])
        s=stats.linregress(g[col],g["ex5"]); return f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(g)}"
    R=G[G.reg=="unknown"]; N=G[G.reg!="unknown"]
    out["regime counts"]=G.reg.value_counts()
    out["rising: vr quintiles"]=tab(R,"vr")
    out["not rising: vr quintiles"]=tab(N,"vr")
    out["all: z5 quintiles"]=tab(G,"z5")
    out["rising: z5"]=tab(R,"z5"); out["notrising: z5"]=tab(N,"z5")
    out["all: sdn quintiles"]=tab(G,"sdn")
    out["all: r20 quintiles"]=tab(G,"r20")
    out["all: rng quint"]=tab(G,"rng")
    out["all: clpos quint"]=tab(G,"clpos")
    out["all: vr10 quint"]=tab(G,"vr10")
    out["slopes"]=pd.Series({k:slope(gg,c) for k,gg,c in [("R vr",R,"vr"),("N vr",N,"vr"),("all vr",G,"vr"),("all z5",G,"z5"),("R z5",R,"z5"),("N z5",N,"z5"),("all r20",G,"r20"),("N r20",N,"r20"),("all vr10",G,"vr10"),("all clpos",G,"clpos")]})
    wd=D.dropna(subset=["fwd1"]).groupby("wd")["fwd1"].agg(["mean","std","size"]); wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["size"]))
    out["weekday 1d"]=wd.round(4)
    yb=R.groupby("yr").apply(lambda g: pd.Series({"n":len(g),"corr_vr":g[["vr","ex5"]].corr().iloc[0,1]}))
    out["rising vr corr by year"]=yb.round(3)
    return out
