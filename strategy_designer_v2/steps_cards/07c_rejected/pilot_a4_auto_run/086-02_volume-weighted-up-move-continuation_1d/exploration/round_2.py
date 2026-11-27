def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [3, 5, 10]
    drift = {}
    rows = []
    for coin, wins in data["bars"].items():
        for h in H:
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(allr) if allr else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            z = r1 / sd
            vr = b["volume"] / b["volume"].rolling(20).mean()
            r3 = c / c.shift(3) - 1
            r5 = c / c.shift(5) - 1
            r10 = c / c.shift(10) - 1
            fc = (b["regime"] == "unknown").values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            n = len(c)
            for h in H:
                for i in range(n - h):
                    if not fc[i]:
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, off=i % h, year=yr[i], i=i,
                                     z=z[i], vr=vr[i], r1=r1[i],
                                     r3s=r3[i] / sd[i] if sd[i] > 0 else np.nan,
                                     r5s=r5[i] / sd[i] if sd[i] > 0 else np.nan,
                                     r10s=r10[i] / sd[i] if sd[i] > 0 else np.nan,
                                     unus=c[i + h] / c[i] - 1 - drift[(coin, h)]))
    df = pd.DataFrame(rows).dropna(subset=["z", "vr", "unus"])
    out = {}
    # per grid offset: spearman of each past measure with forward unusual move
    res = []
    for h in H:
        for off in range(h):
            g = df[(df.h == h) & (df.off == off)]
            if len(g) < 20:
                continue
            d = dict(h=h, off=off, n=len(g))
            for col in ["z", "vr", "r3s", "r5s", "r10s"]:
                gg = g.dropna(subset=[col])
                d["rho_" + col] = stats.spearmanr(gg[col], gg["unus"])[0]
            up = g[g.r1 > 0]
            d["n_up"] = len(up)
            d["up_minus_down"] = up["unus"].mean() - g[g.r1 <= 0]["unus"].mean()
            d["rho_vr_up"] = stats.spearmanr(up["vr"], up["unus"])[0]
            d["rho_z_up"] = stats.spearmanr(up["z"], up["unus"])[0]
            res.append(d)
    out["by_offset"] = pd.DataFrame(res)
    # pooled over offsets h=5, mean by quintile with t from offset-averaged means
    a = df[df.h == 5].copy()
    for col in ["z", "r3s", "r5s"]:
        a[col + "_q"] = pd.qcut(a[col], 5, labels=False)
        tab = a.groupby([col + "_q", "off"])["unus"].mean().unstack()
        out["h5_" + col + "_quintile_mean_by_offset"] = tab.assign(mean=tab.mean(axis=1))
    up = a[a.r1 > 0].copy()
    up["vr_t"] = pd.qcut(up["vr"], 3, labels=["light", "mid", "heavy"])
    up["z_t"] = pd.qcut(up["z"], 3, labels=["small", "mid", "big"])
    out["h5_up_z_by_vr_mean"] = up.groupby(["z_t", "vr_t"])["unus"].agg(["count", "mean"])
    # by window and coin: rho of z with unusual (all offsets pooled)
    out["h5_rho_z_by_coin"] = a.groupby("coin").apply(lambda g: pd.Series(dict(n=len(g), rho_z=stats.spearmanr(g.z, g.unus)[0], rho_r3=stats.spearmanr(g.r3s.dropna(), g.loc[g.r3s.notna(), "unus"])[0])))
    out["h5_rho_z_by_year"] = a.groupby("year").apply(lambda g: pd.Series(dict(n=len(g), rho_z=stats.spearmanr(g.z, g.unus)[0], rho_vr=stats.spearmanr(g.vr, g.unus)[0])))
    out["h5_rho_z_by_window"] = a.groupby("w").apply(lambda g: pd.Series(dict(n=len(g), rho_z=stats.spearmanr(g.z, g.unus)[0] if len(g) > 5 else np.nan)))
    return out
