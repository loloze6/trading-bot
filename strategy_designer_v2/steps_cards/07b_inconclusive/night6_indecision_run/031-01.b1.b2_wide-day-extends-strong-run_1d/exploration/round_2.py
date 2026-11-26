def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []
    drift = {}
    H = 3
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            n = len(df)
            rng = pd.Series(hi - lo)
            rm = (rng / rng.rolling(20, min_periods=20).mean()).values
            r5 = pd.Series(c).pct_change(5).values
            r60 = pd.Series(c).pct_change(60).values
            ma50 = pd.Series(c).rolling(50, min_periods=50).mean().values
            ts = pd.to_datetime(df["timestamp"])
            f = df["forecast"].values
            for t in range(0, n - H, H):
                fr = c[t + H] / c[t] - 1
                allr.append(fr)
                rows.append(dict(coin=coin, win=w, year=ts.iloc[t].year, day=ts.iloc[t].normalize(),
                                 f=f[t], fr=fr, r5=r5[t], rm=rm[t], r60=r60[t],
                                 above50=(c[t] > ma50[t]) if not np.isnan(ma50[t]) else np.nan))
        drift[coin] = np.mean(allr)
    d = pd.DataFrame(rows)
    d["u"] = d["fr"] - d["coin"].map(drift)

    def tstat(g):
        s = g.groupby("day")["u"].sum()
        nd = len(s); m = g["u"].mean()
        se = s.std(ddof=1) * np.sqrt(nd) / len(g) if nd > 1 else np.nan
        return pd.Series({"n": len(g), "days": nd, "mean_u": m, "t": m / se if se else np.nan})

    out = {}
    up = d[(d.r5 > 0) & d.rm.notna()].copy()
    up["prod"] = up["r5"] * up["rm"]
    up["rq"] = pd.qcut(up["r5"], 2, labels=["rise_lo", "rise_hi"])
    up["mq"] = pd.qcut(up["rm"], 2, labels=["rng_lo", "rng_hi"])
    out["rise_x_range"] = up.groupby(["rq", "mq"]).apply(tstat)
    out["by_above50"] = up.groupby("above50").apply(tstat)
    up["r60s"] = np.where(up.r60 > 0, "r60_up", np.where(up.r60 <= 0, "r60_dn", "na"))
    out["by_r60"] = up.groupby("r60s").apply(tstat)
    upp = up[up.r60 > 0].copy()
    upp["pq"] = pd.qcut(upp["prod"], 4, labels=False)
    out["r60up_prod_q"] = upp.groupby("pq").apply(tstat)
    upn = up[up.r60 <= 0].copy()
    upn["pq"] = pd.qcut(upn["prod"], 4, labels=False)
    out["r60dn_prod_q"] = upn.groupby("pq").apply(tstat)
    out["r60up_by_year"] = upp.groupby("year").apply(tstat)
    out["r60up_by_coin"] = upp.groupby("coin").apply(tstat)
    # corr of product with u, graded check
    out["spearman_prod_u_all"] = float(up[["prod", "u"]].corr("spearman").iloc[0, 1])
    out["spearman_prod_u_r60up"] = float(upp[["prod", "u"]].corr("spearman").iloc[0, 1])
    out["spearman_prod_u_r60dn"] = float(upn[["prod", "u"]].corr("spearman").iloc[0, 1])
    # down runs with wide range (brief's own reversal side): 5d fall, product with range
    dn = d[(d.r5 < 0) & d.rm.notna()].copy()
    dn["pq"] = pd.qcut(-dn["r5"] * dn["rm"], 4, labels=False)
    out["fall_x_range_q"] = dn.groupby("pq").apply(tstat)
    return out
