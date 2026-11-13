def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r=c.pct_change()
            sc=r.abs().shift(1).rolling(20,min_periods=20).mean()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),"r":r,"z":r/sc,
                "f1":c.shift(-1)/c-1,"f5":c.shift(-5)/c-1,"f10":c.shift(-10)/c-1,
                "volq":sc/sc.rolling(120,min_periods=60).median(),"mom20":c/c.shift(20)-1,
                "clv":(c-l)/(h-l).replace(0,np.nan),"wd":ts.dt.weekday,"yr":ts.dt.year,
                "fc":b["forecast"].astype(float),"alloc":b["postRebalance_current_allocation"].astype(float)})
            rows.append(d)
    D=pd.concat(rows).reset_index(drop=True)
    D["mu"]=D["coin"].map(D.groupby("coin")["r"].mean())
    D["x1"]=D["f1"]-D["mu"]; D["x5"]=D["f5"]-5*D["mu"]; D["x10"]=D["f10"]-10*D["mu"]
    D["vb"]=pd.cut(D["volq"],[0,0.8,1.2,99]).astype(str)
    D["mb"]=np.where(D["mom20"]>0,"mom+","mom-")
    D["cb"]=pd.cut(D["clv"],[-0.01,0.33,0.67,1.01]).astype(str)
    def dedup(E,gap=5):
        idx=[]
        for _,g in E.sort_values(["coin","w","i"]).groupby(["coin","w"],sort=False):
            last=-999
            for ix,i in zip(g.index,g["i"]):
                if i-last>gap: idx.append(ix); last=i
        return E.loc[idx]
    def summ(E,col="x5"):
        x=E[col].dropna(); n=len(x)
        if n<3: return {"n":n}
        return {"n":n,"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(n),"hit":(x>0).mean()}
    out={}
    D["zb"]=pd.cut(D["z"],[-99,-3,-2,-1,1,2,3,99]).astype(str)
    zt={}
    for k,g in D.groupby("zb"):
        E=dedup(g); r={}
        for col in ["x1","x5","x10"]:
            s=summ(E,col); r["n"]=s.get("n"); r[col]=s.get("mean"); r["t"+col[1:]]=s.get("t")
        zt[k]=r
    out["by_z_bucket"]=pd.DataFrame(zt).T
    tab={}
    for lab,sub in [("up",D[D["z"]>=2]),("dn",D[D["z"]<=-2])]:
        for col in ["coin","yr","vb","mb","cb","wd"]:
            for k,g in sub.groupby(col):
                tab[f"{lab} {col}={k}"]=summ(dedup(g))
    out["splits"]=pd.DataFrame(tab).T
    N=D[D["i"]%5==0]
    g=N.groupby(["vb","mb"])["x5"].agg(["count","mean","std"]); g["t"]=g["mean"]/g["std"]*np.sqrt(g["count"])
    out["base5_vol_mom"]=g
    wd=D.groupby("wd")["x1"].agg(["count","mean","std"]); wd["t"]=wd["mean"]/wd["std"]*np.sqrt(wd["count"])
    out["weekday_next"]=wd
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): T.append(t.assign(coin=coin))
    T=pd.concat(T); T["dur_d"]=T["duration_minutes"]/1440
    out["trades"]=T.groupby("coin").agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"),
        mean_gross=("profit_loss_percent","mean"),hit=("net_profit_loss_percent",lambda x:(x>0).mean()),dur=("dur_d","mean"),comm=("total_commission","mean"))
    T["db"]=pd.cut(T["dur_d"],[0,1.5,3.5,10,999]).astype(str)
    out["trades_by_dur"]=T.groupby("db").agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"),mean_gross=("profit_loss_percent","mean"))
    D["inpos"]=D["alloc"].abs()>0.05
    out["alloc_share"]=D.groupby("coin")["inpos"].mean()
    return out
