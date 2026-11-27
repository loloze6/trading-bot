def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].values; n=len(b)
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            b["loc"]=(b["close"]-b["low"])/rng
            for h in (1,2,3):
                fr=np.full(n,np.nan); fr[:n-h]=c[h:]/c[:n-h]-1; b[f"f{h}"]=fr
            b["agit"]=(b["regime"]!="chop").astype(int)
            b["pos"]=np.arange(n); b["coin"]=coin
            ts=pd.to_datetime(b["timestamp"])
            b["day"]=ts.dt.floor("D"); b["year"]=ts.dt.year
            b["tr60"]=b["close"]/b["close"].shift(60)-1
            b["r1"]=b["close"].pct_change()
            rows.append(b[["coin","pos","loc","agit","day","year","tr60","r1","f1","f2","f3"]])
    d=pd.concat(rows,ignore_index=True)
    for h in (1,2,3):
        dr=d[d.pos%h==0].groupby("coin")[f"f{h}"].mean()
        d[f"u{h}"]=d[f"f{h}"]-d.coin.map(dr)
    d["locc"]=d["loc"]-0.5
    d["tp"]=pd.cut(d["tr60"],[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    d["locq"]=pd.cut(d["loc"],[-0.01,0.2,0.4,0.6,0.8,1.01],labels=["q1","q2","q3","q4","q5"])
    def cs(g,y):
        g=g.dropna(subset=[y,"locc"])
        if len(g)<30: return [np.nan]*4
        X=g["locc"].values; Y=g[y].values
        b=np.sum(X*(Y-Y.mean()))/np.sum(X*X); e=(Y-Y.mean())-b*X
        s=pd.Series(X*e).groupby(g["day"].values).sum()
        se=np.sqrt(np.sum(s**2))/np.sum(X*X)
        return [b,b/se,len(g),g["day"].nunique()]
    def cm(g,y):
        g=g.dropna(subset=[y])
        if len(g)<10: return [np.nan]*3
        m=g[y].mean(); s=(g[y]-m).groupby(g["day"].values).sum()
        se=np.sqrt(np.sum(s**2))/len(g)
        return [m,m/se,g["day"].nunique()]
    res=[]
    for a in (0,1):
        for h in (1,2,3):
            g=d[(d.agit==a)&(d.pos%h==0)]
            res.append([f"agit{a}",h,*cs(g,f"u{h}")])
    A=d[(d.agit==1)]
    for yr,g in A.groupby("year"): res.append([str(yr),1,*cs(g,"u1")])
    for tp,g in A.groupby("tp"): res.append([str(tp),1,*cs(g,"u1")])
    out={"slope_dayclus":pd.DataFrame(res,columns=["grp","h","slope","t","n","days"])}
    q=[]
    for tp in ["falling","choppy","rising"]:
        for lq in ["q1","q5"]:
            g=A[(A.tp==tp)&(A.locq==lq)]
            q.append([tp,lq,*cm(g,"u1"),*cm(g,"f1")[:2]])
    out["q1q5_next_day_by_trend"]=pd.DataFrame(q,columns=["trend","locq","u1","t_u1","days","f1","t_f1"])
    yy=[]
    for yr,g in A.groupby("year"):
        yy.append([yr,*cm(g[g.locq=="q5"],"u1"),*cm(g[g.locq=="q1"],"u1")])
    out["q5_q1_u1_by_year"]=pd.DataFrame(yy,columns=["year","q5u1","q5t","q5d","q1u1","q1t","q1d"])
    return out
