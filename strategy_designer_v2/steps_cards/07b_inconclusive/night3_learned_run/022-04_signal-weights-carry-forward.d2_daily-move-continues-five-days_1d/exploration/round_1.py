def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    def ols_t(x, y):
        x = np.asarray(x, float); y = np.asarray(y, float)
        m = ~(np.isnan(x) | np.isnan(y))
        x, y = x[m], y[m]
        if len(x) < 30 or np.std(x) == 0: return (np.nan, np.nan, len(x))
        r = stats.linregress(x, y)
        return (r.slope, r.slope / r.stderr, len(x))
    rows_by_h = {}
    for h in [1, 2, 3, 5, 10, 20]:
        recs = []
        for coin, wins in bars.items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].values.astype(float)
                f = b["forecast"].values.astype(float)
                ts = pd.to_datetime(b["timestamp"])
                r20 = pd.Series(c).pct_change(20).values
                r1 = pd.Series(c).pct_change(1)
                vol = r1.rolling(20).std().values
                vol120 = r1.rolling(120, min_periods=60).std().values
                for i in range(0, len(b) - h, h):
                    recs.append(dict(coin=coin, w=w, year=ts.iloc[i].year, f=f[i],
                                     fwd=c[i + h] / c[i] - 1, r20=r20[i],
                                     volrel=vol[i] / vol120[i] if vol120[i] > 0 else np.nan))
        d = pd.DataFrame(recs)
        d["fwd_dm"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
        rows_by_h[h] = d
    out = {}
    # by horizon
    hz = []
    for h, d in rows_by_h.items():
        s, t, n = ols_t(d["f"], d["fwd_dm"])
        hz.append(dict(h=h, slope=s, t=t, n=n))
    out["by_horizon"] = pd.DataFrame(hz)
    d = rows_by_h[5]
    def grp(col):
        res = []
        for k, g in d.groupby(col):
            s, t, n = ols_t(g["f"], g["fwd_dm"])
            res.append(dict(key=k, slope=s, t=t, n=n))
        return pd.DataFrame(res)
    out["by_coin"] = grp("coin")
    out["by_year"] = grp("year")
    d["side"] = np.sign(d["f"])
    out["by_side"] = grp("side")
    d["fq"] = pd.qcut(d["f"], 10, labels=False, duplicates="drop")
    out["decile_mean_fwd_dm"] = d.groupby("fq").agg(f=("f", "mean"), fwd_dm=("fwd_dm", "mean"), n=("f", "size"))
    d["trend_agree"] = np.sign(d["f"]) == np.sign(d["r20"])
    out["by_trend_agree"] = grp("trend_agree")
    d["r20_side"] = np.sign(d["r20"])
    out["by_r20_sign"] = grp("r20_side")
    d["volq"] = pd.qcut(d["volrel"], 3, labels=["lowvol", "midvol", "highvol"])
    out["by_volregime"] = grp("volq")
    # signed move in direction, by |f| tercile
    d["dirmove"] = np.sign(d["f"]) * d["fwd_dm"]
    d["absq"] = pd.qcut(d["f"].abs(), 4, labels=False, duplicates="drop")
    out["dirmove_by_absf_quartile"] = d.groupby("absq").agg(absf=("f", lambda x: x.abs().mean()),
        mean=("dirmove", "mean"), t=("dirmove", lambda x: x.mean() / x.std() * np.sqrt(len(x))), n=("dirmove", "size"))
    return out
