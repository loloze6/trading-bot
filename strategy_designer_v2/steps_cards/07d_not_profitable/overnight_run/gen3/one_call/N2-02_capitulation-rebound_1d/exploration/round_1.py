def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["win"] = w
            tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    T["fb"] = pd.cut(T["entry_forecast"].abs(), [-0.01, 1, 5, 10, 20.01])
    agg = lambda g: pd.Series({"n": len(g), "days_mean": g["days"].mean(), "days_med": g["days"].median(),
        "gross_mean": g["profit_loss_percent"].mean(), "net_mean": g["net_profit_loss_percent"].mean(),
        "comm_mean": g["total_commission"].mean(), "win_share": (g["profit_loss_percent"] > 0).mean()})
    out["trades_all"] = agg(T).to_frame().T
    out["trades_by_side"] = T.groupby("side").apply(agg)
    out["trades_by_entry_fc"] = T.groupby("fb").apply(agg)
    out["trades_by_coin"] = T.groupby("coin").apply(agg)
    # days: book returns by position, market state
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            b = data["bars"][c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            d = d.copy(); d["day"] = pd.to_datetime(d["day"])
            pos = b.set_index("day")["postRebalance_current_allocation"].astype(float)
            fc = b.set_index("day")["forecast"].astype(float)
            d = d.set_index("day")
            d["pos_prev"] = pos.shift(1).reindex(d.index)
            d["fc_prev"] = fc.shift(1).reindex(d.index)
            cl = b.set_index("day")["close"]
            r = np.log(cl).diff()
            vol = r.rolling(20).std()
            d["vol_prev"] = vol.shift(1).reindex(d.index)
            d["mom10_prev"] = (cl / cl.shift(10) - 1).shift(1).reindex(d.index)
            d["coin"] = c; d["win"] = w; d["year"] = d.index.year
            rows.append(d.reset_index())
    D = pd.concat(rows, ignore_index=True).dropna(subset=["book_return"])
    inpos = D[D["pos_prev"].abs() > 1e-6]
    out["share_days_in_pos"] = float(len(inpos) / len(D))
    out["mean_pos_when_in"] = float(inpos["pos_prev"].mean())
    D["pb"] = pd.cut(D["pos_prev"].abs(), [-1e-9, 1e-6, 0.25, 0.5, 1.0, 3.0])
    out["book_by_pos"] = D.groupby("pb")["book_return"].agg(["count", "mean", "sum"])
    inpos = D[D["pos_prev"].abs() > 1e-6].copy()
    inpos["mkt"] = np.where(inpos["coin_return"] > 0, "up", "down")
    out["inpos_by_mktday"] = inpos.groupby("mkt")["book_return"].agg(["count", "mean", "sum"])
    inpos["mom"] = np.where(inpos["mom10_prev"] > 0, "prior10 up", "prior10 down")
    out["inpos_by_prior_mom"] = inpos.groupby("mom").agg(n=("book_return", "count"), book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"))
    q = inpos["vol_prev"].quantile([0.33, 0.66]).values
    inpos["volb"] = pd.cut(inpos["vol_prev"], [-1, q[0], q[1], 9])
    out["inpos_by_vol"] = inpos.groupby("volb").agg(n=("book_return", "count"), book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"))
    out["book_by_year"] = D.groupby("year").agg(n=("book_return", "count"), book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), inpos_share=("pos_prev", lambda x: (x.abs() > 1e-6).mean()))
    out["book_by_coin"] = D.groupby("coin").agg(book_mean=("book_return", "mean"), book_sum=("book_return", "sum"), coin_mean=("coin_return", "mean"))
    # non-overlapping 10-bar forward returns by forecast bucket
    nb = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values.astype(float); fc = b["forecast"].values.astype(float)
            lr = np.log(cl)
            for i in range(0, len(b) - 10, 10):
                m10 = cl[i] / cl[i - 10] - 1 if i >= 10 else np.nan
                nb.append((c, fc[i], cl[i + 10] / cl[i] - 1, m10, b["regime"].iloc[i]))
    N = pd.DataFrame(nb, columns=["coin", "fc", "fwd", "mom10", "reg"])
    N["ex"] = N["fwd"] - N.groupby("coin")["fwd"].transform("mean")
    N["fb"] = pd.cut(N["fc"], [-0.01, 0.001, 1, 5, 10, 20.01])
    out["fwd10_by_fc"] = N.groupby("fb")["ex"].agg(["count", "mean", "std"]).assign(t=lambda x: x["mean"] / x["std"] * np.sqrt(x["count"]))
    act = N[N["fc"] > 0.001].copy()
    act["mom"] = np.where(act["mom10"] > 0, "prior10 up", "prior10 down")
    out["fwd10_active_by_mom"] = act.groupby("mom")["ex"].agg(["count", "mean", "std"]).assign(t=lambda x: x["mean"] / x["std"] * np.sqrt(x["count"]))
    return out
