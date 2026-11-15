def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        dr = [df["close"].pct_change().dropna() for df in wins.values()]
        mu = pd.concat(dr).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(df)
            dist = df["debug_info.components.below_ma.last_history_value"].values.astype(float)
            dist = np.where(np.abs(dist) > 2, dist / 100.0, dist)
            sma = c / (1 + dist)
            fc = df["forecast"].values
            al = df["postRebalance_current_allocation"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            sl = np.full(n, np.nan)
            sl[20:] = sma[20:] / sma[:-20] - 1
            r60 = np.full(n, np.nan)
            r60[60:] = c[60:] / c[:-60] - 1
            h = 10
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, yr=yr[i], dist=dist[i], fc=fc[i], al=al[i],
                                 ex=c[i + h] / c[i] - 1 - h * mu, sl=sl[i], r60=r60[i]))
    d = pd.DataFrame(rows)
    def summ(g):
        s = g["ex"].dropna()
        return pd.Series({"n": len(s), "mean_ex": s.mean(),
                          "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan,
                          "share_down": (s < 0).mean()})
    out = {}
    out["dist_scale"] = pd.Series({"dist_median_abs": np.nanmedian(np.abs(d["dist"])), "dist_min": np.nanmin(d["dist"])})
    b = d[d.fc < 0].copy()
    a = d[d.fc >= 0].copy()
    for name, x in [("below", b), ("above", a)]:
        x["sls"] = np.where(x["sl"].isna(), "na", np.where(x["sl"] < 0, "sma_falling", "sma_rising"))
        out[name + "_by_smaslope"] = x.groupby("sls").apply(summ)
        x["r60s"] = np.where(x["r60"].isna(), "na", np.where(x["r60"] < 0, "r60neg", "r60pos"))
        out[name + "_by_r60"] = x.groupby("r60s").apply(summ)
    bf = b[b.sl.notna()].copy()
    bf["slq"] = pd.qcut(bf["sl"], 4, labels=["fall_fast", "fall2", "q3", "rise_most"])
    out["below_by_slope_quart"] = bf.groupby("slq").apply(summ)
    out["below_falling_by_year"] = b[b.sl < 0].groupby("yr").apply(summ)
    out["below_rising_by_year"] = b[b.sl >= 0].groupby("yr").apply(summ)
    bf2 = bf[bf.sl < 0]
    if len(bf2) > 10:
        r = stats.linregress(bf2["sl"], bf2["ex"])
        out["below_falling_reg_ex_on_slope"] = pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(bf2)})
    # book: market vs timing
    bk = []
    for coin, wins in data["days"].items():
        dr = pd.concat([df["coin_return"] for df in wins.values()]).dropna()
        mu = dr.mean()
        for w, df in wins.items():
            bw = bars[coin][w].copy()
            bw["day"] = pd.to_datetime(bw["timestamp"]).dt.floor("D")
            pos = bw.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd = df.copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D") if not np.issubdtype(dd["day"].dtype, np.datetime64) else dd["day"].dt.floor("D")
            dd = dd.merge(pos.rename("pos").reset_index(), on="day", how="left")
            dd["mkt"] = dd["pos"] * mu
            bk.append(dd[["book_return", "mkt"]].dropna())
    bk = pd.concat(bk)
    out["book_parts"] = pd.Series({"book_mean": bk["book_return"].mean(), "market_part": bk["mkt"].mean(),
                                   "timing_part": bk["book_return"].mean() - bk["mkt"].mean()})
    return out
