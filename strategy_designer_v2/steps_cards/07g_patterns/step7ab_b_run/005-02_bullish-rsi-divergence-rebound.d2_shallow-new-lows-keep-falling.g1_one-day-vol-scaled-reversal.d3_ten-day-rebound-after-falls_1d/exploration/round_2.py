def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book: drift vs timing
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    D = pd.concat(dd, ignore_index=True)
    # position held at day end from bars
    pos = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            p = pd.DataFrame({"coin": coin, "win": w,
                              "pos": b["postRebalance_current_allocation"].astype(float),
                              "c": b["close"].astype(float)})
            p["next"] = p["c"].shift(-1) / p["c"] - 1
            pos.append(p)
    P = pd.concat(pos, ignore_index=True).dropna(subset=["next"])
    cm = P.groupby("coin")["next"].mean()
    P["drift_gain"] = P["pos"] * P["coin"].map(cm)
    P["gain"] = P["pos"] * P["next"]
    out["book_drift_vs_timing"] = P.groupby("coin")[["pos", "gain", "drift_gain"]].mean().assign(
        timing=lambda x: x["gain"] - x["drift_gain"], share_in=P.groupby("coin")["pos"].apply(lambda s: (s > 0.01).mean()))
    # multi-horizon reaction to big moves both signs and longer momentum, horizons 5,10,20
    res = []
    for H in [5, 10, 20]:
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                c = pd.Series(b.sort_values("timestamp")["close"].astype(float).values)
                r1 = c.pct_change(); v = r1.rolling(20, min_periods=10).std()
                df = pd.DataFrame({"coin": coin, "z1": r1 / v,
                                   "z5": c.pct_change(5) / (v * np.sqrt(5)),
                                   "r60": c.pct_change(60),
                                   "fwd": c.shift(-H) / c - 1})
                rows.append(df.iloc[::H].dropna())
        g = pd.concat(rows, ignore_index=True)
        g["ex"] = g["fwd"] - g["coin"].map(g.groupby("coin")["fwd"].mean())
        for col in ["z1", "z5", "r60"]:
            s = stats.linregress(g[col], g["ex"])
            hi = g[g[col] >= g[col].quantile(0.8)]["ex"]; lo = g[g[col] <= g[col].quantile(0.2)]["ex"]
            tw = stats.ttest_ind(hi, lo, equal_var=False)
            res.append({"H": H, "x": col, "n": len(g), "slope_t": s.slope / s.stderr,
                        "top20": hi.mean(), "bot20": lo.mean(), "top_minus_bot_t": tw.statistic})
    out["horizon_grid"] = pd.DataFrame(res)
    # book worst/best days: coin's prior 5d return
    D = D.dropna(subset=["book_return"])
    D["q"] = pd.qcut(D["book_return"].rank(method="first"), 10, labels=False)
    out["book_deciles"] = D.groupby("q")[["book_return", "coin_return"]].mean()
    return out
