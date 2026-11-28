def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for H in [3, 5, 10]:
        for coin, wins in data["bars"].items():
            allf = []
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].astype(float)
                r = c.pct_change()
                sd30 = r.rolling(30, min_periods=20).std()
                ret60 = c / c.shift(60) - 1
                dn = (r < 0).astype(int)
                run = dn.groupby((dn == 0).cumsum()).cumsum()
                prevrun = run.shift(1)
                hi20 = (c / c.rolling(20, min_periods=10).max() - 1) / sd30
                hi60 = (c / c.rolling(60, min_periods=30).max() - 1) / sd30
                lo20 = (c / c.rolling(20, min_periods=10).min() - 1) / sd30
                z20 = (c / c.shift(20) - 1) / (sd30 * np.sqrt(20))
                f = c.shift(-H) / c - 1
                grid = np.arange(len(b)) % H == 0
                allf.append(pd.DataFrame({"H": H, "coin": coin, "win": w, "f": f, "grid": grid,
                    "inprof": b["regime"].isin(["trending", "unknown"]).values,
                    "turn": (b["regime"] == "trending").values,
                    "ret60": ret60, "hi20": hi20, "hi60": hi60, "lo20": lo20, "z20": z20,
                    "zr": r / sd30, "prevrun": prevrun,
                    "year": pd.to_datetime(b["timestamp"]).dt.year}))
            d = pd.concat(allf, ignore_index=True)
            g = d[d.grid & d.f.notna()]
            d["u"] = d.f - g.f.mean()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    G = D[D.grid & D.u.notna() & D.inprof]
    res = []
    for H in [3, 5, 10]:
        s0 = G[G.H == H]
        for col in ["hi20", "hi60", "lo20", "z20", "ret60"]:
            s = s0[[col, "u", "coin", "year"]].dropna()
            rho, p = stats.spearmanr(s[col], s.u)
            q = pd.qcut(s[col].rank(method="first"), 3, labels=False)
            t = stats.ttest_ind(s.u[q == 2], s.u[q == 0], equal_var=False).statistic
            res.append({"H": H, "feat": col, "n": len(s), "rho": rho, "p": p,
                        "low": s.u[q == 0].mean(), "high": s.u[q == 2].mean(), "t_hi_lo": t})
    out["inprof_by_horizon"] = pd.DataFrame(res)
    s = G[G.H == 5][["hi20", "u", "coin", "year"]].dropna()
    out["hi20_rho_by_coin"] = s.groupby("coin").apply(lambda x: pd.Series({"n": len(x), "rho": stats.spearmanr(x.hi20, x.u)[0]}))
    out["hi20_rho_by_year"] = s.groupby("year").apply(lambda x: pd.Series({"n": len(x), "rho": stats.spearmanr(x.hi20, x.u)[0] if len(x) > 5 else np.nan}))
    # turning days only, H=5 all turning bars once per grid
    T = D[(D.H == 5) & D.turn & D.u.notna()]
    tg = T.groupby(T.prevrun.clip(upper=5)).u.agg(["count", "mean", "std"])
    tg["t"] = tg["mean"] / (tg["std"] / np.sqrt(tg["count"]))
    out["turn_by_run_overlap"] = tg
    # book: largest days
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            br.append(dd[["book_return", "coin_return"]].assign(coin=coin))
    B = pd.concat(br).dropna()
    B = B[B.book_return != 0]
    top = B.nlargest(20, "book_return"); bot = B.nsmallest(20, "book_return")
    out["book_extremes"] = pd.Series({"n_active": len(B), "top20_mean": top.book_return.mean(),
        "bot20_mean": bot.book_return.mean(), "sum_top20": top.book_return.sum(),
        "sum_bot20": bot.book_return.sum(), "sum_all": B.book_return.sum()})
    return out
