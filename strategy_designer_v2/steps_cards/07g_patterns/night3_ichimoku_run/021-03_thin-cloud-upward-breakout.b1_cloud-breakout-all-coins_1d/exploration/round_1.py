def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 26
    bars = data["bars"]
    drift, usd = {}, {}
    for coin, ws in bars.items():
        rs = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rs.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(rs) if rs else np.nan
        usd[coin] = np.std(rs, ddof=1) if len(rs) > 1 else np.nan
    grid, cases, daily = [], [], []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]; r1 = c.pct_change()
            past26 = c / c.shift(26) - 1
            past7 = c / c.shift(7) - 1
            vol20 = r1.rolling(20).std()
            volu = df["volume"] / df["volume"].rolling(20).mean()
            hi = df["high"].rolling(26).max(); lo = df["low"].rolling(26).min()
            pos = (c - lo) / (hi - lo)
            f = df["forecast"].fillna(0)
            sig = ((f - f.shift(1)) >= 2) & (f.shift(1) == 0)
            rawcol = "debug_info.components.thin_cloud.last_history_value"
            raw = df[rawcol] if rawcol in df else pd.Series(np.nan, index=df.index)
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for k in range(n - 1):
                daily.append((coin, ts.dt.weekday.iloc[k + 1], r1.iloc[k + 1], abs(r1.iloc[k]) if k > 0 else np.nan, r1.iloc[k]))
            for i in range(0, n - H, H):
                fwd = c.iloc[i + H] / c.iloc[i] - 1
                grid.append(dict(coin=coin, un=fwd - drift[coin], tot=fwd, p26=past26.iloc[i], p7=past7.iloc[i],
                                 vol=vol20.iloc[i], pos=pos.iloc[i], act=f.iloc[i] > 0, yr=ts.iloc[i].year))
            for i in range(0, n, H):
                js = [j for j in range(i, min(i + H, n)) if sig.iloc[j]]
                if not js: continue
                j = js[0]
                if j + H >= n: continue
                fwd = c.iloc[j + H] / c.iloc[j] - 1
                f13 = c.iloc[j + 13] / c.iloc[j] - 1
                cases.append(dict(coin=coin, un=fwd - drift[coin], un13=f13 - drift[coin] / 2, raw=raw.iloc[j], p26=past26.iloc[j],
                                  r1=r1.iloc[j], volu=volu.iloc[j], vol=vol20.iloc[j], pos=pos.iloc[j],
                                  yr=ts.iloc[j].year, s=(fwd - drift[coin]) / usd[coin]))
    G = pd.DataFrame(grid); C = pd.DataFrame(cases)
    def q(df, col, k=5):
        d = df.dropna(subset=[col, "un"]).copy()
        d["q"] = d.groupby("coin")[col].rank(pct=True)
        d["q"] = np.minimum((d["q"] * k).astype(int), k - 1)
        g = d.groupby("q")["un"].agg(["mean", "std", "count"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        return g.round(4)
    def sp(df, col):
        d = df.dropna(subset=[col, "un"])
        r, p = stats.spearmanr(d[col], d["un"])
        return round(r, 3), round(p, 4), len(d)
    out = {}
    for col in ["p26", "p7", "vol", "pos"]:
        out["grid_by_" + col] = q(G, col)
    ga = G.groupby("act")["un"].agg(["mean", "std", "count"]); ga["t"] = ga["mean"] / (ga["std"] / np.sqrt(ga["count"]))
    out["grid_active_vs_not"] = ga.round(4)
    gy = G.groupby("yr")["un"].agg(["mean", "count"]); out["grid_by_year"] = gy.round(4)
    for col in ["raw", "p26", "r1", "volu", "vol", "pos"]:
        out["cases_q3_" + col] = q(C, col, 3)
    out["case_spearman"] = pd.DataFrame({col: sp(C, col) for col in ["raw", "p26", "r1", "volu", "vol", "pos"]}, index=["rho", "p", "n"])
    cy = C.groupby("yr")["un"].agg(["mean", "count"]); out["cases_by_year"] = cy.round(4)
    out["cases_un13_vs_un26"] = pd.Series({"un13": C["un13"].mean(), "un26": C["un"].mean(), "n": len(C)}).round(4)
    D = pd.DataFrame(daily, columns=["coin", "wd", "r", "absprev", "prev"]).dropna()
    wd = D.groupby("wd")["r"].agg(["mean", "std", "count"]); wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["daily_by_weekday"] = wd.round(5)
    D["pq"] = D.groupby("coin")["prev"].rank(pct=True); D["pq"] = np.minimum((D["pq"] * 10).astype(int), 9)
    pq = D.groupby("pq")["r"].agg(["mean", "std", "count"]); pq["t"] = pq["mean"] / (pq["std"] / np.sqrt(pq["count"]))
    out["next_day_by_prev_day_decile"] = pq.round(5)
    # book
    dd = []
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            x = df[["day", "book_return", "coin_return"]].copy(); x["w"] = w; x["coin"] = coin; dd.append(x)
    B = pd.concat(dd).dropna()
    B["wn"] = B["w"].str[1:].astype(int)
    P = B.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    P["yr"] = pd.to_datetime(P["day"]).dt.year
    by = P.groupby("yr")[["book_return", "coin_return"]].agg(["mean", "std"])
    out["book_by_year"] = by.round(5)
    eq = (1 + P["book_return"]).cumprod(); dd_ = eq / eq.cummax() - 1
    P["dd"] = dd_.values
    out["book_deepest_fall"] = round(dd_.min(), 4)
    pw = P.groupby("wn").apply(lambda g: pd.Series({"book": (1 + g.book_return).prod() - 1, "coin": (1 + g.coin_return).prod() - 1}))
    out["book_by_window"] = pw.round(4)
    T = []
    for coin, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df): x = df[["net_profit_loss_percent", "entry_forecast"]].copy(); x["coin"] = coin; T.append(x)
    T = pd.concat(T)
    out["trades_summary"] = T["net_profit_loss_percent"].describe().round(3)
    return out
