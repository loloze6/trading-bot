def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    H = 84
    out = {}
    # per coin drift
    rows_case = []; rows_grid = []; rows_short = []; hourly = []
    for coin, wins in bars.items():
        nonov = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            nonov += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(nonov); sd = np.std(nonov)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; hi = df["high"]; lo = df["low"]
            r6 = c / c.shift(6) - 1
            ma = r6.abs().rolling(180, min_periods=60).mean()
            rng = (hi.rolling(6).max() - lo.rolling(6).min()) / c.shift(6)
            mr = rng.rolling(180, min_periods=60).mean()
            panic = np.where(r6 < 0, (-r6 / ma) * (rng / mr), 0.0)
            panic = pd.Series(panic)
            fwd = c.shift(-H) / c - 1
            r1 = c.pct_change()
            vol42 = r1.rolling(42).std(); vol180 = r1.rolling(180).std()
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)),
                              "panic0": panic, "panic6": panic.shift(6), "r6": r6, "r6z": r6 / ma,
                              "r42": c / c.shift(42) - 1, "r180": c / c.shift(180) - 1,
                              "volratio": vol42 / vol180, "vol42": vol42,
                              "ex": (fwd - drift), "exs": (fwd - drift) / sd,
                              "fc": df["forecast"]})
            d["cell"] = d["pos"] // H
            rows_case.append(d)
            g = d[d["pos"] % H == 0]
            rows_grid.append(g)
            # short horizon: next 6 bars after r1 shocks, grid 6
            f6 = c.shift(-6) / c - 1
            s = pd.DataFrame({"coin": coin, "r1z": r1 / r1.rolling(180).std(), "f6": f6, "pos": np.arange(len(df))})
            rows_short.append(s[s["pos"] % 6 == 0])
            hourly.append(pd.DataFrame({"hour": ts.dt.hour, "wd": ts.dt.weekday, "r": r1.shift(-1)}))
    A = pd.concat(rows_case); G = pd.concat(rows_grid).dropna(subset=["ex"])
    def reg(df, x, y="ex"):
        df = df.dropna(subset=[x, y])
        if len(df) < 10: return [len(df), np.nan, np.nan]
        r = stats.linregress(df[x], df[y])
        return [len(df), r.slope, r.slope / r.stderr]
    # panic at t (immediate), graded
    for lab, col in [("panic0", "panic0"), ("panic6", "panic6")]:
        sub = A[A[col] >= 3].dropna(subset=["ex"]).groupby(["coin", "w", "cell"]).head(1).copy()
        sub["lp"] = np.log(sub[col])
        q = pd.qcut(sub[col], 4, labels=False)
        tab = sub.groupby(q)["ex"].agg(["count", "mean"])
        tab["t"] = sub.groupby(q)["ex"].apply(lambda v: v.mean() / (v.std() / np.sqrt(len(v))))
        out[lab + " quartile excess"] = tab
        out[lab + " reg ex on log panic (n,slope,t)"] = str(reg(sub, "lp"))
        out[lab + " mean ex all, t"] = str([len(sub), sub["ex"].mean(), sub["ex"].mean() / (sub["ex"].std() / np.sqrt(len(sub)))])
    # grid regressions all bars
    res = {}
    for x in ["r6z", "r42", "r180", "volratio", "vol42"]:
        res[x] = reg(G, x, "exs")
    out["grid all bars: exs on predictor (n,slope,t)"] = pd.DataFrame(res, index=["n", "slope", "t"]).T
    # quintiles of r42 and volratio
    for x in ["r42", "r180", "volratio"]:
        gg = G.dropna(subset=[x]); q = pd.qcut(gg[x], 5, labels=False)
        t = gg.groupby(q)["ex"].agg(["count", "mean", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        out["grid quintile " + x] = t[["count", "mean", "t"]]
    S = pd.concat(rows_short).dropna()
    q = pd.qcut(S["r1z"], 10, labels=False)
    t = S.groupby(q)["f6"].agg(["count", "mean", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["next 24h after 4h shock decile"] = t[["count", "mean", "t"]]
    Hh = pd.concat(hourly).dropna()
    t = Hh.groupby("hour")["r"].agg(["count", "mean", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["4h bar return by start hour"] = t[["count", "mean", "t"]]
    D = pd.concat([df.assign(coin=c, w=w) for c, ws in days.items() for w, df in ws.items()])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    t = D.groupby("wd")["coin_return"].agg(["count", "mean", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["coin daily return by weekday"] = t[["count", "mean", "t"]]
    T = pd.concat([df.assign(coin=c) for c, ws in trades.items() for w, df in ws.items()])
    T["fsign"] = np.sign(T["entry_forecast"])
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
