def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            v=b["volume"]
            f=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),
                "z0":r/sd,"width":(b["high"]-b["low"])/c/sd,
                "loc":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "tr60":c/c.shift(60)-1,
                "lvr":np.log(v/v.rolling(20,min_periods=10).mean()),
                "sd":sd,"nxt":c.shift(-1)/c-1,"nxt2":c.shift(-2)/c-1})
            # non-overlap grid for 2-day
            f["g2"]=(np.arange(len(f))%2==0)
            rows.append(f)
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin")["nxt"].mean(); d["ex"]=d["nxt"]-d["coin"].map(mu)
    d["exz"]=d["ex"]/d["sd"]
    d["day"]=d["ts"].dt.floor("D")
    d["yr"]=d["ts"].dt.year
    def summ(g,col="ex"):
        g=g.dropna(subset=[col])
        if len(g)<15: return pd.Series({"n":len(g)})
        s=g.groupby("day")[col].sum(); nd=len(s)
        return pd.Series({"n":len(g),"days":nd,"mean%":100*g[col].mean(),
                          "t_day":s.mean()/(s.std(ddof=1)/np.sqrt(nd))})
    out={}
    d=d.dropna(subset=["lvr","z0"])
    d["vq"]=d.groupby("coin")["lvr"].transform(lambda x: pd.qcut(x,3,labels=["lo","mid","hi"]))
    d["zs"]=pd.cut(d["z0"],[-100,-1,1,100],labels=["down","flat","up"])
    out["vol tercile x own move"]=d.groupby(["zs","vq"]).apply(summ).unstack()
    # residual of next-day excess z on z0 within coin, then by volume
    d["res"]=d["exz"]-d.groupby(["coin","zs"])["exz"].transform("mean")
    out["vol tercile, residual exz"]=d.groupby("vq").apply(lambda g: summ(g,"res"))
    out["vol tercile by year (ex)"]=d.groupby(["yr","vq"]).apply(summ)["t_day"].unstack()
    d["trb"]=pd.cut(d["tr60"],[-10,-0.1,0.1,100],labels=["fall","chop","rise"])
    out["vol tercile x trend"]=d.groupby(["trb","vq"]).apply(summ).unstack()
    # signed: volume x sign of day
    d["sv"]=d["lvr"]*np.sign(d["z0"])
    d["svq"]=pd.qcut(d["sv"],5)
    out["signed volume quintile"]=d.groupby("svq").apply(summ)
    hw=d[(d.width>=2)&(d["loc"]>=0.75)&(d.trb=="fall")]
    out["fall wide high-close by vol"]=hw.groupby("vq").apply(summ)
    out["fall wide high-close by year"]=hw.groupby("yr").apply(summ)
    out["fall up-days z>0.5 by year"]=d[(d.trb=="fall")&(d.z0>0.5)].groupby("yr").apply(summ)
    lw=d[(d.width>=2)&(d["loc"]<=0.25)]
    out["wide low-close by year"]=lw.groupby("yr").apply(summ)
    return out
