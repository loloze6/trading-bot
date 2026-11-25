def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float); h = d["high"].astype(float); l = d["low"].astype(float)
            n = len(d)
            pos = np.arange(n)
            hi60 = h.shift(1).rolling(60, min_periods=60).max()
            lo60 = l.shift(1).rolling(60, min_periods=60).min()
            hi20 = h.shift(1).rolling(20, min_periods=20).max()
            lo20 = l.shift(1).rolling(20, min_periods=20).min()
            ch = (c - c.shift(60)).abs(); vol = c.diff().abs().rolling(60).sum()
            er = (ch / vol).rolling(5).mean()
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            ret5p = c / c.shift(5) - 1
            ret20p = c / c.shift(20) - 1
            out = pd.DataFrame({"coin": coin, "w": w, "pos": pos,
                "dhi": c / hi60 - 1, "dlo": c / lo60 - 1, "dhi20": c / hi20 - 1, "dlo20": c / lo20 - 1,
                "er": er, "r1": r1, "sd20": sd20, "ret5p": ret5p, "ret20p": ret20p,
                "regime": d["regime"].values, "fc": d["forecast"].astype(float).values,
                "alloc": d["postRebalance_current_allocation"].astype(float).values,
                "wd": pd.to_datetime(d["timestamp"]).dt.weekday.values,
                "yr": pd.to_datetime(d["timestamp"]).dt.year.values,
                "day": pd.to_datetime(d["timestamp"]).dt.floor("D").values})
            for H in (5, 20):
                out[f"f{H}"] = c.shift(-H) / c - 1
                out[f"cell{H}"] = pos // H
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin per horizon (non-overlapping grid)
    drift = {}
    for H in (5, 20):
        g = A[(A.pos % H == 0)].dropna(subset=[f"f{H}"])
        drift[H] = g.groupby("coin")[f"f{H}"].mean()
        A[f"u{H}"] = A[f"f{H}"] - A.coin.map(drift[H])
    res = {}
    def ev(mask, H, sign=1, name=""):
        s = A[mask & A[f"u{H}"].notna()].copy()
        s = s.sort_values("pos").groupby(["coin", "w", f"cell{H}"]).head(1)
        s["x"] = sign * s[f"u{H}"]
        dd = s.groupby("day")["x"].sum()
        m = s["x"].mean()
        se = dd.std(ddof=1) * np.sqrt(len(dd)) / len(s) if len(dd) > 1 else np.nan
        return {"n": len(s), "days": len(dd), "mean_unusual": m, "t_day": m / se if se else np.nan,
                "hit_pos": (s["x"] > 0).mean()}
    tab = {}
    chop = A.er < 0.3; trend = A.er >= 0.3
    for H in (5, 20):
        tab[f"up60_chop_H{H}"] = ev(chop & (A.dhi > 0), H)
        tab[f"up60_trend_H{H}"] = ev(trend & (A.dhi > 0), H)
        tab[f"dn60_chop_H{H}_long"] = ev(chop & (A.dlo < 0), H)
        tab[f"dn60_trend_H{H}_long"] = ev(trend & (A.dlo < 0), H)
        tab[f"up20_all_H{H}"] = ev(A.dhi20 > 0, H)
        tab[f"dn20_all_H{H}_long"] = ev(A.dlo20 < 0, H)
        z = A.r1 / A.sd20
        tab[f"bigup1d_H{H}"] = ev(z > 2, H)
        tab[f"bigdn1d_H{H}_long"] = ev(z < -2, H)
        tab[f"ret20p_top_H{H}"] = ev(A.ret20p > A.groupby("coin").ret20p.transform(lambda x: x.quantile(0.8)), H)
        tab[f"ret20p_bot_H{H}_long"] = ev(A.ret20p < A.groupby("coin").ret20p.transform(lambda x: x.quantile(0.2)), H)
        tab[f"vol_high_H{H}_long"] = ev(A.sd20 > A.groupby("coin").sd20.transform(lambda x: x.quantile(0.8)), H)
        tab[f"vol_low_H{H}_long"] = ev(A.sd20 < A.groupby("coin").sd20.transform(lambda x: x.quantile(0.2)), H)
        tab[f"er_low_H{H}_long"] = ev(A.er < 0.15, H)
        tab[f"er_high_H{H}_long"] = ev(A.er > 0.45, H)
    res["events"] = pd.DataFrame(tab).T
    # graded: correlation of past 20d return z with next 20d unusual on grid
    g = A[(A.pos % 20 == 0)].dropna(subset=["u20", "ret20p", "sd20", "dhi", "er"]).copy()
    g["z20"] = g.ret20p / (g.sd20 * np.sqrt(20))
    gr = {}
    for col in ["z20", "dhi", "dlo", "er", "sd20"]:
        gg = g.dropna(subset=[col])
        r, p = stats.spearmanr(gg[col], gg["u20"])
        gr[col] = {"n": len(gg), "spearman": r, "p": p}
    # within chop
    gc = g[g.er < 0.3]
    for col in ["z20", "dhi", "dlo"]:
        r, p = stats.spearmanr(gc[col], gc["u20"]); gr[col + "_chop"] = {"n": len(gc), "spearman": r, "p": p}
    gt = g[g.er >= 0.3]
    for col in ["z20", "dhi", "dlo"]:
        r, p = stats.spearmanr(gt[col], gt["u20"]); gr[col + "_trend"] = {"n": len(gt), "spearman": r, "p": p}
    res["graded_20d_grid"] = pd.DataFrame(gr).T
    # weekday daily returns
    wdt = A.dropna(subset=["r1"]).groupby("wd")["r1"].agg(["mean", "std", "count"])
    wdt["t"] = wdt["mean"] / (wdt["std"] / np.sqrt(wdt["count"]))
    res["weekday_r1"] = wdt
    # book by year
    dl = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            x = d.copy(); x["coin"] = coin; x["w"] = w; dl.append(x)
    D = pd.concat(dl)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bk["yr"] = pd.to_datetime(bk["day"]).dt.year
    res["book_by_window"] = bk.groupby("w")[["book_return", "coin_return"]].agg(["mean", "count"])
    # trades
    T = []
    for coin in data["trades"]:
        for w, t in data["trades"][coin].items():
            x = t.copy(); x["coin"] = coin; T.append(x)
    T = pd.concat(T)
    T["q"] = pd.qcut(T["entry_forecast"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    res["trades_by_fc_tercile"] = T.groupby("q")["net_profit_loss_percent"].agg(["mean", "median", "count"])
    res["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"])
    return res
