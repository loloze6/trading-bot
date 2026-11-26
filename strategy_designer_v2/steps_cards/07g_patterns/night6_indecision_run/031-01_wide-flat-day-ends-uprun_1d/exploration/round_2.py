def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            if len(b)<30: continue
            o,h,l,c=b.open,b.high,b.low,b.close
            rng=(h-l).replace(0,np.nan)
            clv=(c-l)/rng
            rr=(h-l)/(h-l).rolling(20).mean()
            r1=c/c.shift(1)-1
            ts=pd.to_datetime(b.timestamp)
            d=pd.DataFrame(dict(coin=coin,win=w,pos=np.arange(len(b)),clv=clv,rr=rr,r1=r1,
                f1=c.shift(-1)/c-1,f2=c.shift(-2)/c-1,f3=c.shift(-3)/c-1,
                day=ts.dt.floor("D"),yr=ts.dt.year,wd=ts.dt.weekday,
                alloc=b.postRebalance_current_allocation))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    def ct(x,col):
        x=x.dropna(subset=[col]); n=len(x)
        if n<5: return pd.Series(dict(n=n))
        m=x[col].mean(); ds=(x[col]-m).groupby(x.day).sum()
        se=np.sqrt((ds**2).sum())/n
        return pd.Series(dict(n=n,days=len(ds),mean=m,t=m/se))
    for hz in [1,2,3]:
        g=D[(D.pos%hz==0)].dropna(subset=["f%d"%hz,"clv"]).copy()
        dr=g.groupby("coin")["f%d"%hz].mean(); sd=g.groupby("coin")["f%d"%hz].std()
        g["u"]=g["f%d"%hz]-g.coin.map(dr); g["s"]=g.u/g.coin.map(sd)
        g["b"]=g.groupby("coin").clv.transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
        out["clv_q_h%d"%hz]=g.groupby("b").apply(lambda x: pd.concat([ct(x,"u"),pd.Series(dict(str=x.s.mean()))]))
        # graded signal: (0.5-clv) times u, sign
        g["sig"]=(0.5-g.clv)
        g["su"]=np.sign(g.sig)*g.u
        if hz==1:
            out["h1_signed_by_coin"]=g.groupby("coin").apply(lambda x: ct(x,"su"))
            out["h1_signed_by_year"]=g.groupby("yr").apply(lambda x: ct(x,"su"))
            out["h1_signed_all"]=ct(g,"su")
            # extremes per year: low close quintile minus high
            out["h1_lowq_by_year"]=g[g.b==0].groupby("yr").apply(lambda x: ct(x,"u"))
            out["h1_highq_by_year"]=g[g.b==4].groupby("yr").apply(lambda x: ct(x,"u"))
            # by wide vs narrow range
            g["wide"]=g.rr>=1.0
            out["h1_clvq_by_wide"]=g.groupby(["wide","b"]).apply(lambda x: ct(x,"u"))
            out["h1_lowq_by_wd"]=g[g.b==0].groupby("wd").apply(lambda x: ct(x,"u"))
            out["corr_sig_u"]=float(np.corrcoef(g.sig,g.s)[0,1])
    # book: days in position, mean coin return next day when short
    p=D[D.alloc.fillna(0)!=0]
    out["pos_share_and_mean_alloc"]=pd.Series(dict(n=len(p),mean_alloc=p.alloc.mean(),mean_f1=p.f1.mean()))
    return out
