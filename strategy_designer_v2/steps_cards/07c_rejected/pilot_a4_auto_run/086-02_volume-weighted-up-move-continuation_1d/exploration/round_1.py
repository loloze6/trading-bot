def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [1, 3, 5, 10]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in data["bars"].items():
        for h in H:
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(allr) if allr else np.nan
            usual[(coin, h)] = np.std(allr, ddof=1) if len(allr) > 2 else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            vr = b["volume"] / b["volume"].rolling(20).mean()
            z = r1 / sd
            fc = (b["regime"] == "unknown")
            r5past = c / c.shift(5) - 1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in H:
                n = len(c)
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i], fc=bool(fc[i]),
                                     r1=r1[i], z=z[i], vr=vr[i], prod=z[i] * vr[i],
                                     past5=r5past[i],
                                     fwd=c[i + h] / c[i] - 1,
                                     unus=c[i + h] / c[i] - 1 - drift[(coin, h)],
                                     strength=(c[i + h] / c[i] - 1 - drift[(coin, h)]) / usual[(coin, h)]))
    df = pd.DataFrame(rows).dropna(subset=["z", "vr", "fwd"])
    out = {}
    def summ(g):
        x = g["unus"]
        return pd.Series(dict(n=len(x), mean_unus=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              mean_total=g["fwd"].mean(), strength=g["strength"].mean()))
    fcd = df[df.fc]
    fcd = fcd.assign(day=np.where(fcd.r1 > 0, "up", "down"))
    out["fc_all_vs_rest_by_h"] = df.groupby(["h", "fc"]).apply(summ)
    out["fc_up_down_by_h"] = fcd.groupby(["h", "day"]).apply(summ)
    up = fcd[fcd.r1 > 0].copy()
    up["vr_t"] = up.groupby("h")["vr"].transform(lambda s: pd.qcut(s, 3, labels=["light", "mid", "heavy"]))
    up["prod_t"] = up.groupby("h")["prod"].transform(lambda s: pd.qcut(s, 3, labels=["low", "mid", "high"]))
    out["fc_up_by_volume_tercile"] = up.groupby(["h", "vr_t"]).apply(summ)
    out["fc_up_by_product_tercile"] = up.groupby(["h", "prod_t"]).apply(summ)
    dn = fcd[fcd.r1 <= 0].copy()
    dn["vr_t"] = dn.groupby("h")["vr"].transform(lambda s: pd.qcut(s, 3, labels=["light", "mid", "heavy"]))
    out["fc_down_by_volume_tercile"] = dn.groupby(["h", "vr_t"]).apply(summ)
    sp = []
    for h in H:
        u = up[up.h == h]
        sp.append(dict(h=h, n=len(u), rho_prod=stats.spearmanr(u["prod"], u["unus"])[0],
                       rho_vr=stats.spearmanr(u["vr"], u["unus"])[0], rho_z=stats.spearmanr(u["z"], u["unus"])[0]))
        a = fcd[fcd.h == h]
        sp.append(dict(h=h, n=len(a), rho_prod=stats.spearmanr(a["prod"], a["unus"])[0],
                       rho_vr=stats.spearmanr(a["vr"], a["unus"])[0], rho_z=stats.spearmanr(a["z"], a["unus"])[0]))
    out["spearman_up_then_all_fc"] = pd.DataFrame(sp)
    u5 = up[up.h == 5]
    out["fc_up_h5_by_coin"] = u5.groupby("coin").apply(summ)
    out["fc_up_h5_by_year"] = u5.groupby("year").apply(summ)
    out["fc_up_h5_by_coin_vr"] = u5.groupby(["coin", "vr_t"]).apply(summ)
    a5 = fcd[fcd.h == 5].copy()
    a5["z_q"] = pd.qcut(a5["z"], 5, labels=False)
    out["fc_h5_by_dayreturn_quintile"] = a5.groupby("z_q").apply(summ)
    a5["p5_q"] = pd.qcut(a5["past5"], 5, labels=False)
    out["fc_h5_by_past5_quintile"] = a5.groupby("p5_q").apply(summ)
    return out
