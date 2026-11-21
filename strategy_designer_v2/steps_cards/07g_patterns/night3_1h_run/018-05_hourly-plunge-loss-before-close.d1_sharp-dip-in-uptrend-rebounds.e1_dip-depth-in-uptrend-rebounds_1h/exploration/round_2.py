def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            ma = r24.abs().rolling(720, min_periods=360).mean()
            z = r24 / ma
            r720 = c / c.shift(720) - 1
            vol = c.pct_change().rolling(720, min_periods=360).std()
            for h in (12, 24, 48, 72):
                idx = np.arange(0, len(c) - h, h)
                fr = (c.shift(-h) / c - 1).iloc[idx]
                recs.append(pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]), "h": h, "fr": fr.values,
                                          "z": z.iloc[idx].values, "r720": r720.iloc[idx].values,
                                          "vol": vol.iloc[idx].values, "hour": ts.iloc[idx].dt.hour.values}))
    A = pd.concat(recs).dropna(subset=["fr", "z", "r720", "vol"])
    A["u"] = A["fr"] - A.groupby(["coin", "h"])["fr"].transform("mean")
    A["s"] = A["u"] / A.groupby(["coin", "h"])["fr"].transform("std")
    A["up"] = np.where(A["r720"] > 0, "up30", "down30")
    A["volq"] = A.groupby(["coin", "h"])["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out = {}
    def slope(g):
        n = len(g)
        if n < 20: return pd.Series({"n": n})
        x = -g["z"].clip(-6, 6); y = g["u"]
        r = stats.linregress(x, y)
        p = x * y
        tp = p.mean() / (p.std() / np.sqrt(n))
        return pd.Series({"n": n, "corr": round(r.rvalue, 3), "t_slope": round(r.slope / r.stderr, 2),
                          "slope_bps_per_unit": round(r.slope * 1e4, 1), "t_prod": round(tp, 2)})
    out["reversal_slope_by_h_regime"] = A.groupby(["h", "up"]).apply(slope)
    a24 = A[A.h == 24]
    out["h24_down30_by_coin"] = a24[a24.up == "down30"].groupby("coin").apply(slope)
    a24 = a24.assign(half=np.where(a24.wn <= 12, "w1-12", "w13-24"))
    out["h24_by_half_regime"] = a24.groupby(["half", "up"]).apply(slope)
    out["h24_by_vol_regime"] = a24.groupby(["up", "volq"]).apply(slope)
    out["h24_by_hourgroup"] = a24.assign(hg=a24.hour // 6).groupby(["hg"]).apply(slope)
    # big |z| cases at 24h, both regimes: mean u in reversal direction
    big = a24[a24.z.abs() > 1.5].copy()
    big["rev"] = -np.sign(big.z) * big.u
    big["revs"] = -np.sign(big.z) * big.s
    out["h24_big_moves_reversal"] = big.groupby(["up", np.sign(big.z)]).agg(
        n=("rev", "size"), mean_rev=("rev", "mean"), strength=("revs", "mean"),
        t=("rev", lambda x: x.mean() / (x.std() / np.sqrt(len(x))))).round(4)
    a72 = A[(A.h == 72) & (A.z < -1)]
    out["h72_dip_by_vol_regime_slope"] = a72.groupby(["up", "volq"]).apply(slope)
    return out
