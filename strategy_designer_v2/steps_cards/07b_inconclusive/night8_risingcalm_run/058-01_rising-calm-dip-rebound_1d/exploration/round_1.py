def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 2, 3, 5, 10]
    # coin mean h-bar return over all windows (grid)
    coinmean = {}
    for c, ws in bars.items():
        for h in H:
            vals = []
            for w, b in ws.items():
                cl = b["close"].values
                for i in range(0, len(cl) - h, h):
                    vals.append(cl[i + h] / cl[i] - 1)
            coinmean[(c, h)] = np.mean(vals) if vals else np.nan
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r = cl.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            pb = (cl / cl.shift(3) - 1) / sd
            tr = cl / cl.shift(60) - 1
            n = len(b)
            for i in range(0, n - 5, 5):
                d = {"coin": c, "win": w, "i": i, "pb": pb.iloc[i], "tr": tr.iloc[i],
                     "inprof": b["regime"].iloc[i] == "unknown", "fc": b["forecast"].iloc[i],
                     "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                     "day": pd.Timestamp(b["timestamp"].iloc[i]).normalize()}
                for h in H:
                    if i + h < n:
                        d["x%d" % h] = cl.iloc[i + h] / cl.iloc[i] - 1 - coinmean[(c, h)]
                rows.append(d)
    df = pd.DataFrame(rows)
    out = {}
    def slope_t(s, y):
        s = s.dropna(subset=["pb", y])
        if len(s) < 10: return (len(s), np.nan, np.nan, np.nan)
        x = -s["pb"]; yy = s[y]
        res = stats.linregress(x, yy)
        return (len(s), res.slope, res.slope / res.stderr, yy.mean())
    dip = df[df.pb < 0]
    cats = {
        "rc_dip": dip[dip.inprof],
        "notrc_dip": dip[~dip.inprof],
        "rising_notrc_dip(agitated?)": dip[(~dip.inprof) & (dip.tr > 0.10)],
        "choppy_dip": dip[(dip.tr.abs() <= 0.10)],
        "falling_dip": dip[(dip.tr < -0.10)],
        "all_dip": dip,
    }
    tab = []
    for k, s in cats.items():
        for h in H:
            n, sl, t, m = slope_t(s, "x%d" % h)
            tab.append({"set": k, "h": h, "n": n, "slope": sl, "t": t, "mean_x": m})
    out["slope_by_set_h"] = pd.DataFrame(tab)
    rc = dip[dip.inprof].copy()
    rc["q"] = pd.qcut(-rc["pb"], 4, labels=False, duplicates="drop")
    out["rc_depth_quartiles"] = rc.groupby("q").agg(n=("x5", "size"), depth=("pb", "mean"),
        x3=("x3", "mean"), x5=("x5", "mean"), x10=("x10", "mean"))
    nr = dip[~dip.inprof].copy()
    nr["q"] = pd.qcut(-nr["pb"], 4, labels=False, duplicates="drop")
    out["notrc_depth_quartiles"] = nr.groupby("q").agg(n=("x5", "size"), depth=("pb", "mean"),
        x3=("x3", "mean"), x5=("x5", "mean"), x10=("x10", "mean"))
    out["rc_by_coin"] = rc.groupby("coin").agg(n=("x5", "size"), x5=("x5", "mean"),
        corr=("x5", lambda v: np.corrcoef(-rc.loc[v.index, "pb"], v)[0, 1] if len(v) > 3 else np.nan))
    out["rc_by_year"] = rc.groupby("year").agg(n=("x5", "size"), x5=("x5", "mean"),
        corr=("x5", lambda v: np.corrcoef(-rc.loc[v.index, "pb"], v)[0, 1] if len(v) > 3 else np.nan))
    out["rc_by_win"] = rc.groupby("win").agg(n=("x5", "size"), x5=("x5", "mean"))
    out["inprof_share_grid"] = float(df.inprof.mean())
    return out
