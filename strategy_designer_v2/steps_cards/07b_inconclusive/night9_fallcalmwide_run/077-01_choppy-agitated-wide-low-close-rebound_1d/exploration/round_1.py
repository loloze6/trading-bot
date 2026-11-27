import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows, allrows = [], []
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            rets.append(c[1:] / c[:-1] - 1)
        mu = np.concatenate(rets).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c, h, l = df["close"], df["high"], df["low"]
            rng = h - l
            df["width"] = rng / rng.rolling(30, min_periods=30).mean()
            df["loc"] = (c - l) / rng.replace(0, np.nan)
            r = c.pct_change()
            df["rngvol"] = rng / c / r.rolling(30).std()
            for k in (1, 2, 3, 5):
                df[f"f{k}"] = c.shift(-k) / c - 1 - k * mu
            df["ret0"] = r - mu
            df["tr60"] = c / c.shift(60) - 1
            df["coin"] = coin
            df["win"] = w
            df["year"] = pd.to_datetime(df["timestamp"]).dt.year
            rows.append(df[df["forecast"] > 0])
            allrows.append(df)
    cs = pd.concat(rows)
    al = pd.concat(allrows)

    def summ(g, col="f1"):
        x = g[col].dropna()
        n = len(x)
        t = x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": t})

    out = {}
    out["cases by horizon"] = pd.DataFrame({k: summ(cs, k) for k in ["f1", "f2", "f3", "f5"]}).T
    out["cases by coin"] = cs.groupby("coin").apply(summ)
    out["cases by year"] = cs.groupby("year").apply(summ)
    out["cases by window"] = cs.groupby("win").apply(summ)
    cs["fq"] = pd.qcut(cs["forecast"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    cs["rq"] = pd.qcut(cs["rngvol"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    cs["lq"] = pd.qcut(cs["loc"].rank(method="first"), 3, labels=["nearlow", "mid", "higher"])
    cs["dq"] = pd.qcut(cs["ret0"].rank(method="first"), 3, labels=["bigfall", "mid", "small"])
    out["cases by forecast tercile"] = cs.groupby("fq").apply(summ)
    out["cases by range/vol tercile"] = cs.groupby("rq").apply(summ)
    out["cases by loc tercile"] = cs.groupby("lq").apply(summ)
    out["cases by same-day return tercile"] = cs.groupby("dq").apply(summ)

    a = al.dropna(subset=["width", "loc", "f1"]).copy()
    a["wq"] = pd.cut(a["width"], [0, 1, 1.5, 2, 100]).astype(str)
    a["lb"] = pd.cut(a["loc"], [-0.01, 0.25, 0.75, 1.01], labels=["low", "mid", "high"])
    out["all bars width x loc next-day mean%"] = a.groupby(["wq", "lb"])["f1"].mean().mul(100).unstack()
    out["all bars width x loc n"] = a.groupby(["wq", "lb"])["f1"].count().unstack()
    a["tb"] = pd.cut(a["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    w = a[a["width"] >= 1]
    out["wide days trend x loc next-day mean%"] = w.groupby(["tb", "lb"])["f1"].mean().mul(100).unstack()
    out["wide days trend x loc n"] = w.groupby(["tb", "lb"])["f1"].count().unstack()
    return out
