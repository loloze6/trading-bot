def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            vol = r.shift(1).rolling(30, min_periods=15).std()  # past-only vol
            z = r / vol
            raw = b["debug_info.components.low_prox.last_history_value"]
            d = pd.DataFrame(dict(coin=coin, w=w, i=np.arange(len(b)), ts=b["timestamp"],
                                  r=r, z=z, vol=vol, raw=raw,
                                  n1=c.shift(-1)/c-1, n3=c.shift(-3)/c-1, n5=c.shift(-5)/c-1,
                                  p60=c/c.shift(60)-1))
            dl = []
            dl.append(d)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = pd.to_datetime(D["ts"]).dt.floor("D")
    D["wd"] = pd.to_datetime(D["ts"]).dt.dayofweek
    D["yr"] = pd.to_datetime(D["ts"]).dt.year
    mu1 = D.groupby("coin")["n1"].transform("mean")
    D["e1"] = D["n1"] - mu1
    def clus_t(s, days):
        g = s.groupby(days).sum()
        n = s.groupby(days).size()
        m = s.sum()/len(s)
        dev = (s - m).groupby(days).sum()
        se = np.sqrt((dev**2).sum())/len(s)
        return m/se, g.size
    zb = pd.cut(D["z"], [-99,-3,-2,-1.5,-1,1,1.5,2,3,99])
    res = []
    for k, g in D.dropna(subset=["z","e1"]).groupby(zb):
        t, nd = clus_t(g["e1"], g["day"])
        res.append(dict(bin=str(k), n=len(g), days=nd, e1=g["e1"].mean(), t_day=t))
    out["next1_excess_by_pastvol_z"] = pd.DataFrame(res)
    dd = D.dropna(subset=["z","e1"])
    dn = dd[dd["z"]<0]
    sl = stats.linregress(dn["z"], dn["e1"])
    out["slope_e1_on_z_downdays"] = pd.Series(dict(slope=sl.slope, t=sl.slope/sl.stderr, n=len(dn)))
    up = dd[dd["z"]>0]
    sl2 = stats.linregress(up["z"], up["e1"])
    out["slope_e1_on_z_updays"] = pd.Series(dict(slope=sl2.slope, t=sl2.slope/sl2.stderr, n=len(up)))
    big = dd[dd["z"]<=-2]
    out["bigdrop_by_window"] = big.groupby("w")["e1"].agg(["size","mean"])
    out["bigdrop_by_coin"] = big.groupby("coin")["e1"].agg(["size","mean"])
    out["bigdrop_by_year"] = big.groupby("yr")["e1"].agg(["size","mean"])
    out["bigdrop_by_weekday"] = big.groupby("wd")["e1"].agg(["size","mean"])
    big = big.copy()
    big["near"] = pd.qcut(big["raw"].rank(method="first"), 3, labels=["far","mid","near"])
    out["bigdrop_by_nearness"] = big.groupby("near")["e1"].agg(["size","mean","std"])
    big["tr"] = np.where(big["p60"]>0.1,"rising",np.where(big["p60"]<-0.1,"falling","choppy"))
    out["bigdrop_by_trend60"] = big.groupby("tr")["e1"].agg(["size","mean","std"])
    # 3-day after big drop, non overlap approximated by first in 3-day block
    b3 = big[big["n3"].notna()].copy()
    b3["e3"] = b3["n3"] - b3.groupby("coin")["n3"].transform("mean")
    t3, nd3 = clus_t(b3["e3"], b3["day"])
    out["bigdrop_next3"] = pd.Series(dict(n=len(b3), mean=b3["n3"].mean(), t_day=t3, days=nd3))
    # does day after big drop open gap? intraday: next day high-low recovery
    # weekday effect clustered by day
    wdres=[]
    for k,g in dd.groupby("wd"):
        t,nd=clus_t(g["e1"],g["day"]); wdres.append(dict(wd=k,n=len(g),days=nd,e1=g["e1"].mean(),t_day=t))
    out["weekday_next1_excess"]=pd.DataFrame(wdres)
    # near yearly low: next-day reversal at the low (raw>0.5)
    at = dd[dd["raw"]>0.3]
    out["at_low_next1"] = pd.Series(dict(n=len(at), e1=at["e1"].mean(), t=at["e1"].mean()/(at["e1"].std()/np.sqrt(len(at)))))
    return out
