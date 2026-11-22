def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            H = c.rolling(30).max(); L = c.rolling(30).min()
            pos = (c - L) / (H - L)
            d = 2 * pos - 1
            net = (c - c.shift(30)).abs() / (H - L)
            flat = 1 - net
            past5 = c / c.shift(5) - 1
            past30 = c / c.shift(30) - 1
            r1 = c.pct_change()
            vol = r1.rolling(30).std()
            vol_ratio = r1.rolling(5).std() / r1.rolling(60).std()
            fwd = c.shift(-5) / c - 1
            idx = np.arange(0, len(b), 5)
            for i in idx:
                rows.append(dict(coin=coin, w=w, d=d.iloc[i], flat=flat.iloc[i], past5=past5.iloc[i],
                                 past30=past30.iloc[i], vol=vol.iloc[i], vr=vol_ratio.iloc[i], fwd=fwd.iloc[i],
                                 fc=b["forecast"].iloc[i], wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                                 yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = df.groupby("coin")["fwd"].transform("mean")
    df["ex"] = df["fwd"] - drift
    out = {}
    def tab(g):
        a = g["ex"]
        return pd.Series({"n": len(a), "mean%": a.mean() * 100, "t": a.mean() / (a.std() / np.sqrt(len(a))) if len(a) > 2 else np.nan})
    x = df.dropna(subset=["d", "flat"]).copy()
    x["dq"] = pd.qcut(x["d"], 5, labels=False)
    x["fh"] = (x["flat"] > x["flat"].median()).map({True: "flat", False: "trend"})
    out["by d quintile x flatness"] = x.groupby(["fh", "dq"]).apply(tab)
    x["fcq"] = pd.qcut(x["fc"].rank(method="first"), 5, labels=False)
    out["by forecast quintile"] = x.groupby("fcq").apply(tab)
    y = df.dropna(subset=["past5"]).copy()
    y["p5q"] = pd.qcut(y["past5"], 5, labels=False)
    out["by past5 quintile"] = y.groupby("p5q").apply(tab)
    y = df.dropna(subset=["past30"]).copy()
    y["p30q"] = pd.qcut(y["past30"], 5, labels=False)
    out["by past30 quintile"] = y.groupby("p30q").apply(tab)
    y = df.dropna(subset=["vol"]).copy()
    y["vq"] = pd.qcut(y["vol"], 5, labels=False)
    out["by vol quintile"] = y.groupby("vq").apply(tab)
    y = df.dropna(subset=["vr"]).copy()
    y["vrq"] = pd.qcut(y["vr"], 5, labels=False)
    out["by vol ratio 5/60 quintile"] = y.groupby("vrq").apply(tab)
    out["by year"] = df.groupby("yr").apply(tab)
    # signed position per coin: d * ex correlation
    z = x.groupby("coin").apply(lambda g: pd.Series({"n": len(g), "corr_d_ex": g["d"].corr(g["ex"]),
                                                       "corr_past30_ex": g["past30"].corr(g["ex"])}))
    out["per coin corr"] = z
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; dd.append(t)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book by weekday"] = D.groupby("wd").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    out["book by coin"] = D.groupby("coin").agg(book=("book_return", "mean"), sd=("book_return", "std"), coin=("coin_return", "mean"))
    return out
