def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 10
    # --- book daily series ---
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).dropna().reset_index().sort_values(["wn", "day"])
    B["val"] = (1 + B["book"]).cumprod()
    B["hval"] = (1 + B["hold"]).cumprod()
    B["peak"] = B["val"].cummax()
    B["dd"] = B["val"] / B["peak"] - 1
    B["i"] = np.arange(len(B))
    # deepest falls: episodes
    ep = []
    in_dd = False
    for _, r in B.iterrows():
        if r["dd"] < 0 and not in_dd:
            in_dd = True; start = r["i"] - 1; trough = r["i"]; tv = r["dd"]
        if in_dd:
            if r["dd"] < tv: tv = r["dd"]; trough = r["i"]
            if r["dd"] == 0:
                ep.append((start, trough, r["i"], tv)); in_dd = False
    if in_dd: ep.append((start, trough, B["i"].iloc[-1], tv))
    E = pd.DataFrame(ep, columns=["s", "t", "e", "depth"]).sort_values("depth").head(6)
    res = []
    for _, r in E.iterrows():
        seg = B.iloc[int(max(r.s, 0)):int(r.t) + 1]
        res.append({"depth": r.depth, "days_to_trough": int(r.t - r.s), "days_to_recover": int(r.e - r.t),
                    "windows": ",".join(sorted(set("w%d" % x for x in seg.wn))),
                    "hold_ret_in_fall": seg["hval"].iloc[-1] / B["hval"].iloc[int(max(r.s, 0))] - 1,
                    "book_ret_in_fall": seg["val"].iloc[-1] / B["val"].iloc[int(max(r.s, 0))] - 1})
    out["deepest_falls"] = pd.DataFrame(res)
    out["book_maxdd_vs_hold"] = pd.Series({"book_dd": B["dd"].min(), "hold_dd": (B["hval"] / B["hval"].cummax() - 1).min(),
                                           "book_corr_hold": B[["book", "hold"]].corr().iloc[0, 1]})
    # --- bar-level features and grid ---
    G = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            f = pd.DataFrame({"coin": c, "w": w, "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"]})
            f["fwd"] = cl.shift(-H) / cl - 1
            f["r30"] = cl / cl.shift(30) - 1
            f["r90"] = cl / cl.shift(90) - 1
            f["ma100"] = cl / cl.rolling(100, min_periods=60).mean() - 1
            lr = np.log(cl).diff()
            f["vol30"] = lr.rolling(30).std()
            f["dd90"] = cl / cl.rolling(90, min_periods=30).max() - 1
            f["pos"] = np.arange(len(b))
            G.append(f)
    G = pd.concat(G, ignore_index=True)
    drift = G[G.pos % H == 0].groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    g = G[(G.pos % H == 0)].dropna(subset=["fwd"])
    out["alloc_share"] = pd.Series({"mean_alloc": G["alloc"].mean(), "share_alloc>0": (G["alloc"] > 0).mean(),
                                    "share_fc>0": (G["fc"] > 0).mean()})
    g = g.copy()
    g["sig"] = g["fc"] > 0
    def summ(x):
        return pd.Series({"n": len(x), "fwd": x["fwd"].mean(), "ex": x["ex"].mean(),
                          "t_ex": x["ex"].mean() / (x["ex"].std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "worst_fwd_q10": x["fwd"].quantile(0.1)})
    g["fcb"] = pd.cut(g["fc"], [-0.1, 0, 4, 8, 14, 21], labels=["0", "0-4", "4-8", "8-14", "14+"])
    out["by_fc"] = g.groupby("fcb").apply(summ)
    for col in ["r30", "ma100", "vol30", "dd90"]:
        gg = g.dropna(subset=[col]).copy()
        gg["q"] = pd.qcut(gg[col], 4, labels=["q1", "q2", "q3", "q4"])
        out["sig_x_" + col] = gg.groupby(["q", "sig"]).apply(summ)
    # book daily return by coin state: book returns per coin day vs trailing state
    return out
