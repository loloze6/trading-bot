def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [24, 120, 240]
    rows = []
    for coin, wins in bars.items():
        drift = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(rs)
        for w, df in wins.items():
            c = df["close"].values.astype(float); n = len(c)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            s = pd.Series(c)
            r24 = s / s.shift(24) - 1
            surge = (r24 / r24.abs().rolling(720, min_periods=720).mean()).values
            p7 = (s.shift(24) / s.shift(192) - 1).values
            vol = (s.pct_change().rolling(720, min_periods=720).std() * np.sqrt(168)).values
            on = surge >= 3; seen = set()
            for t in range(1, n):
                if on[t] and not on[t-1] and not np.isnan(p7[t]):
                    cell = t // 120
                    if cell in seen: continue
                    seen.add(cell)
                    rec = dict(coin=coin, yr=yr[t], up=p7[t] >= 0, surge=surge[t], p7s=p7[t] / vol[t])
                    for h in H:
                        rec[f"r{h}"] = (c[t+h]/c[t]-1-drift[h]) if t+h < n else np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g):
        out = {"n": len(g)}
        for h in H:
            x = g[f"r{h}"].dropna()
            out[f"m{h}"] = x.mean(); out[f"t{h}"] = x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    def slope(g, xcol, ycol):
        g = g[[xcol, ycol]].dropna()
        b = np.polyfit(g[xcol], g[ycol], 1)[0]
        r = np.corrcoef(g[xcol], g[ycol])[0, 1]
        return pd.Series({"slope": b, "corr": r, "t_corr": r*np.sqrt((len(g)-2)/(1-r*r)), "n": len(g)})
    up = d[d.up].copy(); dn = d[~d.up].copy()
    up["sq"] = pd.qcut(up.surge, 3, labels=False); up["pq"] = pd.qcut(up.p7s, 3, labels=False)
    dn["sq"] = pd.qcut(dn.surge, 3, labels=False); dn["pq"] = pd.qcut(dn.p7s, 3, labels=False)
    return {
        "rise_by_surge_t": up.groupby("sq").apply(summ),
        "rise_by_p7s_t": up.groupby("pq").apply(summ),
        "rise_by_coin": up.groupby("coin").apply(summ),
        "rise_by_year": up.groupby("yr").apply(summ),
        "rise_slope_surge_r120": slope(up, "surge", "r120"),
        "rise_slope_p7s_r120": slope(up, "p7s", "r120"),
        "fall_by_surge_t": dn.groupby("sq").apply(summ),
        "fall_by_p7s_t": dn.groupby("pq").apply(summ),
        "fall_slope_p7s_r24": slope(dn, "p7s", "r24"),
        "fall_slope_surge_r24": slope(dn, "surge", "r24"),
    }
