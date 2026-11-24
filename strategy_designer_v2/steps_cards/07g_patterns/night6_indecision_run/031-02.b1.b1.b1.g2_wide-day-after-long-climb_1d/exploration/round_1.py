def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        grid_rets = []
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l)
            ratio = rng / rng.rolling(20).mean()
            r20 = c / c.shift(20) - 1
            r5 = c / c.shift(5) - 1
            body = (c - o) / rng.replace(0, np.nan)
            vol20 = np.log(c).diff().rolling(20).std()
            fwd = c.shift(-3) / c - 1
            idx = np.arange(0, len(b), 3)
            g = pd.DataFrame({"ts": b["timestamp"].values[idx], "ratio": ratio.values[idx], "r20": r20.values[idx],
                              "r5": r5.values[idx], "body": body.values[idx], "vol20": vol20.values[idx],
                              "fwd": fwd.values[idx], "fc": b["forecast"].values[idx],
                              "regime": b["regime"].values[idx]})
            g["coin"] = coin; g["win"] = w
            recs.append(g)
        d = pd.concat(recs)
        d["ex"] = d["fwd"] - d["fwd"].mean()
        rows.append(d)
    D = pd.concat(rows).dropna(subset=["fwd", "ratio", "r20"])
    D["day"] = pd.to_datetime(D["ts"]).dt.floor("D")
    D["wd"] = pd.to_datetime(D["ts"]).dt.weekday
    D["year"] = pd.to_datetime(D["ts"]).dt.year

    def stat(x):
        if len(x) < 5:
            return pd.Series({"n": len(x), "mean": np.nan, "t_day": np.nan})
        s = x.groupby(x.index).sum() if False else None
        dd = x.groupby(D.loc[x.index, "day"] if False else None)
        return None

    def agg(df, by):
        out = []
        for k, gdf in df.groupby(by, observed=True):
            per = gdf.groupby("day")["ex"].sum()
            n = len(gdf); nd = len(per)
            m = gdf["ex"].mean()
            t = per.mean() / (per.std(ddof=1) / np.sqrt(nd)) if nd > 2 else np.nan
            out.append({"group": str(k), "n": n, "days": nd, "mean_ex_%": 100 * m, "t_day": t})
        return pd.DataFrame(out)

    D = D.reset_index(drop=True)
    D["wide"] = np.where(D["ratio"] >= 1.5, "wide", "notwide")
    D["r20q"] = pd.qcut(D["r20"], 5, labels=False)
    D["ratioq"] = pd.cut(D["ratio"], [0, 0.6, 0.8, 1.0, 1.25, 1.5, 2, 3, 99])
    W = D[D["wide"] == "wide"].copy()
    W["absbody"] = pd.cut(W["body"].abs(), [-0.01, 0.2, 0.5, 1.01])
    W["dir"] = np.sign(W["body"])
    W["up20"] = np.where(W["r20"] > 0, "r20+", "r20-")
    res = {}
    res["all_by_r20_quintile_x_wide"] = agg(D, ["wide", "r20q"])
    res["all_by_range_ratio"] = agg(D, "ratioq")
    res["wide_by_dir_x_r20sign"] = agg(W, ["up20", "dir"])
    res["wide_by_flatness_x_r20sign"] = agg(W, ["up20", "absbody"])
    D["volq"] = pd.qcut(D["vol20"], 4, labels=False)
    res["all_by_vol_q_x_wide"] = agg(D, ["volq", "wide"])
    res["all_by_weekday"] = agg(D, "wd")
    res["wide_r20pos_by_year"] = agg(W[W["r20"] > 0], "year")
    D["r5q"] = pd.qcut(D["r5"], 5, labels=False)
    res["notwide_by_r5q"] = agg(D[D["wide"] == "notwide"], "r5q")
    return res
