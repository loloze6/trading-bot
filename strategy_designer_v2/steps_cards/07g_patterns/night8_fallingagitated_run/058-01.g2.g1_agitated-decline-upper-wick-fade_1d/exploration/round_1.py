def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            allr.append(b["close"].pct_change())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            vol = r1.rolling(30).std()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "reg": b["regime"].astype(str),
                "r1s": r1 / vol,
                "uw": (b["high"] - c) / c / vol,
                "lw": (c - b["low"]) / c / vol,
                "rng": (b["high"] - b["low"]) / c / vol,
                "r3s": (c / c.shift(3) - 1) / (vol * np.sqrt(3)),
                "r5s": (c / c.shift(5) - 1) / (vol * np.sqrt(5)),
                "tr60": c / c.shift(60) - 1,
                "fwd1": c.shift(-1) / c - 1 - drift,
                "fwd3": (c.shift(-3) / c - 1 - 3 * drift),
                "pos": np.arange(len(b)),
                "alloc": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["prof"] = D["reg"].isin(["trending", "unknown"])
    D["up"] = D["r1s"] > 0
    out = {}
    out["regime counts"] = D["reg"].value_counts()

    def tab(sub, feat, y="fwd1", q=5):
        s = sub.dropna(subset=[feat, y])
        if y == "fwd3":
            s = s[s["pos"] % 3 == 0]
        if len(s) < 50:
            return None
        s = s.copy()
        s["qq"] = pd.qcut(s[feat].rank(method="first"), q, labels=False)
        g = s.groupby("qq")[y].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        rho, p = stats.spearmanr(s[feat], s[y])
        g.loc["rho", "mean"] = rho
        g.loc["rho", "t"] = rho * np.sqrt(len(s))
        return g.round(5)

    P = D[D["prof"]]
    O = D[~D["prof"]]
    for nm, sub in [("prof_up", P[P["up"]]), ("prof_down", P[~P["up"]]), ("out_up", O[O["up"]]), ("out_down", O[~O["up"]])]:
        for f in ["uw", "lw", "r1s", "r3s", "rng"]:
            for y in ["fwd1"]:
                r = tab(sub, f, y)
                if r is not None:
                    out[f"{nm}|{f}|{y}"] = r
    for f in ["r3s", "r5s"]:
        out[f"prof_all|{f}|fwd3"] = tab(P, f, "fwd3")
        out[f"out_all|{f}|fwd3"] = tab(O, f, "fwd3")
    # out of profile by 60d trend (where available)
    O2 = O.dropna(subset=["tr60"]).copy()
    O2["trend"] = np.where(O2["tr60"] > 0.1, "rising", np.where(O2["tr60"] < -0.1, "falling", "choppy"))
    for tr in ["rising", "choppy", "falling"]:
        s = O2[(O2["trend"] == tr) & O2["up"]]
        out[f"out_{tr}_up|uw|fwd1"] = tab(s, "uw", "fwd1", 3)
    # weekday in profile
    g = P.groupby("wd")["fwd1"].agg(["mean", "count", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["prof weekday fwd1"] = g.round(5)
    # window of profile
    g = P.groupby("win")["fwd1"].agg(["mean", "count"])
    out["prof by window"] = g.round(5)
    return out
