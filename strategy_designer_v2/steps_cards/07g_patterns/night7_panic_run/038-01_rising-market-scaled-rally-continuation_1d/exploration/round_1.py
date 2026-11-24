def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            ret3 = c / c.shift(3) - 1
            fwd3 = c.shift(-3) / c - 1
            fwd1 = c.shift(-1) / c - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": r1, "ret3": ret3, "sd30": sd30,
                "z3": ret3 / (sd30 * np.sqrt(3)), "z1": r1 / sd30,
                "ret10": c / c.shift(10) - 1,
                "fwd3": fwd3, "fwd1": fwd1,
                "rising": (b["regime"] != "chop").values,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["pos"] % 3 == 0].dropna(subset=["fwd3"]).copy()
    drift = G.groupby("coin")["fwd3"].mean()
    usual = G.groupby("coin")["fwd3"].std()
    G["ex3"] = G["fwd3"] - G["coin"].map(drift)
    G["str3"] = G["ex3"] / G["coin"].map(usual)
    G = G.dropna(subset=["z3"])
    out = {}

    def tab(df, key):
        g = df.groupby(key)["str3"]
        t = g.agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["ex3_mean"] = df.groupby(key)["ex3"].mean()
        return t.drop(columns="std").round(4)

    G["zq"] = pd.qcut(G["z3"], 6, labels=False)
    out["z3 sextile x rising: strength"] = tab(G, ["rising", "zq"])
    out["z3 sextile edges"] = G.groupby("zq")["z3"].agg(["min", "max"]).round(2)
    # slopes inside / outside rising, full z3 including negatives
    sl = {}
    for rv in [True, False]:
        s = G[G["rising"] == rv]
        res = stats.linregress(s["z3"], s["str3"])
        sl[f"rising={rv}"] = pd.Series({"n": len(s), "slope": res.slope, "t": res.slope / res.stderr})
        s2 = s[s["z3"] < 0]
        res = stats.linregress(s2["z3"], s2["str3"])
        sl[f"rising={rv} falls only"] = pd.Series({"n": len(s2), "slope": res.slope, "t": res.slope / res.stderr})
    out["slopes str3 on z3"] = pd.DataFrame(sl).T.round(4)
    # volatility level
    G["volq"] = G.groupby("coin")["sd30"].transform(lambda x: pd.qcut(x, 3, labels=False))
    G["up"] = np.sign(G["z3"])
    out["vol tercile x sign(z3) x rising"] = tab(G, ["rising", "volq", "up"])
    # 10-day return
    G["q10"] = pd.qcut(G["ret10"] / G["sd30"], 5, labels=False)
    out["10d scaled ret quintile x rising"] = tab(G.dropna(subset=["q10"]), ["rising", "q10"])
    # weekday on daily returns (all bars)
    A2 = A.dropna(subset=["fwd1"]).copy()
    A2["wd"] = A2["ts"].dt.weekday
    wd = A2.groupby("wd")["fwd1"].agg(["count", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["next-day return by weekday of signal bar"] = wd.round(5)
    # large 1-day moves
    A2["z1q"] = pd.qcut(A2["z1"], 10, labels=False)
    t1 = A2.groupby(["rising", "z1q"])["fwd1"].agg(["count", "mean", "std"])
    t1["t"] = t1["mean"] / (t1["std"] / np.sqrt(t1["count"]))
    out["next-day ret by z1 decile x rising"] = t1.round(5)
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    tr["fq"] = pd.qcut(tr["entry_forecast"], 4, labels=False, duplicates="drop")
    out["trades by entry forecast quartile"] = tr.groupby("fq").agg(n=("net_profit_loss_percent", "size"),
        net=("net_profit_loss_percent", "mean"), fc=("entry_forecast", "mean"),
        dur_days=("duration_minutes", lambda x: x.mean() / 1440)).round(3)
    out["trades by year"] = tr.assign(y=pd.to_datetime(tr["entry_time"]).dt.year).groupby("y")["net_profit_loss_percent"].agg(["size", "mean"]).round(3)
    return out
