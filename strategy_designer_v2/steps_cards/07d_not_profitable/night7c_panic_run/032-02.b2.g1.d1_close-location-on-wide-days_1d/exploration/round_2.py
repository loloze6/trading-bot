def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w, b in wins.items():
            c=b["close"].reset_index(drop=True); allr.append((c.shift(-1)/c-1).dropna())
        drift=pd.concat(allr).mean()
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            h,l,c=b["high"],b["low"],b["close"]
            rng=(h-l)
            avg=rng.shift(1).rolling(20,min_periods=20).mean()
            cl=(2*c-h-l)/rng.replace(0,np.nan)
            mult=rng/avg
            raw=(2*c-h-l)/avg
            r1=c.shift(-1)/c-1
            alloc=b["postRebalance_current_allocation"]
            chg=(alloc-b["previous_allocation"]).abs()
            df=pd.DataFrame(dict(coin=coin,w=w,cl=cl.values,mult=mult.values,raw=raw.values,
                                 raw3=raw.rolling(3).mean().values,
                                 r1=r1.values,ex1=(r1-drift).values,
                                 r2=(c.shift(-2)/c-1-2*drift).values,r3=(c.shift(-3)/c-1-3*drift).values,
                                 fc=b["forecast"].values,alloc=alloc.values,pg=(alloc*r1).values,chg=chg.values,
                                 ret20=(c/c.shift(20)-1).values,pos=np.arange(len(b))))
            rows.append(df)
    d=pd.concat(rows,ignore_index=True).dropna(subset=["cl","mult","ex1"]).reset_index(drop=True)
    d["sig"]=-d["cl"]
    d["side"]=np.where(d.sig>0,"long","short")
    d["mq"]=pd.qcut(d["mult"],5,labels=False)
    d["cq"]=pd.cut(d["cl"],[-1.01,-0.6,-0.2,0.2,0.6,1.01],labels=["low","midlow","mid","midhigh","high"])
    def ag(g,col="ex1"):
        x=np.sign(g.sig)*g[col]
        return pd.Series(dict(n=len(g),dir_pct=100*x.mean(),t=x.mean()/x.std()*np.sqrt(len(x))))
    out={}
    out["by_multq_side"]=d.groupby(["mq","side"]).apply(ag)
    out["rawex_cl_x_multq_pct"]=d.pivot_table(index="cq",columns="mq",values="ex1",aggfunc="mean")*100
    out["mult_edges"]=d.groupby("mq")["mult"].agg(["min","max"])
    d3=d[d.pos%3==0].dropna(subset=["r3"])
    out["r3_by_multq_side"]=d3.groupby(["mq","side"]).apply(lambda g: ag(g,"r3"))
    d2=d[d.pos%2==0].dropna(subset=["r2"])
    out["r2_by_multq_side"]=d2.groupby(["mq","side"]).apply(lambda g: ag(g,"r2"))
    # condition alone: mid-close bars by mult quintile, raw excess
    out["midclose_rawex_by_multq_pct"]=d[d.cq=="mid"].groupby("mq")["ex1"].agg(lambda s:100*s.mean())
    d["ps"]=np.where(d.alloc>0,"long",np.where(d.alloc<0,"short","flat"))
    out["book_by_side"]=d.groupby("ps").agg(n=("pg","size"),gain_pct=("pg",lambda s:100*s.mean()),absalloc=("alloc",lambda s:s.abs().mean()))
    out["gross_pg_pct_per_bar"]=100*d.pg.mean()
    out["turnover_per_bar"]=d.chg.mean()
    out["est_cost_pct_per_bar"]=100*d.chg.mean()*0.0019/2
    out["absalloc_mean"]=d.alloc.abs().mean()
    out["sign_flip_share"]=(np.sign(d.alloc)!=np.sign(d.groupby(["coin","w"]).alloc.shift(1))).mean()
    out["corr_alloc_vs_sig"]=d[["alloc","sig","fc"]].corr()
    # book gain by mult quintile
    out["pg_by_multq_pct"]=d.groupby("mq").agg(pg_pct=("pg",lambda s:100*s.mean()),absalloc=("alloc",lambda s:s.abs().mean()),chg=("chg","mean"))
    out["by_window"]=d.groupby("w").apply(lambda g: pd.Series(dict(pg_pct=100*g.pg.mean(),dir_pct=100*(np.sign(g.sig)*g.ex1).mean(),coin_pct=100*g.r1.mean())))
    d["down"]=d.ret20<0
    out["trend_side_wide"]=d[d.mq>=3].groupby(["down","side"]).apply(ag)
    out["trend_side_all"]=d.groupby(["down","side"]).apply(ag)
    # smoothed signal: 3-day mean of raw, tercile excess
    e=d.dropna(subset=["raw3"]).copy()
    e["s3q"]=pd.qcut(-e.raw3,5,labels=False)
    out["raw3_quint_ex1_pct"]=e.groupby("s3q")["ex1"].agg(lambda s:100*s.mean())
    e["s1q"]=pd.qcut(-e.raw,5,labels=False)
    out["raw_quint_ex1_pct"]=e.groupby("s1q")["ex1"].agg(lambda s:100*s.mean())
    # book daily falls
    dd=[]
    for coin,wins in data["days"].items():
        for w,t in wins.items():
            dd.append(pd.DataFrame(dict(coin=coin,w=w,i=np.arange(len(t)),br=t["book_return"].values,cr=t["coin_return"].values)))
    D=pd.concat(dd,ignore_index=True)
    bk=D.groupby(["w","i"])[["br","cr"]].mean().reset_index()
    out["book_daily_by_window"]=bk.groupby("w").agg(book_pct=("br",lambda s:100*s.mean()),hold_pct=("cr",lambda s:100*s.mean()))
    return out
