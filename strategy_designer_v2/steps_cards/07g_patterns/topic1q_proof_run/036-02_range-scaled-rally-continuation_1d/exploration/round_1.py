def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            rr = ((h - l) / c).rolling(30).mean()
            r3 = c / c.shift(3) - 1
            r1 = c / c.shift(1) - 1
            s3 = r3 / rr
            s1 = r1 / rr
            tr60 = c / c.shift(60) - 1
            tr20 = c / c.shift(20) - 1
            vol30 = r1.rolling(30).std()
            f7 = c.shift(-7) / c - 1
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "s3": s3, "s1": s1,
                               "tr60": tr60, "tr20": tr20, "vol30": vol30, "f7": f7, "f1": f1, "f3": f3,
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "wd": ts.dt.weekday, "year": ts.dt.year,
                               "closepos": (c - l) / (h - l).replace(0, np.nan)})
            rows.append(df)
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            drows.append(d)
    A = pd.concat(rows, ignore_index=True)
    D = pd.concat(drows, ignore_index=True)
    out = {}
    # coin means
    g7 = A[A.pos % 7 == 0].dropna(subset=["f7"])
    m7 = g7.groupby("coin")["f7"].mean()
    A["x7"] = A["f7"] - A["coin"].map(m7)
    m1 = A.dropna(subset=["f1"]).groupby("coin")["f1"].mean()
    A["x1"] = A["f1"] - A["coin"].map(m1)
    g3 = A[A.pos % 3 == 0].dropna(subset=["f3"])
    m3 = g3.groupby("coin")["f3"].mean()
    A["x3"] = A["f3"] - A["coin"].map(m3)
    G7 = A[(A.pos % 7 == 0)].dropna(subset=["x7", "s3"])
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    G7 = G7.copy(); G7["q"] = pd.qcut(G7["s3"], 10, labels=False)
    out["x7 by s3 decile (grid7)"] = G7.groupby("q").apply(lambda g: pd.concat([summ(g, "x7"), pd.Series({"s3med": g.s3.median()})]))
    G7["tr"] = pd.cut(G7["tr60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    G7["side"] = np.where(G7.s3 > 0, "up3", "down3")
    G7["big"] = G7["s3"].abs() > G7["s3"].abs().quantile(0.7)
    out["x7 by trend x side x big"] = G7.groupby(["tr", "side", "big"]).apply(lambda g: summ(g, "x7"))
    # 1-day grid: next-day after scaled 1d move deciles
    G1 = A.dropna(subset=["x1", "s1"]).copy()
    G1["q"] = pd.qcut(G1["s1"], 10, labels=False)
    out["x1 by s1 decile (all bars)"] = G1.groupby("q").apply(lambda g: summ(g, "x1"))
    G3 = A[A.pos % 3 == 0].dropna(subset=["x3", "s1"]).copy()
    G3["q"] = pd.qcut(G3["s1"], 5, labels=False)
    G3["tr"] = pd.cut(G3["tr60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    out["x3 by s1 quintile x trend (grid3)"] = G3.groupby(["tr", "q"]).apply(lambda g: summ(g, "x3"))
    out["x1 by weekday (all bars)"] = G1.groupby("wd").apply(lambda g: summ(g, "x1"))
    # vol level
    G7["vq"] = G7.groupby("coin")["vol30"].transform(lambda v: pd.qcut(v, 3, labels=False, duplicates="drop"))
    out["x7 by vol tercile x side"] = G7.groupby(["vq", "side"]).apply(lambda g: summ(g, "x7"))
    # close position in range: next 3 days
    G3["cq"] = pd.qcut(G3["closepos"], 5, labels=False, duplicates="drop")
    out["x3 by close-in-range quintile"] = G3.groupby("cq").apply(lambda g: summ(g, "x3"))
    # book by weekday and window
    Dd = D.dropna(subset=["book_return"])
    out["book ret by weekday"] = Dd.groupby("wd").apply(lambda g: summ(g, "book_return"))
    out["book ret by window"] = Dd.groupby("w").apply(lambda g: summ(g, "book_return"))
    out["by year x7 up3 big"] = G7[(G7.side == "up3") & G7.big].groupby("year").apply(lambda g: summ(g, "x7"))
    return out
