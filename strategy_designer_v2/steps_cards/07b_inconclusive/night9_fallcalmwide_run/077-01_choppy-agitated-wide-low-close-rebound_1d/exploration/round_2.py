import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    allrows = []
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
            r = c.pct_change()
            df["width"] = rng / rng.rolling(30, min_periods=30).mean()
            df["loc"] = (c - l) / rng.replace(0, np.nan)
            s30 = r.rolling(30).std()
            df["rngvol"] = rng / c / s30
            df["prod"] = (h - c) / c / s30
            df["f1"] = c.shift(-1) / c - 1 - mu
            df["f2"] = c.shift(-2) / c - 1 - 2 * mu
            df["tr60"] = c / c.shift(60) - 1
            df["agit"] = s30 > s30.rolling(250, min_periods=120).median()
            df["coin"] = coin; df["win"] = w
            df["day"] = pd.to_datetime(df["timestamp"]).dt.floor("D")
            df["year"] = pd.to_datetime(df["timestamp"]).dt.year
            allrows.append(df)
    a = pd.concat(allrows).dropna(subset=["width", "loc", "f1", "tr60", "rngvol"])

    def summ(g, col="f1"):
        x = g.dropna(subset=[col])
        n = len(x)
        if n < 3:
            return pd.Series({"n": n, "days": x["day"].nunique(), "mean%": 100 * x[col].mean(), "t_day": np.nan})
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / n
        return pd.Series({"n": n, "days": G, "mean%": 100 * m, "t_day": m / se})

    out = {}
    a["tb"] = pd.cut(a["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"]).astype(str)
    a["ag"] = np.where(a["agit"], "agit", "calm")
    wl = a[(a["width"] >= 1) & (a["loc"] <= 0.25)].copy()
    out["wide low close by trend x agitation f1"] = wl.groupby(["tb", "ag"]).apply(summ)
    out["wide low close by trend x agitation f2"] = wl.groupby(["tb", "ag"]).apply(lambda g: summ(g, "f2"))
    ca = wl[(wl["tb"] == "chop") & (wl["ag"] == "agit")].copy()
    if len(ca) > 6:
        ca["pq"] = pd.qcut(ca["prod"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
        out["choppy agitated wide-low by raw product tercile"] = ca.groupby("pq").apply(summ)
        ca["wq"] = pd.cut(ca["width"], [1, 1.5, 2, 100]).astype(str)
        out["choppy agitated wide-low by width"] = ca.groupby("wq").apply(summ)
        out["choppy agitated slope f1 on prod"] = float(np.polyfit(ca["prod"], ca["f1"], 1)[0])
    cs = a[a["forecast"] > 0].copy()
    out["cases corr forecast vs raw prod"] = float(cs[["forecast", "prod"]].corr().iloc[0, 1]) if len(cs) > 3 else np.nan
    out["cases slope f1 on prod"] = float(np.polyfit(cs["prod"], cs["f1"], 1)[0]) if len(cs) > 3 else np.nan
    out["cases slope f1 on forecast"] = float(np.polyfit(cs["forecast"], cs["f1"], 1)[0]) if len(cs) > 3 else np.nan
    # graded over all choppy agitated days: low-close nearness * width, any width
    chag = a[(a["tb"] == "chop") & (a["ag"] == "agit")].copy()
    chag["g"] = chag["rngvol"] * (1 - chag["loc"])
    chag["gq"] = pd.qcut(chag["g"].rank(method="first"), 5, labels=list("12345"))
    out["choppy agitated all days by width*lownearness quintile"] = chag.groupby("gq").apply(summ)
    return out
