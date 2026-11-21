def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 72
    rows = []
    for coin, wins in bars.items():
        # coin mean returns per horizon over all windows
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            f = df["forecast"].values.astype(float)
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            # raw efficiency and 3-day return recomputed
            dif = np.abs(np.diff(c, prepend=np.nan))
            s = pd.Series(dif).rolling(72).sum().values
            r72 = np.full(n, np.nan); r72[72:] = c[72:] / c[:-72] - 1
            er = np.full(n, np.nan); er[72:] = np.abs(c[72:] - c[:-72]) / s[72:]
            for i in range(0, n, H):
                rec = {"coin": coin, "w": w, "year": ts.iloc[i].year, "f": f[i], "r72": r72[i], "er": er[i]}
                for h in (24, 72, 144, 240):
                    rec["fwd%d" % h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    for h in (24, 72, 144, 240):
        d["ex%d" % h] = d["fwd%d" % h] - d.groupby("coin")["fwd%d" % h].transform("mean")
    pos = d[d.f > 0].copy()
    pos["m"] = pos.f / 10 * pos.ex72

    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["by_coin"] = pos.groupby("coin")["m"].apply(tt).unstack()
    out["by_year"] = pos.groupby("year")["m"].apply(tt).unstack()
    pos["fq"] = pd.qcut(pos.f, 5, labels=False, duplicates="drop")
    out["ex72_by_forecast_q"] = pos.groupby("fq").agg(n=("ex72", "count"), fmean=("f", "mean"), ermean=("er", "mean"), ex72=("ex72", "mean"), r72=("r72", "mean"))
    pos["rq"] = pd.qcut(pos.r72, 5, labels=False, duplicates="drop")
    out["ex72_by_r72_q"] = pos.groupby("rq").agg(n=("ex72", "count"), r72=("r72", "mean"), er=("er", "mean"), ex72=("ex72", "mean"), ex144=("ex144", "mean"))
    hz = {}
    for h in (24, 72, 144, 240):
        hz["ex%d" % h] = tt(pos.f / 10 * pos["ex%d" % h])
    out["by_horizon_main"] = pd.DataFrame(hz).T
    # raw er among rises: double sort er within r72 terciles
    pos["rt"] = pd.qcut(pos.r72, 3, labels=False)
    pos["et"] = pos.groupby("rt")["er"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["ex72_r72tercile_x_ertercile"] = pos.groupby(["rt", "et"])["ex72"].mean().unstack()
    # falls: er on down moves
    neg = d[d.r72 < 0].copy()
    neg["eq"] = pd.qcut(neg.er, 5, labels=False)
    out["falls_ex72_by_er_q"] = neg.groupby("eq").agg(n=("ex72", "count"), er=("er", "mean"), r72=("r72", "mean"), ex72=("ex72", "mean"), ex144=("ex144", "mean"))
    # raw er on rises, correlation
    out["corr_rises"] = pd.Series({"spear_er_ex72": stats.spearmanr(pos.er, pos.ex72, nan_policy="omit")[0],
                                    "spear_f_ex72": stats.spearmanr(pos.f, pos.ex72, nan_policy="omit")[0],
                                    "spear_r72_ex72": stats.spearmanr(pos.r72, pos.ex72, nan_policy="omit")[0]})
    return out
