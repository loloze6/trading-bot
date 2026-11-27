def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 3
    rows = []
    for coin, ws in bars.items():
        rs = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rs.append(c[i + H] / c[i] - 1)
        dr = np.mean(rs); usual = np.std(rs)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            f = df["forecast"].fillna(0).values
            n = len(df)
            lr = np.log(c)
            r1 = pd.Series(np.r_[np.nan, np.diff(lr)])
            vol = r1.rolling(20).std().values
            # grid cells: first bar in each cell with a new short bet (forecast<0 and previous >=0 or magnitude rising >=2)
            low_since = 0.0
            taken = set()
            for i in range(n):
                if f[i] >= 0:
                    low_since = 0.0; continue
                newbet = (i == 0 or f[i-1] >= 0) or (abs(f[i]) - abs(low_since) >= 2)
                cell = i // H
                if newbet and cell not in taken and i + H < n:
                    taken.add(cell)
                    low_since = f[i]
                    loc = (c[i] - lo[i]) / (hi[i] - lo[i]) if hi[i] > lo[i] else np.nan
                    s5 = (lr[i] - lr[i-5]) / (vol[i] * np.sqrt(5)) if i >= 5 and vol[i] > 0 else np.nan
                    ret = c[i + H] / c[i] - 1
                    rows.append({"coin": coin, "win": w, "day": str(df["timestamp"].iloc[i])[:10],
                                 "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 "f": f[i], "loc": loc, "s5": s5,
                                 "ex": -(ret - dr), "tot": -ret, "str": -(ret - dr) / usual,
                                 "core": coin in ("BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD")})
    E = pd.DataFrame(rows)

    def tday(g, col="ex"):
        g = g.dropna(subset=[col])
        if len(g) < 3: return (g[col].mean(), np.nan, len(g), g["day"].nunique())
        dev = g[col] - g[col].mean()
        sd = dev.groupby(g["day"]).sum(); D = len(sd)
        se = np.sqrt((sd ** 2).sum() * D / (D - 1)) / len(g)
        return (g[col].mean(), g[col].mean() / se, len(g), D)

    def tab(key):
        r = []
        for k, g in E.groupby(key):
            m, t, n, D = tday(g); s = g["str"].mean()
            r.append({"grp": k, "ex3": m, "t": t, "strength": s, "n": n, "days": D})
        return pd.DataFrame(r)
    out = {}
    m, t, n, D = tday(E)
    out["grid_cases_all"] = pd.Series({"ex3": m, "t": t, "n": n, "days": D, "tot": E["tot"].mean(), "strength": E["str"].mean()})
    E["locb"] = pd.cut(E["loc"], [0.49, 0.625, 0.75, 0.875, 1.001], labels=[".50-.62", ".62-.75", ".75-.87", ".87-1"])
    out["by_loc_band"] = tab("locb")
    E["s5q"] = pd.qcut(E["s5"], 4, labels=["deepest", "q2", "q3", "shallowest"])
    out["by_s5_quartile"] = tab("s5q")
    out["by_year"] = tab("year")
    out["by_core"] = tab("core")
    hiE = E[E["loc"] >= 0.75]; loE = E[E["loc"] < 0.75]
    r = []
    for y in sorted(E["year"].unique()):
        a = hiE[hiE.year == y]; b = loE[loE.year == y]
        r.append({"year": y, "hi_loc_ex": a["ex"].mean(), "n_hi": len(a), "lo_loc_ex": b["ex"].mean(), "n_lo": len(b)})
    out["loc_hi_vs_lo_by_year"] = pd.DataFrame(r)
    from scipy import stats
    g = E.dropna(subset=["loc", "ex", "s5"])
    out["spearman"] = pd.Series({"loc_vs_ex": stats.spearmanr(g["loc"], g["ex"])[0],
                                 "s5_vs_ex (neg=deeper better)": stats.spearmanr(g["s5"], g["ex"])[0],
                                 "absf_vs_ex": stats.spearmanr(g["f"].abs(), g["ex"])[0], "n": len(g)})
    return out
