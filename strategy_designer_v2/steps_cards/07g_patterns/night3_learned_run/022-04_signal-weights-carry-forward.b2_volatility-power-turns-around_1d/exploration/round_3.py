def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "r1": r1,
                               "vol30": r1.rolling(30, min_periods=20).std(),
                               "yr": ts.dt.year, "i": np.arange(len(b)),
                               "pos": b["postRebalance_current_allocation"].astype(float)})
            for L in [14, 21, 28, 42]:
                df["r%d" % L] = c / c.shift(L) - 1
            for h in [7, 10, 14]:
                df["f%d" % h] = c.shift(-h) / c - 1
            df["wn"] = int(w[1:])
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["r28v"] = A["r28"] / (A["vol30"] * np.sqrt(28))
    out = {}
    res = []
    for sig in ["r14", "r21", "r28", "r42", "r28v"]:
        for h in [7, 10, 14]:
            g = A[A.i % h == 0].dropna(subset=[sig, "f%d" % h, "vol30"]).copy()
            f = "f%d" % h
            g["ex"] = g[f] - g.groupby("coin")[f].transform("mean")
            g["sd"] = g.groupby("coin")[f].transform("std")
            g["rk"] = g.groupby("coin")[sig].rank(pct=True) - 0.5
            s = stats.linregress(g.rk, g.ex / g.sd)
            pc = sum(stats.linregress(d.rk, d.ex).slope > 0 for _, d in g.groupby("coin"))
            early = g[g.wn <= 12]; late = g[g.wn > 12]
            se = stats.linregress(early.rk, early.ex / early.sd)
            sl = stats.linregress(late.rk, late.ex / late.sd)
            top = g[g.rk > 0.3]
            res.append({"sig": sig, "h": h, "n": len(g), "slope": s.slope, "t": s.slope / s.stderr,
                        "coins_pos": pc, "t_w1_12": se.slope / se.stderr, "t_w13_24": sl.slope / sl.stderr,
                        "top_ex": top.ex.mean(), "top_tot": top[f].mean(),
                        "top_strength": (top.ex / top.sd).mean()})
    out["mom_grid"] = pd.DataFrame(res)
    # per-window sign of r28 h10 slope
    g = A[A.i % 10 == 0].dropna(subset=["r28", "f10"]).copy()
    g["ex"] = g.f10 - g.groupby("coin").f10.transform("mean")
    g["rk"] = g.groupby("coin").r28.rank(pct=True) - 0.5
    pw = g.groupby("wn").apply(lambda d: np.polyfit(d.rk, d.ex, 1)[0] if len(d) > 5 else np.nan)
    out["r28_h10_windows"] = pd.Series({"windows": pw.notna().sum(), "positive": (pw > 0).sum(),
                                        "median_slope": pw.median()})
    # book position vs momentum
    out["corr_pos_r28"] = float(A[["pos", "r28"]].corr().iloc[0, 1])
    return out
