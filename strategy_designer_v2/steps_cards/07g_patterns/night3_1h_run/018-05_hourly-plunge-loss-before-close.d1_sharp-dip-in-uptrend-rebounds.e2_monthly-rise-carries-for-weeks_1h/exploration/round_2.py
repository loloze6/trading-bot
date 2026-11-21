def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    col = "debug_info.components.scaled_30d_return.last_history_value"
    out = {}
    def tstat(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

    # B: position in 20-day range and distance to 20-day high, graded, on grids
    recs = []
    for h in (168, 336):
        for coin, ws in bars.items():
            rows = []
            for w, b in ws.items():
                c = b["close"].reset_index(drop=True)
                hi = b["high"].reset_index(drop=True).rolling(480, min_periods=480).max()
                lo = b["low"].reset_index(drop=True).rolling(480, min_periods=480).min()
                pos = (c - lo) / (hi - lo)
                r1d = c / c.shift(24) - 1
                sd1d = (c / c.shift(24) - 1).rolling(720, min_periods=480).std()
                z1d = r1d / sd1d
                raw = pd.to_numeric(b[col], errors="coerce").reset_index(drop=True) if col in b else pd.Series(np.nan, index=c.index)
                yr = pd.to_datetime(b["timestamp"]).dt.year.values
                cv = c.values
                for i in range(0, len(cv) - h, h):
                    rows.append((coin, w, h, cv[i + h] / cv[i] - 1, pos.iloc[i], z1d.iloc[i], raw.iloc[i], yr[i]))
            df = pd.DataFrame(rows, columns=["coin", "w", "h", "ret", "pos", "z1d", "raw", "year"])
            df["ex"] = df["ret"] - df["ret"].mean()
            recs.append(df)
    g = pd.concat(recs)
    tb = []
    for h, d in g.groupby("h"):
        d = d.dropna(subset=["pos"]).copy()
        d["pb"] = pd.cut(d["pos"], [-0.01, 0.2, 0.4, 0.6, 0.8, 0.95, 1.01])
        for k, e in d.groupby("pb", observed=True):
            tb.append((h, str(k), len(e), e["ex"].mean(), tstat(e["ex"])))
        r = stats.linregress(d["pos"], d["ex"])
        tb.append((h, "slope_all", len(d), r.slope, r.slope / r.stderr))
        e = d[d.pos > 0.5]; r = stats.linregress(e["pos"], e["ex"])
        tb.append((h, "slope_upperhalf", len(e), r.slope, r.slope / r.stderr))
    out["B_range_position"] = pd.DataFrame(tb, columns=["h", "bucket", "n", "mean_ex", "t"])

    # B2: 24h move z (on hourly grid at h) graded -> h-forward
    tb = []
    for h, d in g.groupby("h"):
        d = d.dropna(subset=["z1d"]).copy()
        d["zb"] = pd.cut(d["z1d"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
        for k, e in d.groupby("zb", observed=True):
            tb.append((h, str(k), len(e), e["ex"].mean(), tstat(e["ex"])))
        for side, e in (("pos", d[d.z1d > 0]), ("neg", d[d.z1d < 0])):
            r = stats.linregress(e["z1d"], e["ex"])
            tb.append((h, "slope_" + side, len(e), r.slope, r.slope / r.stderr))
    out["B2_24h_move_z"] = pd.DataFrame(tb, columns=["h", "bucket", "n", "mean_ex", "t"])

    # B3: 30d scaled return near zero vs far, both sides, 168h
    d = g[g.h == 168].dropna(subset=["raw"]).copy()
    d["ab"] = pd.cut(d["raw"].abs(), [-0.01, 0.3, 0.7, 1.2, np.inf])
    out["B3_168_by_abs_raw"] = d.groupby("ab", observed=True)["ex"].agg(["count", "mean", tstat])
    out["B3_168_pos_slope_by_half"] = pd.DataFrame(
        [(nm, len(e), stats.linregress(e.raw, e.ex).slope, stats.linregress(e.raw, e.ex).slope / stats.linregress(e.raw, e.ex).stderr)
         for nm, e in (("<=2021", d[(d.raw > 0) & (d.year <= 2021)]), (">2021", d[(d.raw > 0) & (d.year > 2021)]))],
        columns=["half", "n", "slope", "t"])

    # S: stability of Saturday and hours 21-22, 14 by halves
    dd = []
    for coin, ws in days.items():
        for w, x in ws.items():
            x = x.copy(); x["coin"] = coin; dd.append(x)
    D = pd.concat(dd); D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D.day.dt.weekday; D["half"] = np.where(D.day.dt.year <= 2021, "early", "late")
    D["cex"] = D.coin_return - D.groupby("coin").coin_return.transform("mean")
    out["S_weekday_by_half"] = D.groupby(["half", "wd"])["cex"].agg(["count", "mean", tstat]).unstack(0)
    hh = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            ts = pd.to_datetime(b["timestamp"])
            hh.append(pd.DataFrame({"hr": ts.dt.hour.values, "half": np.where(ts.dt.year <= 2021, "early", "late"),
                                    "r": b["close"].pct_change().values, "coin": coin}))
    H = pd.concat(hh).dropna()
    H["r"] -= H.groupby("coin").r.transform("mean")
    H = H[H.hr.isin([1, 2, 3, 14, 21, 22])]
    out["S_hours_by_half"] = H.groupby(["hr", "half"])["r"].agg(["count", "mean", tstat]).unstack(1)

    # E: book: market rise vs timing, and gain by position size
    D = D.sort_values(["coin", "day"])
    alloc = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            ts = pd.to_datetime(b["timestamp"]).dt.floor("D")
            a = b.groupby(ts.values)["postRebalance_current_allocation"].last()
            alloc.append(pd.DataFrame({"coin": coin, "day": a.index, "alloc": a.values}))
    A = pd.concat(alloc); A["day"] = pd.to_datetime(A["day"])
    M = D.merge(A, on=["coin", "day"], how="left")
    M["alloc_prev"] = M.groupby("coin")["alloc"].shift(1)
    mu = M.groupby("coin").coin_return.transform("mean")
    M["mkt"] = M.alloc_prev * mu
    out["E_book_mean_vs_market_part"] = pd.DataFrame({"book_mean": [M.book_return.mean()], "market_part": [M.mkt.mean()]})
    M["ab"] = pd.cut(M.alloc_prev, [-0.01, 0.001, 0.5, 1.0, 1.5, 2.01])
    out["E_book_by_prev_alloc"] = M.groupby("ab", observed=True).agg(n=("book_return", "size"), book=("book_return", "mean"),
                                                                    coin_ex=("cex", "mean"), t=("cex", tstat))
    return out
