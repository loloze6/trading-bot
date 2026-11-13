def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sc=r.abs().shift(1).rolling(20,min_periods=20).mean()
            z=r/sc
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            f10=c.shift(-10)/c-1
            volq=sc/sc.rolling(120,min_periods=60).median()
            mom20=c/c.shift(20)-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),"r":r,"z":z,"f1":f1,"f5":f5,"f10":f10,
                            "volq":volq,"mom20":mom20,"wd":ts.dt.weekday,"yr":ts.dt.year,"fc":b["forecast"]})
            rows.append(d)
    D=pd.concat(rows)
    mu=D.groupby("coin")["r"].mean()
    D["mu"]=D["coin"].map(mu)
    D["x1"]=D["f1"]-D["mu"]; D["x5"]=D["f5"]-5*D["mu"]; D["x10"]=D["f10"]-10*D["mu"]
    def dedup(E,gap=5):
        keep=[]
        for (c,w),g in E.groupby(["coin","w"]):
            last=-999
            for idx,i in zip(g.index,g["i"]):
                if i-last>gap: keep.append(True); last=i
                else: keep.append(False)
        return E[np.array(keep)] if len(E) else E
    D=D.reset_index(drop=True)
    def summ(E,col="x5"):
        x=E[col].dropna()
        if len(x)<3: return pd.Series({"n":len(x)})
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)),"hit":(x>0).mean()})
    out={}
    D["zb"]=pd.cut(D["z"],[-99,-3,-2,-1,1,2,3,99])
    zt=[]
    for k,g in D.groupby("zb",observed=True):
        E=dedup(g.sort_values(["coin","w","i"]))
        s5=summ(E,"x5"); s1=summ(E,"x1"); s10=summ(E,"x10")
        zt.append(pd.Series({"n":s5.get("n"),"x1":s1.get("mean"),"t1":s1.get("t"),"x5":s5.get("mean"),"t5":s5.get("t"),"x10":s10.get("mean"),"t10":s10.get("t")},name=str(k)))
    out["by_z_bucket"]=pd.DataFrame(zt)
    up=D[D["z"]>=2]
    tab=[]
    for col,grp in [("coin","coin"),("yr","yr")]:
        for k,g in up.groupby(grp):
            E=dedup(g.sort_values(["coin","w","i"])); s=summ(E)
            tab.append(pd.Series(s,name=f"up {col}={k}"))
    up=up.assign(vb=pd.cut(up["volq"],[0,0.8,1.2,99]),mb=np.where(up["mom20"]>0,"mom+","mom-"))
    for col in ["vb","mb"]:
        for k,g in up.groupby(col,observed=True):
            E=dedup(g.sort_values(["coin","w","i"])); s=summ(E)
            tab.append(pd.Series(s,name=f"up {col}={k}"))
    dn=D[D["z"]<=-2].assign(vb=pd.cut(D["volq"],[0,0.8,1.2,99]),mb=np.where(D["mom20"]>0,"mom+","mom-"))
    for col in ["vb","mb","coin"]:
        for k,g in dn.groupby(col,observed=True):
            E=dedup(g.sort_values(["coin","w","i"])); s=summ(E)
            tab.append(pd.Series(s,name=f"dn {col}={k}"))
    out["splits"]=pd.DataFrame(tab)
    # weekday one-bar returns
    wd=D.groupby("wd")["x1"].agg(["count","mean","std"]); wd["t"]=wd["mean"]/wd["std"]*np.sqrt(wd["count"])
    out["weekday_next"]=wd
    # all bars non-overlapping 5-bar by vol level and momentum
    N=D[D["i"]%5==0].copy()
    N["vb"]=pd.cut(N["volq"],[0,0.8,1.2,99]); N["mb"]=np.where(N["mom20"]>0,"mom+","mom-")
    g=N.groupby(["vb","mb"],observed=True)["x5"].agg(["count","mean","std"]); g["t"]=g["mean"]/g["std"]*np.sqrt(g["count"])
    out["base5_vol_mom"]=g
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): T.append(t.assign(coin=coin))
    T=pd.concat(T)
    T["dur_d"]=T["duration_minutes"]/1440
    out["trades"]=T.groupby("coin").agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"),
        hit=("net_profit_loss_percent",lambda x:(x>0).mean()),dur=("dur_d","mean"),comm=("total_commission","mean"))
    return out
