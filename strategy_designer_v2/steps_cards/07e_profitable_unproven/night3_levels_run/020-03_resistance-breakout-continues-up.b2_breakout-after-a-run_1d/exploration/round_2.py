def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]; out = {}
    hs = [5, 10, 20]
    drift = {}
    for coin in bars:
        for h in hs:
            r = []
            for w, b in bars[coin].items():
                c = b["close"].values; idx = np.arange(0, len(c) - h, h)
                r.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(r)
    recs = []
    for coin in bars:
        for w, b in bars[coin].items():
            c = pd.Series(b["close"].values)
            run20 = c.pct_change(20).values
            near = (c / c.rolling(60, min_periods=20).max()).values
            vol = c.pct_change().rolling(20, min_periods=10).std().values
            tr = (b["regime"].values == "trending")
            cv = c.values
            for h in hs:
                for i in np.arange(0, len(cv) - h, h):
                    # breakout anywhere in cell's first bar? use the cell's start bar
                    recs.append((coin, w, h, run20[i], near[i], vol[i], tr[i],
                                 cv[i + h] / cv[i] - 1 - drift[(coin, h)]))
    R = pd.DataFrame(recs, columns=["coin", "w", "h", "run20", "near", "vol", "tr", "unus"]).dropna()
    def tt(x):
        return pd.Series({"n": len(x), "unus": x.unus.mean(),
                          "t": x.unus.mean() / (x.unus.std() / np.sqrt(len(x)))})
    for h in hs:
        S = R[R.h == h].copy()
        S["rq"] = S.groupby("coin")["run20"].transform(lambda s: pd.qcut(s, 5, labels=False))
        out[f"h{h}_by_run20_quint"] = S.groupby("rq").apply(tt)
        S["nq"] = S.groupby("coin")["near"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out[f"h{h}_by_near60_quint"] = S.groupby("nq").apply(tt)
        P = S[S.run20 > 0]
        out[f"h{h}_run20pos_breakout_vs_not"] = P.groupby("tr").apply(tt)
        # strength by run quintile: unusual / coin usual move
        P2 = S[S.rq == 4]
        out[f"h{h}_toprun_breakout_vs_not"] = P2.groupby("tr").apply(tt)
        # regression unus on zrun20, znear, tr
        X = np.column_stack([np.ones(len(S)),
                             S.groupby("coin")["run20"].transform(lambda s: (s - s.mean()) / s.std()),
                             S.groupby("coin")["near"].transform(lambda s: (s - s.mean()) / s.std()),
                             S.tr.astype(float)])
        y = S.unus.values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ beta
        cov = np.linalg.inv(X.T @ X) * (e @ e) / (len(y) - X.shape[1])
        out[f"h{h}_ols"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))},
                                        index=["const", "z_run20", "z_near60", "breakout"])
        sd = R[R.h == h].groupby("coin").unus.std()
        out[f"h{h}_usual_move"] = sd
    # book concentration
    D = pd.concat([d.assign(coin=c, w=w) for c in days for w, d in days[c].items()]).dropna(subset=["book_return"])
    D["year"] = pd.to_datetime(D["day"]).dt.year
    daily = D.groupby(["w", "day"])["book_return"].mean()
    s = daily.sort_values(ascending=False)
    k = max(1, len(s) // 100)
    out["book_conc"] = pd.Series({"n_days": len(s), "mean": s.mean(), "mean_drop_top1pct": s.iloc[k:].mean(),
                                  "mean_drop_top5pct": s.iloc[len(s)//20:].mean(),
                                  "mean_excl_2020": D[D.year != 2020].book_return.mean(),
                                  "sharpe": s.mean() / s.std() * np.sqrt(365)})
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values() if len(t)])
    T["year"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades_by_year"] = T.groupby("year")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
