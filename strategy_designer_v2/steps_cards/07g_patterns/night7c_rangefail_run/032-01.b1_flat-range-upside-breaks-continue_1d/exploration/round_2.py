def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float); h = d["high"].astype(float); l = d["low"].astype(float)
            n = len(d); pos = np.arange(n)
            hi60 = h.shift(1).rolling(60, min_periods=60).max()
            lo60 = l.shift(1).rolling(60, min_periods=60).min()
            ch = (c - c.shift(60)).abs(); vv = c.diff().abs().rolling(60).sum()
            er = (ch / vv).rolling(5).mean()
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            ret20p = c / c.shift(20) - 1
            ret10p = c / c.shift(10) - 1
            ts = pd.to_datetime(d["timestamp"])
            out = pd.DataFrame({"coin": coin, "w": w, "pos": pos,
                "rng": (c - lo60) / (hi60 - lo60), "er": er, "r1": r1, "sd20": sd20,
                "z20": ret20p / (sd20 * np.sqrt(20)), "z10": ret10p / (sd20 * np.sqrt(10)),
                "wd": ts.dt.weekday.values, "yr": ts.dt.year.values, "day": ts.dt.floor("D").values,
                "r1next": c.shift(-1) / c - 1})
            for H in (5, 10, 20):
                out[f"f{H}"] = c.shift(-H) / c - 1
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    res = {}
    # graded momentum: z20 / z10 vs future unusual, grid, by subgroup
    for H in (5, 10, 20):
        g = A[A.pos % H == 0].dropna(subset=[f"f{H}"]).copy()
        dr = g.groupby("coin")[f"f{H}"].mean()
        A[f"u{H}"] = A[f"f{H}"] - A.coin.map(dr)
    out = {}
    for H in (5, 10, 20):
        g = A[A.pos % H == 0].dropna(subset=[f"u{H}", "z20", "er", "rng"]).copy()
        for name, m in [("all", g.er > -1), ("chop", g.er < 0.3), ("chop_veryflat", g.er < 0.15),
                        ("chop_lessflat", (g.er >= 0.15) & (g.er < 0.3))]:
            s = g[m]
            for col in ["z20", "rng"]:
                r, p = stats.spearmanr(s[col], s[f"u{H}"])
                out[f"H{H}_{name}_{col}"] = {"n": len(s), "spearman": r, "p": p}
    res["graded"] = pd.DataFrame(out).T
    # z20 chop by coin and by year, H20 and H10
    g = A[A.pos % 10 == 0].dropna(subset=["u10", "z20", "er"])
    gc = g[g.er < 0.3]
    bc = {}
    for k, s in gc.groupby("coin"):
        r, p = stats.spearmanr(s.z20, s.u10); bc[k] = {"n": len(s), "sp": r}
    for k, s in gc.groupby("yr"):
        r, p = stats.spearmanr(s.z20, s.u10); bc[str(k)] = {"n": len(s), "sp": r}
    res["z20_chop_H10_by_coin_year"] = pd.DataFrame(bc).T
    # quintiles of z20 in chop, H10
    gc = gc.copy(); gc["q"] = pd.qcut(gc.z20, 5, labels=False)
    res["z20_chop_quintile_H10"] = gc.groupby("q")["u10"].agg(["mean", "count"])
    # weekday by year and coin, next-day return
    B = A.dropna(subset=["r1"])
    B = B.assign(frisat=B.wd.isin([4, 5]))
    wy = B.groupby(["yr", "frisat"])["r1"].mean().unstack()
    wy["diff"] = wy[True] - wy[False]
    res["frisat_by_year"] = wy
    wc = B.groupby(["coin", "frisat"])["r1"].mean().unstack(); wc["diff"] = wc[True] - wc[False]
    res["frisat_by_coin"] = wc
    # graded weekday: prior day return vs next by weekday? check Fri/Sat after Thursday drop
    B2 = A.dropna(subset=["r1", "r1next"])
    th = B2[B2.wd == 3]
    r, p = stats.spearmanr(th.r1, th.r1next); res["thu_r1_vs_fri"] = pd.Series({"n": len(th), "sp": r, "p": p})
    allr, allp = stats.spearmanr(B2.r1, B2.r1next); res["all_r1_vs_next"] = pd.Series({"sp": allr, "p": allp})
    # by volatility: z of 1d move vs next 5d in chop
    g5 = A[A.pos % 5 == 0].dropna(subset=["u5", "er", "r1", "sd20"])
    g5 = g5.assign(z1=g5.r1 / g5.sd20)
    for nm, m in [("chop", g5.er < 0.3), ("trend", g5.er >= 0.3)]:
        s = g5[m]; r, p = stats.spearmanr(s.z1, s.u5)
        res[f"z1_vs_u5_{nm}"] = pd.Series({"n": len(s), "sp": r, "p": p})
    return res
