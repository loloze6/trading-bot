def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float)
            r1 = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r1.rolling(20).std()
            z = (c / sma - 1) / sd
            vol60 = r1.rolling(30).std()
            ret5 = c / c.shift(5) - 1
            ret20 = c / c.shift(20) - 1
            for h in (1, 3, 10):
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["r1"] = r1; d["z"] = z; d["sd"] = sd; d["ret5"] = ret5; d["ret20"] = ret20
            d["choppy"] = (d["regime"] == "unknown").astype(int)
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["w"] = w
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            d["fc"] = d["forecast"]
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # drift per coin for 10-day grid
    g10 = A[(A["pos"] % 10 == 0) & A["f10"].notna()].copy()
    drift = g10.groupby("coin")["f10"].mean()
    g10["x10"] = g10["f10"] - g10["coin"].map(drift)
    g10["zq"] = pd.cut(g10["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    def summ(gr, col):
        s = gr[col]
        return pd.Series({"n": s.count(), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(s.count())) if s.count() > 2 else np.nan})
    out["x10 by z bin x choppy"] = g10.groupby(["choppy", "zq"]).apply(lambda g: summ(g, "x10")).round(4)
    # 3-day grid
    g3 = A[(A["pos"] % 3 == 0) & A["f3"].notna()].copy()
    dr3 = g3.groupby("coin")["f3"].mean()
    g3["x3"] = g3["f3"] - g3["coin"].map(dr3)
    g3["zq"] = pd.cut(g3["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["x3 by z bin x choppy"] = g3.groupby(["choppy", "zq"]).apply(lambda g: summ(g, "x3")).round(4)
    # 1-day: after large daily moves scaled by sd
    A["m1"] = A["r1"] / A["sd"].shift(1)
    dr1 = A.groupby("coin")["f1"].mean()
    A["x1"] = A["f1"] - A["coin"].map(dr1)
    A["mq"] = pd.cut(A["m1"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["x1 after scaled daily move x choppy"] = A.dropna(subset=["x1"]).groupby(["choppy", "mq"]).apply(lambda g: summ(g, "x1")).round(4)
    # weekday
    out["x1 by weekday of next day"] = A.dropna(subset=["x1"]).groupby(A["wd"].add(1) % 7).apply(lambda g: summ(g, "x1")).round(4)
    # vol level: sd tercile within coin
    A["sdq"] = A.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    g10["sdq"] = g10.index.map(A["sdq"])
    out["x10 by vol tercile x choppy"] = g10.groupby(["choppy", "sdq"]).apply(lambda g: summ(g, "x10")).round(4)
    # 20-day return momentum on 10 grid
    g10["r20q"] = pd.cut(g10["ret20"] / (g10["sd"] * np.sqrt(20)), [-np.inf, -1, -0.3, 0.3, 1, np.inf])
    out["x10 by scaled 20d ret x choppy"] = g10.groupby(["choppy", "r20q"]).apply(lambda g: summ(g, "x10")).round(4)
    # book: daily returns, largest gains/losses
    days = []
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            dd = df.copy(); dd["coin"] = coin; dd["w"] = w; days.append(dd)
    D = pd.concat(days, ignore_index=True)
    out["book by window"] = D.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean")).round(5)
    out["share regime unknown"] = float(A["choppy"].mean())
    return out
