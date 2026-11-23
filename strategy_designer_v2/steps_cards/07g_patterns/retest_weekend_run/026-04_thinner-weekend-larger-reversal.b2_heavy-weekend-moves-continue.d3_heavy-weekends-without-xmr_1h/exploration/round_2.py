def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; hr = []
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            c = b["close"].values
            g += list(c[48::48]/c[:-48:48][:len(c[48::48])]-1)
        sd48 = np.std(g); mu48 = np.mean(g)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); c = b["close"].values; v = b["volume"].values.astype(float)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            # volatility level: trailing 24h abs-return mean, known at bar open
            vol24 = pd.Series(np.abs(r1)).shift(1).rolling(168, min_periods=100).mean().values
            hr.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,
                                    "year":ts.dt.year.values,"win":w,"r":r1,"vol":vol24}))
            idx = np.where(ts.dt.hour.values==23)[0]
            for i in idx:
                if i-168 < 0 or i+48 >= len(c): continue
                past = c[i]/c[i-48]-1
                vr = v[i-47:i+1].mean()/max(v[i-167:i-47].mean(),1e-12)
                f48 = c[i+48]/c[i]-1
                rows.append(dict(coin=coin, win=w, year=ts[i].year, wd=ts[i].weekday(), pz=past/sd48,
                                 vr=vr, f48=(f48-mu48)/sd48))
    d = pd.DataFrame(rows)
    d["sg"] = np.sign(d.pz)*d.f48
    d["lvr"] = np.log(d.vr)
    # graded by log volume ratio, every ending weekday: regression of signed fwd on log vr
    res=[]
    for wd in range(7):
        s=d[d.wd==wd].dropna(subset=["sg","lvr"])
        r=stats.linregress(s.lvr, s.sg); res.append(dict(endday=wd,n=len(s),slope=r.slope,t=r.slope/r.stderr))
    out["signed_fwd_on_logvr_by_endday"]=pd.DataFrame(res)
    s=d[d.wd==6].copy()
    s["vrq"]=pd.qcut(s.vr,5,labels=False)
    def tt(x): return pd.Series({"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)),"n":len(x)})
    out["sun_vrq_rise"]=s[s.pz>0].groupby("vrq")["sg"].apply(tt).unstack()
    out["sun_vrq_fall"]=s[s.pz<0].groupby("vrq")["sg"].apply(tt).unstack()
    out["sun_logvr_slope_by_coin"]=s.groupby("coin").apply(lambda x: pd.Series(dict(
        slope=stats.linregress(x.lvr,x.sg).slope, t=stats.linregress(x.lvr,x.sg).slope/stats.linregress(x.lvr,x.sg).stderr)))
    # interaction: does signed continuation scale with |pz| within heavy weekends
    hv=s[s.vr>1]; r=stats.linregress(hv.pz.abs(), hv.sg)
    out["sun_heavy_sg_on_absmove"]=pd.Series(dict(slope=r.slope,t=r.slope/r.stderr,n=len(hv)))
    h=pd.concat(hr).dropna(subset=["r"])
    h["late"]=h.hour.isin([21,22])
    def tm(x): return pd.Series({"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)),"n":len(x)})
    out["h21_22_by_coin"]=h[h.late].groupby("coin")["r"].apply(tm).unstack()
    out["h21_22_by_year"]=h[h.late].groupby("year")["r"].apply(tm).unstack()
    out["h21_22_by_weekday"]=h[h.late].groupby("wd")["r"].apply(tm).unstack()
    # day-level t (pooling coins into one daily value) to remove cross-coin correlation
    hl=h[h.late].copy(); hl["k"]=hl.win+"_"+hl.year.astype(str)
    h["dayid"]=h.groupby(["coin","win"]).cumcount()//24
    agg=h[h.late].groupby(["win","dayid"])["r"].mean()
    out["h21_22_poolcoins_t"]=pd.Series(dict(mean=agg.mean(),t=agg.mean()/agg.std()*np.sqrt(len(agg)),n=len(agg)))
    h["volq"]=h.groupby("coin")["vol"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    out["h21_22_by_volq"]=h[h.late].groupby("volq")["r"].apply(tm).unstack()
    out["h2_3_by_year"]=h[h.hour.isin([2,3])].groupby("year")["r"].apply(tm).unstack()
    return out
