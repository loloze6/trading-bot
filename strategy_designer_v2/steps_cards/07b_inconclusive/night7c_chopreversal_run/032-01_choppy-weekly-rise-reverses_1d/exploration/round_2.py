def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            ret7 = c / c.shift(7) - 1
            net30 = (c - c.shift(30)).abs()
            path30 = c.diff().abs().rolling(30, min_periods=20).sum()
            er = net30 / path30
            scaled = ret7 / (sd30 * np.sqrt(7))
            n = len(b)
            h = 7
            fwd = c.shift(-h) / c - 1
            for i in range(0, n, h):
                if i + h >= n: continue
                rows.append(dict(coin=coin, w=w, day=str(b["timestamp"].iloc[i])[:10],
                                 regime=b["regime"].iloc[i], fc=b["forecast"].iloc[i],
                                 scaled=scaled.iloc[i], er=er.iloc[i], fwd=fwd.iloc[i],
                                 sd30=sd30.iloc[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby("coin")["fwd"].transform("mean")
    d["unus"] = d["fwd"] - d["drift"]
    d["usual"] = d.groupby("coin")["fwd"].transform("std")
    d["mr"] = d["regime"] == "mean_reversion"
    d["year"] = d["day"].str[:4]
    d = d.dropna(subset=["scaled", "unus", "sd30"])
    d["vq"] = d.groupby("coin")["sd30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))

    def clus_t(g, col):
        s = g.groupby("day")[col].sum()
        G = len(s); m = g[col].mean(); N = len(g)
        dev = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / N
        return m / se if se > 0 else np.nan

    def summ(g):
        if len(g) < 8: return pd.Series(dict(n=len(g)))
        g = g.copy()
        g["sgn_unus"] = np.sign(g["scaled"]) * g["unus"]
        g["sgn_str"] = g["sgn_unus"] / g["usual"]
        return pd.Series(dict(n=len(g), days=g["day"].nunique(),
                              cont_mean=g["sgn_unus"].mean(), cont_t=clus_t(g, "sgn_unus"),
                              strength=g["sgn_str"].mean(),
                              rho=stats.spearmanr(g["scaled"], g["unus"])[0]))
    out = {}
    out["all"] = summ(d)
    out["by_vq"] = d.groupby("vq").apply(summ)
    out["by_mr_vq"] = d.groupby(["mr", "vq"]).apply(summ)
    out["vq2_by_year"] = d[d.vq == 2].groupby("year").apply(summ)
    out["vq2_by_coin"] = d[d.vq == 2].groupby("coin").apply(summ)
    out["vq01_by_year"] = d[d.vq < 2].groupby("year").apply(summ)
    out["vq01_by_coin"] = d[d.vq < 2].groupby("coin").apply(summ)
    out["mr_by_year"] = d[d.mr].groupby("year").apply(summ)
    out["mr_by_coin"] = d[d.mr].groupby("coin").apply(summ)
    # large moves only, abs scaled > 1
    big = d[d.scaled.abs() > 1]
    out["big_by_mr_vq"] = big.groupby(["mr", "vq"]).apply(summ)
    return out
