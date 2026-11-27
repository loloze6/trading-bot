def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            cl=(c-b["low"])/rng
            df=pd.DataFrame(dict(coin=coin,w=w,pos=np.arange(len(b)),cl=cl,
                r5=c/c.shift(5)-1,r20=c/c.shift(20)-1,r60=c/c.shift(60)-1,r1=c.pct_change(),
                fwd=c.shift(-5)/c-1,fwd2=c.shift(-2)/c-1,fwd10=c.shift(-10)/c-1,
                regime=b["regime"].values,fc=b["forecast"].values,alloc=b["postRebalance_current_allocation"].values,
                prev=b["previous_allocation"].values))
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    g=d[d.pos%5==0].copy()
    drift=g.groupby("coin")["fwd"].mean(); sd=g.groupby("coin")["fwd"].std()
    g["un"]=-(g["fwd"]-g["coin"].map(drift)); g["tot"]=-g["fwd"]; g["st"]=g["un"]/g["coin"].map(sd)
    g10=d[d.pos%10==0].copy(); dr10=g10.groupby("coin")["fwd10"].mean()
    g10["un"]=-(g10["fwd10"]-g10["coin"].map(dr10))
    g=g.dropna(subset=["fwd","cl","r5","r20"])
    def summ(x):
        if len(x)<3: return pd.Series(dict(n=len(x)))
        return pd.Series(dict(n=len(x),un=x.un.mean(),tot=x.tot.mean(),t=stats.ttest_1samp(x.un,0).statistic,strength=x.st.mean() if "st" in x else np.nan))
    def C(G):
        ch=G.r60.between(-.1,.1); up=G.cl>.5; neg5=G.r5<0; deep=G.r20<=-.1
        return {
         "all":G.un==G.un,"regime_mr":G.regime=="mean_reversion",
         "chop up neg5 deep (no agit)":ch&up&neg5&deep,
         "deep only":deep,"deep up":deep&up,"deep neg5":deep&neg5,"deep up neg5 anytrend":deep&up&neg5,
         "deep lowclose neg5":deep&(~up)&neg5,
         "deep up neg5 r60<-10":deep&up&neg5&(G.r60<-.1),
         "deep up neg5 r60 nan":deep&up&neg5&G.r60.isna(),
         "r20 -5..-10 up neg5":G.r20.between(-.1,-.05)&up&neg5,
         "r20 -5..-10 up neg5 chop":G.r20.between(-.1,-.05)&up&neg5&ch,
         "r20 -5..-10 only":G.r20.between(-.1,-.05),
         "r20 0..-5 up neg5":G.r20.between(-.05,0)&up&neg5,
         "r20>0 up neg5":(G.r20>0)&up&neg5,
         "deep<-20 up neg5":(G.r20<=-.2)&up&neg5,
         "chop only":ch,"chop deep":ch&deep,"chop r20<-5 up neg5":ch&(G.r20<-.05)&up&neg5,
        }
    out={}
    out["groups5"]=pd.DataFrame({k:summ(g[v]) for k,v in C(g).items()}).T
    g10=g10.dropna(subset=["fwd10","cl","r5","r20"])
    out["groups10"]=pd.DataFrame({k:pd.Series(dict(n=int(v.sum()),un=g10.un[v].mean())) for k,v in C(g10).items()}).T
    m=(g.cl>.5)&(g.r5<0)
    gg=g[m].copy(); gg["bin"]=pd.cut(gg.r20,[-1,-.3,-.2,-.15,-.1,-.05,0,.05,.1,5])
    out["r20 bins up neg5"]=gg.groupby("bin",observed=True).agg(n=("un","size"),un=("un","mean"),tot=("tot","mean"))
    gb=g.copy(); gb["bin"]=pd.cut(gb.r20,[-1,-.3,-.2,-.15,-.1,-.05,0,.05,.1,5])
    out["r20 bins all"]=gb.groupby("bin",observed=True).agg(n=("un","size"),un=("un","mean"))
    mr=g[g.regime=="mean_reversion"]
    out["mr by window"]=mr.groupby("w").agg(n=("un","size"),un=("un","mean"))
    out["mr by coin"]=mr.groupby("coin").agg(n=("un","size"),un=("un","mean"))
    # book
    D=pd.concat([x.assign(coin=c,w=w) for c,ws in data["days"].items() for w,x in ws.items()])
    D["day"]=pd.to_datetime(D["day"])
    bk=D.groupby(["w","day"]).agg(b=("book_return","mean"),h=("coin_return","mean")).dropna().reset_index()
    out["by window"]=bk.groupby("w").agg(days=("b","size"),bsum=("b","sum"),hsum=("h","sum"),bmin=("b","min"))
    bk=bk.sort_values(["w","day"]) 
    # order windows numerically
    bk["wn"]=bk.w.str[1:].astype(int); bk=bk.sort_values(["wn","day"])
    v=(1+bk.b).cumprod(); dd_=v/v.cummax()-1
    out["book chain"]=pd.Series(dict(maxdd=dd_.min(),final=v.iloc[-1],days=len(v),sd=bk.b.std(),mean=bk.b.mean()))
    bk["dd"]=dd_.values
    out["dd by window (min)"]=bk.groupby("w").dd.min()
    worst=bk.nsmallest(10,"b")[["w","b","h"]]
    out["worst days"]=worst.reset_index(drop=True)
    T=pd.concat([t.assign(coin=c,w=w) for c,ws in data["trades"].items() for w,t in ws.items() if len(t)])
    out["trades"]=pd.Series(dict(n=len(T),mean_net=T.net_profit_loss_percent.mean(),win=(T.net_profit_loss_percent>0).mean(),
        med_dur_days=T.duration_minutes.median()/1440,worst=T.net_profit_loss_percent.min(),best=T.net_profit_loss_percent.max()))
    out["trades by window"]=T.groupby("w").agg(n=("side","size"),net=("net_profit_loss_percent","mean"),sum=("net_profit_loss_percent","sum"))
    out["trades by coin"]=T.groupby("coin").agg(n=("side","size"),net=("net_profit_loss_percent","mean"))
    out["alloc abs mean when in"]=float(d.loc[d.alloc.abs()>0,"alloc"].abs().mean())
    out["share bars in pos"]=float((d.alloc.abs()>0).mean())
    out["share bars regime mr"]=float((d.regime=="mean_reversion").mean())
    return out
