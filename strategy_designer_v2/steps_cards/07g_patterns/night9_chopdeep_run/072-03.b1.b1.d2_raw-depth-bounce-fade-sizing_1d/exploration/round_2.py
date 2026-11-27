def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float); h = d["high"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20).std()
            hi20 = h.rolling(20).max()
            depth = (c - hi20) / hi20 / sd20
            tr60 = (c / c.shift(60) - 1) * 100
            sd30 = r.rolling(30).std()
            pos = np.arange(len(d))
            ts = pd.to_datetime(d["timestamp"])
            out = pd.DataFrame({"coin": coin, "w": w, "r": r, "depth": depth, "tr60": tr60,
                                "f10": c.shift(-10) / c - 1, "f5": c.shift(-5) / c - 1,
                                "pos": pos, "day": ts.dt.floor("D"), "sd30": sd30,
                                "alloc": d["postRebalance_current_allocation"].astype(float),
                                "g1": c.shift(-1) / c - 1})
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    # agitation proxy: sd30 vs its 365-bar median within window not available; use within-coin median over all windows
    A["agit"] = A.sd30 > A.groupby("coin").sd30.transform("median")
    A["prof"] = np.where(A.tr60 > 10, "rising", np.where(A.tr60 < -10, "falling", np.where(A.tr60.notna(), "choppy", None)))
    res = {}
    def grid_stats(sub, col, h, label_col):
        out = []
        for key, g in sub.groupby(label_col):
            vals = []
            for off in range(h):
                gg = g[(g.pos % h) == off]
                vals.append(gg)
            allg = pd.concat(vals)
            x = allg.dropna(subset=[col])
            dev = x[col] - x.coin.map(drift[col])
            byday = dev.groupby(x.day).sum()
            n = len(x); nd = len(byday)
            m = dev.mean()
            se = np.sqrt((byday - byday.mean() * 0).pow(2).sum() - 0) / n if n else np.nan
            # clustered se: sqrt(sum_day (sum dev - n_day*m)^2)/n
            cnt = x.groupby("day").size()
            se = np.sqrt(((byday - cnt * m) ** 2).sum()) / n if n else np.nan
            out.append({"key": str(key), "cases_all_offsets": n, "days": nd, "mean%": 100 * m, "t_cl": m / se if se else np.nan,
                        "t_note": "overlap across offsets"})
        return pd.DataFrame(out).set_index("key")
    drift = {"f10": A[A.pos % 10 == 0].groupby("coin").f10.mean(), "f5": A[A.pos % 5 == 0].groupby("coin").f5.mean()}
    A["dbin"] = pd.cut(A.depth, [-100, -6, -4, -2.5, -1, 1e-9], labels=["a<-6", "b-6..-4", "c-4..-2.5", "d-2.5..-1", "e-1..0"])
    # offset 0 grid, clustered, depth x profile, 10d
    G = A[A.pos % 10 == 0].copy()
    def cl(g, col):
        x = g.dropna(subset=[col])
        dev = x[col] - x.coin.map(drift[col]); n = len(x)
        if n < 3: return pd.Series({"n": n})
        m = dev.mean(); cnt = x.groupby("day").size(); s = dev.groupby(x.day).sum()
        se = np.sqrt(((s - cnt * m) ** 2).sum()) / n
        return pd.Series({"n": n, "days": len(s), "mean%": 100 * m, "t_cl": m / se})
    res["10d grid0: profile x agit x depth"] = G.groupby(["prof", "agit", "dbin"]).apply(lambda g: cl(g, "f10"))
    # offset 5 grid as robustness
    G5 = A[A.pos % 10 == 5]
    res["10d grid5: profile x depth"] = G5.groupby(["prof", "dbin"]).apply(lambda g: cl(g, "f10"))
    # choppy deep (<-4) vs window, grid0
    Cd = G[(G.prof == "choppy") & (G.depth < -4)]
    res["choppy depth<-4 10d by window (grid0)"] = Cd.groupby("w").apply(lambda g: cl(g, "f10"))
    # linear slope depth on u10 in choppy, grid0 and grid5
    for nm, GG in [("g0", G), ("g5", G5)]:
        x = GG[(GG.prof == "choppy")].dropna(subset=["depth", "f10"])
        u = x.f10 - x.coin.map(drift["f10"])
        res[f"choppy corr depth vs u10 {nm}"] = pd.Series({"n": len(x), "corr": np.corrcoef(x.depth.clip(-10, 0), u)[0, 1]})
    # book: DOGE and largest days
    D = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; D.append(x)
    D = pd.concat(D, ignore_index=True)
    res["book by coin x window: sum of daily ret, worst 10"] = D.groupby(["coin", "w"]).book_return.sum().sort_values().head(10)
    res["book share of days |ret|>10%"] = pd.Series({"n_days": int((D.book_return.abs() > 0.1).sum()),
                                                      "sum_of_those": D.book_return[D.book_return.abs() > 0.1].sum(),
                                                      "sum_all": D.book_return.sum()})
    return res
