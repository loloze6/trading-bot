def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    H = [24, 48, 96, 192]
    # drift per coin per horizon (non-overlapping)
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.append(cl[idx + h] / cl[idx] - 1)
            rs = np.concatenate(rs); drift[(c, h)] = rs.mean(); usual[(c, h)] = rs.std()
    # cases
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            f = b["forecast"].fillna(0).values; cl = b["close"].values
            n = len(cl)
            r24 = np.full(n, np.nan); r24[24:] = cl[24:] / cl[:-24] - 1
            r720 = np.full(n, np.nan); r720[720:] = cl[720:] / cl[:-720] - 1
            raw = b.get("debug_info.components.plunge_in_uptrend.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            hr = pd.to_datetime(b["timestamp"]).dt.hour.values
            prev = np.r_[0, f[:-1]]
            cand = np.where((f >= 2) & (prev < 2))[0]
            seen = set()
            for i in cand:
                cell = i // 96
                if cell in seen: continue
                seen.add(cell)
                d = {"coin": c, "win": w, "year": yr[i], "hour": hr[i], "f": f[i], "r24": r24[i], "r720": r720[i], "raw": raw[i]}
                for h in H:
                    d[f"u{h}"] = (cl[i + h] / cl[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                    d[f"t{h}"] = (cl[i + h] / cl[i] - 1) if i + h < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    def summ(g):
        r = {}
        for h in H:
            x = g[f"u{h}"].dropna()
            r[f"u{h}"] = x.mean(); r[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        r["n"] = g["u96"].notna().sum()
        return pd.Series(r)
    out["cases_all"] = summ(df).to_frame().T
    out["cases_by_coin"] = df.groupby("coin").apply(summ)
    out["cases_by_year"] = df.groupby("year").apply(summ)
    df["fq"] = pd.qcut(df["f"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["cases_by_forecast_tercile"] = df.groupby("fq").apply(summ)
    df["rq"] = pd.qcut(df["r720"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["cases_by_30d_tercile"] = df.groupby("rq").apply(summ)
    df["dq"] = pd.qcut(df["r24"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["cases_by_24h_fall_tercile"] = df.groupby("dq").apply(summ)
    out["case_feature_means"] = df[["r24", "r720", "f"]].describe().T
    # book decomposition
    brs = []; mkt = []
    for c in bars:
        allr = []
        for w, b in bars[c].items():
            cl = b["close"].values; allr.append(cl[1:] / cl[:-1] - 1)
        mh = np.concatenate(allr).mean()
        for w, b in bars[c].items():
            a = b["postRebalance_current_allocation"].fillna(0).values
            ts = pd.to_datetime(b["timestamp"])
            t = pd.DataFrame({"day": ts.dt.floor("D").values, "m": a * mh})
            md = t.groupby("day")["m"].sum()
            dd = days[c][w][["day", "book_return", "coin_return"]].copy()
            dd["day"] = pd.to_datetime(dd["day"])
            dd = dd.set_index("day").join(md.rename("mkt"))
            dd["coin"] = c; dd["win"] = w
            dd["year"] = dd.index.year
            brs.append(dd.reset_index())
    B = pd.concat(brs).dropna(subset=["book_return"])
    daily = B.groupby(["win", "day"]).agg(book=("book_return", "mean"), mkt=("mkt", "mean"), hold=("coin_return", "mean"), year=("year", "first"))
    out["book_decomp"] = pd.DataFrame({"mean_book": [daily.book.mean()], "mean_mkt": [daily.mkt.mean()], "timing": [daily.book.mean() - daily.mkt.mean()],
                                       "sharpe": [daily.book.mean() / daily.book.std() * np.sqrt(365)], "hold_sharpe": [daily.hold.mean() / daily.hold.std() * np.sqrt(365)], "ndays": [len(daily)]})
    out["book_by_coin"] = B.groupby("coin").agg(book=("book_return", "mean"), mkt=("mkt", "mean"), hold=("coin_return", "mean"))
    out["book_by_year"] = daily.groupby("year").agg(book=("book", "mean"), mkt=("mkt", "mean"), hold=("hold", "mean"), n=("book", "size"))
    wsum = daily.groupby(level=0)["book"].sum().sort_values()
    out["book_window_sum_sorted"] = wsum
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values() if len(t)])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.DataFrame({"n": [len(p)], "mean_net": [p.mean()], "median_net": [p.median()], "win_share": [(p > 0).mean()],
                                  "top10pct_share_of_sum": [p.head(max(1, len(p)//10)).sum() / p.sum()], "sum_excl_top10pct": [p.iloc[len(p)//10:].sum()],
                                  "mean_dur_h": [T["duration_minutes"].mean() / 60]})
    return out
