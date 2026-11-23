def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        d24 = []; d4 = []
        for w, b in ws.items():
            c = b["close"].values
            i = np.arange(0, len(c) - 24, 24); d24.extend(c[i + 24] / c[i] - 1)
            j = np.arange(0, len(c) - 4, 4); d4.extend(c[j + 4] / c[j] - 1)
        dr24 = np.nanmean(d24); dr4 = np.nanmean(d4)
        sd24 = np.nanstd(d24); sd4 = np.nanstd(d4)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; ts = pd.to_datetime(b["timestamp"])
            r2 = c / c.shift(2) - 1
            sc = r2 / r2.abs().rolling(720, min_periods=120).mean()
            r1 = c.pct_change()
            vol = r1.rolling(168, min_periods=48).std()
            df = pd.DataFrame({"coin": coin, "w": w, "h": (ts.dt.hour + 1) % 24,
                               "yr": ts.dt.year, "sc": sc, "r1": r1,
                               "u4": c.shift(-4) / c - 1 - dr4, "s4": sd4,
                               "u24": c.shift(-24) / c - 1 - dr24, "s24": sd24,
                               "past24": (c / c.shift(24) - 1) / (vol * np.sqrt(24)),
                               "vol": vol})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def slope_t(g, x, y):
        g = g.dropna(subset=[x, y])
        if len(g) < 50: return np.nan, len(g)
        lr = stats.linregress(g[x], g[y]); return lr.slope / lr.stderr, len(g)
    A["neg_sc"] = -A["sc"].clip(-10, 10)
    A["neg_p24"] = -A["past24"].clip(-6, 6)
    # 1) 2h move -> 4h reversal at close hours 12-13, by year; size in top fall quintile
    S = A[A.h.isin([12, 13])].copy()
    S0 = A[A.h.isin([0, 1, 2])].copy()
    hv = A[A.h == 0].dropna(subset=["vol"]).copy()
    hv["vq"] = hv.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False))
    hv = hv[hv.vq == 2]
    r = []
    for y in sorted(A.yr.unique()):
        t1, n1 = slope_t(S[S.yr == y], "neg_sc", "u4")
        t2, n2 = slope_t(S0[S0.yr == y], "neg_sc", "u24")
        t3, n3 = slope_t(hv[hv.yr == y], "neg_p24", "u24")
        h2223 = A[(A.yr == y) & A.h.isin([22, 23])]["r1"].dropna()
        r.append({"yr": y, "t_rev4h_h12_13": t1, "n1": n1, "t_rev24h_h0_2": t2,
                  "t_hivol_daily_rev": t3, "n3": n3,
                  "h22_23_bp": h2223.mean() * 1e4,
                  "t_h22_23": stats.ttest_1samp(h2223, 0).statistic})
    out["by_year"] = pd.DataFrame(r).round(2)
    # sizes: signed move in reversal direction, by quintile of |signal|
    sz = []
    S["side"] = np.sign(S["neg_sc"])
    S["q"] = pd.qcut(S["neg_sc"].abs(), 5, labels=False)
    for q, g in S.dropna(subset=["u4"]).groupby("q"):
        unus = g["side"] * g["u4"]
        sz.append({"set": "h12_13_4h", "q": q, "n": len(g),
                   "unusual_pct": unus.mean() * 100, "strength": (unus / g["s4"]).mean()})
    hv["side"] = np.sign(hv["neg_p24"])
    hv["q"] = pd.qcut(hv["neg_p24"].abs(), 5, labels=False)
    for q, g in hv.dropna(subset=["u24"]).groupby("q"):
        unus = g["side"] * g["u24"]
        sz.append({"set": "hivol_24h", "q": q, "n": len(g),
                   "unusual_pct": unus.mean() * 100, "strength": (unus / g["s24"]).mean()})
    # high-vol daily reversal by side
    for side, g in hv.dropna(subset=["u24"]).groupby("side"):
        unus = g["side"] * g["u24"]
        sz.append({"set": "hivol_side", "q": side, "n": len(g),
                   "unusual_pct": unus.mean() * 100, "strength": (unus / g["s24"]).mean()})
    out["sizes"] = pd.DataFrame(sz).round(4)
    # per coin high-vol daily reversal t
    pc = []
    for coin, g in hv.groupby("coin"):
        t, n = slope_t(g, "neg_p24", "u24"); pc.append({"coin": coin, "t": t, "n": n})
    out["hivol_by_coin"] = pd.DataFrame(pc).round(2)
    return out
