def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    out = {}
    # A. daily book: mean, market part, timing; by window up/down state
    D = []
    for c, ws in days.items():
        allc = pd.concat([d["coin_return"] for d in ws.values()]).dropna()
        mu = allc.mean()
        for w, d in ws.items():
            b = bars[c][w]
            a = b.groupby(pd.to_datetime(b["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"].mean().values
            dd = d.copy().reset_index(drop=True)
            n = min(len(a), len(dd))
            dd = dd.iloc[:n]; dd["alloc"] = np.r_[np.nan, a[:n-1]] if n > 0 else []
            dd["coin"] = c; dd["window"] = w; dd["mu"] = mu
            D.append(dd)
    D = pd.concat(D).dropna(subset=["book_return", "coin_return"])
    D["mkt"] = D["alloc"].fillna(0) * D["mu"]
    br = D.groupby(["window", "day"])["book_return"].mean()
    mk = D.groupby(["window", "day"])["mkt"].mean()
    ho = D.groupby(["window", "day"])["coin_return"].mean()
    out["daily_book"] = pd.Series(dict(mean=br.mean(), market_part=mk.mean(), timing=br.mean() - mk.mean(),
                                       sharpe=br.mean() / br.std() * np.sqrt(365), hold_mean=ho.mean(),
                                       hold_sharpe=ho.mean() / ho.std() * np.sqrt(365), n_days=len(br)))
    # book mean by the coins' trailing 7-day state (day-level, coin level)
    D["c7"] = D.groupby(["coin", "window"])["coin_return"].transform(lambda s: (1 + s).rolling(7).apply(np.prod, raw=True).shift(1) - 1)
    D["c7q"] = pd.qcut(D["c7"].rank(method="first"), 5, labels=False)
    out["book_by_prior7d_quint"] = D.groupby("c7q").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), alloc=("alloc", "mean"), n=("book_return", "size"))
    # B. 18-bar unusual move graded by 7-day return: all grid bars vs breakout bars
    rows = []
    for c, ws in bars.items():
        allr = pd.concat([(b["close"].shift(-18) / b["close"] - 1).iloc[::18].dropna() for b in ws.values()])
        mu, sd = allr.mean(), allr.std()
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            fr = b["close"].shift(-18) / b["close"] - 1
            t7 = b["close"] / b["close"].shift(42) - 1
            vol = (b["close"].pct_change()).rolling(180).std() * np.sqrt(42)
            hi12 = b["high"].rolling(12).max().shift(1)
            brk = b["close"] > hi12
            d = pd.DataFrame(dict(cell=np.arange(len(b)) // 18, fr=fr, t7=t7, z7=t7 / vol, brk=brk))
            g = d.iloc[::18].dropna(); g["kind"] = "grid"
            k = d[d.brk].dropna().groupby("cell").first(); k["kind"] = "breakout"
            for x in (g, k):
                x = x.copy(); x["un"] = x.fr - mu; x["st"] = x.un / sd; rows.append(x)
    R = pd.concat(rows)
    R["zq"] = R.groupby("kind")["z7"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    a = R.groupby(["kind", "zq"]).agg(n=("un", "size"), unusual=("un", "mean"), sd=("un", "std"), strength=("st", "mean"))
    a["t"] = a.unusual / (a.sd / np.sqrt(a.n)); out["h18_by_z7_quint"] = a.drop(columns="sd")
    for k in ["grid", "breakout"]:
        x = R[R.kind == k]; out["corr_z7_st_" + k] = float(np.corrcoef(x.z7, x.st)[0, 1])
    # C. trades by entry state
    T = []
    for c, ws in trades.items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            b = bars[c][w].copy(); b["ts"] = pd.to_datetime(b["timestamp"])
            b["t7"] = b["close"] / b["close"].shift(42) - 1
            t = t.copy(); t["et"] = pd.to_datetime(t["entry_time"])
            m = pd.merge_asof(t.sort_values("et"), b[["ts", "t7"]].sort_values("ts"), left_on="et", right_on="ts", direction="backward")
            T.append(m)
    T = pd.concat(T).dropna(subset=["t7"])
    T["q"] = pd.qcut(T.t7.rank(method="first"), 5, labels=False)
    out["trades_by_entry7d"] = T.groupby("q").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), median_net=("net_profit_loss_percent", "median"), dur_h=("duration_minutes", lambda s: s.mean() / 60))
    return out
