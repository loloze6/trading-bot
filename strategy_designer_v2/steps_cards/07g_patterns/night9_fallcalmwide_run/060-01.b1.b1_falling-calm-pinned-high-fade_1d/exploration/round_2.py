def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"])})
            d["r"]=r
            d["fwd1"]=c.shift(-1)/c-1
            d["fwd3"]=c.shift(-3)/c-1
            d["grid3"]=(np.arange(len(b))%3==0)
            sd=r.rolling(30,min_periods=20).std()
            d["sd30"]=sd
            rng=(b["high"]-b["low"])
            d["width"]=(rng/c)/sd
            d["loc"]=((c-b["low"])/rng.replace(0,np.nan))
            d["ret60"]=c/c.shift(60)-1
            d["fc"]=b["forecast"]
            d["year"]=d["ts"].dt.year
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["u1"]=D["fwd1"]-D.groupby("coin")["fwd1"].transform("mean")
    g3=D[D.grid3]
    m3=g3.groupby("coin")["fwd3"].mean()
    D["u3"]=D["fwd3"]-D["coin"].map(m3)
    D["sdm"]=D.groupby("coin")["sd30"].transform("median")
    D["ag"]=np.where(D["sd30"]>D["sdm"],"agit","calm")
    D["tr"]=np.where(D["ret60"]>0.1,"rising",np.where(D["ret60"]<-0.1,"falling","choppy"))
    D.loc[D["ret60"].isna(),"tr"]="na"
    D["prof"]=D["tr"]+" "+D["ag"]
    def ct(g,col):
        g=g.dropna(subset=[col])
        if len(g)<8: return pd.Series({"n":len(g),"days":g["ts"].nunique(),"mean%":np.nan,"t":np.nan})
        m=g[col].mean()
        dd=g.groupby("ts")[col].agg(["sum","count"])
        D_=len(dd)
        se=np.sqrt(((dd["sum"]-dd["count"]*m)**2).sum()*D_/(D_-1))/len(g)
        return pd.Series({"n":len(g),"days":D_,"mean%":m*100,"t":m/se if se>0 else np.nan})
    X=D.dropna(subset=["width","loc","u1"]).copy()
    q75=X["width"].quantile(0.75)
    W=X[X.width>=q75].copy()
    W["lh"]=pd.cut(W["loc"],[-0.01,0.35,0.65,1.01],labels=["low","mid","high"])
    out={}
    out["q75 width"]=float(q75)
    t1=W.groupby(["prof","lh"]).apply(lambda g: ct(g,"u1")).reset_index()
    out["wide days u1 by profile x loc"]=t1
    W3=W[W.grid3]
    out["wide days u3 (grid) by loc"]=W3.groupby("lh").apply(lambda g: ct(g,"u3")).reset_index()
    out["wide days u3 by agit x loc"]=W3.groupby(["ag","lh"]).apply(lambda g: ct(g,"u3")).reset_index()
    # graded: correlation of u1 with (0.5-loc)*width over wide days, by agit
    res=[]
    for k,g in W.groupby("ag"):
        s=(0.5-g["loc"])*g["width"]
        rr,p=stats.spearmanr(s,g["u1"])
        res.append({"ag":k,"n":len(g),"spearman":rr,"p":p})
    for k,g in W.groupby("tr"):
        s=(0.5-g["loc"])*g["width"]
        rr,p=stats.spearmanr(s,g["u1"])
        res.append({"ag":"tr "+k,"n":len(g),"spearman":rr,"p":p})
    out["graded low-close x width vs u1"]=pd.DataFrame(res)
    # wide low-close by window halves (stability) by year
    WL=W[W.lh=="low"]
    out["wide low close u1 by year"]=WL.groupby("year").apply(lambda g: ct(g,"u1")).reset_index()
    act=X[X.fc<0]
    act=act.assign(s=-act["u1"])
    out["active short cases B,C"]=ct(act,"s").to_frame().T
    return out
