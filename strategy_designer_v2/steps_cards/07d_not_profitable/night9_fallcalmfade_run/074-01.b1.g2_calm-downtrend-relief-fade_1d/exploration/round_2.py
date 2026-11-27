def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            r = pd.Series(c).pct_change().values
            n = len(b)
            run = np.zeros(n, int)
            for i in range(1, n):
                run[i] = run[i-1] + 1 if r[i] < 0 else 0
            sd30 = pd.Series(r).rolling(30).std().shift(1).values
            ret60 = pd.Series(c) / pd.Series(c).shift(60) - 1
            ret5 = pd.Series(c) / pd.Series(c).shift(5) - 1
            for i in range(31, n - 1):
                sig = b["forecast"].iloc[i] < 0
                up_after = (r[i] > 0) and run[i-1] >= 2
                if up_after:
                    rl = run[i-1]
                    depth = -(c[i-1] / c[i-1-rl] - 1) / sd30[i] if i-1-rl >= 0 else np.nan
                    kind = "upday_after_run"
                elif r[i] < 0 and run[i] >= 2:
                    rl = run[i]
                    depth = -(c[i] / c[i-rl] - 1) / sd30[i] if i-rl >= 0 else np.nan
                    kind = "still_falling"
                else:
                    depth = np.nan
                    kind = "other"
                f = lambda h: c[i+h] / c[i] - 1 if i + h < n else np.nan
                rows.append(dict(coin=coin, w=w, sig=sig, kind=kind, depth=depth,
                                 ret60=ret60.iloc[i], ret5=ret5.iloc[i],
                                 n1=f(1), n3=f(3), n5=f(5), i=i,
                                 alloc=b["postRebalance_current_allocation"].iloc[i],
                                 day=str(b["timestamp"].iloc[i])[:10]))
    d = pd.DataFrame(rows)
    for h in ["n1", "n3", "n5"]:
        d["s" + h[1]] = -d[h]
    def summ(g):
        o = dict(n=len(g))
        for h in ["s1", "s3", "s5"]:
            x = g[h].dropna()
            o[h] = x.mean(); o["t" + h[1]] = stats.ttest_1samp(x, 0)[0] if len(x) > 2 else np.nan
        return pd.Series(o)
    fall = d[d.ret60 < -0.10]
    fall = fall.assign(deep=pd.cut(fall.depth, [0, 1.75, 2.85, 100], labels=["<1.75", "1.75-2.85", ">2.85"]))
    out["falling_kind_by_depth"] = fall.groupby(["kind", "deep"]).apply(summ)
    out["falling_signal_vs_not"] = fall.groupby(["sig", "kind"]).apply(summ)
    sg = d[d.sig].copy()
    sg["deep"] = sg.depth > 2.85
    out["signal_deep_vs_not"] = sg.groupby("deep").apply(summ)
    # non-overlapping 5-day for deep signals: count distinct (coin, w, i//5)
    dp = sg[sg.deep].copy()
    dp["cell"] = dp.i // 5
    dp5 = dp.drop_duplicates(["coin", "w", "cell"])
    out["deep_5d_nonoverlap"] = pd.Series(dict(n=len(dp5), s5=dp5.s5.mean(), t5=stats.ttest_1samp(dp5.s5.dropna(), 0)[0],
                                               days=dp5.day.nunique()))
    out["deep_by_window"] = sg[sg.deep].groupby("w").apply(summ)
    out["shallow_by_window"] = sg[~sg.deep].groupby("w").apply(summ)
    # losses of shallow cases: share of book loss
    out["loss_split"] = pd.Series(dict(
        deep_sum_s1=(sg[sg.deep].s1 * sg[sg.deep].alloc.abs()).sum(),
        shallow_sum_s1=(sg[~sg.deep].s1 * sg[~sg.deep].alloc.abs()).sum(),
        shallow_worst=sg[~sg.deep].s1.min(), deep_worst=sg[sg.deep].s1.min(),
        shallow_sd=sg[~sg.deep].s1.std(), deep_sd=sg[sg.deep].s1.std()))
    # deep cases in w9 / w13
    out["w9_w13_cases"] = sg[sg.w.isin(["w9", "w13", "w12", "w17"])].groupby(["w", "deep"]).apply(summ)
    return out
