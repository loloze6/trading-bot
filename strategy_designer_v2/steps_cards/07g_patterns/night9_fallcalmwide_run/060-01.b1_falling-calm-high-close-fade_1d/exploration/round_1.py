def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            f=pd.DataFrame({
                "coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),
                "r0":r,"z0":r/sd,
                "width":(b["high"]-b["low"])/c/sd,
                "loc":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "tr60":c/c.shift(60)-1,
                "tr20":c/c.shift(20)-1,
                "vr":b["volume"]/b["volume"].rolling(20,min_periods=10).mean(),
                "sd":sd,
                "fc":b["forecast"],
                "pos":b["postRebalance_current_allocation"],
                "nxt":c.shift(-1)/c-1,
                "nxt3":c.shift(-3)/c-1})
            rows.append(f)
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin")["nxt"].mean()
    d["ex"]=d["nxt"]-d["coin"].map(mu)
    d["exz"]=d["ex"]/d["sd"]
    d["day"]=d["ts"].dt.floor("D")
    def summ(g,col="ex"):
        g=g.dropna(subset=[col])
        if len(g)<15: return pd.Series({"n":len(g)})
        s=g.groupby("day")[col].sum(); nd=len(s)
        m=g[col].mean()
        t=s.mean()/(s.std(ddof=1)/np.sqrt(nd))*1 if nd>2 else np.nan
        return pd.Series({"n":len(g),"days":nd,"mean%":100*m,"t_day":t})
    out={}
    d["wb"]=pd.cut(d["width"],[0,1,1.5,2,3,100])
    d["lb"]=pd.cut(d["loc"],[-0.01,0.25,0.5,0.75,1.01])
    out["width x loc next-day excess"]=d.groupby(["wb","lb"]).apply(summ).reset_index()
    d["trb"]=pd.cut(d["tr60"],[-10,-0.1,0.1,100],labels=["fall","chop","rise"])
    hw=d[(d.width>=2)&(d["loc"]>=0.75)]
    out["wide high-close by trend60"]=hw.groupby("trb").apply(summ)
    lw=d[(d.width>=2)&(d["loc"]<=0.25)]
    out["wide low-close by trend60"]=lw.groupby("trb").apply(summ)
    d["zb"]=pd.cut(d["z0"],[-100,-2.5,-1.5,-0.5,0.5,1.5,2.5,100])
    out["own-move z bucket next-day"]=d.groupby("zb").apply(summ)
    out["own-move z x trend"]=d.groupby(["trb","zb"]).apply(summ).reset_index()
    d["wd"]=d["ts"].dt.dayofweek
    out["weekday next-day"]=d.groupby("wd").apply(summ)
    d["vb"]=pd.qcut(d["vr"],5)
    out["volume ratio next-day"]=d.groupby("vb").apply(summ)
    act=d[d["fc"]<0]
    out["active cases"]=summ(act)
    out["active by window"]=act.groupby("w").apply(summ)
    out["active by coin"]=act.groupby("coin").apply(summ)
    return out
