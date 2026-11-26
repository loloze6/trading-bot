def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hl = (b["high"] - b["low"]) / c
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd5": c.shift(-5) / c - 1,
                "fwd2": c.shift(-2) / c - 1,
                "ret28": c / c.shift(28) - 1,
                "prox56": c / c.rolling(56).max(),
                "rng": hl.rolling(28).mean() / hl.rolling(90, min_periods=40).mean(),
                "vol28": r1.rolling(28).std(),
            })
            df["pos"] = np.arange(len(df))
            rows.append(df[df["pos"] % 5 == 0])
    g = pd.concat(rows).dropna(subset=["fwd5"])
    g["ex"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")
    g["ex2"] = g["fwd2"] - g.groupby("coin")["fwd2"].transform("mean")

    def slope(col, sub, y="ex"):
        d = sub.dropna(subset=[col, y])
        if len(d) < 8: return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        s = stats.linregress(d[col], d[y])
        return pd.Series({"n": len(d), "slope": s.slope, "t": s.slope / s.stderr})

    out = {}
    dn = g[g["ret28"] <= 0].dropna(subset=["rng"]).copy()
    med = dn["rng"].median()
    vi = dn[dn["rng"] >= med]; ca = dn[dn["rng"] < med]
    # graded: ret28 x range intensity in declines
    dn["depth_x_rng"] = -dn["ret28"] * dn["rng"]
    out["down_depth_x_rng_slope"] = slope("depth_x_rng", dn)
    out["violent_ret28_by_win"] = pd.DataFrame({w: slope("ret28", vi[vi.win == w]) for w in sorted(vi.win.unique())}).T.round(3)
    out["violent_ret28_by_coin"] = pd.DataFrame({c: slope("ret28", vi[vi.coin == c]) for c in vi.coin.unique()}).T.round(3)
    k = pd.qcut(vi["ret28"].rank(method="first"), 4, labels=False)
    o = vi.groupby(k)["ex"].agg(["count", "mean", "std"]); o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"])); o["x"] = vi.groupby(k)["ret28"].mean()
    out["violent_ret28_q"] = o.round(4)
    k = pd.qcut(ca["ret28"].rank(method="first"), 4, labels=False)
    o = ca.groupby(k)["ex"].agg(["count", "mean", "std"]); o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"])); o["x"] = ca.groupby(k)["ret28"].mean()
    out["calm_ret28_q"] = o.round(4)
    d56 = g[g["ret28"] <= 0].dropna(subset=["prox56"])
    out["down_prox56_by_win"] = pd.DataFrame({w: slope("prox56", d56[d56.win == w]) for w in sorted(d56.win.unique())}).T.round(3)
    out["down_prox56_by_coin"] = pd.DataFrame({c: slope("prox56", d56[d56.coin == c]) for c in d56.coin.unique()}).T.round(3)
    out["horizon2"] = pd.DataFrame({"violent_ret28": slope("ret28", vi, "ex2"), "down_prox56": slope("prox56", d56, "ex2")}).T.round(4)
    return out
