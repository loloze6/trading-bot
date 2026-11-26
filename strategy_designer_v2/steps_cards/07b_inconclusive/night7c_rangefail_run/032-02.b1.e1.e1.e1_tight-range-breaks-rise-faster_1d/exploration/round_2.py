def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [5, 10, 20]
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs, ddof=1)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            pmax = cl.shift(1).rolling(60).max()
            pmin = cl.shift(1).rolling(60).min()
            mad = cl.pct_change().abs().shift(1).rolling(60).mean()
            W = (pmax - pmin) / pmin / mad
            brk = cl / pmax - 1
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year
            day = pd.to_datetime(df["timestamp"]).dt.floor("D")
            for hgrid in H:
                seen = set()
                for i in range(n):
                    if brk.iloc[i] > 0 and not np.isnan(W.iloc[i]):
                        cell = i // hgrid
                        if cell in seen: continue
                        seen.add(cell)
                        if i + hgrid >= n: continue
                        u = cl.iloc[i+hgrid] / cl.iloc[i] - 1 - drift[(c, hgrid)]
                        rows.append({"h": hgrid, "coin": c, "year": yr.iloc[i], "W": W.iloc[i],
                                     "fc": df["forecast"].iloc[i], "u": u,
                                     "s": u / usual[(c, hgrid)], "day": day.iloc[i]})
    d = pd.DataFrame(rows)
    res = {}
    out = []
    for h in H:
        g = d[d.h == h].copy()
        med = g["W"].median()
        lo = g[g.W <= med]["u"]; hi = g[g.W > med]["u"]  # tight = low W
        t = stats.ttest_ind(lo, hi, equal_var=False)[0]
        gd = g.groupby("day")["u"].sum()
        tday = g["u"].mean() / (g["u"].std(ddof=1) * np.sqrt(len(gd) / len(g)) / np.sqrt(len(gd))) if len(gd) > 2 else np.nan
        tday2 = gd.mean() / (gd.std(ddof=1) / np.sqrt(len(gd)))
        rho = stats.spearmanr(g["W"], g["u"])[0]
        fm = g[g.fc > 0]
        rho_fc = stats.spearmanr(fm["fc"], fm["u"])[0] if len(fm) > 5 else np.nan
        out.append({"h": h, "n": len(g), "days": len(gd), "mean_u": g["u"].mean(), "strength": g["s"].mean(),
                    "tday_sum": tday2, "tight_minus_wide": lo.mean() - hi.mean(), "welch_t": t,
                    "rho_W": rho, "rho_fc_on_fc_cases": rho_fc})
    res["by_h"] = pd.DataFrame(out)
    g = d[d.h == 5].copy()
    med = g["W"].median(); g["tight"] = (g.W <= med).astype(int)
    res["h5_coin_tight"] = g.groupby(["coin", "tight"])["u"].agg(["count", "mean"]).unstack()
    res["h5_year_tight"] = g.groupby(["year", "tight"])["u"].agg(["count", "mean"]).unstack()
    g2 = d[d.h == 20].copy(); med2 = g2["W"].median(); g2["tight"] = (g2.W <= med2).astype(int)
    res["h20_coin_tight"] = g2.groupby(["coin", "tight"])["u"].agg(["count", "mean"]).unstack()
    res["h20_year_tight"] = g2.groupby(["year", "tight"])["u"].agg(["count", "mean"]).unstack()
    res["W_median"] = med
    return res
