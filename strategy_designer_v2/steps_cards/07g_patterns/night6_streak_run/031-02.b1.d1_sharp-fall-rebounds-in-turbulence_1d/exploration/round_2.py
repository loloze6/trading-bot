def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            mabs=r.abs().rolling(60,min_periods=20).mean()
            turb=r.rolling(10,min_periods=8).std()/r.rolling(60,min_periods=20).std()
            s=np.sign(r.fillna(0)).values; st=np.zeros(len(s))
            for i in range(len(s)):
                if s[i]==0: st[i]=0
                elif i>0 and np.sign(st[i-1])==s[i]: st[i]=st[i-1]+s[i]
                else: st[i]=s[i]
            # streak return scaled
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"sc":r/mabs,"turb":turb,"st":st,
                "f2":c.shift(-2)/c-1,"f1":c.shift(-1)/c-1,"wd":ts.dt.weekday,"yr":ts.dt.year,"day":ts.dt.floor("D")})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    out={}
    g=D[D.pos%2==0].copy()
    g["ex"]=g.f2-g.coin.map(g.groupby("coin").f2.mean())
    g=g.dropna(subset=["ex","turb","sc"])
    def dayt(x,ycol,xcol):
        x=x.dropna(subset=[ycol,xcol])
        X=x[xcol]-x[xcol].mean(); b=(X*x[ycol]).sum()/(X**2).sum()
        a=x[ycol].mean()-b*x[xcol].mean()
        e=(x[ycol]-a-b*x[xcol])*X
        se=np.sqrt((e.groupby(x["day"]).sum()**2).sum())/(X**2).sum()
        return b, b/se, x["day"].nunique(), len(x)
    res={}
    up=g[g.st>0].copy(); up["L"]=up.st.clip(upper=7)
    res["up streak len slope"]=dayt(up,"ex","L")
    dn=g[g.st<0].copy(); dn["L"]=(-dn.st).clip(upper=7)
    res["down streak len slope"]=dayt(dn,"ex","L")
    fd=g[g.sc<0].copy(); fd["lt"]=np.log(fd.turb)
    res["down day: log turb slope"]=dayt(fd,"ex","lt")
    fu=g[g.sc>0].copy(); fu["lt"]=np.log(fu.turb)
    res["up day: log turb slope"]=dayt(fu,"ex","lt")
    fd2=fd.copy(); fd2["x"]=-fd2.sc*fd2.lt
    res["down day: fall x logturb slope"]=dayt(fd2,"ex","x")
    out["slopes (b,t,days,n)"]=pd.DataFrame(res,index=["b","t","days","n"]).T.round(5)
    up["half"]=np.where(up.yr<=2021,"early","late")
    a=up.groupby(["half",up.L.clip(upper=5)]).ex.agg(["mean","count"]); a["mean"]*=100
    out["up streak by half"]=a.round(3)
    a=up[up.L>=4].groupby("coin").ex.agg(["mean","count"]); a["mean"]*=100
    out["up streak>=4 by coin"]=a.round(3)
    a=fd.groupby(["coin",fd.turb>1]).ex.mean().mul(100).unstack(); out["down day calm/turb by coin"]=a.round(3)
    g1=D.copy(); g1["ex"]=g1.f1-g1.coin.map(g1.groupby("coin").f1.mean()); g1=g1.dropna(subset=["ex"])
    g1["half"]=np.where(g1.yr<=2021,"early","late")
    a=g1.groupby(["half","wd"]).ex.agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"])); a["mean"]*=100
    out["weekday by half"]=a[["mean","count","t"]].round(3).unstack(0)
    return out
