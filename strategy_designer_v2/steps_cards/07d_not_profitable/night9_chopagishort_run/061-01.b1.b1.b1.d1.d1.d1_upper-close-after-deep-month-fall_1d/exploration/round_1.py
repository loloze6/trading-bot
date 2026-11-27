def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            loc=(c-b["low"])/rng
            r5=c/c.shift(5)-1; r20=c/c.shift(20)-1; r60=c/c.shift(60)-1
            r1=c.pct_change()
            vol30=r1.rolling(30).std()
            fwd=c.shift(-5)/c-1
            fwd10=c.shift(-10)/c-1
            df=pd.DataFrame(dict(coin=coin,w=w,pos=np.arange(len(b)),loc=loc,r5=r5,r20=r20,r60=r60,vol30=vol30,
                fwd=fwd,fwd10=fwd10,regime=b["regime"],fc=b["forecast"],alloc=b["postRebalance_current_allocation"]))
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    g=d[d.pos%5==0].copy()
    drift=g.groupby("coin")["fwd"].mean()
    sd=g.groupby("coin")["fwd"].std()
    g["un"]=-(g["fwd"]-g["coin"].map(drift))
    g["tot"]=-g["fwd"]
    g["str"]=g["un"]/g["coin"].map(sd)
    g=g.dropna(subset=["fwd","loc","r5","r20"])
    def summ(m):
        x=g[m]
        if len(x)<3: return pd.Series(dict(n=len(x)))
        return pd.Series(dict(n=len(x),un=x.un.mean(),tot=x.tot.mean(),t=stats.ttest_1samp(x.un,0).statistic,strength=x.str.mean()))
    hasr60=g.r60.notna()
    ch=g.r60.between(-.1,.1)
    out={}
    conds={
     "all":g.un==g.un,
     "regime_mr":g.regime=="mean_reversion",
     "full_r20le-10_chop":ch&(g.loc>.5)&(g.r5<0)&(g.r20<=-.1),
     "r20le-10 any trend(loc,r5)":(g.loc>.5)&(g.r5<0)&(g.r20<=-.1),
     "r20le-10 only":(g.r20<=-.1),
     "r20le-10 loc":(g.loc>.5)&(g.r20<=-.1),
     "r20le-10 r5":(g.r5<0)&(g.r20<=-.1),
     "r20 -5..-10 loc r5":(g.loc>.5)&(g.r5<0)&(g.r20.between(-.1,-.05)),
     "r20 -5..-10 only":(g.r20.between(-.1,-.05)),
     "r20 0..-5 loc r5":(g.loc>.5)&(g.r5<0)&(g.r20.between(-.05,0)),
     "r20 >0 loc r5":(g.loc>.5)&(g.r5<0)&(g.r20>0),
     "r20le-10 loclow r5":(g.loc<=.5)&(g.r5<0)&(g.r20<=-.1),
     "r20le-20 loc r5":(g.loc>.5)&(g.r5<0)&(g.r20<=-.2),
     "r20le-10 loc r5 r60<-10":(g.loc>.5)&(g.r5<0)&(g.r20<=-.1)&(g.r60<-.1),
     "r20le-10 loc r5 r60>10":(g.loc>.5)&(g.r5<0)&(g.r20<=-.1)&(g.r60>.1),
     "r20le-10 loc r5 r60 nan":(g.loc>.5)&(g.r5<0)&(g.r20<=-.1)&(~hasr60),
     "chop only":ch,
     "chop r20le-10":ch&(g.r20<=-.1),
    }
    out["groups"]=pd.DataFrame({k:summ(v) for k,v in conds.items()}).T
    # graded by r20 bins among loc>.5 & r5<0
    m=(g.loc>.5)&(g.r5<0)
    gg=g[m].copy(); gg["bin"]=pd.cut(gg.r20,[-1,-.3,-.2,-.15,-.1,-.05,0,.05,.1,5])
    out["r20 bins loc r5"]=gg.groupby("bin").agg(n=("un","size"),un=("un","mean"),tot=("tot","mean"))
    gb=g.copy(); gb["bin"]=pd.cut(gb.r20,[-1,-.3,-.2,-.15,-.1,-.05,0,.05,.1,5])
    out["r20 bins all"]=gb.groupby("bin").agg(n=("un","size"),un=("un","mean"),tot=("tot","mean"))
    # book daily
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            dd.append(x.assign(coin=coin,w=w))
    D=pd.concat(dd)
    D["day"]=pd.to_datetime(D["day"])
    bk=D.groupby(["w","day"]).agg(b=("book_return","mean"),h=("coin_return","mean")).dropna()
    out["by window"]=bk.groupby("w").agg(days=("b","size"),bsum=("b","sum"),hsum=("h","sum"),bmin=("b","min"))
    out["by year"]=bk.reset_index().assign(y=lambda x:x.day.dt.year).groupby("y").agg(bsum=("b","sum"),hsum=("h","sum"))
    # trades
    T=pd.concat([t.assign(coin=c,w=w) for c,ws in data["trades"].items() for w,t in ws.items() if len(t)])
    out["trades"]=pd.Series(dict(n=len(T),mean_net=T.net_profit_loss_percent.mean(),win=(T.net_profit_loss_percent>0).mean(),
        med_dur_days=T.duration_minutes.median()/1440,worst=T.net_profit_loss_percent.min()))
    out["trades by coin"]=T.groupby("coin").agg(n=("side","size"),net=("net_profit_loss_percent","mean"),sum=("net_profit_loss_percent","sum"))
    out["alloc abs mean when in"]=float(d.loc[d.alloc.abs()>0,"alloc"].abs().mean())
    return out
