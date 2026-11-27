def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 30:
                continue
            rng = (b["high"] - b["low"])
            base = rng.shift(1).rolling(20, min_periods=20).mean()
            r0 = b["close"].pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "rm": rng / base,
                "loc": (b["close"] - b["low"]) / rng.replace(0, np.nan),
                "r0": r0,
                "r60": b["close"] / b["close"].shift(60) - 1,
                "nxt": b["close"].shift(-1) / b["close"] - 1,
                "agit": (b["regime"] != "chop").astype(int),
                "vol20": r0.rolling(20).std(),
                "pos": np.arange(len(b)),
            })
            d["z0"] = d["r0"] / d["vol20"]
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    drift = df.groupby("coin")["nxt"].mean()
    df["u"] = df["nxt"] - df["coin"].map(drift)
    df["day"] = df["ts"].dt.floor("D")
    df = df.dropna(subset=["u", "rm", "loc"])

    def tstat(g):
        if len(g) < 5:
            return pd.Series({"n": len(g), "days": np.nan, "mean_u_%": np.nan, "t": np.nan})
        m = g["u"].mean()
        s = g.groupby("day")["u"].sum(); c = g.groupby("day")["u"].size()
        se = np.sqrt(((s - c * m) ** 2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean_u_%": 100 * m, "t": m / se if se > 0 else np.nan})

    out = {}
    # calm wide low-close: graded score (1-loc)*rm
    df["low_score"] = (1 - df["loc"]) * df["rm"]
    df["high_score"] = df["loc"] * df["rm"]
    for a in [0, 1]:
        s = df[df["agit"] == a].copy()
        s["lq"] = pd.qcut(s["low_score"], 5, labels=False)
        out[f"agit{a}_by_low_score_q"] = s.groupby("lq").apply(tstat).round(3)
        s["hq"] = pd.qcut(s["high_score"], 5, labels=False)
        out[f"agit{a}_by_high_score_q"] = s.groupby("hq").apply(tstat).round(3)
    # calm top low-score quintile by window and by trend
    c = df[df["agit"] == 0].copy()
    thr = c["low_score"].quantile(0.8)
    top = c[c["low_score"] >= thr].copy()
    out["calm_toplow_by_win"] = top.groupby("win").apply(tstat).round(3)
    top["tr"] = pd.cut(top["r60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    out["calm_toplow_by_trend"] = top.groupby("tr").apply(tstat).round(3)
    out["calm_toplow_by_coin"] = top.groupby("coin").apply(tstat).round(3)
    # agitated up days, by z0 among up days, and by trend
    a = df[(df["agit"] == 1) & (df["z0"] > 0)].copy()
    a["zq"] = pd.qcut(a["z0"], 4, labels=False)
    a["tr"] = pd.cut(a["r60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    out["agit_up_by_zq_trend"] = a.groupby(["tr", "zq"]).apply(tstat).round(3)
    out["agit_up_by_win"] = a[a["zq"] >= 1].groupby("win").apply(tstat).round(3)
    return out
