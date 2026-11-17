def explore(data):
    import pandas as pd, numpy as np
    out = {}
    coins = list(data["days"].keys())
    recs = []
    for c in coins:
        for w, d in data["days"][c].items():
            b = data["bars"][c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"], utc=True).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last()
            fc = b.groupby("day")["forecast"].last()
            sh = b.groupby("day")["debug_info.components.rsi_below_share.last_history_value"].last()
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"], utc=True).dt.floor("D")
            dd = dd.set_index("day")
            dd["pos_prev"] = pos.reindex(dd.index).shift(1)
            dd["fc_prev"] = fc.reindex(dd.index).shift(1)
            dd["share_prev"] = sh.reindex(dd.index).shift(1)
            cl = dd["close"]
            dd["ret30_prev"] = (cl / cl.shift(30) - 1).shift(1)
            dd["ret7_prev"] = (cl / cl.shift(7) - 1).shift(1)
            dd["vol30_prev"] = dd["coin_return"].rolling(30).std().shift(1)
            dd["coin"] = c; dd["wn"] = int(w[1:])
            recs.append(dd.reset_index())
    D = pd.concat(recs, ignore_index=True)
    D["year"] = D["day"].dt.year
    bk = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
                                      pos=("pos_prev", "mean")).reset_index().sort_values(["wn", "day"])
    bk = bk.dropna(subset=["book"]).reset_index(drop=True)
    eq = (1 + bk["book"]).cumprod().values
    peak = np.maximum.accumulate(eq)
    ddv = eq / peak - 1
    bk["dd"] = ddv
    yr = eq[-1] ** (365 / len(eq)) - 1
    out["summary"] = pd.Series({"yearly": yr, "maxdd": ddv.min(), "calmar": yr / -ddv.min(), "ndays": len(eq)})
    eps = []; start = None
    for i, v in enumerate(ddv):
        if v < 0 and start is None:
            start = i
        if start is not None and (v == 0 or i == len(ddv) - 1):
            seg = bk.iloc[start:i + 1]
            ti = int(seg["dd"].values.argmin()) + start
            fall = bk.iloc[start:ti + 1]
            eps.append({"depth": fall["dd"].min(), "days_to_trough": len(fall),
                        "wn_from": int(fall.wn.min()), "wn_to": int(fall.wn.max()),
                        "coin_ret_sum": fall["coin"].sum(), "mean_pos": fall["pos"].mean(),
                        "share_short_days": (fall["pos"] < 0).mean(),
                        "year": int(fall["day"].dt.year.iloc[0])})
            start = None
    out["top_drawdowns"] = pd.DataFrame(eps).sort_values("depth").head(8).round(4)
    out["per_window"] = bk.groupby("wn").agg(book=("book", "sum"), coin=("coin", "sum"),
                                             pos=("pos", "mean"), mindd=("dd", "min")).round(4)
    X = D.dropna(subset=["book_return", "pos_prev"]).copy()
    X["side"] = np.sign(X["pos_prev"])
    X["gain_mkt"] = X["pos_prev"] * X.groupby("coin")["coin_return"].transform("mean")
    out["by_side"] = X.groupby("side").agg(mean=("book_return", "mean"), std=("book_return", "std"),
                                           n=("book_return", "count"), coin=("coin_return", "mean"),
                                           mkt_part=("gain_mkt", "mean"))
    for col, nm in [("ret30_prev", "r30"), ("vol30_prev", "vol"), ("ret7_prev", "r7")]:
        Y = X.dropna(subset=[col]).copy()
        Y["q"] = Y.groupby("coin")[col].transform(lambda s: pd.qcut(s, 3, labels=False))
        out["side_x_" + nm] = Y.groupby(["side", "q"])["book_return"].agg(["mean", "std", "count"])
    out["by_year"] = X.groupby(["year", "side"])["book_return"].agg(["mean", "count"]).unstack()
    return out
