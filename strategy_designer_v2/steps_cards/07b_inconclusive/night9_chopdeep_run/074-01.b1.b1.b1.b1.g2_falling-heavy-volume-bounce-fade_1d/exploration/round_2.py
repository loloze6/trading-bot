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
            f1 = c.shift(-1) / c - 1
            sd30 = r1.rolling(30).std()
            sdmed = sd30.expanding(30).median()
            for i in range(len(b)):
                rows.append(dict(coin=coin, w=w, year=ts[i].year, day=ts[i].normalize(),
                                 regime=b["regime"][i], fc=b["forecast"][i], r1=r1[i], rr=rr[i], vr=vr[i],
                                 ag=(sd30[i] > sdmed[i]) if pd.notna(sdmed[i]) else np.nan,
                                 f1=f1[i], mu=mu))
    d = pd.DataFrame(rows)
    d["u1"] = -(d["f1"] - d["mu"])
    d["falling"] = d.regime != "chop"

    def st(g, col="u1"):
        g = g.dropna(subset=[col])
        if len(g) < 3:
            return pd.Series(dict(n=len(g), mean=np.nan, t=np.nan, days=0))
        s = g.groupby("day")[col].sum()
        m = g[col].mean()
        se = np.sqrt((s ** 2).sum()) / len(g)
        return pd.Series(dict(n=len(g), mean=m, t=m / se if se > 0 else np.nan, days=len(s)))

    f = d[d.falling]
    out = {}
    out["falling_all_days"] = st(f).to_frame().T
    out["falling_down_days"] = st(f[f.r1 <= 0]).to_frame().T
    out["falling_up_days"] = st(f[f.r1 > 0]).to_frame().T
    out["falling_up_narrow"] = st(f[(f.r1 > 0) & (f.rr <= 1)]).to_frame().T
    out["falling_up_wide_light"] = st(f[(f.r1 > 0) & (f.rr > 1) & (f.vr <= 1)]).to_frame().T
    out["falling_up_wide_heavy"] = st(f[(f.r1 > 0) & (f.rr > 1) & (f.vr > 1)]).to_frame().T
    out["chop_up_days"] = st(d[(~d.falling) & (d.r1 > 0)]).to_frame().T
    up = f[f.r1 > 0].copy()
    up["rq"] = pd.qcut(up.rr.rank(method="first"), 5, labels=False)
    out["falling_up_by_width_quint"] = up.groupby("rq").apply(st)
    up["uq"] = pd.qcut(up.r1.rank(method="first"), 5, labels=False)
    out["falling_up_by_size_quint"] = up.groupby("uq").apply(st)
    out["falling_up_by_agitation"] = up.groupby("ag").apply(st)
    cases = d[(d.regime == "mean_reversion") & (d.fc < 0)]
    out["cases_by_agitation"] = cases.groupby("ag").apply(st)
    out["falling_by_agitation_all"] = f.groupby("ag").apply(st)
    return out
