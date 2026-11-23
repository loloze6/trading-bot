def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book & trade stats
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            a=b["postRebalance_current_allocation"].fillna(0)
            t=data["trades"][c][w]
            rows.append(dict(coin=c,bars=len(b),inpos=(a!=0).sum(),meanabs=a.abs().mean(),trades=len(t),
                             pl=t["net_profit_loss_percent"].sum() if len(t) else 0))
    df=pd.DataFrame(rows)
    out["per_coin"]=df.groupby("coin")[["bars","inpos","trades","pl"]].sum().assign(meanabs=df.groupby("coin")["meanabs"].mean())
    # trades
    T=pd.concat([data["trades"][c][w].assign(coin=c) for c in data["trades"] for w in data["trades"][c] if len(data["trades"][c][w])])
    out["trades_summary"]=pd.Series(dict(n=len(T),mean_net=T["net_profit_loss_percent"].mean(),
        win=(T["net_profit_loss_percent"]>0).mean(),mean_days=T["duration_minutes"].mean()/1440))
    # variants from prices
    H=5; res={}
    for c in data["bars"]:
        allr=[]
        for w,b in data["bars"][c].items():
            cl=b["close"].values
            allr+=list(cl[H::H][:len(cl[::H])-1]/cl[::H][:len(cl[H::H])]-1) if len(cl)>H else []
        drift=np.nanmean(allr) if allr else 0
        for w,b in data["bars"][c].items():
            cl=b["close"].reset_index(drop=True); lo=b["low"].reset_index(drop=True)
            n=len(cl)
            if n<30: continue
            ph=cl.shift(1).rolling(20).max()
            bo=(cl>ph).values
            fwd=(cl.shift(-H)/cl-1).values
            run=(cl/cl.shift(20)-1).values
            for fw in [3,5,10]:
                for kind in ["below_old_high","below_bo_low"]:
                    sig=np.zeros(n,bool); rr=np.full(n,np.nan)
                    for i in range(n):
                        js=[j for j in range(max(0,i-fw),i) if bo[j]]
                        if not js: continue
                        j=js[-1]
                        lvl=ph[j] if kind=="below_old_high" else lo[j]
                        if cl[i]<lvl: sig[i]=True; rr[i]=run[j]
                    # one per grid cell, first signal bar
                    for g in range(0,n,H):
                        idx=[i for i in range(g,min(g+H,n)) if sig[i] and not np.isnan(fwd[i])]
                        if idx:
                            i=idx[0]
                            res.setdefault((kind,fw),[]).append((-(fwd[i]-drift),rr[i],w))
    rows=[]
    for k,v in res.items():
        x=np.array([a for a,_,_ in v]); r=np.array([b for _,b,_ in v])
        ok=~np.isnan(r)
        rows.append(dict(kind=k[0],fw=k[1],n=len(x),mean=x.mean(),t=x.mean()/(x.std(ddof=1)/np.sqrt(len(x))),
                         spear_run=stats.spearmanr(r[ok],x[ok])[0]))
    out["variants"]=pd.DataFrame(rows)
    # book daily falls
    D=pd.concat([data["days"][c][w].assign(coin=c,w=w) for c in data["days"] for w in data["days"][c]])
    D["year"]=pd.to_datetime(D["day"]).dt.year
    bk=D.groupby(["w","day"])["book_return"].mean()
    out["book_by_window"]=bk.groupby(level=0).agg(["mean","sum","count"]).sort_values("sum").head(8)
    return out
