def explore(data):
    import numpy as np, pandas as pd
    out={}
    hr=[];G=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol30=r1.rolling(720).std()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"yr":ts.dt.year,"hour":ts.dt.hour,"z":r1/vol30,
                            "z6":(c/c.shift(6)-1)/(vol30*np.sqrt(6)),
                            "f1":c.shift(-1)/c-1,"f6":c.shift(-6)/c-1,"f24":c.shift(-24)/c-1})
            d["g6"]=(np.arange(len(d))%6==0)
            d["g24"]=(np.arange(len(d))%24==0)
            hr.append(d)
            H=72
            past=c/c.shift(H)-1
            er=(c-c.shift(H)).abs()/(c.diff().abs().rolling(H).sum())
            g=pd.DataFrame({"coin":coin,"w":w,"yr":ts.dt.year,"past":past,"er":er,"fwd":c.shift(-H)/c-1,
                            "f24":c.shift(-24)/c-1}).iloc[::H]
            G.append(g)
    D=pd.concat(hr)
    def agg(x,col):
        a=x.groupby(col)["y"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"])); return a
    # hourly reversal: next-hour by z bucket, by coin (z in (-2,-1] minus mean)
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,1,2,99])
    x=D.dropna(subset=["z","f1"]).copy(); x["y"]=x["f1"]
    a=x[x.z<-1].groupby("coin")["y"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["next1h after z<-1 by coin"]=a
    a=x[x.z<-1].groupby("yr")["y"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["next1h after z<-1 by year"]=a
    # 6h past move graded, next 6h nonoverlap
    x=D[D.g6].dropna(subset=["z6","f6"]).copy(); x["y"]=x["f6"]-x.groupby("coin")["f6"].transform("mean")
    x["b"]=pd.cut(x["z6"],[-99,-3,-2,-1,0,1,2,3,99])
    out["next6h ex by past6h z (grid6)"]=agg(x,"b")
    x=D[D.g24].dropna(subset=["z6","f24"]).copy(); x["y"]=x["f24"]-x.groupby("coin")["f24"].transform("mean")
    x["b"]=pd.cut(x["z6"],[-99,-2,-1,0,1,2,99])
    out["next24h ex by past6h z (grid24)"]=agg(x,"b")
    # hour 20-21 effect by coin and year
    x=D.dropna(subset=["f1"]).copy(); x["y"]=x["f1"]
    s=x[x.hour.isin([20,21])]
    a=s.groupby("coin")["y"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["hours20-21 next1h by coin"]=a
    a=s.groupby("yr")["y"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["hours20-21 next1h by year"]=a
    # ER top in up-moves by coin, year
    G=pd.concat(G).dropna(subset=["fwd","past","er"])
    G["ex"]=G["fwd"]-G.groupby("coin")["fwd"].transform("mean")
    up=G[G.past>0].copy()
    up["q"]=up.groupby("coin")["er"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    top=up[up.q==4].copy(); top["y"]=top["ex"]
    out["up ER top q by coin"]=agg(top,"coin")
    out["up ER top q by year"]=agg(top,"yr")
    up["y"]=up["ex"]
    out["corr er vs ex in up (spearman)"]=float(up[["er","ex"]].corr(method="spearman").iloc[0,1])
    # book cost drag
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            pv=b["total_portfolio_value"].astype(float); post=b["postRebalance_total_value"].astype(float)
            fee=((pv-post)/pv).sum()
            c=b["close"].astype(float)
            gross=(b["postRebalance_current_allocation"]*(c.shift(-1)/c-1)).sum()
            turn=(b["postRebalance_current_allocation"]-b["previous_allocation"]).abs().sum()
            rows.append({"coin":coin,"fee":fee,"gross":gross,"turnover":turn,"bars":len(b)})
    R=pd.DataFrame(rows).groupby("coin").sum()
    R["fee_per_day"]=R.fee/R.bars*24; R["gross_per_day"]=R.gross/R.bars*24; R["turn_per_day"]=R.turnover/R.bars*24
    out["book gross vs fee"]=R[["fee_per_day","gross_per_day","turn_per_day"]]
    return out
