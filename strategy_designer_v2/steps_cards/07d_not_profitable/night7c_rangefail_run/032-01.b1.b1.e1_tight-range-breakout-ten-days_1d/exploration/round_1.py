def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- book daily series
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), n=("coin", "count")).reset_index().sort_values(["wn", "day"])
    B["br"] = B["br"].fillna(0)
    v = (1 + B["br"]).cumprod().values
    peak = np.maximum.accumulate(v)
    dd = v / peak - 1
    B["dd"] = dd
    i_tr = int(np.argmin(dd)); i_pk = int(np.argmax(v[:i_tr + 1]))
    out["deepest_fall"] = pd.Series({"depth": dd[i_tr], "days_peak_to_trough": i_tr - i_pk,
                                     "window_peak": B["wn"].iloc[i_pk], "window_trough": B["wn"].iloc[i_tr],
                                     "yearly_ret": v[-1] ** (365 / len(v)) - 1})
    # falls by window
    g = B.groupby("wn")
    out["by_window"] = pd.DataFrame({"book_sum": g["br"].sum(), "coin_mean_sum": g["cr"].sum(), "min_dd": g["dd"].min(),
                                     "year": B.groupby("wn")["day"].first().astype(str).str[:4]})
    # ---- trade-level features from bars
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            f = b["forecast"].fillna(0).values
            n = len(b)
            ret1 = pd.Series(cl).pct_change()
            for t in range(1, n):
                if f[t] > 0 and f[t - 1] == 0 and t >= 60 and t + 10 < n:
                    ph = hi[t - 60:t].max(); pl = lo[t - 60:t].min()
                    r10 = cl[t + 10] / cl[t] - 1
                    path = cl[t + 1:t + 11] / cl[t] - 1
                    back_in = (cl[t + 1:t + 4] < ph).any()
                    recs.append(dict(coin=c, w=w, brk=cl[t] / ph - 1, width=(ph - pl) / cl[t],
                                     ret60=cl[t] / cl[t - 60] - 1, ret20=cl[t] / cl[t - 20] - 1,
                                     vol20=ret1.iloc[t - 19:t + 1].std(), r1=cl[t] / cl[t - 1] - 1,
                                     r10=r10, mae=path.min(), back_in3=back_in,
                                     r3=cl[t + 3] / cl[t] - 1, r3to10=cl[t + 10] / cl[t + 3] - 1,
                                     below_ph_d3=cl[t + 3] < ph))
    T = pd.DataFrame(recs)
    out["n_entries"] = len(T)
    def grp(col, q=3):
        T["_q"] = pd.qcut(T[col], q, labels=False, duplicates="drop")
        r = T.groupby("_q").agg(lo=(col, "min"), hi=(col, "max"), n=("r10", "count"), r10=("r10", "mean"),
                                mae=("mae", "mean"), share_loss=("r10", lambda x: (x < 0).mean()))
        return r
    for col in ["brk", "width", "ret60", "ret20", "vol20", "r1"]:
        out["by_" + col] = grp(col)
    out["by_below_ph_d3"] = T.groupby("below_ph_d3").agg(n=("r10", "count"), r3=("r3", "mean"), r3to10=("r3to10", "mean"),
                                                         r10=("r10", "mean"))
    out["by_coin"] = T.groupby("coin").agg(n=("r10", "count"), r10=("r10", "mean"), mae=("mae", "mean"))
    out["by_window_trades"] = T.groupby("w").agg(n=("r10", "count"), r10=("r10", "mean"), mae=("mae", "mean"))
    return out
