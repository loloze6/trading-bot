def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    hs = [3, 5, 10, 20]
    def grid_mean(coin, h):
        rs = []
        for w, df in bars[coin].items():
            c = df["close"].values
            idx = np.arange(0, len(c) - h, h)
            rs.extend(c[idx + h] / c[idx] - 1)
        return np.nanmean(rs), np.nanstd(rs)
    means = {(coin, h): grid_mean(coin, h) for coin in bars for h in hs}
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            s = pd.Series(c).shift(1)
            prev_hi = s.rolling(60, min_periods=60).max().values
            prev_lo = s.rolling(60, min_periods=60).min().values
            # realised vol of prior 60 days (daily, pct)
            vol60 = (pd.Series(c).pct_change().shift(1).rolling(60, min_periods=40).std() * 100).values
            ret60 = (s / s.shift(59) - 1).values * 100
            trend = df["regime"].values == "trending"
            last = -10
            for i in range(len(df)):
                if not trend[i] or i - last <= 3:
                    continue
                last = i
                ts = pd.Timestamp(df["timestamp"].iloc[i])
                r = {"coin": coin, "window": w, "year": ts.year, "day": str(ts.date()),
                     "width": (prev_hi[i] / prev_lo[i] - 1) * 100 if prev_lo[i] == prev_lo[i] else np.nan,
                     "vol60": vol60[i], "ret60": ret60[i],
                     "margin": (c[i] / prev_hi[i] - 1) * 100 if prev_hi[i] == prev_hi[i] else np.nan}
                for h in hs:
                    r[f"x{h}"] = (c[i + h] / c[i] - 1 - means[(coin, h)][0]) * 100 if i + h < len(c) else np.nan
                    r[f"u{h}"] = means[(coin, h)][1] * 100
                rows.append(r)
    d = pd.DataFrame(rows).dropna(subset=["width"])
    d["wq"] = pd.qcut(d["width"], 3, labels=["narrow", "mid", "wide"])
    out = {"n_with_width": len(d)}
    out["width_x_year_x10"] = d.pivot_table(index="year", columns="wq", values="x10", aggfunc="mean").round(2)
    out["width_x_year_n"] = d.pivot_table(index="year", columns="wq", values="x10", aggfunc="count")
    out["width_x_coin_x10"] = d.pivot_table(index="coin", columns="wq", values="x10", aggfunc="mean").round(2)
    # day-clustered t of slope of excess return on log width
    def cl_slope(g, xcol, ycol):
        g = g[[xcol, ycol, "day"]].dropna()
        x = g[xcol] - g[xcol].mean(); y = g[ycol]
        b = (x * (y - y.mean())).sum() / (x ** 2).sum()
        e = (y - y.mean() - b * x) * x
        se = np.sqrt(e.groupby(g["day"]).sum().pow(2).sum()) / (x ** 2).sum()
        return f"slope {b:.3f} t {b/se:.2f} n {len(g)} days {g['day'].nunique()}"
    d["lw"] = np.log(d["width"])
    d["lv"] = np.log(d["vol60"])
    sl = {}
    for h in hs:
        sl[f"logwidth_h{h}"] = cl_slope(d, "lw", f"x{h}")
        sl[f"logvol_h{h}"] = cl_slope(d, "lv", f"x{h}")
        sl[f"ret60_h{h}"] = cl_slope(d, "ret60", f"x{h}")
        sl[f"margin_h{h}"] = cl_slope(d, "margin", f"x{h}")
    out["slopes"] = pd.Series(sl)
    # by year spearman width vs x10
    yy = {}
    for y, g in d.groupby("year"):
        x = g[["width", "x10"]].dropna()
        if len(x) > 5:
            r, p = stats.spearmanr(x["width"], x["x10"]); yy[y] = f"rho {r:.3f} p {p:.3f} n {len(x)}"
    out["spearman_width_x10_by_year"] = pd.Series(yy)
    # width vs vol60 relation
    out["corr_logwidth_logvol"] = round(d[["lw", "lv"]].corr().iloc[0, 1], 3)
    d["vq"] = pd.qcut(d["vol60"], 3, labels=["lowvol", "midvol", "highvol"])
    def summ(g):
        s = {}
        for h in hs:
            x = g[f"x{h}"].dropna()
            s[f"m{h}"] = x.mean(); s[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x)))
            s[f"str{h}"] = (g[f"x{h}"] / g[f"u{h}"]).mean()
        s["n"] = len(g)
        return pd.Series(s)
    out["by_vol"] = d.groupby("vq").apply(summ).round(2)
    out["by_width"] = d.groupby("wq").apply(summ).round(2)
    return out
