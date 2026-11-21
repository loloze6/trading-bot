def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r24 = c / c.shift(24) - 1
            mad = r24.abs().rolling(720, min_periods=360).mean()
            r720 = c / c.shift(720) - 1
            r168 = c / c.shift(168) - 1
            lr = np.log(c).diff()
            vol = lr.rolling(720, min_periods=360).std()
            vol24 = lr.rolling(24, min_periods=20).std()
            vol_s = lr.rolling(72, min_periods=48).std()
            idx = np.arange(0, len(b), 72)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "wn": int(w[1:]),
                "z24": (r24 / mad).iloc[idx].values,
                "r720": r720.iloc[idx].values,
                "r168": r168.iloc[idx].values,
                "vr": (vol_s / vol).iloc[idx].values,
                "vr24": (vol24 / vol).iloc[idx].values,
                "fwd72": (c.shift(-72) / c - 1).iloc[idx].values,
                "fwd24": (c.shift(-24) / c - 1).iloc[idx].values,
                "fwd168": (c.shift(-168) / c - 1).iloc[idx].values,
                "yr": ts.dt.year.iloc[idx].values,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in ["fwd72", "fwd24", "fwd168"]:
        d["un_" + h] = d[h] - d.groupby("coin")[h].transform("mean")
    d = d.dropna(subset=["un_fwd72", "z24", "r720", "r168", "vr"])
    d["sd72"] = d.groupby("coin")["fwd72"].transform("std")
    d["s72"] = d["un_fwd72"] / d["sd72"]
    d["z168"] = d["r168"] / d.groupby("coin")["r168"].transform("std")

    def summ(g, col="un_fwd72"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "strength": (g["s72"].mean() if col == "un_fwd72" else np.nan)})

    d["half"] = np.where(d["wn"] <= 12, "w1-12", "w13-24")
    big = d["z24"] < -1.2
    out["bigfall_by_half"] = d[big].groupby("half").apply(summ)
    out["bigfall_by_coin"] = d[big].groupby("coin").apply(summ)
    out["bigfall_by_year"] = d[big].groupby("yr").apply(summ)
    out["bigfall_horizons"] = pd.DataFrame({h: summ(d[big], "un_" + h) for h in ["fwd24", "fwd72", "fwd168"]}).T
    bigr = d["z24"] > 1.3
    out["bigrise_by_half"] = d[bigr].groupby("half").apply(summ)
    out["bigrise_horizons"] = pd.DataFrame({h: summ(d[bigr], "un_" + h) for h in ["fwd24", "fwd72", "fwd168"]}).T
    # is it volatility, not direction? abs z24 vs vr
    d["absz_q"] = pd.qcut(d["z24"].abs(), 5)
    out["by_absz24"] = d.groupby("absz_q").apply(summ)
    d["vr24_q"] = pd.qcut(d["vr24"], 5)
    out["by_vr24"] = d.groupby("vr24_q").apply(summ)
    out["vr24_top_by_half"] = d[d["vr24"] > d["vr24"].quantile(0.8)].groupby("half").apply(summ)
    # graded: spearman correlations
    def sp(x, y):
        m = x.notna() & y.notna()
        r, p = stats.spearmanr(x[m], y[m]); return pd.Series({"rho": r, "p": p, "n": m.sum()})
    out["spearman"] = pd.DataFrame({
        "neg_z24_fall_only": sp(-d.loc[d.z24 < 0, "z24"], d.loc[d.z24 < 0, "un_fwd72"]),
        "abs_z24": sp(d["z24"].abs(), d["un_fwd72"]),
        "vr24": sp(d["vr24"], d["un_fwd72"]),
        "z168": sp(d["z168"], d["un_fwd72"]),
        "z168_top_half_only": sp(d.loc[d.z168 > 0, "z168"], d.loc[d.z168 > 0, "un_fwd72"]),
    }).T
    d["z168_q"] = pd.qcut(d["z168"], 5)
    out["z168_top_by_half"] = d[d["z168"] > d["z168"].quantile(0.8)].groupby("half").apply(summ)
    out["z168_top_by_coin"] = d[d["z168"] > d["z168"].quantile(0.8)].groupby("coin").apply(summ)
    # deep fall in uptrend graded by z24 depth
    up = d[(d.r720 > 0) & (d.z24 < 0)].copy()
    up["dq"] = pd.qcut(-up["z24"], 4)
    out["fall_depth_in_uptrend"] = up.groupby("dq").apply(summ)
    dn = d[(d.r720 <= 0) & (d.z24 < 0)].copy()
    dn["dq"] = pd.qcut(-dn["z24"], 4)
    out["fall_depth_in_downtrend"] = dn.groupby("dq").apply(summ)
    return out
