def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    out = {}
    # mean hourly return per coin over all windows
    mh = {}
    for c in coins:
        rs = []
        for w, b in bars[c].items():
            rs.append(b["close"].pct_change().dropna())
        mh[c] = pd.concat(rs).mean()
    # per-bar gain decomposition, aggregated per day
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            r = b["close"].shift(-1) / b["close"] - 1
            a = b["postRebalance_current_allocation"].fillna(0)
            d = pd.to_datetime(b["timestamp"]).dt.floor("D")
            df = pd.DataFrame({"day": d, "gain": a * r, "mkt": a * mh[c], "time": a * (r - mh[c]),
                               "alloc": a, "fc": b["forecast"]})
            g = df.groupby("day").agg(gain=("gain", "sum"), mkt=("mkt", "sum"), time=("time", "sum"),
                                      alloc=("alloc", "mean"))
            g["coin"] = c; g["w"] = w
            rows.append(g.reset_index())
    D = pd.concat(rows)
    bk = D.groupby(["w", "day"])[["gain", "mkt", "time", "alloc"]].mean().reset_index()
    out["decomp_mean_daily"] = pd.Series({k: bk[k].mean() for k in ["gain", "mkt", "time", "alloc"]})
    out["t_timing"] = bk["time"].mean() / (bk["time"].std() / np.sqrt(len(bk)))
    # book days from days table
    bd = []
    for c in coins:
        for w, t in days[c].items():
            x = t[["day", "book_return", "coin_return"]].copy(); x["coin"] = c; x["w"] = w; bd.append(x)
    BD = pd.concat(bd).dropna()
    BD["year"] = pd.to_datetime(BD["day"]).dt.year
    pc = BD.groupby("coin").agg(book=("book_return", "mean"), hold=("coin_return", "mean"))
    pc["book_sharpe"] = BD.groupby("coin")["book_return"].apply(lambda s: s.mean() / s.std() * np.sqrt(365))
    pc["hold_sharpe"] = BD.groupby("coin")["coin_return"].apply(lambda s: s.mean() / s.std() * np.sqrt(365))
    pc["timing"] = D.groupby("coin")["time"].mean()
    out["per_coin"] = pc
    pb = BD.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    pw = pb.groupby("w").agg(book=("book_return", "mean"), hold=("coin_return", "mean"), n=("book_return", "size"))
    pw["timing"] = bk.groupby("w")["time"].mean()
    pw["book_sum"] = pb.groupby("w")["book_return"].sum()
    out["per_window"] = pw
    pb["year"] = pd.to_datetime(pb["day"]).dt.year
    out["per_year"] = pb.groupby("year").agg(book=("book_return", "mean"), hold=("coin_return", "mean"), n=("book_return", "size"))
    # trades concentration
    tr = []
    for c in coins:
        for w, t in data["trades"][c].items():
            if len(t): x = t.copy(); x["coin"] = c; tr.append(x)
    T = pd.concat(tr)
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "mean_net": p.mean(), "median_net": p.median(), "win": (p > 0).mean(),
                               "sum": p.sum(), "top10_sum": p.head(10).sum(), "top5pct_sum": p.head(max(1, len(p)//20)).sum(),
                               "mean_days": T["duration_minutes"].mean() / 1440,
                               "short_share": (T["side"] == "SHORT").mean()})
    # horizons
    hz = {}
    for h in [24, 72, 168, 336, 720, 1440]:
        cells = []
        for c in coins:
            allr = []
            for w, b in bars[c].items():
                cl = b["close"].values; fc = b["forecast"].values
                idx = np.arange(0, len(cl) - h, h)
                for i in idx:
                    allr.append((c, cl[i + h] / cl[i] - 1, fc[i]))
            cells += allr
        C = pd.DataFrame(cells, columns=["coin", "r", "fc"])
        C["ex"] = C["r"] - C.groupby("coin")["r"].transform("mean")
        P = C[C.fc > 0]; Z = C[C.fc <= 0]
        v = P.fc * P.ex / P.fc.mean()
        sl = stats.linregress(P.fc, P.ex)
        hz[h] = {"n_pos": len(P), "wmean_ex": v.mean(), "t_w": v.mean() / (v.std() / np.sqrt(len(v))),
                 "mean_ex_pos": P.ex.mean(), "mean_ex_flat": Z.ex.mean(), "n_flat": len(Z),
                 "t_pos_vs_flat": stats.ttest_ind(P.ex, Z.ex, equal_var=False).statistic,
                 "slope_t": sl.slope / sl.stderr, "mean_tot_pos": P.r.mean()}
    out["horizons"] = pd.DataFrame(hz).T
    # forecast quintiles at 336 and 720 per coin-agnostic
    q = []
    for h in [336, 720]:
        cells = []
        for c in coins:
            for w, b in bars[c].items():
                cl = b["close"].values; fc = b["forecast"].values
                r30 = b["close"].pct_change(720).values
                for i in range(0, len(cl) - h, h):
                    cells.append((c, cl[i + h] / cl[i] - 1, fc[i], r30[i]))
        C = pd.DataFrame(cells, columns=["coin", "r", "fc", "r30"])
        C["ex"] = C["r"] - C.groupby("coin")["r"].transform("mean")
        C["bin"] = pd.cut(C.fc, [-0.01, 0.001, 0.5, 1, 1.5, 2.5, 25])
        g = C.groupby("bin", observed=True)["ex"].agg(["mean", "count"]); g["h"] = h
        q.append(g.reset_index())
    out["fc_bins"] = pd.concat(q).astype({"bin": str})
    return out
