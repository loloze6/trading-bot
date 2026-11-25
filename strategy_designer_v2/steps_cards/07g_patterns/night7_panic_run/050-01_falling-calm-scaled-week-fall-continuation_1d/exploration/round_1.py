def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r7 = c / c.shift(7) - 1
            r60 = c / c.shift(60) - 1
            r1d = r1
            fwd3 = c.shift(-3) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "s7": r7 / (sd30 * np.sqrt(7)), "z1": r1d / sd30, "r60": r60,
                "fwd3": fwd3, "fwd1": fwd1, "inprof": (b["regime"] == "unknown"),
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "wd": ts.dt.weekday, "yr": ts.dt.year, "sd30": sd30,
                "day": ts.dt.floor("D")})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["pos"] % 3 == 0].dropna(subset=["fwd3"]).copy()
    drift = G.groupby("coin")["fwd3"].mean()
    G["ex3"] = G["fwd3"] - G["coin"].map(drift)
    G["usual"] = G["coin"].map(G.groupby("coin")["fwd3"].std())
    G["str"] = G["ex3"] / G["usual"]
    out = {}
    def summ(g):
        x = g["ex3"].dropna()
        d = g.dropna(subset=["ex3"]).groupby("day")["ex3"].sum()
        n = len(x)
        t = d.mean() / (d.std(ddof=1) / np.sqrt(len(d))) * 0 if len(d) < 3 else (x.sum() / len(d)) / (d.std(ddof=1) / np.sqrt(len(d)))
        return pd.Series({"n": n, "days": len(d), "mean_ex3": x.mean(), "str": g["str"].mean(), "t_day": t})
    G2 = G.dropna(subset=["s7"]).copy()
    G2["q7"] = pd.qcut(G2["s7"], 5, labels=False)
    out["s7 quintile, in falling-calm"] = G2[G2.inprof].groupby("q7").apply(summ)
    out["s7 quintile, outside profile"] = G2[~G2.inprof].groupby("q7").apply(summ)
    G3 = G2.dropna(subset=["r60"]).copy()
    G3["trend"] = np.where(G3.r60 > 0.1, "rising", np.where(G3.r60 < -0.1, "falling", "choppy"))
    G3["agit"] = np.where(G3.inprof, "fc", "other")
    out["s7 quintile x trend (60d avail)"] = G3.groupby(["trend", "q7"]).apply(summ)
    G2["z1q"] = pd.qcut(G2["z1"], 5, labels=False)
    out["1d-scaled quintile, all"] = G2.groupby("z1q").apply(summ)
    out["weekday, all"] = G.groupby("wd").apply(summ)
    out["by year, in profile, s7<0 short-dir"] = G2[G2.inprof & (G2.s7 < 0)].assign(ex3=lambda d: -d.ex3).groupby("yr").apply(summ)
    # book
    D = []
    for coin, ws in days.items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window"] = bk.groupby(level=0).agg(["mean", "std", "count"])
    q = bk["book_return"]
    top = bk[q >= q.quantile(0.98)]; bot = bk[q <= q.quantile(0.02)]
    out["book extremes"] = pd.DataFrame({"n": [len(top), len(bot)], "book": [top.book_return.mean(), bot.book_return.mean()], "coins": [top.coin_return.mean(), bot.coin_return.mean()]}, index=["top2%", "bot2%"])
    T = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["efq"] = pd.qcut(T["entry_forecast"].abs(), 3, labels=False, duplicates="drop")
    out["trades by |entry fc| tercile"] = T.groupby("efq").agg(n=("net_profit_loss_percent", "size"), net=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda x: (x > 0).mean()), dur=("dur_d", "mean"))
    out["trades by coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), net=("net_profit_loss_percent", "mean"))
    return out
