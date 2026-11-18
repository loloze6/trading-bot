def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    # coin mean h-bar returns on non-overlapping grid
    cmean = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            cmean[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            r1 = pd.Series(cl).pct_change()
            sd = r1.rolling(20).std()
            z = (r1 / sd).values
            vr = (df["volume"] / df["volume"].shift(1).rolling(20).mean()).values
            rng = (df["high"] - df["low"]).values
            wick = np.where(rng > 0, (cl - df["low"].values) / rng, np.nan)
            flush = ((z <= -2) & (vr >= 2))
            flush = np.where(np.isnan(z), df["regime"].values == "mean_reversion", flush)
            last = -99
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in np.where(flush)[0]:
                if i - last < 3:
                    continue
                last = i
                d = dict(coin=c, win=w, year=yr[i], z=z[i], vr=vr[i], wick=wick[i], r1=r1.iloc[i])
                for h in H:
                    d[f"x{h}"] = (cl[i + h] / cl[i] - 1 - cmean[(c, h)]) if i + h < len(cl) else np.nan
                rows.append(d)
    f = pd.DataFrame(rows)
    out = {}
    def slope_t(sub, y, x="wick"):
        s = sub[[x, y]].dropna()
        if len(s) < 5: return (np.nan, np.nan, len(s))
        r = stats.linregress(s[x], s[y])
        return (r.slope, r.slope / r.stderr, len(s))
    hz = []
    for h in H:
        s, t, n = slope_t(f, f"x{h}")
        m = f[f"x{h}"].dropna()
        hz.append(dict(h=h, slope=s, t=t, n=n, mean_excess=m.mean(),
                       t_mean=m.mean() / (m.std() / np.sqrt(len(m)))))
    out["by_horizon"] = pd.DataFrame(hz)
    f["wt"] = pd.qcut(f["wick"], 3, labels=["low", "mid", "high"])
    out["wick_tercile"] = f.groupby("wt")[[f"x{h}" for h in H]].agg(["mean", "count"])
    for g in ["coin", "year"]:
        rr = []
        for k, sub in f.groupby(g):
            s, t, n = slope_t(sub, "x3")
            rr.append({g: k, "slope3": s, "t3": t, "n": n, "mean3": sub["x3"].mean(),
                       "mean10": sub["x10"].mean()})
        out["by_" + g] = pd.DataFrame(rr)
    f["zt"] = pd.qcut(f["z"], 3, labels=["deepest", "mid", "shallow"])
    f["vt"] = pd.qcut(f["vr"], 3, labels=["lowv", "midv", "highv"])
    out["by_fall"] = f.groupby("zt")[["x3", "x10", "wick"]].mean().assign(n=f.groupby("zt").size())
    out["by_vol"] = f.groupby("vt")[["x3", "x10", "wick"]].mean().assign(n=f.groupby("vt").size())
    rr = []
    for k, sub in f.groupby("zt"):
        s, t, n = slope_t(sub, "x3"); s10, t10, _ = slope_t(sub, "x10")
        rr.append(dict(zt=k, t3=t, t10=t10, n=n))
    out["slope_by_fall"] = pd.DataFrame(rr)
    return out
