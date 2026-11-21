def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 26
    bars = data["bars"]
    drift = {}
    for coin, ws in bars.items():
        rs = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rs.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(rs) if rs else np.nan
    cases, grid, daily = [], [], []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]; r1 = c.pct_change()
            p26 = c / c.shift(26) - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            vrel = vol20 / vol60
            f = df["forecast"].fillna(0)
            sig = ((f - f.shift(1)) >= 2) & (f.shift(1) == 0)
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for i in range(0, n, H):
                js = [j for j in range(i, min(i + H, n)) if sig.iloc[j]]
                if not js: continue
                j = js[0]
                if j + H >= n: continue
                fwd = c.iloc[j + H] / c.iloc[j] - 1
                cases.append(dict(coin=coin, w=w, un=fwd - drift[coin], p26=p26.iloc[j], vol=vol20.iloc[j],
                                  p26v=p26.iloc[j] / (vol20.iloc[j] * np.sqrt(26)) if vol20.iloc[j] > 0 else np.nan,
                                  vrel=vrel.iloc[j], yr=ts.iloc[j].year))
            for i in range(0, n - H, H):
                fwd = c.iloc[i + H] / c.iloc[i] - 1
                grid.append(dict(coin=coin, w=w, un=fwd - drift[coin], p26=p26.iloc[i], vol=vol20.iloc[i],
                                 p26v=p26.iloc[i] / (vol20.iloc[i] * np.sqrt(26)) if vol20.iloc[i] > 0 else np.nan,
                                 yr=ts.iloc[i].year))
            for k in range(1, n - 1):
                daily.append((coin, w, ts.iloc[k + 1].normalize(), ts.iloc[k + 1].weekday(), r1.iloc[k + 1], r1.iloc[k], vol20.iloc[k]))
    C = pd.DataFrame(cases); G = pd.DataFrame(grid)
    out = {}
    def sp(d, col):
        d = d.dropna(subset=[col, "un"])
        if len(d) < 8: return (np.nan, np.nan, len(d))
        r, p = stats.spearmanr(d[col], d["un"]); return (round(r, 3), round(p, 4), len(d))
    C["half"] = np.where(C["yr"] <= 2022, "to2022", "from2023")
    G["half"] = np.where(G["yr"] <= 2022, "to2022", "from2023")
    rows = {}
    for h in ["to2022", "from2023"]:
        for col in ["p26", "vol", "p26v", "vrel"]:
            rows[("cases", h, col)] = sp(C[C.half == h], col)
        for col in ["p26", "vol", "p26v"]:
            rows[("grid", h, col)] = sp(G[G.half == h], col)
    out["spearman_by_half"] = pd.DataFrame(rows, index=["rho", "p", "n"]).T
    # partial: p26 rank vs vol rank in cases
    d = C.dropna(subset=["p26", "vol", "un"]).copy()
    for col in ["p26", "vol", "un"]: d[col + "_r"] = d.groupby("coin")[col].rank(pct=True)
    X = np.column_stack([np.ones(len(d)), d["p26_r"], d["vol_r"]])
    b, *_ = np.linalg.lstsq(X, d["un_r"].values, rcond=None)
    res = d["un_r"].values - X @ b; s2 = res @ res / (len(d) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["cases_rank_regression"] = pd.DataFrame({"coef": b, "t": b / se}, index=["const", "p26", "vol"]).round(3)
    # cases per coin sign of p26 effect
    pc = {}
    for coin, g in C.groupby("coin"):
        g = g.dropna(subset=["p26"])
        if len(g) >= 8: pc[coin] = stats.spearmanr(g["p26"], g["un"])[0]
    pc = pd.Series(pc); out["cases_p26_rho_per_coin"] = pd.Series({"neg": (pc < 0).sum(), "pos": (pc > 0).sum(), "median": pc.median()}).round(3)
    pv = {}
    for coin, g in C.groupby("coin"):
        g = g.dropna(subset=["vol"])
        if len(g) >= 8: pv[coin] = stats.spearmanr(g["vol"], g["un"])[0]
    pv = pd.Series(pv); out["cases_vol_rho_per_coin"] = pd.Series({"neg": (pv < 0).sum(), "pos": (pv > 0).sum(), "median": pv.median()}).round(3)
    # grid momentum per coin
    pg = {}
    for coin, g in G.groupby("coin"):
        g = g.dropna(subset=["p26"])
        if len(g) >= 15: pg[coin] = stats.spearmanr(g["p26"], g["un"])[0]
    pg = pd.Series(pg); out["grid_p26_rho_per_coin"] = pd.Series({"neg": (pg < 0).sum(), "pos": (pg > 0).sum(), "median": pg.median()}).round(3)
    # daily: weekday on per-day cross-coin mean (removes shared moves)
    D = pd.DataFrame(daily, columns=["coin", "w", "day", "wd", "r", "prev", "vol"]).dropna()
    M = D.groupby(["w", "day"]).agg(r=("r", "mean"), wd=("wd", "first")).reset_index()
    M["yr"] = pd.to_datetime(M["day"]).dt.year
    wk = M.groupby("wd")["r"].agg(["mean", "std", "count"]); wk["t"] = wk["mean"] / (wk["std"] / np.sqrt(wk["count"]))
    out["weekday_on_daily_mean"] = wk.round(5)
    wkh = M.assign(h=np.where(M.yr <= 2022, "to2022", "from2023")).groupby(["h", "wd"])["r"].mean().unstack().round(5)
    out["weekday_by_half"] = wkh
    # prev-day reversal: per coin z = prev/vol; per coin result
    D["z"] = D["prev"] / D["vol"]
    D["zq"] = D.groupby("coin")["z"].rank(pct=True)
    low = D[D.zq <= 0.1]
    pcr = low.groupby("coin")["r"].mean()
    out["after_worst_decile_day"] = pd.Series({"mean": low["r"].mean(), "n": len(low), "coins_pos": (pcr > 0).sum(), "coins": len(pcr),
                                               "mean_all": D["r"].mean()}).round(5)
    low2 = low.copy(); low2["h"] = np.where(pd.to_datetime(low2.day).dt.year <= 2022, "to2022", "from2023")
    out["after_worst_decile_by_half"] = low2.groupby("h")["r"].agg(["mean", "count"]).round(5)
    # dedupe by day: one obs per market day among worst-decile days
    ld = low.groupby(["w", "day"])["r"].mean()
    out["after_worst_decile_daymeans"] = pd.Series({"mean": ld.mean(), "n_days": len(ld), "t": ld.mean() / (ld.std() / np.sqrt(len(ld)))}).round(4)
    return out
