def explore(data):
    import pandas as pd, numpy as np
    out = {}
    coins = list(data["days"].keys())
    recs = []
    for c in coins:
        for w, d in data["days"][c].items():
            b = data["bars"][c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last()
            fc = b.groupby("day")["forecast"].last()
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D") if not np.issubdtype(dd["day"].dtype, np.datetime64) else dd["day"].dt.floor("D")
            dd = dd.set_index("day")
            dd["pos_prev"] = pos.reindex(dd.index).shift(1)
            dd["fc_prev"] = fc.reindex(dd.index).shift(1)
            cl = dd["close"]
            dd["ret30_prev"] = (cl / cl.shift(30) - 1).shift(1)
            dd["ret7_prev"] = (cl / cl.shift(7) - 1).shift(1)
            dd["vol30_prev"] = dd["coin_return"].rolling(30).std().shift(1)
            dd["coin"] = c; dd["window"] = w
            dd["wn"] = int(w[1:])
            recs.append(dd.reset_index())
    D = pd.concat(recs)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    # book daily
    bk = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean"), pos=("pos_prev", "mean")).reset_index().sort_values(["wn", "day"])
    bk = bk.dropna(subset=["book"])
    eq = (1 + bk["book"]).cumprod().values
    peak = np.maximum.accumulate(eq)
    ddv = eq / peak - 1
    bk["dd"] = ddv
    yr = eq[-1] ** (365 / len(eq)) - 1
    out["summary"] = pd.Series({"yearly": yr, "maxdd": ddv.min(), "calmar": yr / -ddv.min(), "ndays": len(eq)})
    # drawdown episodes
    bk["i"] = np.arange(len(bk))
    eps = []
    inn = False
    for i, v in enumerate(ddv):
        if v < 0 and not inn:
            start = i; inn = True
        if inn and (v == 0 or i == len(ddv) - 1):
            seg = bk.iloc[start:i + 1]
            j = seg["dd"].idxmin()
            tr = seg.loc[j]
            pk = start - 1
            sub = bk.iloc[max(pk, 0):bk.index.get_loc(j) + 1] if False else None
            trough_i = int(seg["dd"].values.argmin()) + start
            fall = bk.iloc[start:trough_i + 1]
            eps.append({"depth": seg["dd"].min(), "days_to_trough": trough_i - start + 1,
                        "windows": f"w{int(fall.wn.min())}-w{int(fall.wn.max())}",
                        "coin_ret_sum_fall": fall["coin"].sum(), "mean_pos_fall": fall["pos"].mean(),
                        "share_short_days": (fall["pos"] < 0).mean(), "year": int(pd.to_datetime(fall["day"]).dt.year.iloc[0])})
            inn = False
    E = pd.DataFrame(eps).sort_values("depth").head(8)
    out["top_drawdowns"] = E
    # per window
    out["per_window"] = bk.groupby("wn").agg(book=("book", "sum"), coin=("coin", "sum"), pos=("pos", "mean"), mindd=("dd", "min")).round(4)
    # long vs short per coin-day
    X = D.dropna(subset=["book_return", "pos_prev"]).copy()
    X["side"] = np.sign(X["pos_prev"])
    out["by_side"] = X.groupby("side")["book_return"].agg(["mean", "std", "count", "sum"])
    X["gain_mkt"] = X["pos_prev"] * X.groupby("coin")["coin_return"].transform("mean")
    out["by_side_coinmove"] = X.groupby("side").agg(coin=("coin_return", "mean"), mkt_part=("gain_mkt", "mean"))
    # by prior 30-day return tercile per side
    X["r30q"] = X.groupby("coin")["ret30_prev"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["side_x_r30"] = X.groupby(["side", "r30q"])["book_return"].agg(["mean", "std", "count"])
    X["volq"] = X.groupby("coin")["vol30_prev"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["side_x_vol"] = X.groupby(["side", "volq"])["book_return"].agg(["mean", "std", "count"])
    X["r7q"] = X.groupby("coin")["ret7_prev"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["side_x_r7"] = X.groupby(["side", "r7q"])["book_return"].agg(["mean", "std", "count"])
    out["by_year"] = X.groupby(["year", "side"])["book_return"].agg(["mean", "count"]).unstack()
    return out
