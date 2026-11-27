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
                "pos": b["postRebalance_current_allocation"],
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
    df["tr"] = pd.cut(df["r60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    df["hs"] = df["loc"] * df["rm"]
    a = df[df["agit"] == 1].dropna(subset=["tr"]).copy()
    a["hq"] = a.groupby("tr")["hs"].transform(lambda x: pd.qcut(x, 4, labels=False))
    out["agit_trend_by_highscore_q"] = a.groupby(["tr", "hq"]).apply(tstat).round(3)
    f = a[a["tr"] == "fall"].copy()
    out["fall_agit_top_hs_by_win"] = f[f["hq"] == 3].groupby("win").apply(tstat).round(3)
    out["fall_agit_up_z_ge_q2_by_win"] = f[f["z0"] > f["z0"].quantile(0.6)].groupby("win").apply(tstat).round(3)
    ups = f[f["z0"] > 0]
    out["fall_agit_up_corr_z_u"] = pd.Series({"corr": ups["z0"].corr(ups["u"]), "n": len(ups)})
    act = df[df["pos"] < 0].dropna(subset=["tr"])
    out["active_by_trend"] = act.groupby("tr").apply(tstat).round(3)
    return out
