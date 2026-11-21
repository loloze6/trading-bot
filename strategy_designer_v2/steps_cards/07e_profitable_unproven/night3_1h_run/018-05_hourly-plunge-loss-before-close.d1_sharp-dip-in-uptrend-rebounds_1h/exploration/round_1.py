def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    coins = list(bars.keys())
    # ---- book daily returns, market part
    rows = []
    for c in coins:
        allret = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        mu = allret.mean()
        for w, b in bars[c].items():
            b = b.copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].mean()
            d = days[c][w].copy()
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D")
            d = d.set_index("day")
            d["pos"] = pos.shift(1).reindex(d.index)
            d["coin"] = c; d["w"] = w; d["mu"] = mu
            d["year"] = d.index.year
            rows.append(d.reset_index())
    D = pd.concat(rows)
    D["mkt"] = D["pos"] * D["mu"]
    book = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"),
                                         mkt=("mkt", "mean"), year=("year", "first")).dropna()
    out["book_total"] = pd.Series({"mean_book": book.br.mean(), "mean_mkt_part": book.mkt.mean(),
                                   "timing": book.br.mean() - book.mkt.mean(),
                                   "hold_mean": book.cr.mean(), "n_days": len(book),
                                   "t_book": book.br.mean() / book.br.std() * np.sqrt(len(book))})
    out["by_coin"] = D.groupby("coin").agg(mean_br=("book_return", "mean"), mkt=("mkt", "mean"),
                                           mean_pos=("pos", "mean"), coin_mean=("coin_return", "mean"))
    out["by_window"] = book.groupby("w").agg(br=("br", "mean"), mkt=("mkt", "mean"), cr=("cr", "mean"), n=("br", "size"))
    out["by_year"] = book.groupby("year").agg(br=("br", "mean"), mkt=("mkt", "mean"), cr=("cr", "mean"), n=("br", "size"))
    # ---- trades
    T = pd.concat([trades[c][w].assign(coin=c, w=w) for c in coins for w in trades[c] if len(trades[c][w])])
    p = T["net_profit_loss_percent"]
    ps = p.sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "mean_net": p.mean(), "median_net": p.median(), "win_share": (p > 0).mean(),
                               "top10_share_of_sum": ps.head(10).sum() / p.sum(), "top5pct_share": ps.head(int(len(ps) * .05)).sum() / p.sum(),
                               "mean_dur_h": T["duration_minutes"].mean() / 60, "long_share": (T.side == "LONG").mean(),
                               "entry_fc_mean": T.entry_forecast.mean(), "entry_fc_share20": (T.entry_forecast >= 19.99).mean()})
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    # ---- cases on grid, multiple horizons, graded by raw value
    H = [24, 72, 168, 336]
    cases = []; grid = []
    for c in coins:
        drift = {}
        for h in H:
            r = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r.append(cl[idx + h] / cl[idx] - 1)
            drift[h] = np.concatenate(r).mean()
        for w, b in bars[c].items():
            cl = b["close"].values; f = b["forecast"].fillna(0).values
            raw = b["debug_info.components.dip_in_rise.last_history_value"].values
            n = len(cl)
            onset = np.where((f > 0) & (np.r_[0, f[:-1]] == 0))[0]
            seen = set()
            for i in onset:
                g = i // 72
                if g in seen: continue
                seen.add(g)
                rec = {"coin": c, "raw": raw[i], "fc": f[i], "hour": pd.Timestamp(b["timestamp"].iloc[i]).hour}
                for h in H:
                    rec[f"u{h}"] = cl[i + h] / cl[i] - 1 - drift[h] if i + h < n else np.nan
                cases.append(rec)
            # all-grid: 30d trend and 24h dip, unusual 72h
            s = pd.Series(cl)
            r24 = s.pct_change(24); ma = r24.abs().rolling(720).mean(); r30 = s.pct_change(720)
            idx = np.arange(0, n - 72, 72)
            for i in idx:
                if np.isnan(ma.iloc[i]) or np.isnan(r30.iloc[i]): continue
                grid.append({"coin": c, "dipz": r24.iloc[i] / ma.iloc[i], "r30": r30.iloc[i],
                             "u72": cl[i + 72] / cl[i] - 1 - drift[72]})
    C = pd.DataFrame(cases)
    def tt(x):
        x = x.dropna(); return pd.Series({"mean": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)), "n": len(x)})
    out["cases_by_h"] = pd.DataFrame({h: tt(C[f"u{h}"]) for h in H})
    C["rawq"] = pd.qcut(C["raw"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["cases_by_raw_tercile"] = C.groupby("rawq")[["u24", "u72", "u168", "fc"]].mean()
    out["cases_by_coin"] = C.groupby("coin")["u72"].agg(["mean", "count"])
    G = pd.DataFrame(grid)
    G["up"] = G.r30 > 0
    G["dip"] = pd.cut(G.dipz, [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["grid_up_dip"] = G.groupby(["up", "dip"])["u72"].agg(["mean", "count"])
    out["grid_up_t"] = pd.DataFrame({"up": tt(G[G.up].u72), "down": tt(G[~G.up].u72)})
    return out
