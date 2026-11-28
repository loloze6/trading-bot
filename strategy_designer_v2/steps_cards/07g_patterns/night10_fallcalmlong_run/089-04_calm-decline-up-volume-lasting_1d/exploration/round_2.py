def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def build(h, off):
        rows = []
        for coin, ws in bars.items():
            allr = []
            fs = []
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"]
                fr = c.shift(-h) / c - 1
                g0 = np.arange(0, len(df) - h, h)
                allr.extend(fr.iloc[g0].dropna().tolist())
                g = np.arange(off, len(df) - h, h)
                f = pd.DataFrame({
                    "ret10": (c / c.shift(10) - 1).iloc[g].values,
                    "ret5": (c / c.shift(5) - 1).iloc[g].values,
                    "ret3": (c / c.shift(3) - 1).iloc[g].values,
                    "dl20": (c / df["low"].rolling(20).min() - 1).iloc[g].values,
                    "fwd": fr.iloc[g].values,
                    "fc": (df["regime"] == "unknown").iloc[g].values,
                    "day": pd.to_datetime(df["timestamp"]).dt.floor("D").iloc[g].values,
                    "w": w, "coin": coin})
                fs.append(f)
            F = pd.concat(fs, ignore_index=True)
            F["ex"] = F["fwd"] - np.mean(allr)
            rows.append(F)
        return pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    def clus(S, x):
        S = S.dropna(subset=[x, "ex"])
        X = S[x].values; y = S["ex"].values
        Xc = X - X.mean(); b = (Xc * y).sum() / (Xc ** 2).sum()
        e = y - y.mean() - b * Xc
        sc = pd.Series(Xc * e).groupby(S["day"].values).sum()
        se = np.sqrt((sc ** 2).sum()) / (Xc ** 2).sum()
        return b, b / se, len(S), S["day"].nunique()
    res = []
    for h in (3, 5, 7, 10):
        for x in ("ret10", "ret5", "ret3", "dl20"):
            for off in range(0, h, max(1, h // 3)):
                A = build(h, off)
                b, t, n, nd = clus(A[A.fc], x)
                res.append([h, x, off, b, t, n, nd])
    R = pd.DataFrame(res, columns=["h", "feat", "off", "slope", "t", "n", "days"])
    out["fc slope by horizon feat offset"] = R.groupby(["h", "feat"]).agg(slope=("slope", "mean"), t_mean=("t", "mean"), t_min=("t", "min"), n=("n", "mean")).round(4)
    A = build(5, 0)
    S = A[A.fc].dropna(subset=["ret10"])
    out["ret10 h5 slope by coin"] = pd.DataFrame([[c] + list(clus(S[S.coin == c], "ret10")) for c in S.coin.unique()], columns=["coin", "slope", "t", "n", "days"]).round(4)
    S = S.copy(); S["wn"] = S["w"].str[1:].astype(int)
    out["ret10 h5 slope early/late windows"] = pd.DataFrame([[k] + list(clus(S[(S.wn <= 12) == (k == "w<=12")], "ret10")) for k in ("w<=12", "w>12")], columns=["part", "slope", "t", "n", "days"]).round(4)
    S["q"] = pd.qcut(S["ret10"], 4, labels=False)
    g = S.groupby("q").agg(n=("ex", "count"), ret10=("ret10", "mean"), ex=("ex", "mean"), fwd=("fwd", "mean"))
    out["ret10 quartile h5 fc"] = g.round(4)
    # outside profile for comparison
    O = A[~A.fc]
    out["ret10 h5 slope outside fc"] = pd.DataFrame([list(clus(O, "ret10"))], columns=["slope", "t", "n", "days"]).round(4)
    # book: daily returns, largest gains/losses context
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            D.append(d.assign(coin=coin))
    D = pd.concat(D).dropna(subset=["book_return"])
    act = D[D.book_return != 0]
    out["book active days"] = pd.Series({"n": len(act), "mean": act.book_return.mean(), "t": act.book_return.mean() / act.book_return.std() * np.sqrt(len(act)), "top5pct share of sum": act.book_return.nlargest(max(1, len(act) // 20)).sum() / act.book_return.sum()}).round(4)
    return out
