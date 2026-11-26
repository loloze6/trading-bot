def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # ---- book daily returns
    rows = []
    for c, wd in data["days"].items():
        for w, d in wd.items():
            t = d[["day", "book_return", "coin_return"]].copy()
            t["coin"] = c; t["window"] = w
            rows.append(t)
    D = pd.concat(rows)
    book = D.groupby(["window", "day"])[["book_return", "coin_return"]].mean().dropna()
    bw = book.groupby(level=0)["book_return"].agg(["mean", "std", "count"])
    bw["sharpe"] = bw["mean"] / bw["std"] * np.sqrt(365)
    bw["sum"] = book.groupby(level=0)["book_return"].sum()
    out["book_by_window"] = bw
    out["book_overall"] = pd.Series({"mean": book.book_return.mean(), "sharpe": book.book_return.mean() / book.book_return.std() * np.sqrt(365), "days": len(book)})
    # per coin contribution: sum of coin book_return / number of coins that day
    D2 = D.dropna(subset=["book_return"]).copy()
    ncoin = D2.groupby(["window", "day"])["coin"].transform("count")
    D2["contrib"] = D2.book_return / ncoin
    tot = D2.contrib.sum()
    pc = D2.groupby("coin")["contrib"].sum().to_frame("contrib_sum")
    pc["share"] = pc.contrib_sum / tot
    out["per_coin_contrib"] = pc.sort_values("contrib_sum", ascending=False)
    # ---- bars: market vs timing
    B = []
    for c, wd in data["bars"].items():
        for w, b in wd.items():
            t = b[["timestamp", "open", "high", "low", "close", "regime", "postRebalance_current_allocation", "forecast"]].copy()
            t["coin"] = c; t["window"] = w
            t["ret"] = t.close.pct_change()
            t["std20"] = t.ret.rolling(20).std()
            t["z"] = t.ret / t.std20
            t["r60"] = t.close / t.close.shift(60) - 1
            for h in [1, 2, 3, 5]:
                t[f"f{h}"] = t.close.shift(-h) / t.close - 1
            t["pos"] = np.arange(len(t))
            t["nxt"] = t.close.shift(-1) / t.close - 1
            B.append(t)
    B = pd.concat(B, ignore_index=True)
    mu = B.groupby("coin")["ret"].mean()
    B["mu"] = B.coin.map(mu)
    B["gain"] = B.postRebalance_current_allocation * B.nxt
    B["mkt"] = B.postRebalance_current_allocation * B.mu
    B["timing"] = B.gain - B.mkt
    held = B[B.postRebalance_current_allocation.abs() > 1e-9]
    out["gain_split_sum"] = pd.Series({"gain": held.gain.sum(), "market": held.mkt.sum(), "timing": held.timing.sum(), "held_bars": len(held), "share_long": (held.postRebalance_current_allocation > 0).mean()})
    # gain by z-bucket of entry day, and by regime of held bars
    held = held.copy()
    held["zb"] = pd.cut(held.z, [-np.inf, -3, -2, -1.5, -1, -0.5, 0, np.inf])
    out["gain_by_z"] = held.groupby("zb", observed=True).agg(n=("gain", "size"), gain_sum=("gain", "sum"), nxt_mean=("nxt", "mean"))
    out["gain_by_regime"] = held.groupby("regime").agg(n=("gain", "size"), gain_sum=("gain", "sum"))
    # ---- trades concentration
    T = []
    for c, wd in data["trades"].items():
        for w, t in wd.items():
            t = t.copy(); t["coin"] = c; t["window"] = w; T.append(t)
    T = pd.concat(T, ignore_index=True)
    p = T.net_profit_loss_percent.sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "sum": p.sum(), "top10": p.head(10).sum(), "top20": p.head(20).sum(), "mean_dur_days": T.duration_minutes.mean() / 1440, "win": (p > 0).mean()})
    # ---- signal study, non-overlapping grid, excess returns
    res = []
    for h in [1, 2, 3, 5]:
        g = B[(B.pos % h == 0)].dropna(subset=[f"f{h}", "z"]).copy()
        g["ex"] = g[f"f{h}"] - h * g.mu
        g["prof"] = np.where(g.regime == "unknown", "fa", "other")
        g["side"] = np.where(g.z < 0, "down", "up")
        for (pr, sd), s in g.groupby(["prof", "side"]):
            x = s.ex; zz = s.z.abs()
            sl = stats.linregress(zz, x) if len(s) > 10 else None
            res.append({"h": h, "prof": pr, "side": sd, "n": len(s), "mean_ex": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)), "slope": sl.slope if sl else np.nan, "slope_t": sl.slope / sl.stderr if sl else np.nan})
    out["signal"] = pd.DataFrame(res)
    # in-profile by z buckets h=1, and next-day return conditional
    g = B[(B.regime == "unknown")].dropna(subset=["nxt", "z"]).copy()
    g["ex"] = g.nxt - g.mu
    g["zb"] = pd.cut(g.z, [-np.inf, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 2, np.inf])
    out["fa_nextday_by_z"] = g.groupby("zb", observed=True)["ex"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # day close location in range within profile, down days
    g["clv"] = (g.close - g.low) / (g.high - g.low)
    dd = g[g.z < 0].copy()
    dd["cb"] = pd.qcut(dd.clv, 4)
    out["fa_down_by_closeloc"] = dd.groupby("cb", observed=True)["ex"].agg(["count", "mean"])
    g["year"] = pd.to_datetime(g.timestamp).dt.year
    out["fa_down_by_year"] = g[g.z < -1].groupby("year")["ex"].agg(["count", "mean"])
    return out
