import pandas as pd, numpy as np

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 25: continue
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l)
            cl = (c - l) / rng.replace(0, np.nan)
            rr = rng / rng.rolling(20, min_periods=20).mean()
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            vol20 = r1.rolling(20).std()
            fa = b["regime"].isin(["mean_reversion", "unknown"])
            df = pd.DataFrame({"coin": coin, "win": w, "cl": cl, "rr": rr, "r1": r1, "z1": r1 / vol20,
                               "nxt": c.shift(-1) / c - 1, "nxt2": c.shift(-2) / c - 1, "fa": fa,
                               "t20": c / c.shift(20) - 1, "t60": c / c.shift(60) - 1,
                               "t5": c / c.shift(5) - 1,
                               "day": ts.dt.floor("D"), "yr": ts.dt.year, "pos": b["postRebalance_current_allocation"]})
            rows.append(df)
    P = pd.concat(rows, ignore_index=True)
    drift = P.groupby("coin")["nxt"].mean()
    P["u"] = P["nxt"] - P["coin"].map(drift)
    d2 = P.groupby("coin")["nxt2"].mean()
    P["u2"] = P["nxt2"] - P["coin"].map(d2)

    def tstat(s, d):
        x = pd.DataFrame({"s": s, "d": d}).dropna()
        n = len(x)
        if n < 10: return np.nan
        m = x["s"].mean()
        g = x.groupby("d")["s"].agg(["sum", "size"])
        G = len(g)
        se = np.sqrt(((g["sum"] - g["size"] * m) ** 2).sum() * G / (G - 1)) / n
        return m / se

    def tab(mask, col, bins, val="u"):
        Q = P[mask].dropna(subset=[col, val]).copy()
        Q["b"] = pd.cut(Q[col], bins)
        out = []
        for k, g in Q.groupby("b", observed=True):
            out.append({"bin": str(k), "n": len(g), "mean%": 100 * g[val].mean(), "t_day": tstat(g[val], g["day"])})
        return pd.DataFrame(out)

    res = {}
    up = P["r1"] > 0
    res["FA_upday_by_z1"] = tab(P["fa"] & up, "z1", [0, 0.5, 1, 1.5, 2, 50])
    res["FA_upday_by_z1_2day"] = tab(P["fa"] & up, "z1", [0, 0.5, 1, 1.5, 2, 50], "u2")
    res["FA_highclose_by_t5"] = tab(P["fa"] & (P["cl"] > 0.5), "t5", [-5, -0.1, -0.03, 0, 0.03, 0.1, 50])
    res["FA_all_by_t5"] = tab(P["fa"], "t5", [-5, -0.1, -0.03, 0, 0.03, 0.1, 50])
    res["FA_highclose_by_cl_fine"] = tab(P["fa"] & (P["cl"] > 0.5), "cl", [0.5, 0.65, 0.8, 0.9, 1.01])
    # non-FA split by own 60d trend (falling non-FA = falling calm)
    nf = ~P["fa"]
    res["falling_calm_by_t20"] = tab(nf & (P["t60"] < -0.10), "t20", [-5, -0.2, -0.1, -0.05, 0, 0.05, 50])
    res["choppy_by_t20"] = tab(nf & (P["t60"].between(-0.10, 0.10)), "t20", [-5, -0.2, -0.1, -0.05, 0, 0.05, 50])
    res["rising_by_t20"] = tab(nf & (P["t60"] > 0.10), "t20", [-5, -0.1, -0.05, 0, 0.05, 0.1, 0.2, 50])
    res["falling_calm_by_closeloc"] = tab(nf & (P["t60"] < -0.10), "cl", [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    res["falling_calm_by_z1"] = tab(nf & (P["t60"] < -0.10), "z1", [-50, -1, 0, 1, 50])
    Q = P[nf & (P["t20"] < -0.1) & (P["t20"] > -0.2)]
    res["notFA_t20_m10m20_by_year"] = Q.groupby("yr").apply(lambda g: pd.Series({"n": len(g), "mean%": 100 * g["u"].mean(), "t": tstat(g["u"], g["day"])}))
    res["notFA_t20_m10m20_by_coin"] = Q.groupby("coin").apply(lambda g: pd.Series({"n": len(g), "mean%": 100 * g["u"].mean(), "t": tstat(g["u"], g["day"])}))
    Q2 = P[P["fa"] & up & (P["z1"] <= 1)]
    res["FA_smallup_by_year"] = Q2.groupby("yr").apply(lambda g: pd.Series({"n": len(g), "mean%": 100 * g["u"].mean(), "t": tstat(g["u"], g["day"])}))
    res["FA_smallup_by_coin"] = Q2.groupby("coin").apply(lambda g: pd.Series({"n": len(g), "mean%": 100 * g["u"].mean(), "t": tstat(g["u"], g["day"])}))
    return res
