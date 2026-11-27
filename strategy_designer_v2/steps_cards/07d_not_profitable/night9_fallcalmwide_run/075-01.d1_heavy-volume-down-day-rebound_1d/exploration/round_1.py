def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns: mean over coins per (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day", "book_return", "coin_return"]].copy()
            t["coin"] = c; t["w"] = w
            rows.append(t)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.dropna(subset=["book_return"]).groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), n=("coin", "count")).reset_index().sort_values(["wn", "day"])
    B["val"] = (1 + B["br"]).cumprod()
    B["peak"] = B["val"].cummax()
    B["dd"] = B["val"] / B["peak"] - 1
    out["book_by_window"] = B.groupby("wn").agg(mean_br=("br", "mean"), sd=("br", "std"), min_dd=("dd", "min"), coin_mean=("cr", "mean"), days=("br", "count"))
    i = B["dd"].idxmin()
    trough = B.loc[i]
    pk = B.loc[:i]
    pk = pk[pk["val"] == pk["peak"]].index[-1]
    seg = B.loc[pk:i]
    out["deepest_fall"] = pd.Series({"depth": trough["dd"], "days": len(seg), "w_start": B.loc[pk, "wn"], "w_end": trough["wn"], "book_sum": seg["br"].sum(), "coins_sum": seg["cr"].sum()})
    out["worst20_book_days"] = B.nsmallest(20, "br")[["wn", "br", "cr", "n"]].reset_index(drop=True)

    # case level
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; v = b["volume"]
            r1 = cl / cl.shift(1) - 1
            vr = v / v.shift(1).rolling(20).mean()
            nxt = cl.shift(-1) / cl - 1
            r5 = cl / cl.shift(5) - 1
            r20 = cl / cl.shift(20) - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60, min_periods=40).std()
            rng = (b["high"] - b["low"]) / cl.shift(1)
            clpos = (cl - b["low"]) / (b["high"] - b["low"])
            t = pd.DataFrame({"r1": r1, "vr": vr, "nxt": nxt, "r5": r5, "r20": r20, "volrel": vol20 / vol60, "rng": rng, "clpos": clpos,
                              "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"], "coin": c, "wn": int(w[1:]), "pos": np.arange(len(b))})
            cs.append(t)
    A = pd.concat(cs).dropna(subset=["nxt", "r1", "vr"])
    drift = A.groupby("coin")["nxt"].mean()
    A["ex"] = A["nxt"] - A["coin"].map(drift)
    A["case"] = (A["r1"] < 0) & (A["vr"] > 1)
    A["pnl"] = A["alloc"] * A["nxt"]
    C = A[A["case"]].copy()

    def summ(g):
        return pd.Series({"n": len(g), "mean_nxt": g["nxt"].mean(), "mean_ex": g["ex"].mean(), "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "mean_alloc": g["alloc"].mean(), "pnl_sum": g["pnl"].sum()})
    out["case_by_drop_size"] = C.groupby(pd.qcut(C["r1"], 5)).apply(summ)
    out["case_by_vr"] = C.groupby(pd.qcut(C["vr"], 5)).apply(summ)
    out["case_by_r20"] = C.dropna(subset=["r20"]).groupby(pd.qcut(C["r20"].dropna(), 5)).apply(summ)
    out["case_by_r5"] = C.dropna(subset=["r5"]).groupby(pd.qcut(C["r5"].dropna(), 5)).apply(summ)
    out["case_by_volrel"] = C.dropna(subset=["volrel"]).groupby(pd.qcut(C["volrel"].dropna(), 4)).apply(summ)
    out["case_by_clpos"] = C.dropna(subset=["clpos"]).groupby(pd.qcut(C["clpos"].dropna(), 4)).apply(summ)
    out["case_by_window"] = C.groupby("wn").apply(summ)
    # non-case: condition alone (r20 low) baseline
    N = A[~A["case"]].dropna(subset=["r20"])
    out["noncase_by_r20"] = N.groupby(pd.qcut(N["r20"], 5)).apply(summ)
    out["noncase_down_lowvr_by_drop"] = A[(A["r1"] < 0) & (A["vr"] <= 1)].groupby(pd.qcut(A.loc[(A["r1"] < 0) & (A["vr"] <= 1), "r1"], 5)).apply(summ)
    # held positions beyond case day? pnl on non-case bars
    out["pnl_case_vs_noncase"] = pd.Series({"pnl_case": A.loc[A["case"], "pnl"].sum(), "pnl_noncase": A.loc[~A["case"], "pnl"].sum(),
                                           "noncase_held_bars": int((A.loc[~A["case"], "alloc"].abs() > 0).sum()), "case_bars": int(A["case"].sum()),
                                           "case_fc0": int((C["fc"] <= 0).sum()), "mean_alloc_case": C["alloc"].mean()})
    return out
