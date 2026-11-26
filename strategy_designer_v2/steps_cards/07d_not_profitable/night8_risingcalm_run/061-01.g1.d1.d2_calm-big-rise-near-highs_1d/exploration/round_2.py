def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=30).std()
            z = r1 / sd30
            hi20 = c.rolling(20, min_periods=20).max()
            dist = (hi20 / c - 1) * 100
            ret60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30, min_periods=30).std()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "z": z, "dist": dist, "ret60": ret60, "vol30": vol30,
                               "regime": b["regime"].values, "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "f5": c.shift(-5) / c - 1})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["inprof"] = A["regime"] == "unknown"
    A["choppy"] = A["ret60"].abs() <= 0.1
    g = A[A["pos"] % 5 == 0].dropna(subset=["f5"]).copy()
    drift = g.groupby("coin")["f5"].mean(); usual = g.groupby("coin")["f5"].std()
    g["ex"] = g["f5"] - g["coin"].map(drift)
    g["str"] = g["ex"] / g["coin"].map(usual)
    g["zb"] = pd.cut(g["z"], [-np.inf, 0, 0.5, 1, 1.5, np.inf])
    def tab(m):
        s = g[m]
        return s.groupby("zb", observed=True).agg(n=("ex", "size"), ex=("ex", lambda x: 100*x.mean()),
            t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan),
            strength=("str", "mean")).round(3)
    out["z_grade_inprof"] = tab(g["inprof"])
    out["z_grade_choppy_all"] = tab(g["choppy"])
    out["z_grade_rising"] = tab(g["ret60"] > 0.1)
    out["z_grade_falling"] = tab(g["ret60"] < -0.1)
    out["z_grade_all"] = tab(g["ret60"].notna())
    # z>1 split by near high within choppy
    res = []
    for nm, m in [("choppy z>1 at high", g["choppy"] & (g["z"] > 1) & (g["dist"] < 1)),
                  ("choppy z>1 below high", g["choppy"] & (g["z"] > 1) & (g["dist"] >= 1)),
                  ("choppy at high z<=1", g["choppy"] & (g["z"] <= 1) & (g["dist"] < 1)),
                  ("choppy z in 0-1", g["choppy"] & (g["z"] > 0) & (g["z"] <= 1)),
                  ("all z>1 at high", (g["z"] > 1) & (g["dist"] < 1)),
                  ("all z>1 below high", (g["z"] > 1) & (g["dist"] >= 1)),
                  ("all at high z<=1", (g["z"] <= 1) & (g["dist"] < 1))]:
        s = g[m]
        res.append({"group": nm, "n": len(s), "ex%": 100*s["ex"].mean(),
                    "t": s["ex"].mean()/(s["ex"].std()/np.sqrt(len(s))), "strength": s["str"].mean()})
    out["splits"] = pd.DataFrame(res).round(3)
    # book in position: z of entry bars, share of in-position bars by z bucket of last signal
    A["held"] = A["alloc"].abs() > 1e-6
    A["entry"] = A["held"] & ~A.groupby(["coin", "w"])["held"].shift(1, fill_value=False)
    e = A[A["entry"]]
    out["entry_z"] = e["z"].describe().round(3)
    out["entry_share_z_gt1"] = float((e["z"] > 1).mean())
    # book chain and drawdown
    d = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; d.append(x)
    D = pd.concat(d)
    bk = D.groupby(["w", "day"])["book_return"].mean().dropna()
    order = sorted(bk.index.get_level_values(0).unique(), key=lambda s: int(s[1:]))
    chain = pd.concat([bk.loc[o] for o in order])
    v = (1 + chain.values).cumprod()
    dd = v / np.maximum.accumulate(v) - 1
    out["deepest_fall"] = float(dd.min())
    wl = np.concatenate([[o]*len(bk.loc[o]) for o in order])
    out["fall_window_at_trough"] = str(wl[dd.argmin()])
    out["dd_by_window_min"] = pd.Series(dd, index=wl).groupby(level=0).min().round(4)
    # XMR
    out["by_coin_inprof_z_gt1"] = g[g["choppy"] & (g["z"] > 1)].groupby("coin")["ex"].agg(["size", "mean"]).round(4)
    return out
