def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["pos"]=np.arange(len(b))
            d["r1"]=r; d["r3"]=c/c.shift(3)-1
            sd=r.rolling(30,min_periods=20).std(); d["sd"]=sd
            d["rr"]=((b["high"]-b["low"])/c)/sd
            d["z1"]=r/sd; d["z3"]=d["r3"]/(sd*np.sqrt(3))
            d["f1"]=c.shift(-1)/c-1; d["f2"]=c.shift(-2)/c-1; d["f3"]=c.shift(-3)/c-1
            d["inFA"]=b["regime"]!="chop"
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["day"]=D["ts"].dt.floor("D")
    for h in [1,2,3]:
        dr=D.groupby("coin")["f%d"%h].mean()
        D["u%d"%h]=D["f%d"%h]-D["coin"].map(dr)
    def st(g,col="u1",grid=1):
        g=g[g["pos"]%grid==0].dropna(subset=[col])
        if len(g)<10: return pd.Series({"n":len(g),"mean_u":np.nan,"t_day":np.nan})
        s=g.groupby("day")[col].sum(); G=len(s)
        t=s.sum()/np.sqrt((s**2).sum()*G/(G-1))
        return pd.Series({"n":len(g),"days":G,"mean_u":g[col].mean(),"t_day":t})
    out={}
    FA=D[D.inFA].copy()
    up=FA[FA.r1>0].copy()
    up["z1q"]=pd.qcut(up["z1"],4,labels=False)
    out["FA_up_z1_quartile"]=up.groupby("z1q").apply(st)
    out["FA_up_z1_quartile_mean_z1"]=up.groupby("z1q")["z1"].mean()
    for col in ["u1"]:
        g=up.dropna(subset=["u1","z1"])
        x=g["z1"]-g["z1"].mean(); y=g["u1"]
        b_=(x*y).sum()/(x**2).sum(); e=y-y.mean()-b_*x
        # day-clustered se
        sc=(x*e).groupby(g["day"]).sum()
        se=np.sqrt((sc**2).sum())/(x**2).sum()
        out["FA_up_slope_u1_on_z1"]=pd.Series({"slope":b_,"t_cluster":b_/se,"n":len(g)})
    up["z3q"]=pd.qcut(up["z3"],3,labels=False)
    out["FA_up_z3_tercile"]=up.groupby("z3q").apply(st)
    out["FA_up_z1q_h2"]=up.groupby("z1q").apply(lambda g: st(g,"u2",2))
    out["FA_up_z1q_h3"]=up.groupby("z1q").apply(lambda g: st(g,"u3",3))
    top=up[up.z1q>=2]
    out["FA_up_tophalf_by_coin"]=top.groupby("coin").apply(st)
    out["FA_up_tophalf_by_year"]=top.groupby(top.ts.dt.year).apply(st)
    out["FA_up_tophalf_all"]=st(top)
    nf=D[(~D.inFA)&(D.r1>0)].copy()
    nf["z1q"]=pd.qcut(nf["z1"],4,labels=False)
    out["nonFA_up_z1_quartile"]=nf.groupby("z1q").apply(st)
    return out
