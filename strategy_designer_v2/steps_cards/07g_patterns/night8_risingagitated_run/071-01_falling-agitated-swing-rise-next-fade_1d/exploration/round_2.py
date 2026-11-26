import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change(); sd=r.rolling(20).std()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"z":r/sd,"r":r,"n1":c.shift(-1)/c-1,
                "fa":(b["regime"]=="unknown").astype(int),"tr60":c/c.shift(60)-1,
                "uw":(b["high"]-np.maximum(c,b["open"]))/c/sd,
                "lw":(np.minimum(c,b["open"])-b["low"])/c/sd,
                "r3":(c/c.shift(3)-1)/(sd*np.sqrt(3)),
                "rng":(b["high"]-b["low"])/c/sd,
                "day":ts.dt.floor("D"),"wd":ts.dt.weekday,"yr":ts.dt.year})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["z","n1"])
    mu=D.groupby("coin")["n1"].mean(); D["x1"]=D["n1"]-D["coin"].map(mu)
    def agg(g,col="x1"):
        s=g[col].dropna()
        return pd.Series({"n":len(s),"mean%":100*s.mean(),"t":s.mean()/s.std()*np.sqrt(len(s)) if len(s)>2 else np.nan})
    def cslope(g,xc,yc="x1"):
        g=g.dropna(subset=[xc,yc]); x=g[xc].values; y=g[yc].values
        X=np.column_stack([np.ones(len(x)),x]); b=np.linalg.lstsq(X,y,rcond=None)[0]
        e=y-X@b; XtXi=np.linalg.inv(X.T@X)
        meat=np.zeros((2,2))
        for _,idx in g.groupby("day").indices.items():
            s=X[idx].T@e[idx]; meat+=np.outer(s,s)
        G=g["day"].nunique(); V=XtXi@meat@XtXi*G/(G-1)
        return pd.Series({"n":len(g),"days":G,"slope%":100*b[1],"t":b[1]/np.sqrt(V[1,1])})
    out={}
    FA=D[D.fa==1]
    out["FA slope x1 on z, all days"]=cslope(FA,"z")
    out["FA slope x1 on z, z in (-1,1.5)"]=cslope(FA[(FA.z>-1)&(FA.z<1.5)],"z")
    out["FA slope x1 on r3 (3d scaled)"]=cslope(FA,"r3")
    D["tb"]=pd.cut(D["tr60"],[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    for t in ["fall","chop","rise"]:
        g=D[(D.tb==t)&(D.fa==0)]
        out[f"nonFA {t}: slope x1 on z"]=cslope(g,"z")
    up=FA[FA.z>0].copy()
    out["FA up: slope x1 on upper wick"]=cslope(up,"uw")
    up["ub"]=pd.qcut(up["uw"],3)
    out["FA up by upper wick tercile"]=up.groupby("ub").apply(agg)
    up["r3b"]=pd.qcut(up["r3"],3)
    out["FA up by 3d scaled return tercile"]=up.groupby("r3b").apply(agg)
    dn=FA[FA.z<0].copy(); dn["lb"]=pd.qcut(dn["lw"],3)
    out["FA down by lower wick tercile"]=dn.groupby("lb").apply(agg)
    out["FA up Thu+Sun by year"]=up[up.wd.isin([3,6])].groupby("yr").apply(agg)
    out["FA up other wd by year"]=up[~up.wd.isin([3,6])].groupby("yr").apply(agg)
    out["FA all by weekday"]=FA.groupby("wd").apply(agg)
    nf=D[(D.fa==0)]
    out["nonFA by weekday by year Wed"]=nf[nf.wd==2].groupby("yr").apply(agg)
    out["all by weekday by year Thu"]=D[D.wd==3].groupby("yr").apply(agg)
    # book largest gains/losses
    br=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            br.append(dd.assign(coin=coin,w=w))
    B=pd.concat(br)
    Bd=B.groupby("day").agg(book=("book_return","mean"),coin=("coin_return","mean")).dropna()
    q=Bd["book"].quantile([0.02,0.98])
    out["book tail days: coin mean ret"]=pd.DataFrame({"n":[ (Bd.book<=q[0.02]).sum(),(Bd.book>=q[0.98]).sum()],
        "book%":[100*Bd.book[Bd.book<=q[0.02]].mean(),100*Bd.book[Bd.book>=q[0.98]].mean()],
        "coin%":[100*Bd.coin[Bd.book<=q[0.02]].mean(),100*Bd.coin[Bd.book>=q[0.98]].mean()]},index=["worst2%","best2%"])
    return out
