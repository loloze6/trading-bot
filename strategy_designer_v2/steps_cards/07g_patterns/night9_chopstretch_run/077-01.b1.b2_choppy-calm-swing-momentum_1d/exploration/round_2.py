def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            r1s = r1 / vol30
            tr60 = c / c.shift(60) - 1
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            rng = (df["high"] - df["low"]) / c
            clpos = (df["close"] - df["low"]) / (df["high"] - df["low"]).replace(0, np.nan)
            volu = df["volume"] / df["volume"].rolling(30, min_periods=20).mean()
            vol5 = r1.rolling(5).std()
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)), "regime": df["regime"].values,
                              "r1s": r1s, "tr60": tr60, "f1": f1, "f3": f3, "rv": rng / vol30, "clpos": clpos,
                              "volu": volu, "vratio": vol5 / vol30,
                              "year": pd.to_datetime(df["timestamp"]).dt.year})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    for h in ["f1", "f3"]:
        g = A[A.pos % int(h[1]) == 0].dropna(subset=[h])
        A["x" + h[1]] = A[h] - A["coin"].map(g.groupby("coin")[h].mean())
    A["trend"] = np.where(A.tr60 > 0.10, "rising", np.where(A.tr60 < -0.10, "falling", np.where(A.tr60.notna(), "choppy", np.nan)))
    A["cc"] = np.where(A.regime == "unknown", "choppycalm", "other")
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out = {}
    G1 = A.dropna(subset=["x1", "r1s"]).copy()
    G1["dq"] = pd.qcut(G1.r1s, 5, labels=["d1lo", "d2", "d3", "d4", "d5hi"])
    out["1d fwd x by r1s quint x trend"] = G1.groupby(["trend", "dq"])["x1"].apply(tt).unstack()
    out["1d fwd x by r1s quint x cc"] = G1.groupby(["cc", "dq"])["x1"].apply(tt).unstack()
    G3 = A[A.pos % 3 == 0].dropna(subset=["x3", "r1s"]).copy()
    G3["dq"] = pd.qcut(G3.r1s, 5, labels=["d1lo", "d2", "d3", "d4", "d5hi"])
    out["3d fwd x by r1s quint x trend (grid)"] = G3.groupby(["trend", "dq"])["x3"].apply(tt).unstack()
    # volume split by day sign
    G1["sgn"] = np.sign(G1.r1s)
    G1["vq"] = pd.qcut(G1.volu, 5, labels=False, duplicates="drop")
    out["1d fwd x by volume quint x day sign"] = G1.groupby(["sgn", "vq"])["x1"].apply(tt).unstack()
    # close position on up days only, choppy trend
    up = G1[(G1.sgn > 0)].copy(); up["cq"] = pd.qcut(up.clpos, 5, labels=False, duplicates="drop")
    out["1d fwd x up days by close pos quint x trend"] = up.groupby(["trend", "cq"])["x1"].apply(tt)["mean"].unstack()
    out["same t"] = up.groupby(["trend", "cq"])["x1"].apply(tt)["t"].unstack()
    # big down day rebound by year (stability)
    lo = G1[G1.dq == "d1lo"]
    out["lowest quint r1s 1d fwd x by year"] = lo.groupby("year")["x1"].apply(tt).unstack()
    out["lowest quint r1s, choppy trend, by year"] = lo[lo.trend == "choppy"].groupby("year")["x1"].apply(tt).unstack()
    # book's largest days
    D = pd.concat([d.assign(coin=c, w=w) for c, ws in days.items() for w, d in ws.items()], ignore_index=True)
    bd = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bd.book_return.quantile([0.02, 0.98])
    out["book extreme days: coin mean return"] = pd.Series({"worst2pct_coin": bd[bd.book_return <= q.iloc[0]].coin_return.mean(),
        "best2pct_coin": bd[bd.book_return >= q.iloc[1]].coin_return.mean(), "n_each": int((bd.book_return <= q.iloc[0]).sum()),
        "corr_book_coin": bd.book_return.corr(bd.coin_return)})
    return out
