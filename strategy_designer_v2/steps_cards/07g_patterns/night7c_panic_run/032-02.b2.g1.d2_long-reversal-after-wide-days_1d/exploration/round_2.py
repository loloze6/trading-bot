def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c, h, l, o = b["close"], b["high"], b["low"], b["open"]
            rng = h - l
            d = pd.DataFrame({"day": ts.dt.floor("D").values, "year": ts.dt.year.values})
            d["coin"] = coin; d["win"] = w
            d["clv"] = ((h - c) / rng.replace(0, np.nan)).values
            d["rmult"] = (rng / rng.shift(1).rolling(20).mean()).values
            lr = np.log(c).diff()
            vol20 = lr.rolling(20).std()
            d["vol20"] = vol20.values
            for k in [5, 10, 20]:
                d[f"r{k}"] = (c / c.shift(k) - 1).values
                d[f"z{k}"] = (np.log(c / c.shift(k)) / (vol20 * np.sqrt(k))).values
            d["newlow30"] = (c < c.shift(1).rolling(30).min()).astype(float).values
            d["fc"] = b["forecast"].values
            for H in [1, 3, 5, 10]:
                d[f"f{H}"] = (c.shift(-H) / c - 1).values
            d["pos"] = np.arange(len(b))
            d["alloc"] = b["postRebalance_current_allocation"].values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for H in [1, 3, 5, 10]:
        dr = D[D.pos % H == 0].groupby("coin")[f"f{H}"].mean()
        D[f"e{H}"] = D[f"f{H}"] - D["coin"].map(dr)

    def hl(col, H, sub=None, q=5):
        X = D[D.pos % H == 0] if sub is None else sub[sub.pos % H == 0]
        y = f"e{H}"
        X = X.dropna(subset=[col, y]).copy()
        X["g"] = X.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        a = X[X.g == q-1].groupby("day")[y].mean(); bb = X[X.g == 0].groupby("day")[y].mean()
        return 100*(a.mean()-bb.mean()), stats.ttest_ind(a, bb, equal_var=False).statistic, len(a), len(bb)
    res = {}
    out = []
    for col in ["r5", "r10", "r20", "z5", "z10", "z20", "clv", "fc"]:
        for H in [1, 3, 5, 10]:
            m, t, na, nb = hl(col, H)
            out.append({"col": col, "H": H, "top-bot%": round(m, 3), "t": round(t, 2), "days_top": na, "days_bot": nb})
    res["momentum_grid"] = pd.DataFrame(out)
    # consistency across windows and years for z10 at H=5 and r5 at H=3
    def by(colgrp, col, H):
        o = []
        for g, G in D.groupby(colgrp):
            try:
                m, t, na, nb = hl(col, H, G, q=3)
                o.append({colgrp: g, "top-bot%": round(m, 3), "t": round(t, 2)})
            except Exception:
                pass
        return pd.DataFrame(o)
    res["z10_H5_by_window"] = by("win", "z10", 5)
    res["z10_H5_by_coin"] = by("coin", "z10", 5)
    res["r5_H3_by_year"] = by("year", "r5", 3)
    # clv x rmult interaction at H=1
    X = D.dropna(subset=["clv", "rmult", "e1"]).copy()
    X["cg"] = X.groupby("coin")["clv"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    X["rg"] = X.groupby("coin")["rmult"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    res["clv_x_rmult_e1_mean%"] = (X.groupby(["rg", "cg"])["e1"].mean().unstack() * 100).round(3)
    res["clv_x_rmult_counts"] = X.groupby(["rg", "cg"]).size().unstack()
    # brief: new 30-day close low in volatile decline
    B = D[(D.r20 < 0)].copy()
    B["hv"] = B.groupby("coin")["vol20"].transform(lambda s: s > s.median())
    B = B[B.hv]
    o = []
    for H in [1, 3, 5]:
        a = B[B.newlow30 == 1].dropna(subset=[f"e{H}"]).groupby("day")[f"e{H}"].mean()
        bb = B[B.newlow30 == 0].dropna(subset=[f"e{H}"]).groupby("day")[f"e{H}"].mean()
        o.append({"H": H, "days_low": len(a), "mean_low%": 100*a.mean(), "days_other": len(bb), "mean_other%": 100*bb.mean(),
                  "t": stats.ttest_ind(a, bb, equal_var=False).statistic})
    res["brief_newlow30"] = pd.DataFrame(o).round(3)
    # book: largest gains/losses days - what preceded
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    Dy = pd.concat(dd, ignore_index=True)
    Dy["day"] = pd.to_datetime(Dy["day"]).dt.floor("D")
    bk = Dy.groupby("day")["book_return"].mean().dropna()
    M = D.groupby("day")[["z10", "clv", "rmult", "alloc"]].mean()
    M["bk_next"] = bk.reindex(M.index).values
    M = M.dropna()
    M["bg"] = pd.qcut(M["bk_next"].rank(method="first"), 10, labels=False)
    res["book_decile_vs_sameday_state"] = M.groupby("bg")[["bk_next", "z10", "clv", "rmult", "alloc"]].mean().round(4)
    return res
