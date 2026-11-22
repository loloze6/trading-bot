def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drift = {}
    for coin, wins in bars.items():
        for L in (8,10,5):
            rs=[]
            for w,df in wins.items():
                c=df["close"].values
                idx=np.arange(0,len(c)-L,L)
                rs+=list(c[idx+L]/c[idx]-1)
            drift[(coin,L)]=np.mean(rs)
    rows=[]
    for coin, wins in bars.items():
        for w,df in wins.items():
            c=df["close"].values; n=len(c)
            ts=pd.to_datetime(df["timestamp"]).dt.year.values
            ph=pd.Series(c).shift(1).rolling(20).max().values
            r1=pd.Series(c).pct_change()
            vol=r1.rolling(20).std().values
            bo=c>ph
            last=-100
            for e in range(25,n):
                if bo[e]: continue
                H=None
                for k in (1,2,3):
                    if e-k>=0 and bo[e-k]:
                        H=ph[e-k]; kk=k; break
                if H is None or not c[e]<H: continue
                if e-last<8: continue
                last=e
                depth=(H-c[e])/H
                d=dict(coin=coin,year=ts[e],depth=depth*100,zdepth=depth/vol[e] if vol[e]>0 else np.nan,
                       mom60=(c[e]/c[e-60]-1) if e>=60 else np.nan,
                       overshoot=(c[e-kk:e].max()/H-1)*100)
                if e+10<n:
                    d["d2_10"]=-(c[e+10]/c[e+2]-1-drift[(coin,8)])
                    d["d0_10"]=-(c[e+10]/c[e]-1-drift[(coin,10)])
                    d["second_break"]=float(c[e+1:e+11].max()>max(H,c[e-kk:e].max()))
                rows.append(d)
    ev=pd.DataFrame(rows).dropna(subset=["d2_10"])
    def summ(g):
        x=g["d2_10"]; y=g["d0_10"]
        return pd.Series({"n":len(g),"d2_10%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),
                          "d0_10%":100*y.mean(),"t010":y.mean()/(y.std()/np.sqrt(len(y))),
                          "second_break_share":g["second_break"].mean()})
    res={}
    res["all"]=summ(ev).to_frame().T
    ev["zq"]=pd.qcut(ev["zdepth"],3,labels=["zlow","zmid","zhigh"])
    res["by_zdepth"]=ev.groupby("zq").apply(summ)
    ev["oq"]=pd.qcut(ev["overshoot"],3,labels=["small","mid","big"])
    res["by_overshoot"]=ev.groupby("oq").apply(summ)
    ev["dq"]=pd.qcut(ev["depth"],3,labels=["shallow","mid","deep"])
    sub=ev.dropna(subset=["mom60"]).copy()
    sub["mq"]=pd.qcut(sub["mom60"],3,labels=["m_low","m_mid","m_high"])
    res["by_mom_tercile"]=sub.groupby("mq").apply(summ)
    res["by_mom_depth"]=sub.groupby(["mq","dq"]).apply(summ)[["n","d2_10%","t","d0_10%"]]
    sh=ev[ev["dq"]=="shallow"]
    res["shallow_by_coin"]=sh.groupby("coin").apply(summ)[["n","d2_10%","t"]]
    res["shallow_by_year"]=sh.groupby("year").apply(summ)[["n","d2_10%","t"]]
    dp=ev[ev["dq"]=="deep"]
    res["deep_by_coin"]=dp.groupby("coin").apply(summ)[["n","d2_10%","t","d0_10%"]]
    res["spearman_z_d2_10"]=str(stats.spearmanr(ev["zdepth"],ev["d2_10"],nan_policy="omit"))
    res["spearman_over_d2_10"]=str(stats.spearmanr(ev["overshoot"],ev["d2_10"]))
    return res
