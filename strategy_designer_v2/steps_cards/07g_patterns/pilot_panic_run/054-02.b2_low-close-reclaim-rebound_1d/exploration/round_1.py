def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; lo=b["low"].values; hi=b["high"].values; op=b["open"].values
            n=len(b)
            pl=pd.Series(lo).shift(1).rolling(30,min_periods=30).min().values
            ph=pd.Series(hi).shift(1).rolling(30,min_periods=30).max().values
            r1=np.r_[np.nan, c[1:]/c[:-1]-1]
            vol20=pd.Series(r1).rolling(20,min_periods=15).std().values
            ret5p=np.r_[[np.nan]*5, c[5:]/c[:-5]-1]
            for t in range(n):
                fwd=c[t+H]/c[t]-1 if t+H<n else np.nan
                rng=hi[t]-lo[t]
                rows.append(dict(coin=coin,w=w,t=t,cell=t//H,fwd=fwd,
                    reg=b["regime"].iloc[t],
                    pierce=lo[t]<pl[t] if not np.isnan(pl[t]) else False,
                    reclaim=(lo[t]<pl[t]<c[t]) if not np.isnan(pl[t]) else False,
                    breakdown=(c[t]<pl[t]) if not np.isnan(pl[t]) else False,
                    hpierce=(hi[t]>ph[t]>c[t]) if not np.isnan(ph[t]) else False,
                    cl=(hi[t]-c[t])/rng if rng>0 else np.nan,
                    depth=(pl[t]-lo[t])/c[t] if not np.isnan(pl[t]) else np.nan,
                    r1=r1[t], z1=r1[t]/vol20[t] if vol20[t]>0 else np.nan,
                    ret5p=ret5p[t],
                    wd=pd.Timestamp(b["timestamp"].iloc[t]).weekday(),
                    grid=(t%H==0)))
    d=pd.DataFrame(rows)
    d["infp"]=d["reg"].isin(["mean_reversion","unknown"])
    g=d[d.grid&d.fwd.notna()]
    drift=g.groupby("coin").fwd.mean()
    d["ex"]=d.fwd-d.coin.map(drift)
    out={}
    out["drift5"]=drift
    out["regime_counts"]=d.reg.value_counts()
    def ev(mask,name):
        e=d[mask&d.ex.notna()].groupby(["coin","w","cell"]).head(1)
        if len(e)<3: return dict(name=name,n=len(e))
        day=e.groupby(["w","t"]).ex.sum() # approx day cluster
        tt=e.ex.mean()/(e.ex.std(ddof=1)/np.sqrt(len(e)))
        return dict(name=name,n=len(e),mean=e.ex.mean(),t=tt,hit=(e.ex>0).mean())
    res=[]
    res.append(ev(d.reclaim,"reclaim all"))
    res.append(ev(d.reclaim&d.infp,"reclaim in FA"))
    res.append(ev(d.reclaim&~d.infp,"reclaim outside FA"))
    res.append(ev(d.breakdown,"close below 30d low all"))
    res.append(ev(d.breakdown&d.infp,"close below low FA"))
    res.append(ev(d.breakdown&~d.infp,"close below low out"))
    res.append(ev(d.hpierce,"failed high break all"))
    res.append(ev(d.hpierce&d.infp,"failed high break FA"))
    res.append(ev(d.infp,"any day FA"))
    res.append(ev(~d.infp,"any day out"))
    res.append(ev(d.reclaim&(d.cl>0.5),"reclaim low close"))
    res.append(ev(d.reclaim&(d.cl<=0.5),"reclaim high close"))
    res.append(ev(d.reclaim&~d.infp&(d.cl>0.5),"reclaim low close out"))
    out["events"]=pd.DataFrame(res)
    gg=g.copy(); gg["ex"]=gg.fwd-gg.coin.map(drift)
    gg["zq"]=pd.qcut(gg.z1,5,labels=False)
    out["by_z1_quint_all"]=gg.groupby("zq").ex.agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    gg["pq"]=pd.qcut(gg.ret5p,5,labels=False)
    out["by_ret5past_quint_all"]=gg.groupby("pq").ex.agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["by_ret5past_quint_FA"]=gg[gg.infp].groupby("pq").ex.agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["by_wd"]=gg.groupby("wd").ex.agg(["mean","count"])
    out["by_coin_infp"]=gg.groupby(["coin","infp"]).ex.agg(["mean","count"])
    return out
