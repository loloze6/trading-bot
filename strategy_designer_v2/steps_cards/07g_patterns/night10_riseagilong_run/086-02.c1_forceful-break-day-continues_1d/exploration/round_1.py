def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allf = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            f5 = c.shift(-H) / c - 1
            sd30 = r.rolling(30, min_periods=20).std()
            # down run length ending yesterday / today
            dn = (r < 0).astype(int)
            run = dn.groupby((dn == 0).cumsum()).cumsum()
            prevrun = run.shift(1)
            # depth of run before today: sum of returns over prevrun days
            logr = np.log1p(r)
            cum = logr.cumsum()
            depth = []
            for i in range(len(b)):
                k = prevrun.iloc[i]
                if pd.isna(k) or k == 0 or i - 1 - k < 0:
                    depth.append(0.0 if k == 0 else np.nan)
                else:
                    depth.append(cum.iloc[i - 1] - cum.iloc[int(i - 1 - k)])
            depth = pd.Series(depth)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            clv = (c - b["low"]) / rng
            ret5 = c / c.shift(5) - 1
            ret20 = c / c.shift(20) - 1
            hi20 = c / c.rolling(20, min_periods=10).max() - 1
            volr = b["volume"] / b["volume"].rolling(20, min_periods=10).mean()
            wr = (b["high"] - b["low"]) / c.shift(1) / sd30
            grid = np.arange(len(b)) % H == 0
            df = pd.DataFrame({
                "coin": coin, "win": w, "f5": f5, "grid": grid,
                "inprof": b["regime"].isin(["trending", "unknown"]),
                "turn": b["regime"] == "trending",
                "zr": r / sd30, "prevrun": prevrun, "zdepth": depth / sd30,
                "clv": clv, "z5": ret5 / (sd30 * np.sqrt(5)), "z20": ret20 / (sd30 * np.sqrt(20)),
                "hi20": hi20 / sd30, "volr": volr, "wrange": wr,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc": b["postRebalance_current_allocation"],
            })
            allf.append(df)
        d = pd.concat(allf, ignore_index=True)
        g = d[d.grid & d.f5.notna()]
        drift[coin] = g.f5.mean()
        d["u5"] = d.f5 - drift[coin]
        rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    G = D[D.grid & D.u5.notna()]
    P = G[G.inprof]
    out = {}
    out["counts"] = pd.Series({"grid": len(G), "grid_inprof": len(P), "share_inprof": P.shape[0]/G.shape[0],
                               "inprof_mean_u5": P.u5.mean(),
                               "inprof_t": P.u5.mean()/(P.u5.std()/np.sqrt(len(P))),
                               "notprof_mean_u5": G[~G.inprof].u5.mean()})
    res = []
    for col in ["zr", "prevrun", "zdepth", "clv", "z5", "z20", "hi20", "volr", "wrange"]:
        s = P[[col, "u5"]].dropna()
        rho, p = stats.spearmanr(s[col], s.u5)
        q = pd.qcut(s[col].rank(method="first"), 3, labels=False)
        lo = s.u5[q == 0]; hi = s.u5[q == 2]
        t = stats.ttest_ind(hi, lo, equal_var=False).statistic
        res.append({"feat": col, "n": len(s), "rho": rho, "p": p, "low_tercile": lo.mean(),
                    "mid": s.u5[q == 1].mean(), "high_tercile": hi.mean(), "t_hi_lo": t})
    out["inprof_features"] = pd.DataFrame(res)
    res = []
    for col in ["zr", "z5", "z20", "hi20", "clv", "wrange"]:
        s = G[~G.inprof][[col, "u5"]].dropna()
        rho, p = stats.spearmanr(s[col], s.u5)
        res.append({"feat": col, "n": len(s), "rho": rho, "p": p})
    out["outprof_features"] = pd.DataFrame(res)
    wdg = P.groupby("wd").u5.agg(["count", "mean", "std"])
    wdg["t"] = wdg["mean"] / (wdg["std"] / np.sqrt(wdg["count"]))
    out["inprof_weekday"] = wdg
    cg = P.groupby("coin").u5.agg(["count", "mean"])
    out["inprof_coin"] = cg
    # all bars in profile (not grid) by prevrun on up days
    T = D[D.inprof & D.u5.notna() & (D.zr > 0)]
    tg = T.groupby(T.prevrun.clip(upper=4)).u5.agg(["count", "mean"])
    out["upday_by_prevrun_overlapping"] = tg
    # book daily returns
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            br.append(dd[["book_return", "coin_return"]].assign(coin=coin))
    B = pd.concat(br).dropna()
    out["book"] = pd.Series({"mean": B.book_return.mean(), "q01": B.book_return.quantile(0.01),
                             "q99": B.book_return.quantile(0.99), "share_nonzero": (B.book_return != 0).mean()})
    return out
