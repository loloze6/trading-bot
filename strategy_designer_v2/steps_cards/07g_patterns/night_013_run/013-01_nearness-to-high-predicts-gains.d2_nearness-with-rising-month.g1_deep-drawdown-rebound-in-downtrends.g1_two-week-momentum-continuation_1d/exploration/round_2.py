import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []; dl = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(b)
            s1 = pd.Series(cl)
            r1 = s1.pct_change().values
            ret14 = s1.pct_change(14).values
            ret60 = s1.pct_change(60).values
            hi30 = b["high"].rolling(30).max().values
            prevhi = b["high"].shift(1).rolling(30).max().values
            v = b["volume"].values
            vrel = v / pd.Series(v).rolling(20).mean().values
            vol20 = pd.Series(r1).rolling(20).std().values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - 7, 7):
                rows.append(dict(coin=c, win=w, f=b["forecast"].iloc[i], ret14=ret14[i], ret60=ret60[i],
                                 near=cl[i]/hi30[i]-1, brk=float(cl[i] > prevhi[i]) if not np.isnan(prevhi[i]) else np.nan,
                                 vrel=vrel[i], vol=vol20[i], yr=ts.iloc[i].year, fwd=cl[i+7]/cl[i]-1))
            a = b["postRebalance_current_allocation"].values[:-1]
            r = s1.pct_change().shift(-1).values[:-1]
            dl.append(pd.DataFrame(dict(coin=c, win=w, a=a, r=r, wd=ts.dt.dayofweek.values[:-1],
                                        yr=ts.dt.year.values[:-1], vol=vol20[:-1])))
    s = pd.DataFrame(rows)
    s["dm"] = s["fwd"] - s.groupby("coin")["fwd"].transform("mean")
    dl = pd.concat(dl); dl["g"] = dl["a"]*dl["r"]
    out = {}
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    # deep-fall rebound: bottom decile ret14 by coin and by 60d trend sign
    s["d10"] = pd.qcut(s["ret14"], 10, labels=False)
    out["bottom ret14 decile by coin"] = s[s.d10==0].groupby("coin")["dm"].apply(tt).unstack()
    out["bottom ret14 decile by ret60 sign"] = s[s.d10==0].groupby(np.sign(s["ret60"]))["dm"].apply(tt).unstack()
    out["deciles 1-2 by coin"] = s[s.d10.isin([1,2])].groupby("coin")["dm"].apply(tt).unstack()
    # slope of dm on ret14 inside ret60 sign
    def sl(d, x="ret14"):
        d = d.dropna(subset=[x,"dm"]); r = stats.linregress(d[x], d["dm"])
        return pd.Series({"n": len(d), "slope": r.slope, "t": r.slope/r.stderr})
    out["ret14 slope by ret60 sign"] = s.groupby(np.sign(s["ret60"])).apply(sl)
    # nearness beyond ret14: residual
    d = s.dropna(subset=["near","ret14","dm"])
    X = np.column_stack([np.ones(len(d)), d["ret14"], d["near"]])
    beta, *_ = np.linalg.lstsq(X, d["dm"], rcond=None)
    res = d["dm"] - X@beta; cov = np.linalg.inv(X.T@X)*(res.var()*len(d)/(len(d)-3))
    out["joint ret14+near t"] = pd.Series({"b_ret14": beta[1], "t_ret14": beta[1]/np.sqrt(cov[1,1]), "b_near": beta[2], "t_near": beta[2]/np.sqrt(cov[2,2]), "n": len(d)})
    out["breakout vs not"] = s.groupby("brk")["dm"].apply(tt).unstack()
    s["vq"] = pd.qcut(s["vrel"], 5, labels=False)
    out["breakout by volume quintile"] = s[s.brk==1].groupby("vq")["dm"].apply(tt).unstack()
    out["low volume quintile by coin"] = s[s.vq==0].groupby("coin")["dm"].apply(tt).unstack()
    # book side asymmetry: gain minus market drift
    mu = dl.groupby("coin")["r"].transform("mean")
    dl["timing"] = dl["a"]*(dl["r"]-mu)
    dl["side"] = np.sign(dl["a"])
    out["timing by side"] = dl.groupby("side")["timing"].apply(tt).unstack()
    # weekday: per coin t for Thu+Fri minus others, and by year halves
    dl["tf"] = dl["wd"].isin([3,4])
    def wdiff(x):
        a = x.loc[x.tf,"r"].dropna(); b = x.loc[~x.tf,"r"].dropna()
        return pd.Series({"diff": a.mean()-b.mean(), "t": stats.ttest_ind(a,b,equal_var=False).statistic})
    out["Thu-Fri minus other days by coin"] = dl.groupby("coin").apply(wdiff)
    out["Thu-Fri minus other days by year"] = dl.groupby("yr").apply(wdiff)
    return out
