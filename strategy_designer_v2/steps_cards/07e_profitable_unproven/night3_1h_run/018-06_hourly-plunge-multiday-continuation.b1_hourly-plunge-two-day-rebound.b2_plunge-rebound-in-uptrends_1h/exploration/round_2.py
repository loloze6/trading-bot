def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    H = [24, 48, 96, 192]
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.append(cl[idx + h] / cl[idx] - 1)
            rs = np.concatenate(rs); drift[(c, h)] = rs.mean(); usual[(c, h)] = rs.std()
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            f = b["forecast"].fillna(0).values; cl = b["close"].values
            n = len(cl)
            r24 = np.full(n, np.nan); r24[24:] = cl[24:] / cl[:-24] - 1
            r720 = np.full(n, np.nan); r720[720:] = cl[720:] / cl[:-720] - 1
            col = "debug_info.components.plunge_in_uptrend.last_history_value"
            raw = b[col].values if col in b.columns else np.full(n, np.nan)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            yr = ts.dt.year.values; hr = ts.dt.hour.values
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
    out["forecast_at_case"] = df["f"].describe().to_frame().T
    out["share_f_eq_max"] = float((df["f"] >= df["f"].max() - 1e-9).mean())
    out["cases_by_coin"] = df.groupby("coin").apply(summ)
    out["cases_by_year"] = df.groupby("year").apply(summ)
    for name, colname, labs in [("raw", "raw", ["lo", "mid", "hi"]), ("30d", "r720", ["lo", "mid", "hi"]), ("24h", "r24", ["deep", "mid", "shallow"])]:
        try:
            s = df[colname]
            ok = s.notna()
            q = pd.qcut(s[ok].rank(method="first"), 3, labels=labs)
            out[f"cases_by_{name}_tercile"] = df[ok].assign(q=q.values).groupby("q").apply(summ)
        except Exception as e:
            out[f"err_{name}"] = str(e)
    # baseline: all grid bars with 30d return > 0, vs <=0 (unconditional)
    try:
        g = []
        for c in bars:
            for w, b in bars[c].items():
                cl = b["close"].values; n = len(cl)
                idx = np.arange(720, n - 96, 96)
                r720 = cl[idx] / cl[idx - 720] - 1
                r24 = cl[idx] / cl[idx - 24] - 1
                u = cl[idx + 96] / cl[idx] - 1 - drift[(c, 96)]
                g.append(pd.DataFrame({"r720": r720, "r24": r24, "u96": u}))
        G = pd.concat(g)
        G["up30"] = G.r720 > 0; G["fall24"] = G.r24 < 0
        out["grid_baseline_96h"] = G.groupby(["up30", "fall24"])["u96"].agg(["mean", "count", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    except Exception as e:
        out["err_grid"] = str(e)
    # book decomposition
    try:
        brs = []
        for c in bars:
            allr = []
            for w, b in bars[c].items():
                cl = b["close"].values; allr.append(cl[1:] / cl[:-1] - 1)
            mh = np.concatenate(allr).mean()
            for w, b in bars[c].items():
                a = b["postRebalance_current_allocation"].fillna(0).values
                ts = pd.to_datetime(b["timestamp"], utc=True).dt.tz_localize(None).dt.floor("D")
                md = pd.Series(a * mh, index=ts.values).groupby(level=0).sum()
                md.index = pd.to_datetime(md.index).normalize()
                dd = days[c][w][["day", "book_return", "coin_return"]].copy()
                dd["day"] = pd.to_datetime(dd["day"], utc=True).dt.tz_localize(None).dt.normalize()
                dd["mkt"] = dd["day"].map(md)
                dd["inpos"] = dd["day"].map(pd.Series(np.abs(a), index=ts.values).groupby(level=0).mean())
                dd["coin"] = c; dd["win"] = w; dd["year"] = dd["day"].dt.year
                brs.append(dd)
        B = pd.concat(brs).dropna(subset=["book_return"])
        daily = B.groupby(["win", "day"]).agg(book=("book_return", "mean"), mkt=("mkt", "mean"), hold=("coin_return", "mean"), year=("year", "first"))
        out["book_decomp"] = pd.DataFrame({"mean_book": [daily.book.mean()], "mean_mkt": [daily.mkt.mean()], "timing": [daily.book.mean() - daily.mkt.mean()],
            "sharpe": [daily.book.mean() / daily.book.std() * np.sqrt(365)], "hold_sharpe": [daily.hold.mean() / daily.hold.std() * np.sqrt(365)],
            "mean_hold": [daily.hold.mean()], "ndays": [len(daily)]})
        out["book_by_coin"] = B.groupby("coin").agg(book=("book_return", "mean"), mkt=("mkt", "mean"), hold=("coin_return", "mean"), exposure=("inpos", "mean"))
        out["book_by_year"] = daily.groupby("year").agg(book=("book", "mean"), mkt=("mkt", "mean"), hold=("hold", "mean"), n=("book", "size"))
        ws = daily.groupby(level=0)["book"].sum().sort_values()
        out["book_window_sum_sorted"] = ws
        out["book_share_top3_windows"] = float(ws.tail(3).sum() / ws.sum())
    except Exception as e:
        out["err_book"] = str(e)
    try:
        T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values() if len(t)])
        p = T["net_profit_loss_percent"].sort_values(ascending=False)
        k = max(1, len(p) // 10)
        out["trades"] = pd.DataFrame({"n": [len(p)], "mean_net": [p.mean()], "median_net": [p.median()], "win_share": [(p > 0).mean()],
            "top10pct_share_of_sum": [p.head(k).sum() / p.sum()], "sum_excl_top10pct": [p.iloc[k:].sum()],
            "mean_dur_h": [T["duration_minutes"].mean() / 60], "long_share": [(T["side"] == "LONG").mean()]})
        T["dq"] = pd.qcut((T["duration_minutes"]).rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
        out["trades_by_duration_q"] = T.groupby("dq").agg(net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60), n=("net_profit_loss_percent", "size"))
    except Exception as e:
        out["err_trades"] = str(e)
    return out
