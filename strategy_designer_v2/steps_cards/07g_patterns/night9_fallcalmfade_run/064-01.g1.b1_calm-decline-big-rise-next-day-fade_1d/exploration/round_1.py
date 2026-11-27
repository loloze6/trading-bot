def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            c = d["close"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20, min_periods=20).std()
            d["r1"] = r
            d["z"] = r / sd20.shift(0)
            d["sd20"] = sd20
            d["sd_rank"] = sd20.rank(pct=True)
            for h in [1, 2, 3, 5]:
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["ret5"] = c / c.shift(5) - 1
            d["ret20"] = c / c.shift(20) - 1
            d["rng"] = (d["high"] - d["low"]) / c
            d["clpos"] = (c - d["low"]) / (d["high"] - d["low"])
            d["inprof"] = d["regime"].isin(["mean_reversion", "unknown"])
            d["coin"] = coin; d["win"] = w; d["pos"] = np.arange(len(d))
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["yr"] = pd.to_datetime(d["timestamp"]).dt.year
            d["alloc"] = d["postRebalance_current_allocation"]
            d["bv"] = d["postRebalance_total_value"].astype(float)
            d["bret"] = d["bv"].shift(-1) / d["bv"] - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    drift = {h: A.groupby("coin")[f"f{h}"].apply(lambda s: s[A.loc[s.index, "pos"] % h == 0].mean()) for h in [1, 2, 3, 5]}
    for h in [1, 2, 3, 5]:
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(drift[h])
    out = {}
    def tab(df, key, h):
        g = df[df["pos"] % h == 0].dropna(subset=[key, f"u{h}"])
        res = g.groupby(key)[f"u{h}"].agg(["count", "mean", "std"])
        res["t"] = res["mean"] / (res["std"] / np.sqrt(res["count"]))
        return res.round(5)
    A["zb"] = pd.cut(A["z"], [-99, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 99])
    for h in [1, 2, 3, 5]:
        out[f"z bins all, u{h}"] = tab(A, "zb", h)
        out[f"z bins in profile, u{h}"] = tab(A[A["inprof"]], "zb", h)
    out["z bins out profile, u1"] = tab(A[~A["inprof"]], "zb", 1)
    out["z bins out profile, u3"] = tab(A[~A["inprof"]], "zb", 3)
    A["volq"] = pd.qcut(A["sd20"].rank(pct=True), 4, labels=False)
    out["vol quartile u1"] = tab(A, "volq", 1)
    out["weekday u1"] = tab(A, "wd", 1)
    A["r5b"] = pd.qcut(A["ret5"], 5, labels=False)
    out["ret5 quintile u3"] = tab(A, "r5b", 3)
    A["r20b"] = pd.qcut(A["ret20"], 5, labels=False)
    out["ret20 quintile u5"] = tab(A, "r20b", 5)
    A["cpb"] = pd.qcut(A["clpos"], 5, labels=False)
    out["close position quintile u1"] = tab(A, "cpb", 1)
    big = A[A["z"] >= 1]
    big = big.assign(cp2=pd.qcut(big["clpos"], 3, labels=False))
    out["big up days by close pos, u1"] = tab(big, "cp2", 1)
    out["regime counts"] = A["regime"].value_counts()
    out["profile share"] = float(A["inprof"].mean())
    # book big days
    b = A.dropna(subset=["bret"])
    b = b[b["alloc"].abs() > 0]
    out["book bar returns in pos: n, mean, t"] = pd.Series({"n": len(b), "mean": b["bret"].mean(), "t": b["bret"].mean()/(b["bret"].std()/np.sqrt(len(b)))})
    out["book by year"] = b.groupby("yr")["bret"].agg(["count", "mean"])
    out["book by window"] = b.groupby("win")["bret"].agg(["count", "mean"])
    return out
