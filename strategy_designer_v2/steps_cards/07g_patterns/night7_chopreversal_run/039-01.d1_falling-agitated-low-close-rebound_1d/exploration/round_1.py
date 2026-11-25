def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            rng=(b.high-b.low).replace(0,np.nan)
            b["loc"]=(b.high-b.close)/rng   # 1 at low
            b["r1"]=b.close.pct_change()
            b["nxt"]=b.close.shift(-1)/b.close-1
            b["nxt3"]=b.close.shift(-3)/b.close-1
            b["ret5"]=b.close/b.close.shift(5)-1
            b["vol20"]=b.r1.rolling(20).std()
            b["rng_rel"]=(rng/b.close)/((rng/b.close).rolling(20).mean())
            b["coin"]=coin; b["w"]=w; b["pos"]=np.arange(len(b))
            b["wd"]=pd.to_datetime(b.timestamp).dt.dayofweek
            b["yr"]=pd.to_datetime(b.timestamp).dt.year
            b["inprof"]=(b.regime!="chop")
            b["alloc"]=b.postRebalance_current_allocation
            rows.append(b[["coin","w","pos","loc","r1","nxt","nxt3","ret5","vol20","rng_rel","wd","yr","inprof","alloc","forecast","timestamp"]])
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin").nxt.mean(); d["ex"]=d.nxt-d.coin.map(mu)
    mu3=d[d.pos%3==0].groupby("coin").nxt3.mean(); d["ex3"]=d.nxt3-d.coin.map(mu3)
    d["day"]=pd.to_datetime(d.timestamp).dt.floor("D")
    def summ(g,col="ex"):
        g=g.dropna(subset=[col])
        s=g.groupby("day")[col].sum()
        t=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
        return pd.Series({"n":len(g),"days":len(s),"mean_bp":g[col].mean()*1e4,"t_day":t})
    d["locq"]=pd.cut(d["loc"],[-.01,.2,.4,.6,.8,1.01],labels=["hi","q2","mid","q4","low"])
    out={}
    out["loc_by_profile"]=d.groupby(["inprof","locq"]).apply(summ)
    # graded slope: loc-0.5 times ex
    d["sig"]=(d["loc"]-0.5)*d["ex"]
    out["slope_by_profile"]=d.groupby("inprof").apply(lambda g: summ(g,"sig"))
    d["volq"]=d.groupby("coin").vol20.transform(lambda x: pd.qcut(x,3,labels=["calm","mid","agit"]))
    out["slope_by_volq"]=d.groupby("volq").apply(lambda g: summ(g,"sig"))
    d["r1q"]=d.groupby("coin").r1.transform(lambda x: pd.qcut(x,5,labels=False))
    out["after_r1q"]=d.groupby("r1q").apply(summ)
    d["r5q"]=d.groupby("coin").ret5.transform(lambda x: pd.qcut(x,5,labels=False))
    out["after_r5q_3d"]=d[d.pos%3==0].groupby("r5q").apply(lambda g: summ(g,"ex3"))
    d["rgq"]=d.groupby("coin").rng_rel.transform(lambda x: pd.qcut(x,3,labels=["narrow","mid","wide"]))
    out["slope_by_range"]=d.groupby("rgq").apply(lambda g: summ(g,"sig"))
    out["weekday"]=d.groupby("wd").apply(summ)
    out["slope_by_year"]=d.groupby("yr").apply(lambda g: summ(g,"sig"))
    out["slope_by_coin"]=d.groupby("coin").apply(lambda g: summ(g,"sig"))
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    D=pd.concat(dd)
    bk=D.groupby("day")[["book_return","coin_return"]].mean().dropna()
    out["book"]=pd.Series({"mean_bp":bk.book_return.mean()*1e4,"t":bk.book_return.mean()/(bk.book_return.std()/np.sqrt(len(bk))),"corr_coin":bk.corr().iloc[0,1],"days":len(bk)})
    out["inprof_share_by_year"]=d.groupby("yr").inprof.mean()
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    out["trades"]=T.groupby("side").agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda x:(x>0).mean()),dur_d=("duration_minutes",lambda x:x.mean()/1440))
    return out
