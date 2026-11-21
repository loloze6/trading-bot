import pandas as pd, numpy as np
from scipy import stats

def _grid(data, H):
    rows = []; usual = {}
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); r = c.pct_change()
            f = pd.DataFrame({"coin": coin, "win": w,
                "r28": c / c.shift(28) - 1, "r5": c / c.shift(5) - 1, "r1": r,
                "r10": c / c.shift(10) - 1,
                "vol20": r.rolling(20).std(),
                "fc": b["forecast"].astype(float),
                "fwd": c.shift(-H) / c - 1})
            gr = f.iloc[::H]; gr = gr[gr["fwd"].notna()]
            rows.append(gr); g.append(gr["fwd"])
        g = pd.concat(g); usual[coin] = (g.mean(), g.std())
    d = pd.concat(rows, ignore_index=True)
    d["ex"] = d["fwd"] - d["coin"].map(lambda k: usual[k][0])
    d["st"] = d["ex"] / d["coin"].map(lambda k: usual[k][1])
    return d

def _t(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = ~(np.isnan(x) | np.isnan(y)); x, y = x[m], y[m]
    if len(x) < 10: return np.nan, len(x)
    s = stats.linregress(x, y); return s.slope / s.stderr, len(x)

def explore(data):
    out = {}
    # 1) 5-day momentum: robustness by horizon, coin, half of windows
    res = []
    for H in [3, 5, 10]:
        d = _grid(data, H)
        d["z5"] = d.groupby("coin")["r5"].transform(lambda s: (s - s.mean()) / s.std())
        d["z1"] = d.groupby("coin")["r1"].transform(lambda s: (s - s.mean()) / s.std())
        t5, n5 = _t(d["z5"], d["st"]); t1, n1 = _t(d["z1"], d["st"])
        wn = d["win"].str[1:].astype(int)
        te, _ = _t(d.loc[wn <= 12, "z5"], d.loc[wn <= 12, "st"])
        tl, _ = _t(d.loc[wn > 12, "z5"], d.loc[wn > 12, "st"])
        # r5 net of r28 (partial)
        x = d.dropna(subset=["r5", "r28", "st"])
        X = np.column_stack([np.ones(len(x)), x.groupby("coin")["r5"].transform(lambda s: (s-s.mean())/s.std()),
                             x.groupby("coin")["r28"].transform(lambda s: (s-s.mean())/s.std())])
        beta, *_ = np.linalg.lstsq(X, x["st"].values, rcond=None)
        resid = x["st"].values - X @ beta
        cov = np.linalg.inv(X.T @ X) * resid.var(ddof=3)
        res.append({"H": H, "n": n5, "t_r5": t5, "t_r1": t1, "t_r5_w1_12": te, "t_r5_w13_24": tl,
                    "t_r5_given_r28": beta[1] / np.sqrt(cov[1, 1]), "t_r28_given_r5": beta[2] / np.sqrt(cov[2, 2])})
    out["r5_r1_by_horizon"] = pd.DataFrame(res).round(3)
    d = _grid(data, 10)
    d["z5"] = d.groupby("coin")["r5"].transform(lambda s: (s - s.mean()) / s.std())
    out["r5_t_by_coin_H10"] = d.groupby("coin").apply(lambda x: pd.Series(dict(zip(["t", "n"], _t(x["z5"], x["st"]))))).round(3)
    # 2) rise side: r28 graded within vol terciles
    rs = d[d["r28"] > 0].dropna(subset=["vol20"]).copy()
    rs["vq"] = rs.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    rs["z"] = rs.groupby("coin")["r28"].transform(lambda s: (s - s.mean()) / s.std())
    out["rise_r28_slope_by_vol"] = rs.groupby("vq").apply(lambda x: pd.Series(dict(zip(["t", "n"], _t(x["z"], x["st"]))))).round(3)
    # vol-scaled rise: r28 / vol20
    d["rr"] = d["r28"] / (d["vol20"] * np.sqrt(28))
    pos = d[d["r28"] > 0]
    out["rise_side_raw_vs_volscaled_t"] = pd.Series({"raw_t": _t(pos.groupby("coin")["r28"].transform(lambda s:(s-s.mean())/s.std()), pos["st"])[0],
                                                     "volscaled_t": _t(pos.groupby("coin")["rr"].transform(lambda s:(s-s.mean())/s.std()), pos["st"])[0],
                                                     "n": len(pos)}).round(3)
    # 3) trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; tr.append(t)
    tr = pd.concat(tr, ignore_index=True)
    tr["fq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 4, labels=False)
    tr["days"] = tr["duration_minutes"] / 1440
    out["trades_by_entry_forecast_q"] = tr.groupby("fq").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), med_net=("net_profit_loss_percent", "median"),
        win=("net_profit_loss_percent", lambda s: (s > 0).mean()), days=("days", "mean"), fc=("entry_forecast", "mean")).round(3)
    # 4) book days: share of gain from largest days; what precedes worst days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy().reset_index(drop=True); x["coin"] = coin
            x["prev5"] = (1 + x["coin_return"]).rolling(5).apply(np.prod, raw=True).shift(1) - 1
            x["next5"] = (1 + x["coin_return"]).rolling(5).apply(np.prod, raw=True).shift(-5) - 1
            dd.append(x)
    dd = pd.concat(dd, ignore_index=True).dropna(subset=["book_return"])
    act = dd[dd["book_return"] != 0]
    q = act["book_return"].quantile([0.05, 0.95])
    lo = act[act["book_return"] <= q.iloc[0]]; hi = act[act["book_return"] >= q.iloc[1]]
    out["book_tails"] = pd.DataFrame({"n": [len(lo), len(hi)], "mean_book": [lo["book_return"].mean(), hi["book_return"].mean()],
        "prev5_coin": [lo["prev5"].mean(), hi["prev5"].mean()], "next5_coin": [lo["next5"].mean(), hi["next5"].mean()],
        "share_of_total_gain": [lo["book_return"].sum() / dd["book_return"].sum(), hi["book_return"].sum() / dd["book_return"].sum()]},
        index=["worst5pct", "best5pct"]).round(4)
    # 5) large-day reversal, daily bars, next 3 days, non-overlapping grid of 3
    d3 = _grid(data, 3)
    d3["az"] = d3.groupby("coin")["r1"].transform(lambda s: (s - s.mean()) / s.std())
    big = d3[d3["az"].abs() > 1.5]
    out["after_large_day_3d"] = pd.Series({"n_up": (big["az"] > 0).sum(), "mean_st_up": big.loc[big["az"] > 0, "st"].mean(),
        "n_dn": (big["az"] < 0).sum(), "mean_st_dn": big.loc[big["az"] < 0, "st"].mean(),
        "t_slope_big": _t(big["az"], big["st"])[0]}).round(4)
    return out
