def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        r48 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            r48 += list(c[idx + 48] / c[idx] - 1)
        drift = np.mean(r48); usual = np.std(r48)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values; v = df["volume"].values
            fc = df["forecast"].values
            n = len(c)
            hrs = ts.dt.hour.values; dows = ts.dt.dayofweek.values; yrs = ts.dt.year.values
            for i in range(720, n - 48):
                if hrs[i] != 23 or dows[i] != 6:
                    continue
                back = c[i] / c[i - 48] - 1
                base = v[i - 167:i - 48].mean()
                near = v[i - 47:i + 1].mean()
                longv = v[i - 719:i + 1].mean()
                if near <= 0 or longv <= 0:
                    continue
                f48 = c[i + 48] / c[i] - 1
                rows.append(dict(coin=coin, year=yrs[i], z=back / usual, thin=base / near,
                                 near_rel=near / longv, base_rel=base / longv,
                                 u48=(f48 - drift) / usual, tot48=f48, fc=fc[i]))
    d = pd.DataFrame(rows)
    d["side"] = np.where(d.z > 0, "weekend_up", "weekend_down")
    d["rev48"] = -np.sign(d.z) * d.u48
    d["revtot_pct"] = -np.sign(d.z) * d.tot48 * 100
    d["thq"] = pd.qcut(d.thin, 4, labels=False)
    d["nearq"] = pd.qcut(d.near_rel, 4, labels=False)
    d["baseq"] = pd.qcut(d.base_rel, 4, labels=False)
    def summ(g):
        return pd.Series({"n": len(g), "rev48": g.rev48.mean(),
                          "t": stats.ttest_1samp(g.rev48, 0).statistic,
                          "revtot_pct": g.revtot_pct.mean()})
    out["thin_q_by_side"] = d.groupby(["thq", "side"]).apply(summ)
    out["near_rel_q"] = d.groupby("nearq").apply(summ)
    out["base_rel_q"] = d.groupby("baseq").apply(summ)
    out["thin_q_by_year_top"] = d[d.thq == 3].groupby("year").apply(summ)
    out["thin_q_by_coin_top"] = d[d.thq == 3].groupby("coin").apply(summ)
    d["prod"] = d.z * d.thin
    def reg(x, y):
        m = np.isfinite(x) & np.isfinite(y)
        r = stats.linregress(x[m], y[m])
        return r.slope / r.stderr
    d["prod_rank"] = d["prod"].rank(pct=True) - 0.5
    d["z_clip"] = d.z.clip(-3, 3)
    d["prod_clip"] = d["prod"].clip(d["prod"].quantile(0.01), d["prod"].quantile(0.99))
    out["t_of_slope_u48_on"] = pd.Series({
        "prod": reg(d["prod"].values, d.u48.values),
        "prod_clip": reg(d["prod_clip"].values, d.u48.values),
        "prod_rank": reg(d["prod_rank"].values, d.u48.values),
        "z_clip": reg(d.z_clip.values, d.u48.values),
        "neg_forecast": reg(d.fc.values, d.u48.values),
        "sign_z_times_thinrank": reg((np.sign(d.z) * d.thin.rank(pct=True)).values, d.u48.values),
        "n": len(d)})
    d["fcq"] = pd.qcut(d.fc.abs().rank(method="first"), 5, labels=False)
    out["by_abs_forecast_quintile"] = d.groupby("fcq").apply(
        lambda g: pd.Series({"n": len(g), "signed_u48": (np.sign(g.fc) * g.u48).mean(),
                             "mean_abs_fc": g.fc.abs().mean(),
                             "share_weekend_up": (g.z > 0).mean()}))
    return out
