def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            z = r1 / sd30
            r5past = c / c.shift(5) - 1
            tr = c / c.shift(60) - 1
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            fwd = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            n = len(b)
            for i in range(0, n, 5):
                rows.append(dict(coin=coin, win=w, z=z[i], r1=r1[i], fwd=fwd[i], fwd1=fwd1[i],
                                 calm=b["regime"].iloc[i] != "chop", tr=tr[i], zp5=r5past[i] / (sd30[i] * np.sqrt(5)) if sd30[i] > 0 else np.nan,
                                 clpos=clpos[i], rng_sd=rng[i] / sd30[i] if sd30[i] > 0 else np.nan,
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                                 year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 day=pd.Timestamp(b["timestamp"].iloc[i]).normalize()))
    d = pd.DataFrame(rows).dropna(subset=["fwd", "z"])
    drift = d.groupby("coin")["fwd"].mean()
    d["ex"] = d["fwd"] - d["coin"].map(drift)
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(), t=g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    d["zbin"] = pd.cut(d["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    out = {}
    out["z_by_calm"] = d.groupby(["calm", "zbin"]).apply(summ).unstack(0)
    d["tbin"] = pd.cut(d["tr"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    out["calm_z_up_by_trend"] = d[d.calm & (d.z > 0)].groupby(["tbin", pd.cut(d["z"], [0, 1, 2, 99])]).apply(summ)
    d["p5bin"] = pd.cut(d["zp5"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    out["past5_by_calm"] = d.groupby(["calm", "p5bin"]).apply(summ).unstack(0)
    d["rbin"] = pd.qcut(d["rng_sd"], 4)
    out["range_by_calm"] = d.groupby(["calm", "rbin"]).apply(summ).unstack(0)
    d["cbin"] = pd.cut(d["clpos"], [0, 0.2, 0.5, 0.8, 1.0001])
    out["closepos_by_calm"] = d.groupby(["calm", "cbin"]).apply(summ).unstack(0)
    out["calm_bigup_by_year"] = d[d.calm & (d.z > 1)].groupby("year").apply(summ)
    out["by_coin_calm_zgt1"] = d[d.calm & (d.z > 1)].groupby("coin").apply(summ)
    # book daily by weekday
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; dd.append(x)
    dd = pd.concat(dd).dropna(subset=["book_return"])
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    out["book_by_weekday"] = dd.groupby("wd")["book_return"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    out["coin_by_weekday"] = dd.groupby("wd")["coin_return"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    return out
