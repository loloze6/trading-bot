def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            n=len(b)
            r60=c/c.shift(60)-1; r10=c/c.shift(10)-1; r1=c.pct_change()
            vr=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            vol30=r1.rolling(30).std()
            clpos=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            f5=c.shift(-5)/c-1; f2=c.shift(-2)/c-1
            vg=b.get("debug_info.components.vol_growth.post_pipeline_value")
            fd=b.get("debug_info.components.fall10.post_pipeline_value")
            for i in range(0,n-5,5):
                rows.append(dict(coin=coin,w=w,ts=str(b["timestamp"][i])[:10],r60=r60[i],r10=r10[i],r1=r1[i],vr=vr[i],
                    vol30=vol30[i],clpos=clpos[i],f5=f5[i],fc=b["forecast"][i],
                    al=b["postRebalance_current_allocation"][i],
                    vg=vg[i] if vg is not None else np.nan, fd=fd[i] if fd is not None else np.nan,
                    yr=pd.Timestamp(b["timestamp"][i]).year))
    d=pd.DataFrame(rows).dropna(subset=["f5"])
    d["u5"]=d["f5"]-d["coin"].map(d.groupby("coin")["f5"].mean())
    d["volq"]=d.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    def tab(g):
        g=g.dropna(subset=["u5"])
        s=g.groupby("ts")["u5"].sum(); m=g["u5"].mean(); k=len(s)
        dev=g.assign(e=g["u5"]-m).groupby("ts")["e"].sum()
        se=np.sqrt((dev**2).sum())/len(g) if len(g)>2 else np.nan
        return pd.Series(dict(n=len(g),days=k,mean=m,tc=m/se if se else np.nan))
    out={}
    F=d[d["r60"]<-0.1].copy()
    F["vrq"]=pd.qcut(F["vr"],5,labels=False)
    out["fall: volratio quintile x vol tercile"]=F.groupby(["volq","vrq"]).apply(tab)
    out["fall: volratio quintile by year (bottom vs top)"]=F[F["vrq"].isin([0,4])].groupby(["yr","vrq"]).apply(tab)
    out["fall: volratio quintile by coin, bottom"]=F[F["vrq"]==0].groupby("coin").apply(tab)
    F["clq"]=pd.qcut(F["clpos"],4,labels=False)
    out["fall: dryup half x close quartile"]=F.assign(dry=(F["vr"]<0).astype(int)).groupby(["dry","clq"]).apply(tab)
    NR=d[d["r60"]<0.1].copy()
    NR["clq"]=pd.qcut(NR["clpos"],5,labels=False)
    out["not rising: close position quintile"]=NR.groupby("clq").apply(tab)
    out["not rising: close quintile 0 by year"]=NR[NR["clq"]==0].groupby("yr").apply(tab)
    R=d[d["r60"]>0.1]
    out["rise: vol tercile"]=R.groupby("volq").apply(tab)
    # regime cases: falling, vr>0, r10<0
    G=d[(d["r60"]<-0.1)&(d["vr"]>0)&(d["r10"]<0)].copy()
    G["vrh"]=pd.qcut(G["vr"],3,labels=False); G["r10h"]=pd.qcut(G["r10"],3,labels=False)
    out["regime: vr tercile"]=G.groupby("vrh").apply(tab)
    out["regime: r10 tercile (0 deepest)"]=G.groupby("r10h").apply(tab)
    out["all falling: r10 decile"]=F.assign(q=pd.qcut(F["r10"],10,labels=False)).groupby("q").apply(tab)
    t=[]
    for coin,wins in data["trades"].items():
        for w,x in wins.items():
            if len(x): x=x.copy(); x["coin"]=coin; t.append(x)
    T=pd.concat(t)
    T["efq"]=pd.qcut(T["entry_forecast"],4,labels=False,duplicates="drop")
    out["trades: entry forecast quartile"]=T.groupby("efq").agg(n=("net_profit_loss_percent","size"),
        mean=("net_profit_loss_percent","mean"),fcmin=("entry_forecast","min"),dur_h=("duration_minutes",lambda s:s.mean()/60))
    return out
