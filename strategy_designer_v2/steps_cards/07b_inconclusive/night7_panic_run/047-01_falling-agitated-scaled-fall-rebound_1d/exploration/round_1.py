def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 3, 5, 10]
    # drift per coin per horizon on the grid over all its windows
    drift = {}
    for c, ws in bars.items():
        for h in H:
            vals = []
            for w, b in ws.items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                vals.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.nanmean(vals)
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            r = pd.Series(cl).pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = (r / sd).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            n = len(cl)
            for i in range(0, n - 3, 3):
                rec = dict(coin=c, win=w, year=yr[i], regime=b["regime"].iloc[i],
                           fc=b["forecast"].iloc[i], z=z[i], ret1=r.iloc[i],
                           day=str(pd.to_datetime(b["timestamp"].iloc[i]).date()))
                for h in H:
                    rec[f"u{h}"] = (cl[i + h] / cl[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                rows.append(rec)
    df = pd.DataFrame(rows)
    df["inprof"] = df["regime"] == "unknown"
    df["down"] = df["ret1"] < 0

    def tday(s, sub):
        g = sub.groupby("day")[s].sum()
        g = g.dropna()
        if len(g) < 3: return (np.nan, len(g))
        return (g.mean() / (g.std(ddof=1) / np.sqrt(len(g))), len(g))

    def summ(sub):
        out = {}
        for h in H:
            t, nd = tday(f"u{h}", sub)
            out[f"mean_u{h}"] = sub[f"u{h}"].mean()
            out[f"t_u{h}"] = t
        out["cases"] = len(sub)
        out["days"] = sub["day"].nunique()
        return pd.Series(out)

    cases = df[df["inprof"] & (df["fc"] > 0)]
    res = {}
    res["cases_overall"] = summ(cases)
    res["by_coin"] = cases.groupby("coin").apply(summ)
    res["by_year"] = cases.groupby("year").apply(summ)
    res["by_window"] = cases.groupby("win").apply(summ)
    cases = cases.copy()
    cases["zq"] = pd.qcut(-cases["z"], 4, labels=["q1_small", "q2", "q3", "q4_large"])
    res["by_fall_size_quartile"] = cases.groupby("zq").apply(summ)
    # comparisons
    res["prof_down_all"] = summ(df[df.inprof & df.down])
    res["prof_up"] = summ(df[df.inprof & ~df.down & df.ret1.notna()])
    res["outprof_down"] = summ(df[~df.inprof & df.down])
    out_d = df[~df.inprof & df.down].copy()
    out_d["zq"] = pd.qcut(-out_d["z"], 4, labels=["q1_small", "q2", "q3", "q4_large"])
    res["outprof_down_by_quartile"] = out_d.groupby("zq").apply(summ)
    pu = df[df.inprof & ~df.down & df.ret1.notna()].copy()
    pu["zq"] = pd.qcut(pu["z"], 4, labels=["q1_small", "q2", "q3", "q4_large"])
    res["prof_up_by_quartile"] = pu.groupby("zq").apply(summ)
    # slope
    s = stats.linregress(-cases["z"].fillna(0), cases["u3"].fillna(0))
    res["slope_u3_on_scaledfall"] = pd.Series(dict(slope=s.slope, t=s.slope / s.stderr, n=len(cases)))
    return res
