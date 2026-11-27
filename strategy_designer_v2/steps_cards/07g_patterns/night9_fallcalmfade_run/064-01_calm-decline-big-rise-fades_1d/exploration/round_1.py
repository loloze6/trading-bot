def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd=r1.rolling(20).std()
            sw=r1/sd
            tr=c/c.shift(60)-1
            vol30=r1.rolling(30).std()
            volrank=vol30.rolling(90,min_periods=60).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            f3=c.shift(-3)/c-1
            f1=c.shift(-1)/c-1
            df=pd.DataFrame({"coin":coin,"w":w,"sw":sw,"tr":tr,"vr":volrank,"f3":f3,"f1":f1,
                             "day":b["timestamp"].astype(str).str[:10],"wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                             "reg":b["regime"],"fc":b["forecast"],"pos":np.arange(len(b))})
            rows.append(df)
    d=pd.concat(rows)
    g=d[(d.pos%3==0)&d.f3.notna()].copy()
    drift=g.groupby("coin").f3.mean()
    g["ex"]=g.f3-g.coin.map(drift)
    g["trb"]=pd.cut(g.tr,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    g["swb"]=pd.cut(g.sw,[-99,-2,-1,0,1,2,99])
    def agg(x):
        n=len(x); m=x.ex.mean()
        ds=(x.ex-0).groupby(x.day).sum()  # approximate
        se=np.sqrt(((x.ex-m).groupby(x.day).sum()**2).sum())/n if n>1 else np.nan
        return pd.Series({"n":n,"mean_ex":m,"t_day":m/se if se else np.nan})
    out={}
    out["sw_by_trend"]=g.dropna(subset=["trb","swb"]).groupby(["trb","swb"]).apply(agg)
    gc=g[g.vr<=0.5]
    out["sw_by_trend_calmproxy"]=gc.dropna(subset=["trb","swb"]).groupby(["trb","swb"]).apply(agg)
    ga=g[g.vr>0.5]
    out["sw_by_trend_agitproxy"]=ga.dropna(subset=["trb","swb"]).groupby(["trb","swb"]).apply(agg)
    cs=g[g.reg=="mean_reversion"]
    out["cases_by_coin"]=cs.groupby("coin").apply(agg)
    out["cases_by_w"]=cs.groupby("w").apply(agg)
    out["regime_counts"]=d.reg.value_counts()
    out["corr_sw_ex_fall"]=float(g[g.trb=="fall"][["sw","ex"]].corr().iloc[0,1])
    out["corr_sw_ex_all"]=float(g[["sw","ex"]].corr().iloc[0,1])
    return out
