def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    drift = {}
    for coin, ws in bars.items():
        for H in [3,5,10]:
            rr=[]
            for w,b in ws.items():
                c=b["close"].values; idx=np.arange(0,len(c)-H,H); rr+=list(c[idx+H]/c[idx]-1)
            drift[(coin,H)]=(np.mean(rr),np.std(rr))
    rows=[]
    for coin, ws in bars.items():
        for w,b in ws.items():
            b=b.reset_index(drop=True); c=b["close"]; v=b["volume"]
            vr=v/v.shift(1).rolling(20,min_periods=20).mean()
            r1=c/c.shift(1)-1
            rng=(b["high"]-b["low"])/c
            clv=(c-b["low"])/(b["high"]-b["low"])
            fc=b["regime"]!="chop"
            for H in [3,5,10]:
                f=c.shift(-H)/c-1
                for off in range(H):
                    for i in range(off,len(b)-H,H):
                        if not fc.iloc[i] or pd.isna(vr.iloc[i]) or pd.isna(r1.iloc[i]): continue
                        rows.append(dict(coin=coin,w=w,H=H,off=off,day=str(b["timestamp"].iloc[i])[:10],
                          year=str(b["timestamp"].iloc[i])[:4],vr=vr.iloc[i],r1=r1.iloc[i],clv=clv.iloc[i],
                          u=(f.iloc[i]-drift[(coin,H)][0]),s=(f.iloc[i]-drift[(coin,H)][0])/drift[(coin,H)][1]))
    d=pd.DataFrame(rows)
    def tday(g):
        g2=g.groupby("day")["u"].sum(); m=g["u"].mean(); n=len(g)
        dev=(g["u"]-m).groupby(g["day"]).sum()
        se=np.sqrt((dev**2).sum())/n if n>1 else np.nan
        return pd.Series(dict(n=n,mean=m,strength=g["s"].mean(),t=m/se if se>0 else np.nan))
    up=d[d.r1>0]
    out["up_vs_down_by_H_off"]=d.assign(side=np.where(d.r1>0,"up","down")).groupby(["H","off","side"]).apply(tday).unstack("side")[["n","mean","t"]]
    sp=[]
    for (H,off),g in up.groupby(["H","off"]):
        sp.append(dict(H=H,off=off,rho_r1=stats.spearmanr(g.r1,g.u)[0],rho_vr=stats.spearmanr(g.vr,g.u)[0],rho_clv=stats.spearmanr(g.clv,g.u)[0],n=len(g)))
    out["up_spearman_by_H_off"]=pd.DataFrame(sp)
    u5=up[up.H==5].copy()
    u5["r1q"]=pd.qcut(u5.r1,3,labels=["small","mid","big"])
    u5["vq"]=np.where(u5.vr>1,"heavy","light")
    out["up5_r1tercile_x_vol_alloffsets"]=u5.groupby(["r1q","vq"]).apply(tday)
    out["up5_coin_alloff"]=u5.groupby(["coin","vq"]).apply(tday)
    out["up5_year_alloff"]=u5.groupby("year").apply(tday)
    a5=d[d.H==5].copy(); a5["q"]=pd.qcut(a5.r1,5,labels=False)
    out["all5_r1quintile_alloff"]=a5.groupby("q").apply(tday)
    out["all5_r1quintile_coin_BTC_XMR"]=a5[a5.coin!="DOGEUSD"].groupby(["coin","q"]).apply(tday)[["n","mean","t"]]
    return out
