def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            allr.append((c.shift(-1) / c - 1).dropna())
        drift = pd.concat(allr).mean() if allr else 0.0
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            d = pd.DataFrame({"ts": b["timestamp"], "coin": coin, "win": w})
            d["r1"] = c / c.shift(1) - 1
            d["r5"] = c / c.shift(5) - 1
            d["r20"] = c / c.shift(20) - 1
            d["r60"] = c / c.shift(60) - 1
            d["nxt"] = c.shift(-1) / c - 1
            d["nxt3"] = c.shift(-3) / c - 1
            d["dev"] = d["nxt"] - drift
            rng = (h - l) / c
            d["rngrel"] = rng / rng.shift(1).rolling(20).mean()
            d["clpos"] = (c - l) / (h - l).replace(0, np.nan)
            d["vol20"] = d["r1"].rolling(20).std()
            d["volrel"] = d["vol20"] / d["r1"].rolling(60).std()
            d["falling"] = (b["regime"] != "chop")
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            d["sd"] = drift
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["nxt", "r5"])

    def ct(sub, col="dev", sign=1.0):
        s = sub.dropna(subset=[col])
        if len(s) < 20: return pd.Series({"n": len(s), "mean": np.nan, "t": np.nan, "days": 0})
        x = sign * s[col]
        m = x.mean()
        g = (x - m).groupby(s["ts"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "mean": m, "t": m / se, "days": G})

    out = {}
    # 1. by trend bucket (r60) and up/down day, 5d sign
    D["trend"] = pd.cut(D["r60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    D["up"] = D["r1"] > 0
    D["neg5"] = D["r5"] < 0
    out["nextday_by_trend_up_neg5"] = D.dropna(subset=["trend"]).groupby(["trend", "up", "neg5"]).apply(ct).round(4)
    # 2. within trend, quintile of r5 among up days
    for tr in ["falling", "choppy", "rising"]:
        s = D[(D["trend"] == tr) & D["up"]].copy()
        s["q5"] = pd.qcut(s["r5"], 5, labels=False)
        out[f"up_days_{tr}_by_r5_quintile"] = s.groupby("q5").apply(ct).round(4)
    # 3. down days in falling by r1 quintile
    s = D[(D["trend"] == "falling") & ~D["up"]].copy()
    s["q1"] = pd.qcut(s["r1"], 5, labels=False)
    out["down_days_falling_by_r1_quintile"] = s.groupby("q1").apply(ct).round(4)
    # 4. all days, by r1 quintile x trend
    s = D.dropna(subset=["trend"]).copy()
    s["q1"] = s.groupby("trend")["r1"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["all_by_trend_r1_quintile"] = s.groupby(["trend", "q1"]).apply(ct).round(4)
    # 5. close position within range, by trend
    s = D.dropna(subset=["trend", "clpos"]).copy()
    s["qc"] = pd.cut(s["clpos"], [0, 0.2, 0.4, 0.6, 0.8, 1.0001], include_lowest=True, labels=False)
    out["by_trend_closepos"] = s.groupby(["trend", "qc"]).apply(ct).round(4)
    # 6. weekday by trend
    out["weekday_by_trend"] = D.dropna(subset=["trend"]).groupby(["trend", "wd"]).apply(ct).round(4)
    # 7. book: daily returns, largest gains/losses context
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    DD = pd.concat(dd)
    book = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = book.groupby(level=0).agg(["count", "mean", "std"]).round(5)
    act = D[D["alloc"].abs() > 1e-6]
    act = act.assign(pnl=act["alloc"] * act["nxt"])
    out["active_pnl_by_year"] = act.groupby("year")["pnl"].agg(["count", "mean", "sum"]).round(5)
    out["active_pnl_by_coin"] = act.groupby("coin")["pnl"].agg(["count", "mean", "sum"]).round(5)
    return out
