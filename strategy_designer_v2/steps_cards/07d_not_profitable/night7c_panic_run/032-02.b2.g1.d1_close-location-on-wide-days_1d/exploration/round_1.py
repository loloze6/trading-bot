def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; allr.append((c.shift(-1)/c-1).dropna())
        drift=pd.concat(allr).mean()
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            h,l,c=b["high"],b["low"],b["close"]
            rng=(h-l)
            avg=rng.shift(1).rolling(20,min_periods=20).mean()
            cl=(2*c-h-l)/rng.replace(0,np.nan)
            mult=rng/avg
            r1=c.shift(-1)/c-1
            r3=c.shift(-3)/c-1
            ret20=c/c.shift(20)-1
            alloc=b["postRebalance_current_allocation"]
            pos_gain=alloc*r1
            chg=b["allocation_change"].abs() if "allocation_change" in b else (alloc-b["previous_allocation"]).abs()
            df=pd.DataFrame(dict(coin=coin,w=w,cl=cl,mult=mult,r1=r1,ex1=r1-drift,r3=r3-3*drift,
                                 fc=b["forecast"],alloc=alloc,pg=pos_gain,chg=chg,ret20=ret20,year=pd.to_datetime(b["timestamp"]).dt.year,
                                 pos=np.arange(len(b))))
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["cl","mult","ex1"])
    d["sig"]=-d["cl"]  # +long
    d["side"]=np.where(d.sig>0,"long","short")
    d["mq"]=pd.qcut(d["mult"],5,labels=False)
    d["cq"]=pd.cut(d["cl"],[-1.01,-0.6,-0.2,0.2,0.6,1.01],labels=["low","midlow","mid","midhigh","high"])
    def ag(g):
        x=np.sign(g.sig)*g.ex1
        return pd.Series(dict(n=len(g),direx_pct=100*x.mean(),t=x.mean()/x.std()*np.sqrt(len(x)),raw_ex_pct=100*g.ex1.mean()))
    out={}
    out["by_multq_side"]=d.groupby(["mq","side"]).apply(ag)
    out["by_cl_multq_rawex"]=d.pivot_table(index="cq",columns="mq",values="ex1",aggfunc="mean")*100
    out["mult_quintile_edges"]=d.groupby("mq")["mult"].agg(["min","max"])
    # 3-day grid non-overlapping
    d3=d[d.pos%3==0].dropna(subset=["r3"])
    out["r3_by_multq_side"]=d3.groupby(["mq","side"]).apply(lambda g: pd.Series(dict(n=len(g),dir_pct=100*(np.sign(g.sig)*g.r3).mean())))
    # book: gain by side, turnover
    d["pgside"]=np.where(d.alloc>0,"long",np.where(d.alloc<0,"short","flat"))
    out["book_pos_gain_by_side"]=d.groupby("pgside").agg(n=("pg","size"),mean_gain_pct=("pg",lambda s:100*s.mean()),mean_absalloc=("alloc",lambda s:s.abs().mean()))
    out["turnover_per_bar"]=d["chg"].mean()
    out["gross_mean_pg_pct"]=100*d.pg.mean()
    out["by_window"]=d.groupby("w").apply(lambda g: pd.Series(dict(pg_pct=100*g.pg.mean(),direx_pct=100*(np.sign(g.sig)*g.ex1).mean(),coinret_pct=100*g.r1.mean())))
    out["by_ret20sign_side_widetop"]=d[d.mq>=3].assign(down=d.ret20<0).groupby(["down","side"]).apply(ag)
    out["by_ret20sign_side_all"]=d.assign(down=d.ret20<0).groupby(["down","side"]).apply(ag)
    return out
