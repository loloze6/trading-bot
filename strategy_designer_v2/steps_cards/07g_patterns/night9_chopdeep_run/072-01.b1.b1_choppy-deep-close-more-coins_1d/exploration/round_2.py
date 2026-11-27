import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            hh20 = b["high"].rolling(20).max()
            pos = np.arange(len(b))
            for h in (1, 2, 3, 5):
                b[f"f{h}"] = c.shift(-h) / c - 1
                b[f"g{h}"] = (pos % h == 0)
            b["depth"] = (c - hh20) / hh20 / vol20
            b["rz"] = r1 / vol20.shift(1)
            b["r1"] = r1
            b["vol20"] = vol20
            b["ret60"] = c / c.shift(59) - 1 if len(b) > 60 else np.nan
            b["coin"] = coin; b["win"] = w
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["choppy"] = (b["regime"] == "unknown")
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    df = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 3, 5):
        drift = df[df[f"g{h}"]].groupby("coin")[f"f{h}"].mean()
        df[f"x{h}"] = df[f"f{h}"] - df["coin"].map(drift)
    df["vrank"] = df.groupby("coin")["vol20"].rank(pct=True)

    def ct(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 5: return (np.nan, np.nan, len(s), 0)
        m = s[col].mean()
        dev = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return (m, m / se if se > 0 else np.nan, len(s), s["day"].nunique())

    def tab(sub, key, h, q=5):
        s = sub[sub[f"g{h}"]].dropna(subset=[key, f"x{h}"]).copy()
        s["bin"] = pd.qcut(s[key].rank(method="first"), q, labels=False)
        out = []
        for bn, g in s.groupby("bin"):
            m, t, n, nd = ct(g, f"x{h}")
            out.append([bn, g[key].mean(), m, t, n, nd])
        return pd.DataFrame(out, columns=["bin", "key", "mean_x", "t_day", "n", "days"]).set_index("bin")

    res = {}
    ch = df[df["choppy"]]; nch = df[~df["choppy"]]
    res["choppy depth x5 clustered"] = tab(ch, "depth", 5)
    res["choppy depth x1 clustered"] = tab(ch, "depth", 1)
    res["choppy upday depth x1 cl"] = tab(ch[ch["r1"] > 0], "depth", 1)
    res["all rz x1 clustered"] = tab(df, "rz", 1)
    res["choppy rz x1 cl"] = tab(ch, "rz", 1)
    res["nonchoppy rz x1 cl"] = tab(nch, "rz", 1)
    res["hivol rz x1 cl"] = tab(df[df["vrank"] > 0.5], "rz", 1)
    res["lovol rz x1 cl"] = tab(df[df["vrank"] <= 0.5], "rz", 1)
    res["upday rz x1 cl"] = tab(df[df["r1"] > 0], "rz", 1)
    res["downday rz x2 cl"] = tab(df[df["r1"] < 0], "rz", 2)
    res["nonchoppy depth x5 cl"] = tab(nch, "depth", 5)
    # weekday, clustered by day
    out = []
    s = df[df["g1"]]
    for wd, g in s.groupby("wd"):
        out.append([wd, *ct(g, "x1")])
    res["weekday x1 cl"] = pd.DataFrame(out, columns=["wd", "mean", "t_day", "n", "days"]).set_index("wd")
    # deepest choppy quintile x5 by year and by window
    s = ch[ch["g5"]].dropna(subset=["depth", "x5"]).copy()
    cut = s["depth"].quantile(0.2)
    deep = s[s["depth"] <= cut]
    out = []
    for y, g in deep.groupby("year"):
        out.append([y, *ct(g, "x5")])
    res["choppy deepest q x5 by year"] = pd.DataFrame(out, columns=["year", "mean", "t", "n", "days"]).set_index("year")
    out = []
    for cn, g in deep.groupby("coin"):
        out.append([cn, *ct(g, "x5")])
    res["choppy deepest q x5 by coin"] = pd.DataFrame(out, columns=["coin", "mean", "t", "n", "days"]).set_index("coin")
    # spearman slope of rz->x1 per year
    out = []
    s1 = df[df["g1"]].dropna(subset=["rz", "x1"])
    for y, g in s1.groupby("year"):
        out.append([y, g[["rz", "x1"]].corr(method="spearman").iloc[0, 1], len(g)])
    res["rz x1 spearman by year"] = pd.DataFrame(out, columns=["year", "rho", "n"]).set_index("year")
    return res
