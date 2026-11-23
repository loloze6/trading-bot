def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---------- book daily returns ----------
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    # side held per coin-day: allocation held at the last bar of the previous day ~ use bars
    book = D.groupby(["wn", "day"])["book_return"].mean().dropna().reset_index().sort_values(["wn", "day"])
    v = (1 + book["book_return"]).cumprod()
    peak = v.cummax(); dd_ = v / peak - 1
    book["dd"] = dd_.values; book["v"] = v.values
    i_tr = int(np.argmin(dd_.values)); i_pk = int(np.argmax(v.values[:i_tr + 1]))
    out["deepest_fall"] = pd.Series({"depth": dd_.values[i_tr], "days_peak_to_trough": i_tr - i_pk,
                                     "peak_window": book["wn"].iloc[i_pk], "trough_window": book["wn"].iloc[i_tr],
                                     "peak_year": pd.Timestamp(book["day"].iloc[i_pk]).year,
                                     "trough_year": pd.Timestamp(book["day"].iloc[i_tr]).year})
    # falls by window: worst drawdown inside each window and window return
    g = []
    for wn, b in book.groupby("wn"):
        vv = (1 + b["book_return"]).cumprod()
        g.append({"wn": wn, "ret": vv.iloc[-1] - 1, "maxdd": (vv / vv.cummax() - 1).min(),
                  "sharpe": b["book_return"].mean() / b["book_return"].std() * np.sqrt(365)})
    out["by_window"] = pd.DataFrame(g).set_index("wn").round(4)
    # ---------- cases ----------
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            cl = b["close"].astype(float); vol = b["volume"].astype(float)
            r1 = cl.pct_change()
            mad = r1.abs().rolling(60, min_periods=20).mean().shift(1)
            r20 = cl / cl.shift(20) - 1
            r7 = cl / cl.shift(7) - 1
            vr = vol / vol.rolling(60, min_periods=20).mean().shift(1)
            sd20 = r1.rolling(20).std()
            sd60 = r1.rolling(60).std()
            fwd = cl.shift(-2) / cl - 1
            for i in range(len(b)):
                if ts[i].weekday() == 6 and b["forecast"].iloc[i] != 0 and not np.isnan(fwd[i]):
                    cs.append({"coin": c, "wn": int(w[1:]), "year": ts[i].year,
                               "f": b["forecast"].iloc[i], "r1": r1[i], "z": r1[i] / mad[i] if mad[i] else np.nan,
                               "fwd": fwd[i], "alloc": b["postRebalance_current_allocation"].iloc[i],
                               "r20": r20[i], "r7": r7[i], "vr": vr[i], "volratio": sd20[i] / sd60[i]})
    C = pd.DataFrame(cs)
    C["side"] = np.sign(C["f"])
    C["sret"] = C["side"] * C["fwd"]
    C["aret"] = C["alloc"] * C["fwd"]  # position gain over the 2 days
    def summ(gb):
        r = gb.agg(n=("sret", "size"), mean_sret=("sret", "mean"), sd=("sret", "std"),
                   book_gain_sum=("aret", "sum"), worst_book=("aret", "min"))
        r["t"] = r["mean_sret"] / (r["sd"] / np.sqrt(r["n"]))
        return r.round(5)
    out["by_side"] = summ(C.groupby("side"))
    out["by_year"] = summ(C.groupby("year"))
    C["absz_q"] = pd.qcut(C["z"].abs(), 5, labels=False)
    out["by_absz_quintile"] = summ(C.groupby("absz_q"))
    # trend: does the bet go against the 20-day trend?
    C["against_trend"] = np.sign(C["r20"]) != C["side"]  # side opposite to the 20d move = bet against trend
    out["by_side_x_against20dtrend"] = summ(C.groupby(["side", "against_trend"]))
    C["volr_q"] = pd.qcut(C["volratio"], 3, labels=False)
    out["by_vol_ratio_tercile"] = summ(C.groupby("volr_q"))
    C["vr_q"] = pd.qcut(C["vr"], 3, labels=False)
    out["by_sunday_volume_tercile"] = summ(C.groupby("vr_q"))
    # tail of losses
    q = C["aret"].quantile([0.01, 0.05, 0.5, 0.95, 0.99])
    out["case_book_gain_quantiles"] = q
    out["share_of_loss_in_worst_5pct"] = C.loc[C["aret"] <= q[0.05], "aret"].sum() / C.loc[C["aret"] < 0, "aret"].sum()
    out["mean_abs_alloc_by_absz_q"] = C.groupby("absz_q")["alloc"].apply(lambda s: s.abs().mean())
    return out
