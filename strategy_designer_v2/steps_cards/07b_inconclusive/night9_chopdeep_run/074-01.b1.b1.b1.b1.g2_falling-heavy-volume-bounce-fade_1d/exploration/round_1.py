def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allret = []
        for w, b in wins.items():
            c = b["close"].values
            allret.append(c[1:] / c[:-1] - 1)
        mu = np.nanmean(np.concatenate(allret))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; v = b["volume"]
            rng = (h - l) / c
            rr = rng / rng.rolling(20).mean()
            vr = v / v.shift(1).rolling(20).mean()
            r1 = c / c.shift(1) - 1
            ts = pd.to_datetime(b["timestamp"])
            for hz in (1, 2, 3, 5):
                b["f%d" % hz] = c.shift(-hz) / c - 1
            sd30 = r1.rolling(30).std()
            for i in range(len(b)):
                rows.append(dict(coin=coin, w=w, year=ts[i].year, day=ts[i].normalize(),
                                 regime=b["regime"][i], fc=b["forecast"][i], r1=r1[i], rr=rr[i], vr=vr[i],
                                 sd30=sd30[i], f1=b["f1"][i], f2=b["f2"][i], f3=b["f3"][i], f5=b["f5"][i], mu=mu))
    d = pd.DataFrame(rows)
    d["u1"] = -(d["f1"] - d["mu"])
    for hz in (2, 3, 5):
        d["u%d" % hz] = -(d["f%d" % hz] - hz * d["mu"])

    def st(g, col="u1"):
        g = g.dropna(subset=[col])
        if len(g) < 3:
            return pd.Series(dict(n=len(g), mean=np.nan, t=np.nan, days=0))
        s = g.groupby("day")[col].sum()
        m = g[col].mean()
        se = np.sqrt((s ** 2).sum()) / len(g)
        return pd.Series(dict(n=len(g), mean=m, t=m / se if se > 0 else np.nan, days=len(s)))

    cases = d[(d.regime == "mean_reversion") & (d.fc < 0)].copy()
    out = {}
    out["all_cases"] = st(cases).to_frame().T
    out["by_horizon"] = pd.DataFrame({hz: st(cases, "u%d" % hz) for hz in (1, 2, 3, 5)}).T
    out["by_coin"] = cases.groupby("coin").apply(st)
    out["by_year"] = cases.groupby("year").apply(st)
    cases["fq"] = pd.qcut(cases.fc.abs().rank(method="first"), 4, labels=False)
    out["by_fc_quart"] = cases.groupby("fq").apply(st)
    cases["rq"] = pd.qcut(cases.rr.rank(method="first"), 4, labels=False)
    out["by_width_quart"] = cases.groupby("rq").apply(st)
    cases["vq"] = pd.qcut(cases.vr.rank(method="first"), 4, labels=False)
    out["by_volratio_quart"] = cases.groupby("vq").apply(st)
    cases["uq"] = pd.qcut(cases.r1.rank(method="first"), 4, labels=False)
    out["by_upday_size_quart"] = cases.groupby("uq").apply(st)
    cases["aq"] = pd.qcut(cases.sd30.rank(method="first"), 2, labels=False)
    out["by_sd30_half"] = cases.groupby("aq").apply(st)
    # comparison: falling-market up days not in the regime
    other = d[(d.regime == "unknown") & (d.r1 > 0)]
    out["other_falling_updays"] = st(other).to_frame().T
    nonfall = d[(d.regime == "chop") & (d.r1 > 0) & (d.rr > 1) & (d.vr > 1)]
    out["nonfalling_wide_heavy_updays"] = st(nonfall).to_frame().T
    out["corr_u1"] = pd.Series(dict(fc=cases[["u1"]].assign(x=cases.fc.abs()).corr().iloc[0, 1],
                                     rr=cases[["u1", "rr"]].corr().iloc[0, 1],
                                     vr=cases[["u1", "vr"]].corr().iloc[0, 1],
                                     r1=cases[["u1", "r1"]].corr().iloc[0, 1]))
    return out
