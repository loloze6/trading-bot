def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; v=b["volume"].values.astype(float); n=len(b)
            vs=pd.Series(v)
            m1=vs.rolling(30).mean(); m0=vs.shift(30).rolling(30).mean()
            lvr=np.log(m1/m0)
            r1=pd.Series(c).pct_change()
            r20=pd.Series(c).pct_change(20)
            r5b=pd.Series(c).pct_change(5)
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,n-H,H):
                rows.append(dict(coin=coin,w=w,fwd=c[i+H]/c[i]-1,reg=b["regime"].iloc[i],
                    fc=b["forecast"].iloc[i],alloc=b["postRebalance_current_allocation"].iloc[i],
                    lvr=lvr.iloc[i],r1=r1.iloc[i],r20=r20.iloc[i],r5b=r5b.iloc[i],wd=ts.iloc[i].dayofweek,yr=ts.iloc[i].year))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    out={}
    def tt(x):
        x=x.dropna(); 
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    def slope(g,xc):
        g=g[[xc,"ex"]].dropna()
        if len(g)<20: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan))
        r=stats.linregress(g[xc],g["ex"]); return pd.Series(dict(n=len(g),slope=r.slope,t=r.slope/r.stderr))
    out["regime_counts_ex"]=d.groupby("reg")["ex"].apply(tt).unstack()
    out["lvr_slope_by_regime"]=d.groupby("reg").apply(lambda g: slope(g,"lvr"))
    act=d[d.reg=="mean_reversion"].copy()
    act["fq"]=pd.qcut(act["fc"],5,labels=False,duplicates="drop")
    out["active_fc_quintile"]=act.groupby("fq").agg(n=("ex","size"),fc=("fc","mean"),ex=("ex","mean"),r20=("r20","mean"))
    act["side"]=np.sign(act["fc"])
    out["active_side"]=act.groupby("side")["ex"].apply(tt).unstack()
    out["active_by_year_slope"]=act.groupby("yr").apply(lambda g: slope(g,"fc"))
    act["r20q"]=pd.qcut(act["r20"],3,labels=False)
    out["active_r20_tercile_slope"]=act.groupby("r20q").apply(lambda g: slope(g,"fc"))
    out["active_r20_tercile_ex"]=act.groupby("r20q")["ex"].apply(tt).unstack()
    out["active_r5back_slope"]=slope(act,"r5b")
    for rg in ["chop","unknown"]:
        s=d[d.reg==rg]
        out[f"{rg}_r5back_slope"]=slope(s,"r5b")
        out[f"{rg}_r20_slope"]=slope(s,"r20")
    out["all_r1_slope_by_regime"]=d.groupby("reg").apply(lambda g: slope(g,"r1"))
    out["weekday_ex"]=d.groupby("wd")["ex"].apply(tt).unstack()
    # trades
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values() if len(t)])
    out["trades_side"]=tr.groupby("side")["net_profit_loss_percent"].agg(["size","mean","median"])
    # book daily
    dd=pd.concat([x.assign(coin=c,w=w) for c,ws in data["days"].items() for w,x in ws.items()])
    bk=dd.groupby(["w","day"])["book_return"].mean().dropna()
    out["book_daily"]=pd.Series(dict(n=len(bk),mean=bk.mean(),sd=bk.std(),top10share=bk.nlargest(int(len(bk)*0.1)).sum()/bk.sum()))
    return out
