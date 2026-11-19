import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 72
    rows = []
    hr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            hr.append(pd.DataFrame({"coin": coin, "year": ts.dt.year.values, "hour": ts.dt.hour.values,
                                    "wd": ts.dt.weekday.values, "r_next": np.r_[r1[1:], np.nan]}))
            if n < 3 * H:
                continue
            for t in range(H, n - H, H):
                past = r1[t - H + 1:t + 1]
                pr = c[t] / c[t - H] - 1
                fr = c[t + H] / c[t] - 1
                fr24 = c[t + 24] / c[t] - 1
                eff = abs(np.nansum(past)) / np.nansum(np.abs(past))
                p24 = r1[t - 23:t + 1]
                eff24 = abs(np.nansum(p24)) / np.nansum(np.abs(p24))
                rows.append(dict(coin=coin, w=w, year=ts.iloc[t].year, pr=pr, fr=fr, fr24=fr24, eff=eff, eff24=eff24,
                                 vol=np.nanstd(past)))
    d = pd.DataFrame(rows).dropna()
    d["fr_x"] = d["fr"] - d.groupby("coin")["fr"].transform("mean")
    d["fr24_x"] = d["fr24"] - d.groupby("coin")["fr24"].transform("mean")
    d["eq"] = d.groupby("coin")["eff"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    d["up"] = (d["pr"] > 0).astype(int)
    out = {}
    def agg(g, col="fr_x"):
        a = g[col].agg(["mean", "count", "std"])
        return a
    a = d.groupby(["up", "eq"])["fr_x"].agg(["mean", "std", "count"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["eff_quint_by_sign"] = a[["mean", "count", "t"]]
    # slope of fr_x on eff per year, per coin
    def slope(g, x="eff", y="fr_x"):
        g = g.dropna(subset=[x, y])
        s = stats.linregress(g[x], g[y]); return pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(g)})
    out["eff_slope_by_year"] = d.groupby("year").apply(slope)
    out["eff_slope_by_coin"] = d.groupby("coin").apply(slope)
    out["eff_slope_up_down"] = d.groupby("up").apply(slope)
    out["eff_slope_controls"] = None
    X = np.c_[np.ones(len(d)), d["eff"], np.abs(d["pr"] / d["vol"]), d["pr"] / d["vol"], d["vol"]]
    y = d["fr_x"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ beta
    se = np.sqrt(np.diag(res @ res / (len(y) - 5) * np.linalg.inv(X.T @ X)))
    out["eff_slope_controls"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["c", "eff", "|z|", "z", "vol"])
    out["eff24_slope_fr24"] = slope(d, "eff24", "fr24_x")
    out["eff24_slope_fr72"] = slope(d, "eff24", "fr_x")
    h = pd.concat(hr).dropna()
    h["h2021"] = h["hour"].isin([20, 21]).astype(int)
    def tt(g):
        a = g["r_next"]; b = g.loc[g["h2021"] == 1, "r_next"]; o = g.loc[g["h2021"] == 0, "r_next"]
        return pd.Series({"mean_2021": b.mean(), "mean_other": o.mean(), "welch_t": stats.ttest_ind(b, o, equal_var=False).statistic, "n": len(b)})
    out["h2021_by_year"] = h.groupby("year").apply(tt)
    out["h2021_by_coin"] = h.groupby("coin").apply(tt)
    h["fri"] = (h["wd"] == 4).astype(int)
    def tf(g):
        b = g.loc[g["fri"] == 1, "r_next"]; o = g.loc[g["fri"] == 0, "r_next"]
        return pd.Series({"mean_fri": b.mean(), "mean_other": o.mean(), "welch_t": stats.ttest_ind(b, o, equal_var=False).statistic})
    out["fri_by_year"] = h.groupby("year").apply(tf)
    out["fri_by_coin"] = h.groupby("coin").apply(tf)
    return out
