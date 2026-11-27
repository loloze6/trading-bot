def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    out = {}
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = (b.close - b.low) / (b.high - b.low)
            r1 = b.close / b.close.shift(1) - 1
            df = pd.DataFrame({"coin": c, "w": w, "cl": cl,
                               "r5": b.close / b.close.shift(5) - 1,
                               "r20": b.close / b.close.shift(20) - 1,
                               "r10": b.close / b.close.shift(10) - 1,
                               "vol": r1.rolling(20).std(),
                               "inprof": b.regime != "chop", "sig": b.regime == "mean_reversion",
                               "alloc": b.postRebalance_current_allocation,
                               "prev": b.previous_allocation, "pos": np.arange(len(b)),
                               "day": pd.to_datetime(b.timestamp).dt.floor("D")})
            df["ent"] = (df.alloc < 0) & (df.prev >= 0)
            for h in (2, 3, 5, 10):
                df[f"f{h}"] = b.close.shift(-h) / b.close - 1
            recs.append(df)
    S = pd.concat(recs, ignore_index=True)
    def summ(x, col="f5"):
        y = -x[col].dropna()
        return pd.Series({"n": len(y), "short_mean": y.mean(),
                          "t": y.mean() / (y.std() / np.sqrt(len(y))) if len(y) > 2 else np.nan})
    g = S[S.pos % 5 == 0]
    deep20 = g.r20 < -0.10
    out["condition_alone_vs_with_signal_grid"] = pd.DataFrame({
        "prof_r20lt-10_signal": summ(g[g.inprof & g.sig & deep20]),
        "prof_r20lt-10_nosignal": summ(g[g.inprof & ~g.sig & deep20]),
        "prof_r20ge-10_signal": summ(g[g.inprof & g.sig & ~deep20]),
        "outprof_r20lt-10_all": summ(g[~g.inprof & deep20]),
        "outprof_r20lt-10_upCL_r5neg": summ(g[~g.inprof & deep20 & (g.cl > .5) & (g.r5 < 0)]),
        "prof_r5lt-5_nosignal": summ(g[g.inprof & ~g.sig & (g.r5 < -0.05)]),
        "prof_r5lt-5_signal": summ(g[g.inprof & g.sig & (g.r5 < -0.05)]),
        "prof_r5ge-5_signal": summ(g[g.inprof & g.sig & (g.r5 >= -0.05)]),
    }).T
    # all signal bars (not only grid) by r5 bucket and r20 bucket
    sg = S[S.sig]
    out["signalbars_by_r5"] = sg.groupby(pd.cut(sg.r5, [-1, -0.15, -0.10, -0.05, -0.02, 0])).apply(summ)
    out["signalbars_by_r10"] = sg.groupby(pd.cut(sg.r10, [-1, -0.2, -0.1, 0, 0.1, 9])).apply(summ)
    out["signalbars_by_r20"] = sg.groupby(pd.cut(sg.r20, [-1, -0.2, -0.1, 0, 9])).apply(summ)
    for h in (2, 3, 10):
        out[f"signalbars_r20_f{h}"] = sg.groupby(pd.cut(sg.r20, [-1, -0.1, 9])).apply(lambda x: summ(x, f"f{h}"))
    # entries: r20 deep share and adverse path
    E = S[S.ent].copy()
    E["deep20"] = E.r20 < -0.10
    E["adv2"] = E.f2 > 0.03
    out["entries_deep20_x_adv2"] = E.groupby(["deep20", "adv2"]).apply(lambda x: pd.Series({
        "n": len(x), "f2": x.f2.mean(), "f5": x.f5.mean(), "f10": x.f10.mean()}))
    # book days: contribution from deep20 entries vs others, per window
    E["contrib"] = -E.f5 * E.alloc.abs()
    out["entries_contrib_by_deep20_window"] = E.groupby(["w", "deep20"]).contrib.sum().unstack()
    out["entries_alloc"] = pd.Series({"mean_abs_alloc": E.alloc.abs().mean(),
                                      "mean_abs_alloc_deep20": E[E.deep20].alloc.abs().mean(),
                                      "mean_abs_alloc_other": E[~E.deep20].alloc.abs().mean()})
    # entries around worst book days
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return"]].copy(); dd["w"] = w; rows.append(dd)
    Dd = pd.concat(rows).groupby(["w", "day"]).book_return.mean().reset_index().dropna()
    worst = Dd.nsmallest(10, "book_return")
    out["worst10_days_by_window"] = worst.groupby("w").book_return.agg(["size", "sum"])
    # held bars on worst days: r20 at entry of the position held
    S["held"] = S.alloc < 0
    hd = S[S.held].copy()
    hd["day"] = hd["day"]
    wk = set(zip(worst.w, pd.to_datetime(worst.day)))
    hd["onworst"] = [(a, b) in wk for a, b in zip(hd.w, hd.day)]
    out["held_on_worst_days"] = hd[hd.onworst].assign(d20=hd.r20 < -0.1).groupby("d20").size()
    return out
