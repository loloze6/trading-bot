def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            r = b["close"].shift(-1) / b["close"] - 1
            allr.append(r)
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True).copy()
            b["coin"] = coin; b["win"] = w
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["nxt2"] = b["close"].shift(-2) / b["close"] - 1
            b["ex"] = b["nxt"] - drift
            rng = b["high"] - b["low"]
            b["clv"] = np.where(rng > 0, 2 * (b["close"] - b["low"]) / rng - 1, np.nan)
            b["wide"] = rng / rng.rolling(20, min_periods=20).mean()
            b["ret1"] = b["close"].pct_change()
            b["vol20"] = b["ret1"].rolling(20, min_periods=15).std()
            b["z1"] = b["ret1"] / b["vol20"].shift(1)
            b["ret5"] = b["close"] / b["close"].shift(5) - 1
            b["inprof"] = b["regime"] != "chop"
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    d = d.dropna(subset=["ex"])

    def stat(g, col="ex"):
        g = g.dropna(subset=[col])
        n = len(g)
        if n < 5: return pd.Series({"n": n, "mean": np.nan, "t_day": np.nan, "days": np.nan})
        m = g[col].mean()
        s = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum() * len(s) / max(len(s) - 1, 1)) / n
        return pd.Series({"n": n, "mean": m, "t_day": m / se if se > 0 else np.nan, "days": len(s)})

    out = {}
    d["clvq"] = pd.cut(d["clv"], [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01], labels=["q1low", "q2", "q3", "q4", "q5high"])
    d["widec"] = np.where(d["wide"] >= 1, "wide", "narrow")
    out["clv_by_profile_width"] = d.groupby(["inprof", "widec", "clvq"]).apply(stat).round(4)
    out["inprof_all"] = d.groupby("inprof").apply(stat).round(4)
    ip = d[d["inprof"]]
    ip = ip.copy()
    ip["z1q"] = pd.qcut(ip["z1"], 5, labels=False, duplicates="drop")
    out["inprof_by_z1q"] = ip.groupby("z1q").apply(stat).round(4)
    ip["r5q"] = pd.qcut(ip["ret5"], 5, labels=False, duplicates="drop")
    out["inprof_by_ret5q"] = ip.groupby("r5q").apply(stat).round(4)
    out["inprof_by_wd"] = ip.groupby("wd").apply(stat).round(4)
    out["inprof_by_year"] = ip.groupby("yr").apply(stat).round(4)
    op = d[~d["inprof"]].copy()
    op["z1q"] = pd.qcut(op["z1"], 5, labels=False, duplicates="drop")
    out["outprof_by_z1q"] = op.groupby("z1q").apply(stat).round(4)
    out["all_by_wd"] = d.groupby("wd").apply(stat).round(4)
    cases = d[d["forecast"] < 0]
    out["cases_by_coin"] = cases.groupby("coin").apply(stat).round(4)
    out["cases_by_year"] = cases.groupby("yr").apply(stat).round(4)
    # 2-day horizon on cases
    c2 = cases.copy(); c2["ex2"] = -(c2["nxt2"])
    out["cases_2day_shortsigned_mean"] = float(c2["ex2"].mean())
    # day return sign among high closes in profile wide
    hc = ip[(ip["clv"] > 0) & (ip["wide"] >= 1)].copy()
    hc["upday"] = np.where(hc["ret1"] > 0, "up", "down")
    out["inprof_widehigh_by_dayreturn_sign"] = hc.groupby("upday").apply(stat).round(4)
    return out
