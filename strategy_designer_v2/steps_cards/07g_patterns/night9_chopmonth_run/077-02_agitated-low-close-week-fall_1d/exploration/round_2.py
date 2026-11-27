def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].values; n=len(b)
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            b["loc"]=(b["close"]-b["low"])/rng
            for h in (1,7):
                fr=np.full(n,np.nan); fr[:n-h]=c[h:]/c[:n-h]-1; b[f"f{h}"]=fr
            fr=np.full(n,np.nan); fr[1:n-7]=c[8:]/c[1:n-7]-1; b["f2_8"]=fr  # day1 close -> day8 close
            b["agit"]=(b["regime"]!="chop").astype(int)
            b["pos"]=np.arange(n); b["coin"]=coin; b["win"]=w
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["tr60"]=b["close"]/b["close"].shift(60)-1
            rows.append(b[["coin","win","pos","loc","agit","day","year","tr60","f1","f7","f2_8"]])
    d=pd.concat(rows,ignore_index=True)
    g7=d[d.pos%7==0]
    dr7=g7.groupby("coin")["f7"].mean(); dr1=d.groupby("coin")["f1"].mean()
    d["u7"]=d["f7"]-d.coin.map(dr7); d["u28"]=d["f2_8"]-d.coin.map(dr7)
    d["u1"]=d["f1"]-d.coin.map(dr1)
    d["locq"]=pd.cut(d["loc"],[-0.01,0.2,0.4,0.6,0.8,1.01],labels=["q1","q2","q3","q4","q5"])
    d["locc"]=d["loc"]-0.5
    out={}
    def clus_slope(g,y):
        g=g.dropna(subset=[y,"locc"])
        X=g["locc"].values; Y=g[y].values
        b=np.sum(X*(Y-Y.mean()))/np.sum(X*X)
        e=(Y-Y.mean())-b*X
        s=pd.Series(X*e).groupby(g["day"].values).sum()
        se=np.sqrt(np.sum(s**2))/np.sum(X*X)
        return b,b/se,len(g),g["day"].nunique()
    A=d[(d.agit==1)&(d.pos%7==0)]
    res=[]
    for y in ("u7","u28"):
        res.append(["all",y,*clus_slope(A,y)])
    for coin,g in A.groupby("coin"):
        if len(g)>30: res.append([coin,"u7",*clus_slope(g,"u7")])
    for yr,g in A.groupby("year"): res.append([str(yr),"u7",*clus_slope(g,"u7")])
    A=A.copy(); A["tp"]=pd.cut(A["tr60"],[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    for tp,g in A.groupby("tp"): res.append([str(tp),"u7",*clus_slope(g,"u7")])
    C=d[(d.agit==0)&(d.pos%7==0)]
    res.append(["calm","u7",*clus_slope(C,"u7")])
    out["slope_clustered"]=pd.DataFrame(res,columns=["group","y","slope","t_dayclus","n","days"])
    # all grid offsets for robustness of q5 and q1
    rr=[]
    for off in range(7):
        g=d[(d.agit==1)&(d.pos%7==off)].dropna(subset=["u7"])
        m=g.groupby("locq")["u7"].mean()
        b,t,n,_=clus_slope(g,"u7")
        rr.append([off,m["q1"],m["q5"],b,t,n])
    out["offsets"]=pd.DataFrame(rr,columns=["off","q1_u7","q5_u7","slope","t","n"])
    g=d[(d.agit==1)&(d.pos%7==0)].dropna(subset=["u28"])
    r=g.groupby("locq")["u28"].agg(["mean","count","std"]); r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
    out["u_day2to8_by_loc_agit"]=r
    A2=A.dropna(subset=["u7"])
    r=A2.groupby(["tp","locq"])["u7"].agg(["mean","count"])
    out["tp_loc_u7"]=r
    return out
