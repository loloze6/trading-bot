def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            ret14 = c / c.shift(14) - 1
            ss = ret14 / (vol30 * np.sqrt(14))
            ret7p = c / c.shift(7) - 1
            ss7 = ret7p / (vol30 * np.sqrt(7))
            r1s = r1 / vol30
            tr30 = c / c.shift(30) - 1
            f7 = c.shift(-7) / c - 1
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            rng = (df["high"] - df["low"]) / c
            clpos = (df["close"] - df["low"]) / (df["high"] - df["low"]).replace(0, np.nan)
            volu = df["volume"] / df["volume"].rolling(30, min_periods=20).mean()
            wd = pd.to_datetime(df["timestamp"]).dt.weekday
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)), "regime": df["regime"].values,
                              "fc": df["forecast"].astype(float).values, "ss": ss, "ss7": ss7, "r1s": r1s, "r1": r1,
                              "tr30": tr30, "f7": f7, "f1": f1, "f3": f3, "rng": rng, "clpos": clpos, "volu": volu,
                              "wd": wd, "vol30": vol30, "alloc": df["postRebalance_current_allocation"].astype(float)})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin
    g7 = A[A.pos % 7 == 0].dropna(subset=["f7"])
    drift7 = g7.groupby("coin")["f7"].mean()
    A["x7"] = A["f7"] - A["coin"].map(drift7)
    g1 = A.dropna(subset=["f1"]); drift1 = g1.groupby("coin")["f1"].mean()
    A["x1"] = A["f1"] - A["coin"].map(drift1)
    G7 = A[(A.pos % 7 == 0)].dropna(subset=["x7", "ss"])
    out = {}
    out["regime share"] = A["regime"].value_counts(normalize=True)
    def binstat(D, col, y, q=5):
        D = D.dropna(subset=[col, y]).copy()
        D["b"] = pd.qcut(D[col], q, labels=False, duplicates="drop")
        t = D.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=(y, "size"), mean=(y, "mean"),
                               t=(y, lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
        return t
    out["7d fwd excess by ss14 quint, choppycalm"] = binstat(G7[G7.regime == "unknown"], "ss", "x7")
    out["7d fwd excess by ss14 quint, outside"] = binstat(G7[G7.regime != "unknown"], "ss", "x7")
    out["7d fwd excess by tr30 quint, all"] = binstat(G7, "tr30", "x7")
    G1 = A.dropna(subset=["x1", "r1s"])
    out["1d fwd excess by r1s decile, all (overlap-free daily)"] = binstat(G1, "r1s", "x1", 10)
    out["1d fwd excess by clpos quint, all"] = binstat(G1, "clpos", "x1")
    out["1d fwd excess by volume ratio quint"] = binstat(G1, "volu", "x1")
    out["1d fwd excess by range/vol quint"] = binstat(G1.assign(rv=G1.rng / G1.vol30), "rv", "x1")
    out["coin 1d return by weekday"] = G1.groupby("wd")["x1"].agg(["size", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    out["7d fwd excess by ss7 quint, all"] = binstat(G7, "ss7", "x7")
    # by window: choppycalm slope sign
    cc = G7[G7.regime == "unknown"]
    out["cc corr ss vs x7 by window"] = cc.groupby("w").apply(lambda d: pd.Series({"n": len(d), "corr": d["ss"].corr(d["x7"]), "mean_signed": (np.sign(d["ss"]) * d["x7"]).mean()}))
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in trades.items() for w, t in ws.items() if len(t)], ignore_index=True)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["size", "mean", "median"])
    T["absf"] = T["entry_forecast"].abs()
    out["trades by |entry fc| tercile"] = T.groupby(pd.qcut(T.absf, 3, labels=False, duplicates="drop"))["net_profit_loss_percent"].agg(["size", "mean"])
    return out
