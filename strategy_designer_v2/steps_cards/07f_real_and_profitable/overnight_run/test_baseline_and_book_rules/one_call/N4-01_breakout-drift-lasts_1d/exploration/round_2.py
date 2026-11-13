def explore(data):
    import pandas as pd, numpy as np
    days = data["days"]; trades = data["trades"]; bars = data["bars"]
    out = {}
    # book vs holding, alpha
    rows = []
    for c in days:
        for w, d in days[c].items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["coin"] = c; x["window"] = w
            rows.append(x)
    A = pd.concat(rows).dropna(subset=["book_return"])
    bk = A.groupby(["window", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    X = np.vstack([np.ones(len(bk)), bk["cr"].values]).T
    beta, *_ = np.linalg.lstsq(X, bk["br"].values, rcond=None)
    res = bk["br"].values - X @ beta
    se = np.sqrt(res.var(ddof=2) / len(bk) * 1)
    out["alpha_beta"] = pd.Series({"alpha_daily": beta[0], "beta": beta[1], "alpha_t": beta[0] / se, "n_days": len(bk)}).round(5)
    bk["up"] = bk["cr"] > 0
    out["book_on_up_vs_down_market_days"] = bk.groupby("up")["br"].agg(["mean", "count", "sum"]).round(5)
    # trade concentration
    T = pd.concat([t.assign(coin=c, window=w) for c in trades for w, t in trades[c].items()])
    s = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trade_conc"] = pd.Series({"n": len(s), "sum": s.sum(), "top10_share": s.iloc[:10].sum() / s.sum(),
                                   "top1pct_share": s.iloc[:len(s)//100].sum() / s.sum(),
                                   "sum_ex_top1pct": s.iloc[len(s)//100:].sum()}).round(4)
    # events: new 20-day high, non-overlapping 10-bar, by prior state
    ev = []
    allr = {}
    for c in bars:
        r10 = []
        for w, b in bars[c].items():
            cl = b["close"].reset_index(drop=True)
            r10.append((cl.shift(-10) / cl - 1).dropna())
        allr[c] = pd.concat(r10).mean()
    col = "debug_info.components.since_high.last_history_value"
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            lr = np.log(cl).diff()
            vol = lr.rolling(20).std()
            mom = cl / cl.shift(20) - 1
            fwd = cl.shift(-10) / cl - 1
            hi = cl.rolling(20).max().shift(1)
            isev = (cl > hi) if col not in b else (b[col] == 20)
            last = -99
            for i in np.where(isev.values)[0]:
                if i - last < 10 or np.isnan(fwd.iloc[i]): continue
                last = i
                ev.append(dict(coin=c, window=w, ex=fwd.iloc[i] - allr[c], vol=vol.iloc[i], mom=mom.iloc[i],
                               year=pd.to_datetime(b["timestamp"].iloc[i]).year))
    E = pd.DataFrame(ev).dropna()
    def tt(x): return pd.Series({"mean": x.mean(), "n": len(x), "t": x.mean() / x.std() * np.sqrt(len(x)), "median": x.median()})
    E["volq"] = E.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False))
    E["momq"] = E.groupby("coin")["mom"].transform(lambda v: pd.qcut(v, 3, labels=False))
    out["ev_by_volq"] = E.groupby("volq")["ex"].apply(tt).unstack().round(4)
    out["ev_by_momq"] = E.groupby("momq")["ex"].apply(tt).unstack().round(4)
    out["ev_by_coin"] = E.groupby("coin")["ex"].apply(tt).unstack().round(4)
    out["ev_by_year"] = E.groupby("year")["ex"].apply(tt).unstack().round(4)
    out["ev_all"] = tt(E["ex"]).round(4)
    Eo = E.sort_values("ex", ascending=False)
    out["ev_ex_top10"] = tt(Eo["ex"].iloc[10:]).round(4)
    return out
