def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    wk = []
    drift = {}
    usual = {}
    for coin, wins in data["bars"].items():
        r48 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            r48 += list(c[idx + 48] / c[idx] - 1)
        drift[coin] = np.mean(r48); usual[coin] = np.std(r48)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values; v = df["volume"].values
            n = len(c)
            fc = df["forecast"].values
            alloc = df["postRebalance_current_allocation"].values
            for i in range(168, n):
                t = ts.iloc[i]
                if t.hour != 23:
                    continue
                dow = t.dayofweek
                if dow not in (6, 2):  # Sunday close, Wednesday close (compare)
                    continue
                if i + 48 >= n:
                    continue
                back = c[i] / c[i - 48] - 1
                base = v[i - 167:i - 48].mean()
                near = v[i - 47:i + 1].mean()
                thin = base / near if near > 0 else np.nan
                f24 = c[i + 24] / c[i] - 1
                f48 = c[i + 48] / c[i] - 1
                f12 = c[i + 12] / c[i] - 1
                rec = dict(coin=coin, win=w, year=t.year, dow=dow,
                           z=back / usual[coin], thin=thin,
                           u12=(f12) / usual[coin],
                           u24=(f24 - drift[coin] / 2) / usual[coin],
                           u48=(f48 - drift[coin]) / usual[coin],
                           fc=fc[i], alloc=alloc[i])
                rows.append(rec)
    d = pd.DataFrame(rows)
    d["rev48"] = -np.sign(d["z"]) * d["u48"]
    d["rev24"] = -np.sign(d["z"]) * d["u24"]
    d["absz"] = d["z"].abs()
    def summ(g):
        return pd.Series({"n": len(g), "rev24": g.rev24.mean(), "rev48": g.rev48.mean(),
                          "t48": stats.ttest_1samp(g.rev48, 0).statistic if len(g) > 2 else np.nan,
                          "slope_u48_on_z": np.polyfit(g.z, g.u48, 1)[0] if len(g) > 5 else np.nan})
    d["zq"] = pd.qcut(d["absz"], 5, labels=False, duplicates="drop")
    d["thq"] = d.groupby("dow")["thin"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["by_day_and_absz_quintile"] = d.groupby(["dow", "zq"]).apply(summ)
    out["by_day_and_thin_quartile"] = d.groupby(["dow", "thq"]).apply(summ)
    s = d[d.dow == 6]
    out["sunday_by_coin"] = s.groupby("coin").apply(summ)
    out["sunday_by_year"] = s.groupby("year").apply(summ)
    s2 = s.copy(); s2["prod"] = s2.z * s2.thin
    out["sunday_corr_u48_with_prod_and_z"] = pd.Series({
        "corr_prod": s2[["prod", "u48"]].corr().iloc[0, 1],
        "corr_z": s2[["z", "u48"]].corr().iloc[0, 1],
        "corr_z_u24": s2[["z", "u24"]].corr().iloc[0, 1],
        "corr_z_u12": s2[["z", "u12"]].corr().iloc[0, 1],
        "thin_mean_sun": s.thin.mean(), "thin_mean_wed": d[d.dow == 2].thin.mean(),
        "share_fc_nonzero": (s.fc != 0).mean(), "mean_abs_alloc": s.alloc.abs().mean()})
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    out["trades"] = T.groupby("side").agg(n=("profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        dur_h=("duration_minutes", lambda x: x.mean() / 60))
    return out
