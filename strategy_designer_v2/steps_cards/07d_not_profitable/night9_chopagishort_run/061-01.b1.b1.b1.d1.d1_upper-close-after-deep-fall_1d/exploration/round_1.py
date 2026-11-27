def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    # ---- book daily series
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    B = B.dropna().sort_values(["w", "day"]).reset_index(drop=True)
    B["year"] = pd.to_datetime(B["day"]).dt.year
    v = (1 + B["br"]).cumprod(); peak = v.cummax(); dd = v / peak - 1
    B["dd"] = dd.values
    i_trough = int(dd.idxmin()); i_peak = int(v.iloc[:i_trough + 1].idxmax())
    seg = B.iloc[i_peak:i_trough + 1]
    out["deepest_fall"] = pd.Series({"depth": dd.min(), "days": len(seg), "window": seg["w"].iloc[-1],
                                     "year": seg["year"].iloc[-1], "coins_mean_ret_sum": seg["cr"].sum(),
                                     "book_sum": seg["br"].sum()})
    out["book_by_window"] = B.groupby("w").agg(book_sum=("br", "sum"), coin_sum=("cr", "sum"),
                                              min_dd=("dd", "min"), n=("br", "size"))
    out["book_by_year"] = B.groupby("year").agg(book_sum=("br", "sum"), coin_sum=("cr", "sum"))
    # ---- signal bars
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = (b.close - b.low) / (b.high - b.low)
            r5 = b.close / b.close.shift(5) - 1
            r1 = b.close / b.close.shift(1) - 1
            r20 = b.close / b.close.shift(20) - 1
            vol = r1.rolling(20).std()
            f = {h: b.close.shift(-h) / b.close - 1 for h in (1, 2, 3, 5, 10)}
            inprof = b.regime != "chop"
            sig = b.regime == "mean_reversion"
            alloc = b.postRebalance_current_allocation
            ent = (alloc < 0) & (b.previous_allocation >= 0)
            df = pd.DataFrame({"coin": c, "w": w, "cl": cl, "r5": r5, "r1": r1, "r20": r20, "vol": vol,
                               "inprof": inprof, "sig": sig, "ent": ent, "pos": np.arange(len(b)),
                               "year": pd.to_datetime(b.timestamp).dt.year})
            for h in f: df[f"f{h}"] = f[h]
            recs.append(df)
    S = pd.concat(recs, ignore_index=True)
    drift = S[S.pos % 5 == 0].groupby("coin")["f5"].mean()
    S["u5"] = -(S["f5"] - S["coin"].map(drift))  # short direction unusual
    S["t5"] = -S["f5"]
    def summ(x, col="t5"):
        x = x[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    g = S[S.pos % 5 == 0]
    out["grid_groups_short5"] = pd.DataFrame({
        "signal": summ(g[g.sig]), "prof_no_signal": summ(g[g.inprof & ~g.sig]),
        "prof_upperCL_r5pos": summ(g[g.inprof & ~g.sig & (g.cl > .5) & (g.r5 >= 0)]),
        "prof_lowerCL_r5neg": summ(g[g.inprof & ~g.sig & (g.cl <= .5) & (g.r5 < 0)]),
        "out_prof_upperCL_r5neg": summ(g[~g.inprof & (g.cl > .5) & (g.r5 < 0)]),
        "all": summ(g)}).T
    E = S[S.ent]
    out["entries_horizons_short"] = pd.DataFrame({f"f{h}": summ(E, f"f{h}").mul([1, -1, -1]) for h in (1, 2, 3, 5, 10)}).T
    E = E.copy()
    E["r5q"] = pd.qcut(E.r5, 4, labels=False, duplicates="drop")
    E["clq"] = pd.cut(E.cl, [0.5, 0.65, 0.8, 1.01])
    E["r1s"] = np.sign(E.r1)
    E["r20s"] = pd.cut(E.r20, [-9, -0.1, 0, 0.1, 9])
    E["volq"] = pd.qcut(E.vol, 3, labels=False, duplicates="drop")
    for k in ["r5q", "clq", "r1s", "r20s", "volq", "year"]:
        out[f"entries_by_{k}"] = E.groupby(k).apply(lambda x: summ(x))
    out["entries_by_coin"] = E.groupby("coin").apply(lambda x: summ(x))
    # path: after first 2 days adverse
    E["adv2"] = E.f2 > 0.03
    out["entries_adverse2_then_rest"] = E.groupby("adv2").apply(lambda x: pd.Series({
        "n": len(x), "f2": x.f2.mean(), "f5": x.f5.mean(), "f10": x.f10.mean()}))
    # trades
    T = []
    for c in trades:
        for w, t in trades[c].items():
            t = t.copy(); t["coin"] = c; T.append(t)
    T = pd.concat(T)
    out["trades_summary"] = pd.Series({"n": len(T), "mean_net": T.net_profit_loss_percent.mean(),
                                       "median_net": T.net_profit_loss_percent.median(),
                                       "win": (T.net_profit_loss_percent > 0).mean(),
                                       "mean_days": T.duration_minutes.mean() / 1440,
                                       "worst5_mean": T.net_profit_loss_percent.nsmallest(5).mean()})
    return out
