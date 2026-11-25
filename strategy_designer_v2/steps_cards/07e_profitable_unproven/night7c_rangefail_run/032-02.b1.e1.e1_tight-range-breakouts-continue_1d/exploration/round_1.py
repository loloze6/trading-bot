def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars, days, trades = data["bars"], data["days"], data["trades"]
    coins = list(bars.keys())
    # coin mean daily return over all windows
    cmean = {}
    for c in coins:
        r = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        cmean[c] = r.mean()
    rows = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].copy()
            b["ret_next"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"].fillna(0)
            b["bv"] = b["postRebalance_total_value"]
            b["br"] = b["bv"].pct_change()
            b["coin"] = c; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["mkt"] = b["pos"].shift(1) * cmean[c]
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    # book daily (1d bars: bar = day): mean over coins per timestamp
    D = B.dropna(subset=["br"]).groupby(["win", "timestamp"]).agg(br=("br", "mean"), mkt=("mkt", "mean")).reset_index()
    out["book mean daily, mkt part, timing part"] = pd.Series({"mean": D.br.mean(), "mkt": D.mkt.mean(), "timing": D.br.mean() - D.mkt.mean(), "n_days": len(D), "t_mean": D.br.mean() / D.br.std() * np.sqrt(len(D))})
    # per coin contribution (each coin's br / 6 summed)
    pc = B.dropna(subset=["br"]).groupby("coin").agg(sum_br=("br", "sum"), mean_br=("br", "mean"), mkt=("mkt", "mean"), inpos=("pos", lambda x: (x.abs() > 0).mean()))
    out["per coin"] = pc
    pw = D.groupby("win").agg(mean=("br", "mean"), mkt=("mkt", "mean"), n=("br", "size"))
    out["per window"] = pw
    D["year"] = pd.to_datetime(D["timestamp"]).dt.year
    out["per year"] = D.groupby("year").agg(mean=("br", "mean"), mkt=("mkt", "mean"), n=("br", "size"))
    # trades concentration
    T = pd.concat([trades[c][w].assign(coin=c, win=w) for c in coins for w in trades[c] if len(trades[c][w])], ignore_index=True)
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "mean_net": p.mean(), "median_net": p.median(), "win_share": (p > 0).mean(), "sum": p.sum(), "top5_sum": p.head(5).sum(), "top10_sum": p.head(10).sum()})
    # case-level: break bars, recomputed from closes; forward returns at several horizons; non-overlapping grid by horizon
    recs = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"]
            hi = cl.shift(1).rolling(60).max(); lo = cl.shift(1).rolling(60).min()
            mad = cl.pct_change().abs().rolling(60).mean()
            W = (hi - lo) / cl / mad
            dist = cl / hi - 1
            r60 = cl / cl.shift(60) - 1
            vol = cl.pct_change().rolling(60).std()
            for h in [5, 10, 20, 40]:
                fr = cl.shift(-h) / cl - 1
                idx = np.arange(len(b))
                cell = idx // h
                df = pd.DataFrame({"brk": dist > 0, "fr": fr, "W": W, "dist": dist / vol, "r60": r60, "cell": cell, "h": h, "coin": c, "win": w, "ts": b["timestamp"]})
                gridret = fr.iloc[::h].dropna()
                df["drift"] = np.nan
                df["gridall"] = 0
                df.loc[df.index[::h], "gridall"] = 1
                recs.append(df)
    R = pd.concat(recs, ignore_index=True)
    drift = R[R.gridall == 1].dropna(subset=["fr"]).groupby(["coin", "h"])["fr"].mean()
    R["drift"] = [drift.get((c, h), np.nan) for c, h in zip(R.coin, R.h)]
    R["un"] = R.fr - R.drift
    cases = R[R.brk].dropna(subset=["fr", "W"]).groupby(["coin", "win", "h", "cell"]).first().reset_index()
    res = []
    for h, g in cases.groupby("h"):
        dd = g.groupby("ts")["un"].sum()
        n_day = len(dd)
        tt = dd.sum() / np.sqrt((dd ** 2).sum()) if n_day > 1 else np.nan
        res.append({"h": h, "n": len(g), "days": n_day, "mean_un": g.un.mean(), "mean_tot": g.fr.mean(), "t_un_approx": tt,
                    "corr_W": stats.spearmanr(g.W, g.un)[0], "corr_dist": stats.spearmanr(g.dist, g.un)[0], "corr_r60": stats.spearmanr(g.r60, g.un)[0]})
    out["cases by horizon"] = pd.DataFrame(res)
    g = cases[cases.h == 20].copy()
    for col in ["W", "dist", "r60"]:
        g["q"] = pd.qcut(g[col], 3, labels=False, duplicates="drop")
        out["h20 terciles of " + col] = g.groupby("q").agg(n=("un", "size"), mean_un=("un", "mean"), mean_x=(col, "mean"))
    # non-break grid comparison at h20: r60 grading over all grid bars
    a = R[(R.h == 20) & (R.gridall == 1)].dropna(subset=["fr", "r60"]).copy()
    a["q"] = pd.qcut(a["r60"], 5, labels=False)
    out["all grid h20 by r60 quintile"] = a.groupby("q").agg(n=("un", "size"), mean_un=("un", "mean"), brk_share=("brk", "mean"), r60=("r60", "mean"))
    out["h20 cases by coin"] = g.groupby("coin").agg(n=("un", "size"), mean_un=("un", "mean"))
    return out
