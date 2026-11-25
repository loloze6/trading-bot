def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            h, l, c = b["high"], b["low"], b["close"]
            rng = h - l
            base = rng.shift(1).rolling(20).mean()
            d = pd.DataFrame({"coin": coin, "win": w,
                              "year": pd.to_datetime(b["timestamp"]).dt.year,
                              "pos": np.arange(len(b))})
            d["loc"] = ((h - c) / rng.replace(0, np.nan))
            d["mult"] = rng / base
            d["raw"] = (h - c) / base
            d["fc"] = b["forecast"]
            d["ret20"] = c / c.shift(20) - 1
            d["r1"] = c.shift(-1) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["r1"] - D["coin"].map(D.groupby("coin")["r1"].mean())
    D = D.dropna(subset=["x1"])
    out = {}
    def terc(df, col):
        return df.groupby("coin")[col].transform(
            lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    def tmb(df, grp, ycol="x1"):
        t = df[df[grp] == 2]; bo = df[df[grp] == 0]
        if len(t) < 20 or len(bo) < 20:
            return (np.nan, np.nan, len(t))
        a = t.groupby(["win", "pos"])[ycol].mean(); bb = bo.groupby(["win", "pos"])[ycol].mean()
        return (a.mean() - bb.mean(), stats.ttest_ind(a, bb, equal_var=False).statistic, len(t))
    D["T_fc"] = terc(D, "fc")
    dn = D[D["ret20"] < 0].copy(); up = D[D["ret20"] >= 0].copy()
    # terciles re-ranked within the downtrend
    dn["Tw"] = terc(dn, "fc"); up["Tw"] = terc(up, "fc")
    out["within_regime_terciles"] = pd.DataFrame([
        dict(zip(["diff", "t", "n_top"], tmb(dn, "Tw")), regime="ret20<0"),
        dict(zip(["diff", "t", "n_top"], tmb(up, "Tw")), regime="ret20>=0")])
    r = []
    for k, g in dn.groupby("coin"):
        m, t, n = tmb(g, "Tw"); r.append({"coin": k, "diff": m, "t": t, "n": n})
    out["downtrend_by_coin"] = pd.DataFrame(r)
    r = []
    for k, g in dn.groupby("year"):
        m, t, n = tmb(g, "Tw"); r.append({"year": k, "diff": m, "t": t, "n": n})
    out["downtrend_by_year"] = pd.DataFrame(r)
    # depth of decline grading: terciles of ret20 among downtrend, top-fc-tercile excess
    dn["Dq"] = dn.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    r = []
    for k, g in dn.groupby("Dq"):
        m, t, n = tmb(g, "Tw"); r.append({"depth_tercile(0=deepest)": k, "diff": m, "t": t, "n": n})
    out["downtrend_by_depth"] = pd.DataFrame(r)
    # loc x mult 3x3 means, all data
    D["Tl"] = terc(D, "loc"); D["Tm"] = terc(D, "mult")
    out["loc_x_mult_mean_x1"] = D.pivot_table(index="Tl", columns="Tm", values="x1", aggfunc="mean")
    dn["Tl"] = terc(dn, "loc"); dn["Tm"] = terc(dn, "mult")
    out["downtrend_loc_x_mult_mean_x1"] = dn.pivot_table(index="Tl", columns="Tm", values="x1", aggfunc="mean")
    out["downtrend_loc_x_mult_count"] = dn.pivot_table(index="Tl", columns="Tm", values="x1", aggfunc="count")
    # top decile of fc
    D["Dec"] = D.groupby("coin")["fc"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    g = D.groupby("Dec")["x1"]
    out["fc_decile_x1"] = pd.DataFrame({"mean": g.mean(), "n": g.count(), "t": g.mean() / g.std() * np.sqrt(g.count())})
    # share of downtrend bars
    out["share_downtrend"] = float((D["ret20"] < 0).mean())
    return out
