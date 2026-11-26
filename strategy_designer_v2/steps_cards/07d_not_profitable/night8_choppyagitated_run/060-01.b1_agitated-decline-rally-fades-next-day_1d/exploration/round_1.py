def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    bookd = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.shift(1).rolling(30, min_periods=20).std()
            z = r / sd
            inprof = (b["regime"] == "unknown")
            f1 = c.shift(-1) / c - 1
            f2 = c.shift(-2) / c - 1
            f3 = c.shift(-3) / c - 1
            r5 = c / c.shift(5) - 1
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            clv = (c - b["low"]) / rng
            vr = b["volume"] / b["volume"].shift(1).rolling(30, min_periods=10).mean()
            alloc = b["postRebalance_current_allocation"].astype(float)
            pg = alloc * f1
            df = pd.DataFrame({"coin": coin, "w": w, "r": r, "z": z, "inprof": inprof,
                               "f1": f1, "f2": f2, "f3": f3, "r5": r5, "clv": clv, "vr": vr,
                               "alloc": alloc, "pg": pg, "fc": b["forecast"].astype(float),
                               "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "ts": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
        for w, d in data["days"][coin].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = coin; dd["w"] = w
            bookd.append(dd)
    A = pd.concat(rows, ignore_index=True)
    drift = A.groupby("coin")["f1"].mean()
    A["drift"] = A["coin"].map(drift)
    A["u1"] = -(A["f1"] - A["drift"])
    A["s1"] = -A["f1"]; A["s2"] = -A["f2"]; A["s3"] = -A["f3"]
    cases = A[A.inprof & (A.r > 0) & A.f1.notna() & A.z.notna()].copy()
    def summ(g):
        return pd.Series({"n": len(g), "short1": g.s1.mean(), "t1": stats.ttest_1samp(g.s1, 0).statistic if len(g) > 2 else np.nan,
                          "short2": g.s2.mean(), "short3": g.s3.mean(), "unusual1": g.u1.mean(), "pg_mean": g.pg.mean(),
                          "absalloc": g.alloc.abs().mean()})
    cases["zb"] = pd.cut(cases.z, [0, 0.5, 1, 1.5, 2, 3, 99])
    out["cases_by_z"] = cases.groupby("zb", observed=True).apply(summ)
    cases["r5b"] = pd.qcut(cases.r5, 4)
    out["cases_by_prior5d"] = cases.groupby("r5b", observed=True).apply(summ)
    cases["clvb"] = pd.cut(cases.clv, [-0.01, 0.33, 0.66, 1.01])
    out["cases_by_closeloc"] = cases.groupby("clvb", observed=True).apply(summ)
    cases["vrb"] = pd.qcut(cases.vr, 3)
    out["cases_by_volratio"] = cases.groupby("vrb", observed=True).apply(summ)
    out["cases_by_year"] = cases.groupby("year").apply(summ)
    # in-profile non-signal days (condition alone)
    nons = A[A.inprof & (A.r <= 0) & A.f1.notna()]
    out["inprof_down_days_short1"] = pd.Series({"n": len(nons), "short1": nons.s1.mean(), "short2": nons.s2.mean()})
    # position gain by situation
    held = A[A.alloc.abs() > 1e-6]
    out["held_by_sideof_day"] = held.groupby(held.r > 0).agg(n=("pg", "size"), pg=("pg", "mean"), alloc=("alloc", "mean"))
    out["held_by_fc_zero"] = held.groupby(held.fc == 0).agg(n=("pg", "size"), pg=("pg", "mean"))
    # book daily
    D = pd.concat(bookd, ignore_index=True)
    B = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    B = B.dropna()
    B["wn"] = B.w.str[1:].astype(int)
    B = B.sort_values(["wn", "day"])
    B["eq"] = (1 + B.br).cumprod()
    B["dd"] = B.eq / B.eq.cummax() - 1
    out["book_by_window"] = B.groupby("w").agg(days=("br", "size"), mean=("br", "mean"), sd=("br", "std"),
                                               cum=("br", lambda x: (1 + x).prod() - 1), coin=("cr", lambda x: (1 + x).prod() - 1),
                                               mindd=("dd", "min"))
    out["book_maxdd"] = float(B.dd.min())
    # worst 10 book days: coin moves
    worst = B.nsmallest(15, "br")
    out["worst15_days"] = worst[["w", "br", "cr"]].reset_index(drop=True)
    return out
