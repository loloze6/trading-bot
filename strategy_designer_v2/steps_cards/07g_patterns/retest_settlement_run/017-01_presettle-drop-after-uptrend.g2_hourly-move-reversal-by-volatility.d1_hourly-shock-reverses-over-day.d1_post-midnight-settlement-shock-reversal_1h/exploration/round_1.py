def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        # coin drift per horizon, pooled grid over windows
        drift = {}
        for H in (4, 8, 24):
            g = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - H, H)
                g.append(c[idx + H] / c[idx] - 1)
            drift[H] = np.concatenate(g).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"]
            r1 = c.pct_change()
            vol = r1.rolling(24).std()
            z = r1 / vol
            vlong = r1.rolling(24 * 30).std()
            df = pd.DataFrame({"coin": coin, "w": w, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "year": ts.dt.year, "z": z, "vrel": vol / vlong,
                               "volz": b["volume"] / b["volume"].rolling(24 * 7).median()})
            for H in (4, 8, 24):
                df["x%d" % H] = c.shift(-H) / c - 1 - drift[H]
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["z", "x24"])
    d = d[np.isfinite(d.z)]
    d["s"] = -np.sign(d.z)

    def stat(g, H=24):
        x = -g.z.clip(-6, 6); y = g["x%d" % H]
        sl = stats.linregress(x, y)
        big = g[g.z.abs() >= 1]
        sb = big.s * big["x%d" % H]
        return pd.Series({"n": len(g), "slope_t": sl.slope / sl.stderr,
                          "nbig": len(big), "mean_signed_big_%": 100 * sb.mean(),
                          "t_big": sb.mean() / (sb.std() / np.sqrt(len(sb)))})
    out = {}
    out["by_hour_24h"] = d.groupby("hour").apply(stat).round(3)
    h0 = d[d.hour == 0]
    out["hour0_by_horizon"] = pd.DataFrame({H: stat(h0, H) for H in (4, 8, 24)}).T.round(3)
    out["other_hours_by_horizon"] = pd.DataFrame({H: stat(d[d.hour != 0], H) for H in (4, 8, 24)}).T.round(3)
    out["hour0_by_year"] = h0.groupby("year").apply(stat).round(3)
    out["hour0_by_coin"] = h0.groupby("coin").apply(stat).round(3)
    h0 = h0.dropna(subset=["vrel"]).copy()
    h0["vq"] = pd.qcut(h0.vrel, 3, labels=["lowvol", "mid", "highvol"])
    out["hour0_by_vol_regime"] = h0.groupby("vq").apply(stat).round(3)
    allv = d.dropna(subset=["vrel"]).copy()
    allv["vq"] = pd.qcut(allv.vrel, 3, labels=["lowvol", "mid", "highvol"])
    out["allhours_by_vol_regime"] = allv.groupby("vq").apply(stat).round(3)
    out["hour0_by_weekday"] = d[d.hour == 0].groupby("wd").apply(stat).round(3)
    out["median_rel_volume_by_hour"] = d.groupby("hour").volz.median().round(3)
    return out
