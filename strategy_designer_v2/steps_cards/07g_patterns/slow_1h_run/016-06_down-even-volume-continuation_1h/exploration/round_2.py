import numpy as np, pandas as pd
from scipy import stats

def _ols_t(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 30: return (np.nan, np.nan, len(x))
    r = stats.linregress(x, y)
    return (r.slope, r.slope / r.stderr, len(x))

def explore(data):
    rows = []; hour_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            ts = pd.to_datetime(b["timestamp"])
            r1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            hour_rows.append(pd.DataFrame({"coin": coin, "year": ts.dt.year.values, "hour": ts.dt.hour.values,
                                           "wd": ts.dt.weekday.values, "r": r1}))
            n = len(c)
            for i in range(0, n, 72):
                if i < 72 or i + 72 >= n: continue
                rr = lr[i - 71:i + 1]
                sabs = np.nansum(np.abs(rr))
                vol = np.nanstd(rr)
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year,
                                 past=c[i] / c[i - 72] - 1, past24=c[i] / c[i - 24] - 1,
                                 fwd=c[i + 72] / c[i] - 1,
                                 eff=np.nansum(rr) / sabs if sabs > 0 else np.nan, vol=vol))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["z24"] = g["past24"] / (g["vol"] * np.sqrt(24))
    g["z72"] = g["past"] / (g["vol"] * np.sqrt(72))
    out = {}
    dn = g[g.past < 0]; up = g[g.past > 0]
    res = {}
    for key, sub in [("down", dn), ("up", up)]:
        for f in ["past", "past24", "z24", "z72", "eff"]:
            s, t, nn = _ols_t(sub[f].values, sub["ex"].values)
            res[(key, f)] = dict(slope=s, t=t, n=nn)
    # all bars z24
    s, t, nn = _ols_t(g["z24"].values, g["ex"].values); res[("all", "z24")] = dict(slope=s, t=t, n=nn)
    s, t, nn = _ols_t(g["past24"].values, g["ex"].values); res[("all", "past24")] = dict(slope=s, t=t, n=nn)
    out["slopes"] = pd.DataFrame(res).T
    out["down_past24_by_coin"] = pd.DataFrame({c: dict(zip(["slope", "t", "n"], _ols_t(s["past24"].values, s["ex"].values))) for c, s in dn.groupby("coin")}).T
    out["down_past24_by_year"] = pd.DataFrame({y: dict(zip(["slope", "t", "n"], _ols_t(s["past24"].values, s["ex"].values))) for y, s in dn.groupby("year")}).T
    out["up_eff_by_coin"] = pd.DataFrame({c: dict(zip(["slope", "t", "n"], _ols_t(s["eff"].values, s["ex"].values))) for c, s in up.groupby("coin")}).T
    out["up_eff_by_year"] = pd.DataFrame({y: dict(zip(["slope", "t", "n"], _ols_t(s["eff"].values, s["ex"].values))) for y, s in up.groupby("year")}).T
    dn = dn.copy()
    dn["q"] = dn.groupby("coin")["past24"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["down_ex_by_past24_quintile"] = dn.groupby("q")["ex"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    H = pd.concat(hour_rows)
    H["h2021"] = H["hour"].isin([20, 21])
    hh = H[H.h2021]
    out["h2021_t_by_coin"] = hh.groupby("coin")["r"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(s.count())])
    out["h2021_t_by_year"] = hh.groupby("year")["r"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(s.count())])
    out["h2021_minus_other_welch"] = float(stats.ttest_ind(hh["r"].dropna(), H[~H.h2021]["r"].dropna(), equal_var=False).statistic)
    fr = H[H.wd == 4]
    out["fri_t_by_coin"] = fr.groupby("coin")["r"].agg(["mean", lambda s: s.mean() / s.std() * np.sqrt(s.count())])
    out["fri_t_by_year"] = fr.groupby("year")["r"].agg(["mean", lambda s: s.mean() / s.std() * np.sqrt(s.count())])
    return out
