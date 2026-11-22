def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    allfwd={}
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(20).std()
            jump=r1/vol
            r90=c/c.shift(90)-1
            r30=c/c.shift(30)-1
            fdd=b.get("debug_info.components.fall_depth.last_history_value")
            n=len(c)
            for h in (1,2,5,10):
                fwd=c.shift(-h)/c-1
                allfwd.setdefault((coin,h),[]).append(fwd.iloc[::h].dropna())
            fwd5=c.shift(-5)/c-1
            fwd2=c.shift(-2)/c-1
            fwd10=c.shift(-10)/c-1
            fwd1=c.shift(-1)/c-1
            for i in range(n):
                if pd.notna(jump.iloc[i]) and abs(jump.iloc[i])>=1.5:
                    rows.append(dict(coin=coin,w=w,i=i,jump=jump.iloc[i],r90=r90.iloc[i],r30=r30.iloc[i],
                        f1=fwd1.iloc[i],f2=fwd2.iloc[i],f5=fwd5.iloc[i],f10=fwd10.iloc[i],
                        alloc=b["postRebalance_current_allocation"].iloc[i],fc=b["forecast"].iloc[i]))
    df=pd.DataFrame(rows)
    drift={}
    for (coin,h),l in allfwd.items():
        drift[(coin,h)]=pd.concat(l).mean()
    for h in (1,2,5,10):
        df[f"u{h}"]=df[f"f{h}"]-df["coin"].map(lambda x:drift[(x,h)])
    up=df[df.jump>=2].copy()
    up["state"]=np.where(up.r90<0,"r90neg","r90pos")
    def summ(g):
        out={}
        out["n"]=len(g)
        for h in (1,2,5,10):
            x=g[f"u{h}"].dropna()
            out[f"u{h}_mean%"]=100*x.mean(); out[f"t{h}"]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        return pd.Series(out)
    res={}
    res["up jumps by state"]=up.groupby("state").apply(summ)
    neg=up[up.r90<0].copy()
    neg["depthq"]=pd.qcut(neg.r90,4,labels=["deepest","q2","q3","shallow"])
    res["neg by depth quartile"]=neg.groupby("depthq").apply(summ)
    neg["jq"]=pd.qcut(neg.jump,3,labels=["small","mid","big"])
    res["neg by jump size"]=neg.groupby("jq").apply(summ)
    neg["r30s"]=np.where(neg.r30<0,"r30neg","r30pos")
    res["neg by r30 sign"]=neg.groupby("r30s").apply(summ)
    res["neg by coin"]=neg.groupby("coin").apply(summ)
    dn=df[df.jump<=-2].copy(); dn["state"]=np.where(dn.r90<0,"r90neg","r90pos")
    res["down jumps by state (long-side u)"]=dn.groupby("state").apply(summ)
    # book daily
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd.append(d.assign(coin=coin,w=w))
    D=pd.concat(dd)
    res["book by window"]=D.groupby("w").agg(book=("book_return","mean"),coin=("coin_return","mean")).mul(100)
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): tr.append(t.assign(coin=coin))
    T=pd.concat(tr)
    res["trades"]=T.groupby("side").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda x:(x>0).mean()))
    return res
