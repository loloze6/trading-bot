def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            ph = h.shift(1).rolling(30, min_periods=30).max()
            df = pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                               "dist": (c - ph) / ph * 100, "r1": r1,
                               "vol20": r1.rolling(20, min_periods=15).std(),
                               "vrel": v / v.rolling(30, min_periods=20).mean(),
                               "vrel5": v.rolling(5).mean() / v.rolling(30, min_periods=20).mean(),
                               "fwd10": c.shift(-10) / c - 1, "fwd1": c.shift(-1) / c - 1,
                               "fwd3": c.shift(-3) / c - 1})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for k in ["fwd10", "fwd1", "fwd3"]:
        D["ex" + k[3:]] = D[k] - D.groupby("coin")[k].transform("mean")
    out = {}
    S = D[D["pos"] % 10 == 0].dropna(subset=["ex10", "dist", "vrel5"]).copy()
    S["near"] = S["dist"] > S.groupby("coin")["dist"].transform(lambda x: x.quantile(0.6))
    N = S[S["near"]].copy()
    N["vq"] = N.groupby("coin")["vrel5"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    g = N.groupby("vq")["ex10"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["near_by_vol5_tercile_ex10"] = g.round(4)
    a = N[N.vq == 2]["ex10"]; bb = N[N.vq == 0]["ex10"]
    out["near_hi_minus_lo_vol5_welch_t"] = float(stats.ttest_ind(a, bb, equal_var=False).statistic)
    F = S[~S["near"]].copy()
    F["vq"] = F.groupby("coin")["vrel5"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["far_by_vol5_tercile_ex10"] = F.groupby("vq")["ex10"].agg(["mean", "count"]).round(4)
    N["half"] = np.where(N["wn"] <= 12, "early", "late")
    out["near_vol_by_coin"] = N.groupby(["coin"]).apply(lambda d: pd.Series({"hi": d[d.vq == 2].ex10.mean(), "lo": d[d.vq == 0].ex10.mean()})).round(4)
    out["near_vol_by_half"] = N.groupby(["half", "vq"])["ex10"].mean().unstack().round(4)
    # slope of ex10 on log vrel5 within near
    sl = stats.linregress(np.log(N["vrel5"]), N["ex10"]); out["near_slope_logvol_t"] = float(sl.slope / sl.stderr)
    # daily reversal
    E = D.dropna(subset=["r1", "vol20", "ex1"]).copy(); E["z"] = E["r1"] / E["vol20"]
    sl = stats.linregress(E["z"], E["ex1"]); out["rev_slope_ex1_on_z_t"] = float(sl.slope / sl.stderr)
    pc = []
    for coin, d in E.groupby("coin"):
        s = stats.linregress(d["z"], d["ex1"]); pc.append({"coin": coin, "slope": s.slope, "t": s.slope / s.stderr, "n": len(d)})
    out["rev_by_coin"] = pd.DataFrame(pc).round(5)
    E["half"] = np.where(E["wn"] <= 12, "early", "late")
    out["rev_by_half_t"] = E.groupby("half").apply(lambda d: stats.linregress(d["z"], d["ex1"]).slope / stats.linregress(d["z"], d["ex1"]).stderr).round(3)
    E3 = E[E["pos"] % 3 == 0].dropna(subset=["ex3"])
    s = stats.linregress(E3["z"], E3["ex3"]); out["rev3d_slope_t_n"] = f"t={s.slope/s.stderr:.3f} n={len(E3)}"
    E["zb"] = pd.cut(E["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["rev_by_zb_and_vol"] = E.assign(hv=E["vol20"] > E.groupby("coin")["vol20"].transform("median")).groupby(["hv", "zb"])["ex1"].agg(["mean", "count"]).round(5)
    return out
