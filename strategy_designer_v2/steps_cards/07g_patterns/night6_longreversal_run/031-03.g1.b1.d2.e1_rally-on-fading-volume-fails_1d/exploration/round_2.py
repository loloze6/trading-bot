def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}; usual = {}
    for coin, ws in bars.items():
        allr = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 14, 14)
            allr += list(c[idx + 14] / c[idx] - 1)
        drift[coin] = np.mean(allr); usual[coin] = np.std(allr, ddof=1)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]; dv = v * c
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            f = pd.DataFrame({
                "vr": v.rolling(14).mean() / v.rolling(30).mean() - 1,
                "dvr": dv.rolling(14).mean() / dv.rolling(30).mean() - 1,
                "vr7": v.rolling(7).mean() / v.rolling(30).mean() - 1,
                "ret14": c / c.shift(14) - 1,
                "ret28z": (c / c.shift(28) - 1) / (vol20 * np.sqrt(28)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            idx = np.arange(0, len(c) - 14, 14)
            g = f.iloc[idx].copy()
            fw = c.values[idx + 14] / c.values[idx] - 1
            g["ex"] = fw - drift[coin]
            g["exs"] = g["ex"] / usual[coin]
            g["coin"] = coin; g["w"] = w
            rows.append(g)
    d = pd.concat(rows).dropna(subset=["vr", "ex"])
    def ct(s, days):
        x = pd.DataFrame({"x": s.values - s.mean(), "d": days.values}).groupby("d")["x"].sum()
        G = len(x); n = len(s)
        se = np.sqrt((x ** 2).sum() * G / (G - 1)) / n
        return s.mean() / se, G
    out = {}
    def quint(df, col, q=5):
        df = df.dropna(subset=[col]).copy()
        df["bin"] = pd.qcut(df[col], q, labels=False, duplicates="drop")
        res = []
        for k, gg in df.groupby("bin"):
            t, G = ct(gg["ex"], gg["day"])
            res.append([k, gg[col].min(), gg[col].max(), len(gg), gg["ex"].mean(), gg["exs"].mean(), t, G])
        return pd.DataFrame(res, columns=["bin", "lo", "hi", "n", "mean_ex", "strength", "t_dayclust", "days"]).round(4)
    out["vr quint all"] = quint(d, "vr")
    out["dollar vr quint"] = quint(d, "dvr")
    out["vr7 quint"] = quint(d, "vr7")
    out["vr quint, ret14>0"] = quint(d[d["ret14"] > 0], "vr")
    out["vr quint, ret14<=0"] = quint(d[d["ret14"] <= 0], "vr")
    # signed-by-vr per-case: ex * sign... regression slope clustered
    d["z"] = (d["vr"] - d["vr"].mean()) / d["vr"].std()
    d["prod"] = d["z"] * d["exs"]
    t, G = ct(d["prod"], d["day"])
    out["vr-exs product, day-clust"] = pd.Series({"mean": d["prod"].mean(), "t": t, "days": G, "n": len(d)}).round(4)
    # partial: residualize vr on ret28z
    e = d.dropna(subset=["ret28z"]).copy()
    bb = np.polyfit(e["ret28z"], e["vr"], 1)
    e["vres"] = e["vr"] - np.polyval(bb, e["ret28z"])
    out["vr resid on ret28z quint"] = quint(e, "vres")
    out["ret28z quint dayclust"] = quint(e, "ret28z")
    out["corr vr ret28z"] = float(np.corrcoef(e["vr"], e["ret28z"])[0, 1])
    # by year: spearman of vr and ex
    yr = []
    for y, gg in d.groupby("year"):
        r = stats.spearmanr(gg["vr"], gg["ex"]).correlation
        top = gg[gg["vr"] > 0.21]["ex"].mean(); bot = gg[gg["vr"] < -0.21]["ex"].mean()
        yr.append([y, len(gg), r, top, bot])
    out["vr by year"] = pd.DataFrame(yr, columns=["year", "n", "spearman", "ex_vr>0.21", "ex_vr<-0.21"]).round(4)
    cc = []
    for coin, gg in d.groupby("coin"):
        cc.append([coin, len(gg), stats.spearmanr(gg["vr"], gg["ex"]).correlation])
    cc = pd.DataFrame(cc, columns=["coin", "n", "spearman"]).round(3)
    out["vr by coin"] = cc
    out["coins positive share"] = float((cc["spearman"] > 0).mean())
    # weekday day-clustered: coins' mean per day
    D = []
    for coin, ws in data["days"].items():
        for w, x in ws.items():
            D.append(x[["day", "coin_return"]])
    D = pd.concat(D).dropna()
    m = D.groupby("day")["coin_return"].mean().reset_index()
    m["wd"] = pd.to_datetime(m["day"]).dt.weekday
    out["weekday, coins' mean per day"] = m.groupby("wd")["coin_return"].agg(["mean", "std", "size"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["size"]))).round(5)
    return out
