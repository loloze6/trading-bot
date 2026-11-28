def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].values; v = b["volume"].values.astype(float)
            n = len(b)
            vs = pd.Series(v)
            vr3 = np.log(vs.rolling(3).mean() / vs.shift(3).rolling(20).mean())
            vr1 = np.log(vs / vs.shift(1).rolling(20).mean())
            cs = pd.Series(c)
            r1 = cs.pct_change(1); r3 = cs.pct_change(3)
            fc = b["regime"].isin(["trending", "unknown"])
            year = pd.to_datetime(b["timestamp"]).dt.year
            for h in [1, 3, 5, 10]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=year[i], fc=bool(fc[i]), reg=b["regime"][i],
                                     ret=c[i+h]/c[i]-1, vr3=vr3[i], vr1=vr1[i], r1=r1[i], r3=r3[i],
                                     fcast=b["forecast"][i]))
    df = pd.DataFrame(rows)
    mu = df.groupby(["coin", "h"])["ret"].mean().rename("mu")
    df = df.join(mu, on=["coin", "h"]); df["ex"] = df["ret"] - df["mu"]
    out["coin_drift_5"] = df[df.h == 5].groupby("coin")["ret"].agg(["mean", "std", "count"])
    fcd = df[df.fc]
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g.ex.mean(), "t": g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g) > 2 else np.nan, "mean_tot": g.ret.mean()})
    out["fc_vs_not_by_h"] = df.groupby(["h", "fc"]).apply(summ)
    up3 = fcd[fcd.r3 > 0].copy()
    up3["vq"] = up3.groupby("h")["vr3"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["fc_rise3_by_vol3_quartile_h"] = up3.groupby(["h", "vq"]).apply(summ)
    up1 = fcd[fcd.r1 > 0].copy()
    up1["vq"] = up1.groupby("h")["vr1"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["fc_upday_by_vol1_quartile_h"] = up1.groupby(["h", "vq"]).apply(summ)
    # all falling calm bars by 3-day return quartile
    f = fcd.copy()
    f["rq"] = f.groupby("h")["r3"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["fc_by_ret3_quartile_h"] = f.groupby(["h", "rq"]).apply(summ)
    f["r1q"] = f.groupby("h")["r1"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["fc_by_ret1_quartile_h"] = f.groupby(["h", "r1q"]).apply(summ)
    # correlations within fc, per h
    cr = []
    for h in [1, 3, 5, 10]:
        g = fcd[fcd.h == h].dropna(subset=["vr1", "vr3", "r1", "r3"])
        for x in ["vr1", "vr3", "r1", "r3"]:
            r, p = stats.pearsonr(g[x], g.ex); cr.append(dict(h=h, x=x, r=r, t=r*np.sqrt((len(g)-2)/(1-r*r)), n=len(g)))
        gu = g[g.r1 > 0]
        r, p = stats.pearsonr(gu.vr1, gu.ex); cr.append(dict(h=h, x="vr1|up1", r=r, t=r*np.sqrt((len(gu)-2)/(1-r*r)), n=len(gu)))
        gd = g[g.r1 < 0]
        r, p = stats.pearsonr(gd.vr1, gd.ex); cr.append(dict(h=h, x="vr1|down1", r=r, t=r*np.sqrt((len(gd)-2)/(1-r*r)), n=len(gd)))
    out["corr_fc"] = pd.DataFrame(cr)
    g5 = up3[up3.h == 5]
    out["rise3_5d_by_coin"] = g5.groupby("coin").apply(summ)
    out["rise3_5d_by_year"] = g5.groupby("year").apply(summ)
    out["fc5_by_coin"] = fcd[fcd.h == 5].groupby("coin").apply(summ)
    return out
