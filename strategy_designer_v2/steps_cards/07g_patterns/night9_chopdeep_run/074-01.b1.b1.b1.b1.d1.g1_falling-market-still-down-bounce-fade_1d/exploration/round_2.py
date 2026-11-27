def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b.sort_values("timestamp")["close"].astype(float).reset_index(drop=True)
            allr.append((c.shift(-1) / c - 1).dropna())
        drift = pd.concat(allr).mean()
        allr2 = []
        for w, b in wins.items():
            c = b.sort_values("timestamp")["close"].astype(float).reset_index(drop=True)
            allr2.append((c.shift(-2) / c - 1).iloc[::2].dropna())
        drift2 = pd.concat(allr2).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"ts": b["timestamp"], "coin": coin, "win": w})
            d["r1"] = c / c.shift(1) - 1
            d["r5"] = c / c.shift(5) - 1
            d["r60"] = c / c.shift(60) - 1
            d["nxt"] = c.shift(-1) / c - 1
            d["dev"] = d["nxt"] - drift
            d["dev2"] = (c.shift(-2) / c.shift(-1) - 1) - drift
            v30 = d["r1"].rolling(30).std()
            d["volrank"] = v30.rolling(len(c), min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            d["z5"] = d["r5"] / (v30 * np.sqrt(5))
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "r5", "r60"])

    def ct(sub, col="dev"):
        s = sub.dropna(subset=[col])
        if len(s) < 20: return pd.Series({"n": len(s), "mean": np.nan, "t": np.nan, "days": 0})
        x = s[col]; m = x.mean()
        g = (x - m).groupby(s["ts"]).sum(); G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "mean": m, "t": m / se, "days": G})

    D["trend"] = pd.cut(D["r60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    D["agit"] = np.where(D["volrank"] > 0.5, "agitated", "calm")
    S = D[(D["r1"] > 0) & (D["r5"] < 0)]
    out = {}
    out["upneg5_by_trend_agit"] = S.groupby(["trend", "agit"]).apply(ct).round(4)
    out["upneg5_day2_by_trend"] = S.groupby("trend").apply(lambda s: ct(s, "dev2")).round(4)
    for tr in ["falling", "choppy"]:
        s = S[S["trend"] == tr].copy()
        s["q"] = pd.qcut(s["z5"], 3, labels=False)
        out[f"upneg5_{tr}_by_z5_tercile"] = s.groupby(["agit", "q"]).apply(ct).round(4)
    s = D[(D["r1"] > 0) & (D["r5"] < 0) & D["r60"].lt(0.1)]
    s = s.assign(q=pd.qcut(s["z5"], 5, labels=False))
    out["upneg5_notrising_by_z5_quintile"] = s.groupby("q").apply(ct).round(4)
    out["upneg5_by_trend_year"] = S[S["trend"] != "rising"].groupby(["trend", "year"]).apply(ct).round(4)
    act = D[D["alloc"].abs() > 1e-6]
    act = act.assign(pnl=act["alloc"] * act["nxt"])
    out["active_pnl_by_window"] = act.groupby("win")["pnl"].agg(["count", "mean", "sum"]).round(5)
    return out
