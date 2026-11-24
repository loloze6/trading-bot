def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values; h = b["high"].astype(float).values; l = b["low"].astype(float).values
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            for i in range(0, n, 7):
                if i + 7 >= n or i < 7: continue
                tr60 = c[i]/c[i-60]-1 if i >= 60 else np.nan
                vol30 = np.nanstd(r1[max(1,i-29):i+1]) if i >= 30 else np.nan
                volyr = np.nanstd(r1[1:i+1]) if i >= 60 else np.nan
                rows.append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), past7=c[i]/c[i-7]-1, fut7=c[i+7]/c[i]-1,
                                 tr60=tr60, vol30=vol30, agit=(vol30 > volyr) if volyr == volyr else np.nan))
            sd = pd.Series(r1).rolling(30, min_periods=20).std().values
            for i in range(1, n-3):
                rng = h[i]-l[i]
                daily.append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), wd=ts.iloc[i].dayofweek, r=r1[i],
                                  zr=r1[i]/sd[i-1] if i >= 1 and sd[i-1] == sd[i-1] and sd[i-1] > 0 else np.nan,
                                  nxt=c[i+1]/c[i]-1, nxt3=c[i+3]/c[i]-1,
                                  clpos=(c[i]-l[i])/rng if rng > 0 else np.nan,
                                  tr60=c[i]/c[i-60]-1 if i >= 60 else np.nan))
    def clus_t(d, col, key="day"):
        s = d.groupby(key)[col].sum(); cnt = d.groupby(key)[col].count()
        m = s.sum()/cnt.sum()
        dev = d[col]-m; sdv = dev.groupby(d[key]).sum()
        se = np.sqrt((sdv**2).sum())/cnt.sum()
        return m/se, len(s)
    g = pd.DataFrame(rows)
    g["ex"] = g["fut7"] - g["coin"].map(g.groupby("coin")["fut7"].mean())
    g["z"] = g.groupby("coin")["past7"].transform(lambda s: s/s.std())
    g["trend"] = pd.cut(g["tr60"], [-9,-0.1,0.1,99], labels=["fall","chop","rise"])
    def mom(d):
        d = d.dropna(subset=["z","ex"])
        if len(d) < 10: return pd.Series(dict(n=len(d)))
        d = d.assign(p=d["z"]*d["ex"])
        r = np.corrcoef(d["z"], d["ex"])[0,1]
        t, nd = clus_t(d, "p")
        return pd.Series(dict(n=len(d), r=r, t_signed_move_dayclus=t, days=nd, mean_signed=(np.sign(d["z"])*d["ex"]).mean()))
    out["chop_by_agit"] = g[g.trend=="chop"].groupby("agit").apply(mom)
    out["chop_by_window"] = g[g.trend=="chop"].groupby("w").apply(lambda d: pd.Series(dict(n=len(d), r=np.corrcoef(d.z,d.ex)[0,1] if len(d)>3 else np.nan)))
    g["vt"] = g.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["lowvol_by_trend"] = g[g.vt==0].groupby("trend").apply(mom)
    out["lowvol_by_window"] = g[g.vt==0].groupby("w").apply(lambda d: pd.Series(dict(n=len(d), r=np.corrcoef(d.z,d.ex)[0,1] if len(d)>3 else np.nan)))
    d = pd.DataFrame(daily).dropna(subset=["zr","nxt","clpos"])
    d["nex"] = d["nxt"] - d["coin"].map(d.groupby("coin")["nxt"].mean())
    d["n3ex"] = d["nxt3"] - d["coin"].map(d.groupby("coin")["nxt3"].mean())
    # graded: fall size (neg zr) predicts next-day rise
    d["fall"] = (-d["zr"]).clip(lower=0)
    dd = d[d.fall > 0].copy(); dd["p"] = dd["fall"]*dd["nex"]
    t, nd = clus_t(dd, "p")
    out["fall_size_next_day"] = pd.Series(dict(n=len(dd), corr=np.corrcoef(dd.fall, dd.nex)[0,1], t_dayclus=t, days=nd))
    d["fq"] = pd.qcut(d["zr"], 10, labels=False)
    def mt(x, col):
        t, nd = clus_t(x, col); return pd.Series(dict(n=len(x), mean=x[col].mean(), t_dayclus=t, days=nd))
    out["zr_decile_next_ex"] = d.groupby("fq").apply(lambda x: mt(x, "nex"))
    out["zr_bottom2_by_window"] = d[d.fq<=1].groupby("w")["nex"].agg(["count","mean"])
    out["zr_bottom2_by_coin"] = d[d.fq<=1].groupby("coin")["nex"].agg(["count","mean"])
    d["trend"] = pd.cut(d["tr60"], [-9,-0.1,0.1,99], labels=["fall","chop","rise"])
    out["zr_bottom2_by_trend"] = d[d.fq<=1].groupby("trend").apply(lambda x: mt(x, "nex"))
    out["zr_bottom2_next3"] = mt(d[d.fq<=1], "n3ex")
    d["cq"] = pd.cut(d["clpos"], [-0.01,0.2,0.4,0.6,0.8,1.01], labels=False)
    out["closepos_next_ex"] = d.groupby("cq").apply(lambda x: mt(x, "nex"))
    # close position controlling for return: within zr deciles 2-7 (moderate days)
    mid = d[(d.fq>=2)&(d.fq<=7)]
    out["closepos_mid_days"] = mid.groupby("cq").apply(lambda x: mt(x, "nex"))
    out["weekday_next_ex"] = d.groupby("wd").apply(lambda x: mt(x, "nex"))
    return out
