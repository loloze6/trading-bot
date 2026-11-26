def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            run = np.full(len(c), np.nan); cnt = 0
            for i in range(len(c)):
                if r.iloc[i] > 0: run[i] = cnt
                if r.iloc[i] < 0: cnt += 1
                elif r.iloc[i] > 0: cnt = 0
            vol30 = r.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "r": r, "nxt": nxt, "nxt2": nxt2, "run": run,
                               "zr": r / vol30, "z5": (c / c.shift(5) - 1) / vol30,
                               "tr60": c / c.shift(60) - 1, "tr30": c / c.shift(30) - 1, "vol30": vol30,
                               "rngz": ((h - l) / c) / vol30,
                               "clpos": (c - l) / (h - l).replace(0, np.nan),
                               "day": ts.dt.floor("D"), "wd": ts.dt.weekday,
                               "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["nxt"].transform("mean")
    D["un"] = D["nxt"] - mu
    D["agit"] = np.where(D["vol30"] > D.groupby("coin")["vol30"].transform("median"), "agit", "calm")
    D["trend"] = np.where(D["tr60"] < -0.10, "falling", np.where(D["tr60"] > 0.10, "rising", np.where(D["tr60"].notna(), "choppy", "na")))
    # trend on 30 days for na rows, as a proxy
    D["trend30"] = np.where(D["tr30"] < -0.07, "falling", np.where(D["tr30"] > 0.07, "rising", np.where(D["tr30"].notna(), "choppy", "na")))
    def tt(g, col="un"):
        g = g.dropna(subset=[col])
        s = g.groupby("day")[col].apply(lambda x: (x - g[col].mean()).sum())
        nd = len(s); n = len(g)
        se = np.sqrt((s ** 2).sum() * nd / max(nd - 1, 1)) / n if n > 0 else np.nan
        return pd.Series({"n": n, "days": nd, "mean": g[col].mean(), "t_day": g[col].mean() / se if n > 2 else np.nan})
    out = {}
    F = D[D["trend"] == "falling"].copy()
    F["clb"] = pd.cut(F["clpos"], [0, .2, .4, .6, .8, 1.0], include_lowest=True)
    out["falling_closepos_by_agit"] = F.groupby(["agit", "clb"]).apply(tt).unstack(0) if False else F.groupby(["agit", "clb"]).apply(tt)
    # low close in falling: graded by range width
    LC = F[F["clpos"] <= 0.25].copy()
    LC["rb"] = pd.qcut(LC["rngz"], 3, labels=["narrow", "mid", "wide"])
    out["falling_lowclose_by_range"] = LC.groupby(["agit", "rb"]).apply(tt)
    # mid/high close (not cases of the idea) in falling, excluding run-break up days
    MC = F[(F["clpos"] > 0.4) & ~((F["run"] >= 2))]
    out["falling_midhigh_close_noncase"] = MC.groupby(["agit", MC["r"] > 0]).apply(tt)
    # choppy: up days after runs, by agitation
    C = D[(D["trend"] == "choppy") & D["run"].notna()].copy()
    C["runb"] = C["run"].clip(upper=3)
    out["choppy_upday_by_run_agit"] = C.groupby(["agit", "runb"]).apply(tt)
    # choppy: next by today's z
    C2 = D[D["trend"] == "choppy"].copy()
    C2["zrb"] = pd.cut(C2["zr"], [-99, -1, 0, 1, 99])
    out["choppy_by_zr_agit"] = C2.groupby(["agit", "zrb"]).apply(tt)
    # weekday by trend
    out["weekday_by_trend"] = D[D["trend"] != "na"].groupby(["wd"]).apply(tt)
    out["weekday_all_na_too"] = D.groupby(["wd"]).apply(tt)
    # tested idea in rising market (mirror check) and in falling by agitation
    U = D[D["run"] >= 2].copy()
    out["runbreak_by_trend_agit"] = U.groupby(["trend", "agit"]).apply(tt)
    # book's worst/best days: conditions
    dd = pd.concat([d.assign(coin=c, w=w) for c, ws in data["days"].items() for w, d in ws.items()])
    act = dd[dd["book_return"].abs() > 0]
    out["book_active_days"] = pd.Series({"n": len(act), "mean": act["book_return"].mean(),
                                         "share_pos": (act["book_return"] > 0).mean(),
                                         "q05": act["book_return"].quantile(.05), "q95": act["book_return"].quantile(.95)})
    return out
