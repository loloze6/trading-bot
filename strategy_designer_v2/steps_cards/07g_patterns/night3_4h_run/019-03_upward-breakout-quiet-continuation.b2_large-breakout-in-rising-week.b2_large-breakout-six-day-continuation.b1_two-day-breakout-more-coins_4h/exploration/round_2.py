def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 60:
                continue
            c, hi, lo = b["close"].astype(float), b["high"].astype(float), b["low"].astype(float)
            rng = (hi - lo)
            r180 = rng.rolling(180, min_periods=60).mean()
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            d["brk_up"] = (c - hi.shift(1).rolling(12).max()) / r180
            d["brk_dn"] = (lo.shift(1).rolling(12).min() - c) / r180
            d["quiet"] = rng.shift(1).rolling(12).mean() / r180
            d["r7"] = c / c.shift(42) - 1
            for H in [6, 18, 36]:
                d["fwd%d" % H] = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            d["yr"] = ts.dt.year.values
            d["tb"] = (ts.astype("int64") // (6 * 86400 * 10**9)).values
            d["cell"] = d["pos"] // 36
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for H in [6, 18, 36]:
        g = D[D["pos"] % H == 0].dropna(subset=["fwd%d" % H])
        D["unu%d" % H] = D["fwd%d" % H] - D["coin"].map(g.groupby("coin")["fwd%d" % H].mean())
        D["str%d" % H] = D["unu%d" % H] / D["coin"].map(g.groupby("coin")["fwd%d" % H].std())
    out = {}

    def ev(mask):
        e = D[mask].dropna(subset=["fwd36", "quiet"])
        return e.groupby(["coin", "win", "cell"]).head(1).copy()

    def summ(x):
        r = {"n": len(x)}
        for H in [6, 18, 36]:
            v = x["unu%d" % H].dropna()
            r["m%d" % H] = v.mean()
            r["t%d" % H] = v.mean() / (v.std() / np.sqrt(len(v)))
        r["str36"] = x["str36"].mean()
        cm = x.groupby("tb")["unu36"].mean()
        r["n_dates"] = len(cm)
        r["t36_bydate"] = cm.mean() / (cm.std() / np.sqrt(len(cm)))
        cc = x.groupby("coin")["unu36"].mean()
        r["coins_neg_share"] = (cc < 0).mean()
        return pd.Series(r)

    ed = ev((D["brk_dn"] > 0) & (D["r7"] > 0))
    ed["qq"] = pd.qcut(ed["quiet"], 5, labels=False)
    out["dn_rising_by_quiet_quintile"] = ed.groupby("qq").apply(summ)
    out["dn_rising_spearman_quiet_vs_unu36"] = str(stats.spearmanr(ed["quiet"], ed["unu36"]))
    ed["half"] = np.where(ed["yr"] <= 2021, "early", "late")
    eq = ed[ed["qq"] <= 1]
    out["dn_rising_quietest40pct_by_era"] = eq.groupby("half").apply(summ)
    edn = ev((D["brk_dn"] > 0) & (D["r7"] <= 0))
    edn["qq"] = pd.qcut(edn["quiet"], 5, labels=False)
    out["dn_falling_by_quiet_quintile"] = edn.groupby("qq").apply(summ)

    eu = ev((D["brk_up"] > 0) & (D["r7"] > 0))
    eu["sq"] = pd.qcut(eu["brk_up"], 5, labels=False)
    out["up_rising_by_size_quintile"] = eu.groupby("sq").apply(summ)
    out["up_rising_spearman_size"] = str(stats.spearmanr(eu["brk_up"], eu["unu36"]))
    eu["qq"] = pd.qcut(eu["quiet"], 5, labels=False)
    out["up_rising_by_quiet_quintile"] = eu.groupby("qq").apply(summ)
    out["up_rising_spearman_quiet"] = str(stats.spearmanr(eu["quiet"], eu["unu36"]))
    eu["half"] = np.where(eu["yr"] <= 2021, "early", "late")
    out["up_rising_top_size_by_era"] = eu[eu["sq"] >= 3].groupby("half").apply(summ)
    return out
