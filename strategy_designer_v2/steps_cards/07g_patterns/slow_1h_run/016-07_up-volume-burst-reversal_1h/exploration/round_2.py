def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    allrows=[]
    for H,L in [(72,72),(72,48),(72,120),(24,72),(120,72)]:
        rows=[]
        for coin,ws in data["bars"].items():
            for w,b in ws.items():
                b=b.reset_index(drop=True)
                c=b["close"].values; n=len(b)
                lr=np.r_[np.nan,np.diff(np.log(c))]
                past=np.r_[[np.nan]*L, c[L:]/c[:-L]-1]
                eff=np.abs(np.log(1+past))/pd.Series(lr).abs().rolling(L).sum().values
                yr=pd.to_datetime(b["timestamp"]).dt.year.values
                for t in range(0,n-H,H):
                    rows.append(dict(coin=coin,w=w,yr=yr[t],past=past[t],eff=eff[t],fwd=c[t+H]/c[t]-1))
        d=pd.DataFrame(rows).dropna()
        d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
        d["sx"]=d["ex"]*np.sign(d["past"])
        d["er"]=d.groupby("coin")["eff"].rank(pct=True)
        d["pr"]=d.groupby("coin")["past"].abs().rank(pct=True) if False else d.groupby("coin")["past"].transform(lambda x: x.abs().rank(pct=True))
        X=np.c_[np.ones(len(d)),d["er"]-0.5,d["pr"]-0.5]
        beta,res,_,_=np.linalg.lstsq(X,d["sx"].values,rcond=None)
        e=d["sx"].values-X@beta; s2=e@e/(len(d)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        allrows.append(dict(H=H,L=L,n=len(d),b_eff=beta[1],t_eff=beta[1]/se[1],b_size=beta[2],t_size=beta[2]/se[2]))
        if H==72 and L==72:
            pc=[]
            for coin,g in d.groupby("coin"):
                for side,gg in [("up",g[g.past>0]),("dn",g[g.past<0])]:
                    sl=stats.linregress(gg["er"],gg["sx"]); pc.append(dict(coin=coin,side=side,slope=sl.slope,t=sl.slope/sl.stderr,n=len(gg)))
            out["per coin, side: signed cont ~ eff rank"]=pd.DataFrame(pc)
            py=[]
            for y,g in d.groupby("yr"):
                sl=stats.linregress(g["er"],g["sx"]); py.append(dict(yr=y,slope=sl.slope,t=sl.slope/sl.stderr,n=len(g)))
            out["per year slope"]=pd.DataFrame(py)
            g=d.copy(); g["eq"]=pd.qcut(g["er"],3,labels=False); g["pq"]=pd.qcut(g["pr"],3,labels=False)
            out["signed cont mean: eff tercile x size tercile"]=g.pivot_table(index="eq",columns="pq",values="sx",aggfunc="mean")
            out["counts"]=g.pivot_table(index="eq",columns="pq",values="sx",aggfunc="count")
    out["multi-horizon regression signed cont ~ eff rank + size rank"]=pd.DataFrame(allrows)
    # book: fee drag
    fr=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            r=b["close"].shift(-1)/b["close"]-1
            gross=(b["postRebalance_current_allocation"]*r).sum()
            fee=((b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]).sum()
            fr.append(dict(coin=coin,gross=gross,fee=fee,bars=len(b)))
    F=pd.DataFrame(fr).groupby("coin").sum()
    F["gross_per_day"]=F["gross"]/F["bars"]*24; F["fee_per_day"]=F["fee"]/F["bars"]*24
    out["gross vs fee per day"]=F[["gross_per_day","fee_per_day"]]
    return out
