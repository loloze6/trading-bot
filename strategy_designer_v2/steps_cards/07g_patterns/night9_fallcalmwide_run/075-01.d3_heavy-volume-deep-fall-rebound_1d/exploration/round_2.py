def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            allr.append(b["close"].pct_change())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            d["ts"] = pd.to_datetime(b["timestamp"])
            d["r"] = r
            d["sr"] = r / r.rolling(30, min_periods=20).std()
            d["vr"] = b["volume"] / b["volume"].rolling(20, min_periods=10).mean()
            d["lvr"] = np.log(d["vr"])
            d["tr60"] = c / c.shift(60) - 1
            d["vol30"] = r.rolling(30, min_periods=20).std()
            d["vol30rel"] = d["vol30"] / d["vol30"].rolling(60, min_periods=20).median()
            d["f1"] = c.shift(-1) / c - 1 - mu
            d["f2"] = c.shift(-2) / c - 1 - 2 * mu
            d["f1raw"] = c.shift(-1) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["up"] = D["r"] > 0
    D["day"] = D["ts"].dt.floor("D")
    D["yr"] = D["ts"].dt.year
    def tclus(x, key):
        x = x.dropna(); k = key.loc[x.index]
        s = (x - x.mean()).groupby(k).sum()
        n = len(s)
        if n < 3: return np.nan
        se = np.sqrt((s**2).sum() * n / (n - 1)) / len(x)
        return x.mean() / se if se > 0 else np.nan
    def st(g, y="f1"):
        return pd.Series({"n": g[y].notna().sum(), "mean": g[y].mean(), "t": tclus(g[y], g["day"])})
    res = {}
    U = D[D.up].dropna(subset=["vr", "sr", "f1"]).copy()
    U["vq"] = pd.qcut(U.vr, 3, labels=False)
    U["sq"] = pd.qcut(U.sr, 3, labels=False)
    res["up days vol tercile x scaled ret tercile"] = U.groupby(["vq", "sq"]).apply(st)
    # graded: weakness score = -lvr - sr  on up days
    U["weak"] = -U.lvr - U.sr
    U["wq"] = pd.qcut(U.weak, 5, labels=False)
    res["up days by weakness (light vol, small rise) quint"] = U.groupby("wq").apply(st)
    res["up days weakness top quint by year"] = U[U.wq == 4].groupby("yr").apply(st)
    res["up days weakness bottom-quint by year"] = U[U.wq == 0].groupby("yr").apply(st)
    G = U[U.pos % 2 == 0]
    res["up days weakness quint f2 grid"] = G.groupby("wq").apply(lambda g: st(g, "f2"))
    U["trd"] = np.select([U.tr60 > 0.1, U.tr60 < -0.1], ["rising", "falling"], "choppy")
    U.loc[U.tr60.isna(), "trd"] = "na"
    res["up weak top quint by 60d trend"] = U[U.wq == 4].groupby("trd").apply(st)
    res["up all by 60d trend"] = U.groupby("trd").apply(st)
    U["agi"] = np.where(U.vol30rel > 1, "agitated", "calm")
    res["up weak top quint by agitation"] = U[U.wq == 4].groupby("agi").apply(st)
    # all days by volume alone (brief claim)
    A = D.dropna(subset=["vr", "f1"]).copy()
    A["vq"] = pd.qcut(A.vr, 5, labels=False)
    res["all days by volratio"] = A.groupby("vq").apply(st)
    # spearman-like slope of f1 on weak, per year
    res["corr f1 weak by year"] = U.groupby("yr").apply(lambda g: pd.Series({"n": len(g), "rho": g[["weak", "f1"]].corr(method="spearman").iloc[0, 1]}))
    res["up weak top quint by coin"] = U[U.wq == 4].groupby("coin").apply(st)
    return res
