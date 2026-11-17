def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    allfall = []
    coinmean = {}
    for coin, wins in bars.items():
        # coin mean h-bar returns over non-overlapping grid
        for h in [1, 2, 3, 5, 10]:
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals += list(c[idx + h] / c[idx] - 1)
            coinmean[(coin, h)] = np.mean(vals)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ret1 = df["close"].pct_change()
            z = ret1 / ret1.rolling(20).std()
            vr = df["volume"] / df["volume"].rolling(30).mean()
            r30 = df["close"].pct_change(30)
            yr = pd.to_datetime(df["timestamp"]).dt.year
            f = df["forecast"].fillna(0).values
            last = -999
            for t in range(n):
                if f[t] < 0 and t - last >= 5 and t + 5 < n:
                    last = t
                    d = {"coin": coin, "win": w, "year": yr[t], "fc": f[t],
                         "z": z[t], "vr": vr[t], "r30": r30[t]}
                    for h in [1, 2, 3, 5, 10]:
                        if t + h < n:
                            d["x%d" % h] = c[t + h] / c[t] - 1 - coinmean[(coin, h)]
                    rows.append(d)
            # all sharp falls (z<=-2), regardless of volume, non-overlapping
            last = -999
            for t in range(n):
                if z[t] <= -2 and t - last >= 5 and t + 5 < n:
                    last = t
                    allfall.append({"coin": coin, "vr": vr[t],
                                    "x5": c[t + 5] / c[t] - 1 - coinmean[(coin, 5)],
                                    "x1": c[t + 1] / c[t] - 1 - coinmean[(coin, 1)]})
    ev = pd.DataFrame(rows)
    af = pd.DataFrame(allfall)

    def summ(g, col="x5"):
        s = g[col].dropna()
        return pd.Series({"n": len(s), "mean": s.mean(),
                          "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 1 else np.nan,
                          "share_neg": (s < 0).mean()})
    out = {}
    out["overall_by_h"] = pd.DataFrame({h: summ(ev, "x%d" % h) for h in [1, 2, 3, 5, 10]}).T
    out["by_coin"] = ev.groupby("coin").apply(summ)
    out["by_year"] = ev.groupby("year").apply(summ)
    ev["fcq"] = pd.qcut(ev["fc"].rank(method="first"), 3, labels=["strong", "mid", "weak"])
    out["by_fc_tercile"] = ev.groupby("fcq").apply(summ)
    ev["vrq"] = pd.qcut(ev["vr"].rank(method="first"), 3, labels=["lowvr", "midvr", "highvr"])
    out["by_vr_tercile"] = ev.groupby("vrq").apply(summ)
    ev["zq"] = pd.qcut(ev["z"].rank(method="first"), 3, labels=["bigfall", "midfall", "smallfall"])
    out["by_z_tercile"] = ev.groupby("zq").apply(summ)
    ev["trend"] = np.where(ev["r30"] < 0, "down30", "up30")
    out["by_30d_trend"] = ev.groupby("trend").apply(summ)
    af["vrq"] = pd.cut(af["vr"], [0, 1, 1.5, 2.5, 100])
    out["allfalls_by_vr"] = af.groupby("vrq").apply(summ)
    out["allfalls_by_vr_x1"] = af.groupby("vrq").apply(lambda g: summ(g, "x1"))
    return out
