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
            d["low30"] = (c <= c.rolling(30).min()).astype(float)
            for H in [1, 2, 3, 5]:
                d[f"r{H}"] = c.shift(-H) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    drift = {H: D.groupby("coin")[f"r{H}"].mean() for H in [1, 2, 3, 5]}
    for H in [1, 2, 3, 5]:
        D[f"x{H}"] = D[f"r{H}"] - D["coin"].map(drift[H])

    def terc(col):
        return D.groupby("coin")[col].transform(
            lambda s: pd.qcut(s.rank(method="first"), 3, labels=[0, 1, 2]))

    def tmb(df, grp, ycol):
        t = df[df[grp] == 2].dropna(subset=[ycol])
        bo = df[df[grp] == 0].dropna(subset=[ycol])
        if len(t) < 20 or len(bo) < 20:
            return (np.nan, np.nan, len(t))
        a = t.groupby(["win", "pos"])[ycol].mean()
        bb = bo.groupby(["win", "pos"])[ycol].mean()
        return (a.mean() - bb.mean(), stats.ttest_ind(a, bb, equal_var=False).statistic, len(t))

    for col in ["fc", "raw", "loc", "mult"]:
        D["T_" + col] = terc(col)
    # main by component and horizon
    res = []
    for col in ["fc", "raw", "loc", "mult"]:
        for H in [1, 2, 3, 5]:
            sub = D[D["pos"] % H == 0]
            m, t, n = tmb(sub, "T_" + col, f"x{H}")
            res.append({"signal": col, "H": H, "diff": m, "t": t, "n_top": n})
    out["top_minus_bottom_by_signal_horizon"] = pd.DataFrame(res)
    # by coin, by year (fc, H1)
    r = []
    for k, g in D.groupby("coin"):
        m, t, n = tmb(g, "T_fc", "x1"); r.append({"coin": k, "diff": m, "t": t, "n": n})
    out["by_coin_fc_H1"] = pd.DataFrame(r)
    r = []
    for k, g in D.groupby("year"):
        m, t, n = tmb(g, "T_fc", "x1"); r.append({"year": k, "diff": m, "t": t, "n": n})
    out["by_year_fc_H1"] = pd.DataFrame(r)
    # regime: prior 20d return sign, and monthly low
    r = []
    for name, mask in [("ret20<0", D["ret20"] < 0), ("ret20>=0", D["ret20"] >= 0),
                       ("low30", D["low30"] == 1), ("not_low30", D["low30"] == 0)]:
        for H in [1, 3]:
            sub = D[mask & (D["pos"] % H == 0)]
            m, t, n = tmb(sub, "T_fc", f"x{H}")
            r.append({"regime": name, "H": H, "diff": m, "t": t, "n_top": n})
    out["by_regime_fc"] = pd.DataFrame(r)
    # quintile profile of raw signal, H1 excess mean
    D["Q"] = D.groupby("coin")["raw"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["quintile_raw_H1"] = D.groupby("Q")["x1"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(s.count())])
    # in downtrend: quintiles of raw
    dd = D[D["ret20"] < 0]
    out["quintile_raw_H1_downtrend"] = dd.groupby("Q")["x1"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(s.count())])
    out["corr_fc_raw"] = float(D[["fc", "raw"]].corr().iloc[0, 1])
    return out
