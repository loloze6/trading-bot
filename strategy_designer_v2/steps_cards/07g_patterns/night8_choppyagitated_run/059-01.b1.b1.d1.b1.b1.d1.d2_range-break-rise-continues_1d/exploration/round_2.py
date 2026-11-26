def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); n=len(c)
            r1=c.pct_change()
            vol30=r1.rolling(30).std()
            vol7=r1.rolling(7).std()
            r60=c/c.shift(60)-1
            # agitation proxy within window: vol30 vs its expanding median (window-limited)
            ag=vol30>vol30.expanding(30).median()
            fwd=c.shift(-14)/c-1
            fwd3=c.shift(-3)/c-1
            ts=pd.to_datetime(b["timestamp"])
            for off in range(14):
                for i in range(off,n,14):
                    if i+14>=n: break
                    rows.append(dict(coin=coin,w=w,off=off,day=ts[i].normalize(),fwd=fwd[i],
                        r1z=r1[i]/vol30[i] if vol30[i] else np.nan,
                        vr=vol7[i]/vol30[i] if vol30[i] else np.nan,
                        tr=np.where(r60[i]>0.1,"rising",np.where(r60[i]<-0.1,"falling","choppy")) if pd.notna(r60[i]) else "na",
                        ag=bool(ag[i]),year=ts[i].year))
    d=pd.DataFrame(rows).dropna(subset=["fwd"])
    d["ex"]=d["fwd"]-d[d.off==0].groupby("coin")["fwd"].mean().reindex(d["coin"]).values
    def tpool(g):
        s=(g["ex"]-g["ex"].mean()).groupby(g["day"]).sum()
        G=len(s); se=np.sqrt((s**2).sum()*G/(G-1))/len(g) if G>1 else np.nan
        return pd.Series(dict(n=len(g),days=G,mean=g["ex"].mean(),t=g["ex"].mean()/se))
    out={}
    for col in ["r1z","vr"]:
        q=d.dropna(subset=[col]).copy()
        q["b"]=q.groupby("off")[col].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
        # per offset t of bottom quintile minus rest
        res=[]
        for off,g in q.groupby("off"):
            lo=g[g.b==0]["ex"]; hi=g[g.b==4]["ex"]
            res.append(dict(off=off,lo=lo.mean(),hi=hi.mean(),cor=np.corrcoef(g[col],g["ex"])[0,1]))
        out[col+"_by_offset"]=pd.DataFrame(res).set_index("off")
        g0=q[q.off==0]
        out[col+"_q_off0_pooled"]=g0.groupby("b").apply(tpool)
        out[col+"_bottomq_by_trend_ag_off0"]=g0[g0.b==0].groupby(["tr","ag"]).apply(tpool)
        out[col+"_bottomq_by_year_alloff"]=q[q.b==0].groupby("year")["ex"].agg(["mean","count"])
        out[col+"_bottomq_by_coin_alloff"]=q[q.b==0].groupby("coin")["ex"].agg(["mean","count"])
    return out
