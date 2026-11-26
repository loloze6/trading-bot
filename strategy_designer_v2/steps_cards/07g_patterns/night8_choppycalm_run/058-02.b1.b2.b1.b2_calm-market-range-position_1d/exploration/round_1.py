def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 30:
                continue
            hi = b["high"].rolling(20, min_periods=20).max()
            lo = b["low"].rolling(20, min_periods=20).min()
            pos = 2 * (b["close"] - lo) / (hi - lo) - 1
            r1 = b["close"].pct_change()
            ret5past = b["close"] / b["close"].shift(5) - 1
            vol20 = r1.rolling(20, min_periods=15).std()
            ret20 = b["close"] / b["close"].shift(20) - 1
            fwd5 = b["close"].shift(-5) / b["close"] - 1
            fwd1 = b["close"].shift(-1) / b["close"] - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "i": np.arange(len(b)), "pos": pos,
                "r1": r1, "ret5p": ret5past, "vol20": vol20, "ret20": ret20,
                "fwd5": fwd5, "fwd1": fwd1, "regime": b["regime"].values,
                "fc": b["forecast"].values,
                "alloc": b["postRebalance_current_allocation"].values,
                "wd": ts.dt.weekday.values, "yr": ts.dt.year.values,
                "dayk": ts.dt.floor("D").values,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.i % 5 == 0].groupby("coin")["fwd5"].mean()
    A["ex5"] = A["fwd5"] - A["coin"].map(drift)
    G = A[(A.i % 5 == 0)].dropna(subset=["ex5", "pos"]).copy()
    G["calm"] = np.where(G.regime == "unknown", "calm", "agit")
    G["pq"] = pd.cut(G.pos, [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01],
                     labels=["bot", "low", "mid", "high", "top"])

    def summ(g):
        return pd.Series({"n": len(g), "mean_ex5_%": 100 * g.ex5.mean(),
                          "t": g.ex5.mean() / (g.ex5.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    out = {}
    out["by_pos_regime"] = G.groupby(["calm", "pq"]).apply(summ)
    # trend within window: 20-day return tercile
    G["trend"] = pd.cut(G.ret20, [-10, -0.1, 0.1, 10], labels=["fall", "flat", "rise"])
    out["calm_pos_by_trend20"] = G[G.calm == "calm"].groupby(["trend", "pq"]).apply(summ)
    # past 5-day move
    G["p5q"] = pd.qcut(G.ret5p / G.vol20, 5, labels=False)
    out["by_past5_scaled_regime"] = G.groupby(["calm", "p5q"]).apply(summ)
    # vol level
    G["vq"] = G.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["by_vol_tercile_pos"] = G.groupby(["vq", "pq"]).apply(summ)
    out["by_weekday_1d"] = A.dropna(subset=["fwd1"]).groupby("wd")["fwd1"].agg(
        lambda s: 100 * s.mean()).to_frame("mean_fwd1_%")
    out["by_year_calm_slope"] = G[G.calm == "calm"].groupby("yr").apply(
        lambda g: pd.Series({"n": len(g), "corr": g.pos.corr(g.ex5)}))
    out["by_coin_calm_corr"] = G[G.calm == "calm"].groupby("coin").apply(
        lambda g: pd.Series({"n": len(g), "corr": g.pos.corr(g.ex5)}))
    # book: long vs short contribution
    A["gain"] = A.alloc * A.fwd1
    out["book_side"] = A.dropna(subset=["gain"]).assign(
        side=np.sign(A.alloc)).groupby("side")["gain"].agg(["count", "mean", "sum"])
    return out
