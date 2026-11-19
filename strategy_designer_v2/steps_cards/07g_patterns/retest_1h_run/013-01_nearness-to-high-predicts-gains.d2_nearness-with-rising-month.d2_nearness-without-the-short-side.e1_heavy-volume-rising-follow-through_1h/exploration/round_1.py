import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 72
    rows = []
    hourly = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float); hi = b["high"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-H) / c - 1,
                "relvol": v.rolling(24).mean() / v.rolling(480).mean() - 1,
                "ret1d": c / c.shift(24) - 1,
                "ret7d": c / c.shift(168) - 1,
                "ret30d": c / c.shift(720) - 1,
                "dist_hi30": c / hi.rolling(720).max() - 1,
                "volratio": r1.rolling(24).std() / r1.rolling(480).std(),
                "fc": b["forecast"].astype(float),
                "trend": (b["regime"] == "trending").astype(int),
            })
            idx = np.arange(0, len(b), H)
            rows.append(f.iloc[idx])
            ts = pd.to_datetime(b["timestamp"])
            hourly.append(pd.DataFrame({"hour": ts.dt.hour, "wd": ts.dt.weekday, "r": r1, "nxt": r1.shift(-1),
                                        "absz": (r1 / r1.rolling(480).std())}))
    g = pd.concat(rows).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    feats = ["relvol", "ret1d", "ret7d", "ret30d", "dist_hi30", "volratio", "fc"]
    out = []
    for sub, m in [("all", g), ("trend", g[g.trend == 1]), ("nontrend", g[g.trend == 0])]:
        for x in feats:
            d = m[[x, "ex"]].dropna()
            if len(d) < 50: continue
            # demean feature per coin? use raw
            rr = stats.pearsonr(d[x], d["ex"]); sp = stats.spearmanr(d[x], d["ex"])
            n = len(d); tp = rr[0] * np.sqrt((n - 2) / (1 - rr[0] ** 2)); ts_ = sp[0] * np.sqrt((n - 2) / (1 - sp[0] ** 2))
            out.append([sub, x, n, round(rr[0], 4), round(tp, 2), round(sp[0], 4), round(ts_, 2)])
    corr = pd.DataFrame(out, columns=["set", "feat", "n", "pearson", "t_p", "spearman", "t_s"])
    # quintiles of key features, all bars
    q = {}
    for x in ["dist_hi30", "ret7d", "volratio", "ret1d"]:
        d = g[[x, "ex"]].dropna().copy()
        d["q"] = d.groupby(g.loc[d.index, "coin"] if False else np.zeros(len(d)))[x].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        q[x] = d.groupby("q")["ex"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    qt = pd.concat(q, axis=1)
    hh = pd.concat(hourly).dropna()
    byhour = hh.groupby("hour")["r"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # reversal after big hourly moves
    hh["zb"] = pd.cut(hh["absz"], [-np.inf, -3, -1.5, 1.5, 3, np.inf])
    rev = hh.groupby("zb", observed=True)["nxt"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # book daily by weekday
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin
            d["nxt_book"] = d["book_return"].shift(-1); d["nxt_coin"] = d["coin_return"].shift(-1)
            dd.append(d)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    wd = D.groupby("wd")[["book_return", "coin_return"]].mean()
    D["cz"] = pd.qcut(D["coin_return"], 5, labels=False)
    afterbig = D.groupby("cz")[["nxt_coin", "nxt_book"]].agg(["mean", "count"])
    return {"corr": corr, "quintiles_all": qt.round(5), "byhour": byhour.round(6),
            "rev_after_hour_z": rev.round(6), "weekday": wd.round(5), "next_day_by_coin_ret_q": afterbig.round(5)}
