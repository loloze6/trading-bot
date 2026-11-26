def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            df=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r":r,"n1":c.shift(-1)/c-1,"n2":c.shift(-2)/c.shift(-1)-1,
                "rng":(b["high"]-b["low"])/c,
                "cl":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "agit":(b["regime"]!="chop").astype(int),
                "r60":c/c.shift(60)-1,"yr":pd.to_datetime(b["timestamp"]).dt.year})
            df["vol60"]=r.abs().rolling(60,min_periods=20).mean()
            df["z"]=df["r"]/df["vol60"]; df["rz"]=df["rng"]/df["vol60"]
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["x1"]=d["n1"]-d.groupby("coin")["n1"].transform("mean")
    d["x2"]=d["n2"]-d.groupby("coin")["n2"].transform("mean")
    d=d.dropna(subset=["z","x1","cl"])
    out={}
    def ols(s,xs,y):
        s=s.dropna(subset=xs+[y]); X=np.column_stack([np.ones(len(s))]+[s[x].values for x in xs]); Y=s[y].values
        bta=np.linalg.lstsq(X,Y,rcond=None)[0]; e=Y-X@bta
        # day-clustered se
        XtXi=np.linalg.inv(X.T@X); g=pd.DataFrame(X*e[:,None]).groupby(s["ts"].values).sum().values
        V=XtXi@(g.T@g)@XtXi; return bta,bta/np.sqrt(np.diag(V)),len(s),s["ts"].nunique()
    res=[]
    for a in [0,1]:
        for side in ["down","up"]:
            s=d[(d.agit==a)&((d.r<0) if side=="down" else (d.r>0))].copy()
            for xs in [["z"],["z","cl"],["z","rz"],["z","cl","rz"]]:
                for y in ["x1","x2"]:
                    b_,t_,n,nd=ols(s,xs,y)
                    res.append([a,side,"+".join(xs),y]+[f"{v:.4f}/{tt:.2f}" for v,tt in zip(b_[1:],t_[1:])]+[None]*(3-len(xs))+[n,nd])
    out["clustered regs (coef/t)"]=pd.DataFrame(res,columns=["agit","side","xs","y","c1","c2","c3","n","days"])
    d["trend"]=np.where(d.r60>0.1,"rising",np.where(d.r60<-0.1,"falling","choppy"))
    res=[]
    for a in [0,1]:
        for tr in ["rising","choppy","falling"]:
            s=d[(d.agit==a)&(d.trend==tr)&(d.r<0)]
            if len(s)>50:
                b_,t_,n,nd=ols(s,["z"],"x1"); res.append([a,tr,"down",b_[1],t_[1],n,nd])
            s=d[(d.agit==a)&(d.trend==tr)&(d.r>0)]
            if len(s)>50:
                b_,t_,n,nd=ols(s,["z"],"x1"); res.append([a,tr,"up",b_[1],t_[1],n,nd])
    out["slope by profile"]=pd.DataFrame(res,columns=["agit","trend","side","slope","t","n","days"])
    res=[]
    for y in sorted(d.yr.unique()):
        s=d[(d.agit==1)&(d.r<0)&(d.yr==y)]
        if len(s)>40:
            b_,t_,n,nd=ols(s,["z"],"x1"); res.append([y,b_[1],t_[1],n])
    out["agit down slope by year"]=pd.DataFrame(res,columns=["yr","slope","t","n"])
    # all days, agitated: z regression full sample both sides, wide range low close
    s=d[d.agit==1]
    b_,t_,n,nd=ols(s,["z","cl","rz"],"x1"); out["agit all z cl rz"]=pd.Series(list(b_[1:])+list(t_[1:])+[n,nd],index=["bz","bcl","brz","tz","tcl","trz","n","days"])
    return out
