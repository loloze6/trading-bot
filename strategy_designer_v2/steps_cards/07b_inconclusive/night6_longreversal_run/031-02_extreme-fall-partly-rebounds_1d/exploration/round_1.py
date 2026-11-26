def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            ts = pd.to_datetime(df["timestamp"])
            for h in [10, 20, 30, 45, 60]:
                for p in range(0, n, h):
                    if p + h >= n:
                        continue
                    r = c[p + h] / c[p] - 1
                    # past 30-day return inside window if available
                    past30 = c[p] / c[p - 30] - 1 if p >= 30 else np.nan
                    rows.append(dict(coin=coin, win=w, h=h, pos=p, ret=r,
                                     regime=df["regime"].iloc[p],
                                     fc=df["forecast"].iloc[p],
                                     year=ts.iloc[p].year,
                                     day=ts.iloc[p].normalize(),
                                     past30=past30))
    R = pd.DataFrame(rows)
    R["mu"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["mu"]
    R["inreg"] = (R["fc"] > 0)

    def tclust(d):
        g = d.groupby("day")["ex"].sum()
        G = len(g)
        if G < 3: return np.nan
        m = d["ex"].sum() / len(d)
        se = np.sqrt((g - m * d.groupby("day").size()).pow(2).sum() * G / (G - 1)) / len(d)
        return m / se if se > 0 else np.nan

    out = {}
    hz = []
    for h, d in R.groupby("h"):
        s = d[d.inreg]
        o = d[~d.inreg]
        hz.append(dict(h=h, n_in=len(s), days=s.day.nunique(), mean_in=s.ex.mean(), t_in=tclust(s),
                       mean_out=o.ex.mean(), n_out=len(o), raw_in=s.ret.mean()))
    out["by_horizon_inregime"] = pd.DataFrame(hz)

    d30 = R[(R.h == 30) & R.inreg].copy()
    out["h30_by_coin"] = d30.groupby("coin")["ex"].agg(["count", "mean", "median"])
    out["h30_by_year"] = d30.groupby("year")["ex"].agg(["count", "mean", "median"])
    d30["fq"] = pd.qcut(d30["fc"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["h30_by_fc_tercile"] = d30.groupby("fq")[["ex", "fc"]].agg(["count", "mean"])
    d30["p30sign"] = np.where(d30.past30.isna(), "na", np.where(d30.past30 > 0, "past30_up", "past30_down"))
    out["h30_by_past30"] = d30.groupby("p30sign")["ex"].agg(["count", "mean", "median"])
    out["h30_by_pos"] = d30.groupby("pos")["ex"].agg(["count", "mean"])
    out["h30_hit"] = float((d30.ex > 0).mean())
    # all bars in regime (overlapping, descriptive): forward 30 from every in-regime bar
    allr = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            for p in range(len(df) - 30):
                if f[p] > 0:
                    allr.append(dict(coin=coin, r=c[p + 30] / c[p] - 1, fc=f[p], win=w))
    A = pd.DataFrame(allr)
    mu30 = R[R.h == 30].groupby("coin")["ret"].mean()
    A["ex"] = A["r"] - A["coin"].map(mu30)
    out["allbars_inreg_30_by_coin"] = A.groupby("coin")["ex"].agg(["count", "mean"])
    out["allbars_inreg_windows_coin"] = A.groupby("coin")["win"].nunique()
    A["fq"] = pd.qcut(A["fc"].rank(method="first"), 4, labels=False)
    out["allbars_inreg_by_fc_quartile"] = A.groupby("fq")[["ex", "fc"]].mean()
    return out
