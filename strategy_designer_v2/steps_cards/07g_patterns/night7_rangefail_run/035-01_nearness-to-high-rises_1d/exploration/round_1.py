def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]; drows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            raw=b.get("debug_info.components.near_high.last_history_value")
            fwd=c.shift(-H)/c-1
            ret5p=c/c.shift(5)-1
            ret20p=c/c.shift(20)-1
            ret60=c/c.shift(60)-1
            vol20=r1.rolling(20).std()
            z1=r1/vol20.shift(1)
            rng=(b["high"]-b["low"])/c
            clpos=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"fwd":fwd,"raw":raw,"fc":b["forecast"],
                "z1":z1,"r5p":ret5p/ (vol20*np.sqrt(5)),"r20p":ret20p/(vol20*np.sqrt(20)),"ret60":ret60,"vol20":vol20,
                "rng":rng/vol20,"clpos":clpos,"wd":ts.dt.weekday,"day":ts.dt.floor("D"),
                "alloc":b["postRebalance_current_allocation"],"r1n":r1.shift(-1)})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    drift=A[A.pos%H==0].groupby("coin")["fwd"].mean()
    A["ex"]=A["fwd"]-A["coin"].map(drift)
    G=A[(A.pos%H==0)&A.ex.notna()].copy()
    def tab(col,q=5):
        g=G.dropna(subset=[col]).copy()
        g["b"]=pd.qcut(g[col].rank(method="first"),q,labels=False)
        out=g.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("ex","size"),mean_ex=("ex","mean"),sd=("ex","std"))
        out["t"]=out.mean_ex/(out.sd/np.sqrt(out.n))
        return out.drop(columns="sd")
    res={}
    for col in ["raw","z1","r5p","r20p","ret60","vol20","rng","clpos"]:
        res["q_"+col]=tab(col)
    # trend profile x raw
    g=G.dropna(subset=["raw","ret60"]).copy()
    g["tr"]=np.where(g.ret60>0.1,"rising",np.where(g.ret60<-0.1,"falling","choppy"))
    g["rq"]=pd.qcut(g.raw.rank(method="first"),3,labels=["far","mid","near"])
    p=g.groupby(["tr","rq"]).agg(n=("ex","size"),m=("ex","mean"),sd=("ex","std"));p["t"]=p.m/(p.sd/np.sqrt(p.n))
    res["trend_x_near"]=p.drop(columns="sd")
    # slope per window
    sl=[]
    for w,gg in G.dropna(subset=["raw"]).groupby("w"):
        s=stats.linregress(gg.raw,gg.ex); sl.append((w,len(gg),s.slope,s.slope/s.stderr))
    res["slope_by_window"]=pd.DataFrame(sl,columns=["w","n","slope","t"])
    # weekday daily return
    wd=A.dropna(subset=["r1n"]).groupby("wd")["r1n"].agg(["size","mean","std"]);wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["size"]))
    res["next_day_ret_by_weekday_of_bar"]=wd
    # book daily
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy();d["coin"]=coin;d["w"]=w;D.append(d)
    D=pd.concat(D)
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    res["book_by_window"]=bk.groupby(level=0).agg(["mean","std"])
    q=pd.qcut(bk.coin_return.rank(method="first"),5,labels=False)
    res["book_by_market_day_quintile"]=bk.groupby(q.values).mean()
    return res
