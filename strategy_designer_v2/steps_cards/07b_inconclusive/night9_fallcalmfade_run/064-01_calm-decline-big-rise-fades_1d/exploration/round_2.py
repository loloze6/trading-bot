def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            r1 = pd.Series(c).pct_change()
            sw = (r1 / r1.rolling(20).std()).values
            reg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            for i in range(n):
                rec = {"coin": coin, "w": w, "i": i, "reg": reg[i], "sw": sw[i], "day": ts[i]}
                for h in (3, 5, 7, 10):
                    rec[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    for h in (3, 5, 7, 10):
        dr = d[d["i"] % h == 0].groupby("coin")[f"f{h}"].mean()
        d[f"x{h}"] = d[f"f{h}"] - d["coin"].map(dr)
    fc = d[d["reg"] != "chop"].copy()
    out = {}
    def pooled(sub, col):
        s = sub[["day", col]].dropna()
        if len(s) < 3: return (len(s), np.nan, np.nan, 0)
        m = s[col].mean()
        ds = (s[col] - 0).groupby(s["day"]).sum()
        # deviations from 0 mean test: se = sqrt(sum((daysum - m*k)^2))/n
        k = s.groupby("day")[col].count()
        se = np.sqrt((((ds - m * k) ** 2).sum())) / len(s)
        return (len(s), m, m / se, len(ds))
    tab = []
    for h in (3, 5, 7, 10):
        col = f"x{h}"
        base = fc[fc["i"] % h == 0]
        cs = base[base["reg"] == "mean_reversion"]
        n, m, t, nd = pooled(cs, col)
        n2, m2, t2, nd2 = pooled(cs[cs["coin"] != "XRPUSD"], col)
        bm = base[col].mean()
        tab.append({"h": h, "grid cases": n, "mean long excess": m, "t pooled": t, "days": nd,
                    "noXRP n": n2, "noXRP mean": m2, "noXRP t": t2, "falling calm grid base": bm})
    out["grid cases by horizon"] = pd.DataFrame(tab)
    cs = fc[fc["reg"] == "mean_reversion"]
    out["cases by window x3,x10"] = cs.groupby("w")[["x3", "x10"]].agg(["count", "mean"])
    out["cases by coin x10"] = cs.groupby("coin")["x10"].agg(["count", "mean"])
    # graded: among sw>=1 in falling calm, corr with forward
    g = fc[fc["sw"] >= 1]
    for h in (3, 10):
        z = g[["sw", f"x{h}"]].dropna()
        r, p = stats.pearsonr(z["sw"], z[f"x{h}"])
        out[f"sw>=1 corr x{h}"] = f"r={r:.3f} p={p:.3f} n={len(z)}"
    z = cs[["sw", "x3", "x10"]].dropna()
    out["cases corr sw x3/x10"] = f"{stats.pearsonr(z['sw'], z['x3'])[0]:.3f} / {stats.pearsonr(z['sw'], z['x10'])[0]:.3f} n={len(z)}"
    out["share of cases with x3>0"] = float((cs["x3"] > 0).mean())
    out["median x3 cases"] = float(cs["x3"].median())
    return out
