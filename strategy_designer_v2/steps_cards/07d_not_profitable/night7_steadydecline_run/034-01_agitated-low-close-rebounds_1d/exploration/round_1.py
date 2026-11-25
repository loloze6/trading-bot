def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            rng=(h-l)
            b["clv"]=np.where(rng>0,(h-c)/rng,np.nan)  # 0 at high, 1 at low
            b["rngpct"]=rng/c
            b["r1"]=c.shift(-1)/c-1
            b["r2"]=c.shift(-2)/c-1
            b["r3"]=c.shift(-3)/c-1
            b["ret1"]=c/c.shift(1)-1
            b["tr60"]=c/c.shift(60)-1
            b["pos"]=b["postRebalance_current_allocation"].astype(float)
            b["dpos"]=(b["pos"]-b["previous_allocation"].astype(float)).abs()
            b["gain"]=b["pos"]*b["r1"]
            b["fee"]=b["dpos"]*0.00095
            b["coin"]=coin; b["w"]=w; b["i"]=np.arange(len(b))
            b["agit"]=b["regime"]!="chop"
            rows.append(b[["coin","w","i","clv","rngpct","r1","r2","r3","ret1","tr60","pos","dpos","gain","fee","agit","forecast"]])
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin")["r1"].mean(); d["x1"]=d["r1"]-d["coin"].map(mu)
    out={}
    def summ(g,col="x1"):
        s=g[col].dropna(); return pd.Series({"n":len(s),"mean%":s.mean()*100,"t":s.mean()/s.std()*np.sqrt(len(s)) if len(s)>2 else np.nan})
    d["clvq"]=pd.qcut(d["clv"],5,labels=["q1hi","q2","q3","q4","q5low"])
    out["x1 by clv quintile, agitated/calm"]=d.groupby(["agit","clvq"]).apply(summ).unstack(0) if False else d.groupby(["agit","clvq"]).apply(summ)
    a=d[d.agit].copy()
    # range size interaction
    a["rq"]=a.groupby("coin")["rngpct"].transform(lambda s: pd.qcut(s,3,labels=["small","mid","big"]))
    a["sgn"]=np.sign(a["clv"]-0.5)
    a["sx"]=a["sgn"]*a["x1"]
    out["signed x1 (long low close) by range tercile, agitated"]=a.groupby("rq").apply(lambda g: summ(g,"sx"))
    a["side"]=np.where(a["pos"]>0,"long",np.where(a["pos"]<0,"short","flat"))
    out["book gain/fee by side, agitated %"]=a.groupby("side").agg(n=("gain","size"),gross=("gain",lambda s:s.mean()*100),fee=("fee",lambda s:s.mean()*100),turn=("dpos","mean"))
    out["book overall gross,fee sum %"]=pd.Series({"gross_sum":d["gain"].sum()*100,"fee_sum":d["fee"].sum()*100,"mean_abs_pos":d.loc[d.pos!=0,"pos"].abs().mean(),"turnover_per_bar":d["dpos"].mean()})
    # trend
    a["trend"]=pd.cut(a["tr60"],[-np.inf,-0.1,0.1,np.inf],labels=["falling","choppy","rising"])
    out["by trend: signed x1, book gross, fee"]=a.groupby("trend").agg(n=("sx","size"),sx=("sx",lambda s:s.mean()*100),gross=("gain",lambda s:s.mean()*100),fee=("fee",lambda s:s.mean()*100))
    out["by trend x side gross%"]=a.groupby(["trend","side"])["gain"].agg(["size",lambda s:s.mean()*100])
    # longer horizons, extremes
    for k in ["r1","r2","r3"]:
        a[k+"x"]=a[k]-a["coin"].map(d.groupby("coin")[k].mean())
    ext=a[(a.clv>0.8)|(a.clv<0.2)].copy(); ext["s"]=np.sign(ext.clv-0.5)
    out["extreme closes signed excess by horizon %"]=pd.DataFrame({k:[ (ext["s"]*ext[k+"x"]).mean()*100,(ext["s"]*ext[k+"x"]).count()] for k in ["r1","r2","r3"]},index=["mean%","n"])
    # prior day return interaction: low close after big fall day
    a["r1q"]=a.groupby("coin")["ret1"].transform(lambda s: pd.qcut(s,3,labels=["down","mid","up"]))
    out["signed x1 by same-day return tercile"]=a.groupby("r1q").apply(lambda g: summ(g,"sx"))
    # drawdown of book
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; t["w"]=w; t["k"]=np.arange(len(t)); dd.append(t)
    D=pd.concat(dd); D["wn"]=D["w"].str[1:].astype(int)
    bk=D.groupby(["wn","k"])["book_return"].mean().fillna(0)
    eq=(1+bk).cumprod(); dr=eq/eq.cummax()-1
    out["book DD by window: min dd, window return %"]=pd.DataFrame({"min_dd%":dr.groupby(level=0).min()*100,"ret%":(1+bk).groupby(level=0).prod().sub(1)*100})
    return out
