def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # coin mean daily return over all windows
    cm = {}
    for c in days:
        r = pd.concat([d["coin_return"] for d in days[c].values()]).dropna()
        cm[c] = r.mean()
    # per-bar gain decomposition
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            a = b["postRebalance_current_allocation"].fillna(0)
            nr = b["close"].shift(-1) / b["close"] - 1
            g = a * nr
            rows.append(pd.DataFrame({"coin": c, "w": w, "ts": b["timestamp"], "a": a, "g": g,
                                      "mkt": a * cm[c], "year": pd.to_datetime(b["timestamp"]).dt.year}))
    R = pd.concat(rows).dropna(subset=["g"])
    R["side"] = np.where(R["a"] > 0, "long", np.where(R["a"] < 0, "short", "flat"))
    out["gain_by_side"] = R.groupby("side").agg(n=("g", "size"), sum_gain=("g", "sum"), mean_gain=("g", "mean"), sum_mkt=("mkt", "sum"))
    out["gain_by_coin"] = R.groupby("coin").agg(n_in=("a", lambda x: (x != 0).sum()), sum_gain=("g", "sum"), sum_mkt=("mkt", "sum"))
    out["gain_by_window"] = R.groupby("w").agg(n_in=("a", lambda x: (x != 0).sum()), sum_gain=("g", "sum"), sum_mkt=("mkt", "sum"))
    out["gain_by_year_side"] = R[R.side != "flat"].groupby(["year", "side"])["g"].sum().unstack()
    # book daily
    bd = []
    for c in days:
        for w, d in days[c].items():
            bd.append(pd.DataFrame({"day": d["day"], "w": w, "br": d["book_return"]}))
    B = pd.concat(bd).dropna().groupby(["w", "day"])["br"].mean()
    out["book_daily_mean_sd_n"] = pd.Series({"mean": B.mean(), "sd": B.std(), "n": len(B), "sharpe": B.mean() / B.std() * np.sqrt(365)})
    s = B.sort_values(ascending=False)
    out["top_days_share"] = pd.Series({"top10_sum": s.head(10).sum(), "top30_sum": s.head(30).sum(), "all_sum": s.sum()})
    # trades
    T = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if len(t): T.append(t.assign(coin=c, w=w))
    T = pd.concat(T)
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "sum", "median"])
    ts = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades_top"] = pd.Series({"n": len(ts), "top5": ts.head(5).sum(), "top10": ts.head(10).sum(), "all": ts.sum()})
    # forward returns by range position, horizons, in profile
    res = []
    for c in bars:
        allh = {}
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            for h in [3, 5, 10, 20]:
                fr = b["close"].shift(-h) / b["close"] - 1
                allh.setdefault(h, []).append(fr.iloc[::h])
        mh = {h: pd.concat(v).dropna().mean() for h, v in allh.items()}
        sdh = {h: pd.concat(v).dropna().std() for h, v in allh.items()}
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            pos = 2 * (b["close"] - lo) / (hi - lo) - 1
            inprof = b["regime"] == "unknown"
            for h in [3, 5, 10, 20]:
                fr = b["close"].shift(-h) / b["close"] - 1
                idx = np.arange(0, len(b), h)
                d = pd.DataFrame({"pos": pos.iloc[idx], "fr": fr.iloc[idx], "inp": inprof.iloc[idx], "fc": b["forecast"].iloc[idx]})
                d["ex"] = (d["fr"] - mh[h]) / sdh[h]
                d["raw"] = d["fr"] / sdh[h]
                d["h"] = h; d["coin"] = c
                res.append(d)
    D = pd.concat(res).dropna(subset=["pos", "fr"])
    D["q"] = pd.cut(D["pos"], [-1.01, -0.5, 0, 0.5, 0.9, 1.01], labels=["<-.5", "-.5-0", "0-.5", ".5-.9", ">.9"])
    P = D[D.inp]
    out["inprof_strength_by_q_h"] = P.groupby(["h", "q"])["ex"].mean().unstack()
    out["inprof_n_by_q_h"] = P.groupby(["h", "q"])["ex"].size().unstack()
    O = D[~D.inp]
    out["outprof_strength_by_q_h"] = O.groupby(["h", "q"])["ex"].mean().unstack()
    def tt(g):
        r = stats.pearsonr(g["pos"], g["ex"]); return pd.Series({"corr": r[0], "p": r[1], "n": len(g)})
    out["corr_pos_ex_in"] = P.groupby("h").apply(tt)
    out["corr_pos_ex_out"] = O.groupby("h").apply(tt)
    return out
