def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.reset_index(drop=True)
            c=d["close"].astype(float); hi=d["high"].astype(float); lo=d["low"].astype(float)
            low30=c.shift(1).rolling(30).min()
            depth=c/low30-1
            r1=c.pct_change(); vol30=r1.rolling(30).std()
            ret60=c/c.shift(60)-1
            clv=(c-lo)/(hi-lo)
            rng=(hi-lo)/c.shift(1)
            n=len(d)
            fw={h:c.shift(-h)/c-1 for h in (1,2,3,5)}
            for i in range(0,n,3):
                rows.append(dict(coin=coin,win=w,ts=d["timestamp"].iloc[i],depth=depth.iloc[i],
                  r1=r1.iloc[i],r1z=r1.iloc[i]/vol30.iloc[i] if vol30.iloc[i]>0 else np.nan,
                  ret60=ret60.iloc[i],vol30=vol30.iloc[i],reg=d["regime"].iloc[i],clv=clv.iloc[i],
                  rngz=rng.iloc[i]/vol30.iloc[i] if vol30.iloc[i]>0 else np.nan,
                  f1=fw[1].iloc[i],f2=fw[2].iloc[i],f3=fw[3].iloc[i],f5=fw[5].iloc[i]))
    g=pd.DataFrame(rows).dropna(subset=["f3"])
    g["day"]=pd.to_datetime(g["ts"]).dt.floor("D")
    for h in ("f1","f2","f3","f5"):
        g["u"+h]=g[h]-g["coin"].map(g.groupby("coin")[h].mean())
    def summ(s,col="uf3"):
        s=s.dropna(subset=[col])
        if len(s)<5: return pd.Series(dict(n=len(s),days=np.nan,mean=np.nan,t=np.nan))
        m=s[col].mean(); dev=(s[col]-m).groupby(s["day"]).sum()
        se=np.sqrt((dev**2).sum())/len(s)
        return pd.Series(dict(n=len(s),days=s["day"].nunique(),mean=m,t=m/se))
    def slope(s,x,col="uf3"):
        s=s.dropna(subset=[x,col])
        if len(s)<8: return pd.Series(dict(n=len(s),slope=np.nan,t=np.nan))
        X=s[x]-s[x].mean(); b=(X*s[col]).sum()/(X**2).sum()
        e=s[col]-s[col].mean()-b*X
        dev=(X*e).groupby(s["day"]).sum()
        se=np.sqrt((dev**2).sum())/(X**2).sum()
        return pd.Series(dict(n=len(s),slope=b,t=b/se))
    out={}
    tr=g[g.reg=="trending"]
    out["regime counts"]=g["reg"].value_counts()
    out["trending (fall-agit break) horizons"]=pd.DataFrame({h:summ(tr,"u"+h) for h in ("f1","f2","f3","f5")}).T
    fa=g[(g.ret60<-0.1)]
    out["falling: slope u3 on depth / r1z / clv"]=pd.DataFrame({
        "depth(all fall)":slope(fa,"depth"),"depth(brk)":slope(fa[fa.depth<0],"depth"),
        "r1z(all fall)":slope(fa,"r1z"),"clv(brk)":slope(fa[fa.depth<0],"clv"),
        "r1z(all)":slope(g,"r1z"),"depth(all)":slope(g,"depth"),"rngz(all)":slope(g,"rngz")}).T
    g["zq"]=pd.cut(g["r1z"],[-99,-2,-1,1,99])
    g["tr"]=pd.cut(g["ret60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    out["u3 by trend x 1d z"]=pd.DataFrame({f"{a}-{b}":summ(s) for (a,b),s in g.groupby(["tr","zq"],observed=True)}).T
    out["u2 by trend x 1d z"]=pd.DataFrame({f"{a}-{b}":summ(s,"uf2") for (a,b),s in g.groupby(["tr","zq"],observed=True)}).T
    br=g[g.depth<0]
    br["cq"]=pd.cut(br["clv"],[-0.01,0.33,0.66,1.01],labels=["closeLow","mid","closeHigh"])
    out["breaks by close location"]=pd.DataFrame({k:summ(s) for k,s in br.groupby("cq",observed=True)}).T
    # trades
    t=pd.concat([x.assign(coin=c) for c,ws in data["trades"].items() for x in ws.values()],ignore_index=True)
    out["trades"]=pd.Series(dict(n=len(t),win=(t.net_profit_loss_percent>0).mean(),
        mean_net=t.net_profit_loss_percent.mean(),med_net=t.net_profit_loss_percent.median(),
        mean_dur_days=t.duration_minutes.mean()/1440))
    out["trades by coin"]=t.groupby("coin")["net_profit_loss_percent"].agg(["count","mean"])
    return out
