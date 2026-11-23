def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    book_rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True).copy()
            rng = (b["high"] - b["low"])
            b["ratio"] = rng / rng.rolling(30, min_periods=20).mean()
            b["dayret"] = b["close"] / b["close"].shift(1) - 1
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["fwd5"] = b["close"].shift(-5) / b["close"] - 1
            b["alloc"] = b["postRebalance_current_allocation"]
            b["next1"] = b["close"].shift(-1) / b["close"] - 1
            b["gain"] = b["alloc"] * b["next1"]
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            g = b.iloc[::5].copy()
            g["coin"] = coin; g["w"] = w
            rows.append(g[["coin", "w", "year", "ratio", "dayret", "ret20", "fwd5", "forecast", "alloc"]])
            bb = b[["alloc", "gain", "next1", "forecast"]].copy(); bb["coin"] = coin; bb["w"] = w
            book_rows.append(bb)
    G = pd.concat(rows).dropna(subset=["fwd5", "ratio"])
    drift = G.groupby("coin")["fwd5"].mean()
    G["ex"] = G["fwd5"] - G["coin"].map(drift)
    def summ(df, key):
        r = df.groupby(key, observed=True)["ex"].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["fwd_total"] = df.groupby(key, observed=True)["fwd5"].mean()
        return r
    G["rq"] = pd.qcut(G["ratio"], 5, labels=["q1", "q2", "q3", "q4", "q5"])
    G["dir"] = np.where(G["dayret"] > 0, "up", "down")
    G["trend"] = np.where(G["ret20"] > 0, "t_up", "t_down")
    out = {}
    out["by_ratio_quintile"] = summ(G, "rq")
    out["by_quintile_daydir"] = summ(G, ["dir", "rq"])
    out["by_quintile_trend20"] = summ(G, ["trend", "rq"])
    out["by_year_q5_minus_q1"] = G.groupby("year").apply(lambda d: pd.Series({
        "q5": d.loc[d.rq == "q5", "ex"].mean(), "q1": d.loc[d.rq == "q1", "ex"].mean(), "n": len(d)}))
    B = pd.concat(book_rows).dropna(subset=["gain"])
    B["side"] = np.sign(B["alloc"]).map({1.0: "long", -1.0: "short", 0.0: "flat"})
    out["book_by_side"] = B.groupby("side").agg(n=("gain", "size"), mean_gain=("gain", "mean"),
                                               mean_alloc=("alloc", "mean"), coin_next=("next1", "mean"))
    out["alloc_abs_mean"] = float(B["alloc"].abs().mean())
    # book per window vs holding
    D = []
    for coin in days:
        for w, d in days[coin].items():
            x = d[["book_return", "coin_return"]].copy(); x["w"] = w; x["i"] = range(len(x)); D.append(x)
    D = pd.concat(D).groupby(["w", "i"]).mean().dropna()
    pw = D.groupby(level=0).apply(lambda d: pd.Series({"book": (1 + d.book_return).prod() - 1,
                                                       "hold": (1 + d.coin_return).prod() - 1}))
    out["per_window"] = pw
    return out
