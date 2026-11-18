def explore(data):
    import numpy as np, pandas as pd
    out = {}
    days = data["days"]; bars = data["bars"]; trades = data["trades"]
    # book daily returns: per day mean over coins, per window
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    # position at day end
    pos = []
    for c in bars:
        for w, b in bars[c].items():
            bb = b[["timestamp", "postRebalance_current_allocation", "forecast"]].copy()
            bb["day"] = pd.to_datetime(bb["timestamp"]).dt.floor("D")
            g = bb.groupby("day").last().reset_index()
            g["coin"] = c; g["w"] = w
            pos.append(g[["day", "coin", "w", "postRebalance_current_allocation", "forecast"]])
    P = pd.concat(pos)
    D["day"] = pd.to_datetime(D["day"])
    P["day"] = pd.to_datetime(P["day"])
    if D["day"].dt.tz is not None and P["day"].dt.tz is None:
        P["day"] = P["day"].dt.tz_localize(D["day"].dt.tz)
    elif P["day"].dt.tz is not None and D["day"].dt.tz is None:
        P["day"] = P["day"].dt.tz_localize(None)
    D = D.merge(P, on=["day", "coin", "w"], how="left")
    D = D.sort_values(["coin", "w", "day"])
    D["pos_prev"] = D.groupby(["coin", "w"])["postRebalance_current_allocation"].shift(1)
    cm = D.groupby("coin")["coin_return"].mean()
    D["cmean"] = D["coin"].map(cm)
    D["mkt_part"] = D["pos_prev"] * D["cmean"]
    book = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), mk=("mkt_part", "mean"), expo=("pos_prev", lambda x: x.abs().mean())).dropna()
    out["book_overall"] = pd.Series({"mean_br": book.br.mean(), "mean_cr": book.cr.mean(), "mkt_part": book.mk.mean(), "timing": book.br.mean() - book.mk.mean(), "mean_exposure": book.expo.mean(), "sharpe": book.br.mean() / book.br.std() * np.sqrt(365), "hold_sharpe": book.cr.mean() / book.cr.std() * np.sqrt(365)})
    pw = book.groupby("w").agg(br=("br", "mean"), cr=("cr", "mean"), expo=("expo", "mean"), n=("br", "size"))
    pw["br_sum"] = book.groupby("w")["br"].sum()
    pw["cr_sum"] = book.groupby("w")["cr"].sum()
    out["per_window"] = pw
    # per coin
    D2 = D.dropna(subset=["book_return"])
    out["per_coin"] = D2.groupby("coin").agg(br=("book_return", "mean"), cr=("coin_return", "mean"), mk=("mkt_part", "mean"), expo=("pos_prev", lambda x: x.abs().mean()))
    # trades
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()])
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades"] = pd.Series({"n": len(T), "mean_pl": T.profit_loss_percent.mean(), "mean_net": T.net_profit_loss_percent.mean(), "median_net": T.net_profit_loss_percent.median(), "win": (T.net_profit_loss_percent > 0).mean(), "mean_dur_days": T.dur_d.mean(), "median_dur_days": T.dur_d.median()})
    T["durq"] = pd.cut(T.dur_d, [0, 1.5, 3.5, 7.5, 15, 1000])
    out["trades_by_dur"] = T.groupby("durq").agg(n=("net_profit_loss_percent", "size"), net=("net_profit_loss_percent", "mean"), gross=("profit_loss_percent", "mean"))
    # forward returns from breakout bars by distance and by state: daily bars
    rs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b.close; hi = b.high
            ph = hi.shift(1).rolling(20).max()
            dist = (cl - ph) / ph
            r10 = cl.shift(-10) / cl - 1
            r3 = cl.shift(-3) / cl - 1
            r60 = cl / cl.shift(60) - 1
            vol20 = cl.pct_change().rolling(20).std()
            vol60 = cl.pct_change().rolling(60).std()
            rng = (hi.rolling(20).max() - b.low.rolling(20).min()) / cl
            vr = b.volume / b.volume.rolling(20).mean()
            idx = np.arange(0, len(b), 10)
            f = pd.DataFrame({"dist": dist, "r10": r10, "r3": r3, "r60": r60, "vratio": vol20 / vol60, "vr": vr, "fc": b.forecast, "coin": c, "w": w}).iloc[idx]
            rs.append(f)
    R = pd.concat(rs).dropna()
    R["ex10"] = R.r10 - R.coin.map(R.groupby("coin").r10.mean())
    B = R[R.dist > 0].copy()
    out["breakout_n"] = len(B)
    B["distq"] = pd.qcut(B.dist, 3, labels=["low", "mid", "high"])
    out["by_dist"] = B.groupby("distq").agg(n=("ex10", "size"), ex10=("ex10", "mean"), r3=("r3", "mean"))
    B["trend"] = np.where(B.r60 > 0, "up60", "down60")
    out["by_trend60"] = B.groupby("trend").agg(n=("ex10", "size"), ex10=("ex10", "mean"), t=("ex10", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    B["volq"] = pd.qcut(B.vratio, 2, labels=["compressed", "expanding"])
    out["by_volratio"] = B.groupby("volq").agg(n=("ex10", "size"), ex10=("ex10", "mean"))
    B["vq"] = pd.qcut(B.vr, 2, labels=["lowvol", "highvol"])
    out["by_volume"] = B.groupby("vq").agg(n=("ex10", "size"), ex10=("ex10", "mean"))
    # deepest falls of book
    eq = (1 + book.br).cumprod()
    dd = eq / eq.cummax() - 1
    out["maxdd"] = dd.min()
    bw = book.copy(); bw["dd"] = dd.values
    out["dd_by_window_min"] = bw.groupby("w")["dd"].min()
    return out
