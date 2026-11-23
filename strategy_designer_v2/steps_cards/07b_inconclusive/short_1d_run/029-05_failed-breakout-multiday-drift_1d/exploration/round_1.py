def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    hz = {"d0_1":(0,1),"d0_2":(0,2),"d0_5":(0,5),"d0_10":(0,10),"d2_10":(2,10),"d2_6":(2,6),"d0_20":(0,20)}
    # drift per length per coin (grid, all windows)
    drift = {}
    for coin, wins in bars.items():
        for L in set(b-a for a,b in hz.values()):
            rs=[]
            for w,df in wins.items():
                c=df["close"].values
                idx=np.arange(0,len(c)-L,L)
                rs+=list(c[idx+L]/c[idx]-1)
            drift[(coin,L)]=np.mean(rs)
    rows=[]
    fc_at=[]
    for coin, wins in bars.items():
        for w,df in wins.items():
            c=df["close"].values; n=len(c)
            ts=pd.to_datetime(df["timestamp"]).dt.year.values
            ph=pd.Series(c).shift(1).rolling(20).max().values
            bo=c>ph
            last=-100
            for e in range(25,n):
                if bo[e]: continue
                H=None
                for k in (1,2,3):
                    if e-k>=0 and bo[e-k]:
                        H=ph[e-k]; break
                if H is None or not c[e]<H: continue
                if e-last<8: continue
                last=e
                d=dict(coin=coin,win=w,year=ts[e],depth=(H-c[e])/H*100,
                       mom60=(c[e]/c[e-60]-1) if e>=60 else np.nan,
                       brk=(c[e-k]/H-1)*100)
                for nm,(a,b) in hz.items():
                    if e+b<n:
                        r=c[e+b]/c[e+a]-1
                        d[nm]=-(r-drift[(coin,b-a)])
                        d[nm+"_tot"]=-r
                rows.append(d)
                if e+2<n: fc_at.append(df["forecast"].values[e+2])
    ev=pd.DataFrame(rows)
    def summ(g):
        out={}
        for nm in hz:
            x=g[nm].dropna()
            out[nm+"_mean%"]=100*x.mean()
            out[nm+"_t"]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        out["n"]=len(g)
        return pd.Series(out)
    res={}
    res["all"]=summ(ev).to_frame().T
    res["all_total_d2_10_mean%"]=100*ev["d2_10_tot"].mean()
    res["by_coin"]=ev.groupby("coin").apply(summ)[["n","d0_2_mean%","d0_2_t","d2_10_mean%","d2_10_t","d0_10_mean%","d0_10_t"]]
    res["by_year"]=ev.groupby("year").apply(summ)[["n","d0_2_mean%","d2_10_mean%","d2_10_t","d0_10_mean%"]]
    ev["dq"]=pd.qcut(ev["depth"],3,labels=["shallow","mid","deep"])
    res["by_depth"]=ev.groupby("dq").apply(summ)[["n","d0_1_mean%","d0_2_mean%","d2_10_mean%","d2_10_t","d0_10_mean%","d0_10_t","d0_20_mean%"]]
    res["depth_quantiles"]=ev["depth"].describe()
    ev["trend"]=np.where(ev["mom60"]>0,"up60","down60")
    res["by_trend"]=ev.dropna(subset=["mom60"]).groupby("trend").apply(summ)[["n","d0_2_mean%","d2_10_mean%","d2_10_t","d0_10_mean%","d0_10_t","d0_20_mean%","d0_20_t"]]
    res["by_trend_depth"]=ev.dropna(subset=["mom60"]).groupby(["trend","dq"]).apply(summ)[["n","d2_10_mean%","d2_10_t","d0_10_mean%","d0_10_t"]]
    sp=ev.dropna(subset=["d2_10"])
    res["spearman_depth_d2_10"]=str(stats.spearmanr(sp["depth"],sp["d2_10"]))
    fc=pd.Series(fc_at)
    res["forecast_at_e+2"]=fc.describe()
    res["share_fc_eq_-20"]=float((fc<=-19.99).mean())
    return res
