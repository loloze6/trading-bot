def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    # A) hour-of-day robustness: raw 1h returns, hours 21,22,14 vs rest
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            ts = pd.to_datetime(df["timestamp"])
            r = df["close"].pct_change()
            lr = np.log(df["close"]).diff()
            vol = lr.rolling(168).std().shift(1)
            rows.append(pd.DataFrame({"coin": c, "w": w, "yr": ts.dt.year, "h": ts.dt.hour, "wd": ts.dt.weekday,
                                      "reg": df["regime"].values, "r": r, "rz": r / vol, "p24": df["close"].pct_change(24).shift(1)}))
    H = pd.concat(rows).dropna()
    H["hg"] = np.where(H.h.isin([21, 22]), "h21_22", np.where(H.h == 14, "h14", "other"))
    def tt(s): return s.mean() / s.std() * np.sqrt(len(s))
    out["hour_group_raw_bps"] = H.groupby("hg")["r"].agg(lambda s: s.mean() * 1e4).round(2)
    a = H[H.hg == "h21_22"]
    out["h2122_by_year_t"] = a.groupby("yr")["rz"].agg(["mean", "count", tt]).round(3)
    out["h2122_by_coin_t"] = a.groupby("coin")["rz"].agg(["mean", tt]).round(3)
    out["h2122_by_weekday_t"] = a.groupby("wd")["rz"].agg(["mean", "count", tt]).round(3)
    out["h2122_by_regime_t"] = a.groupby("reg")["rz"].agg(["mean", "count", tt]).round(3)
    # graded? h21-22 return vs past 24h return quintile
    a = a.copy(); a["q"] = pd.qcut(a["p24"], 5, labels=False)
    out["h2122_by_past24q"] = a.groupby("q")["rz"].agg(["mean", "count", tt]).round(3)
    b = H[H.hg == "h14"]
    out["h14_by_year_t"] = b.groupby("yr")["rz"].agg(["mean", "count", tt]).round(3)
    # B) 240-bar grid: past5 vs past20 jointly, trending; by year
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            cl = df["close"].values; n = len(cl); ts = pd.to_datetime(df["timestamp"]).values
            reg = df["regime"].values
            for i in range(0, n - 240, 240):
                p20 = cl[i] / cl[i - 480] - 1 if i >= 480 else np.nan
                p5 = cl[i] / cl[i - 120] - 1 if i >= 120 else np.nan
                rows.append((c, w, pd.Timestamp(ts[i]).year, reg[i], p20, p5, cl[i + 240] / cl[i] - 1))
    g = pd.DataFrame(rows, columns=["coin", "w", "yr", "reg", "p20", "p5", "fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    t = g[(g.reg == "trending")].dropna(subset=["p20", "p5"])
    X = np.column_stack([np.ones(len(t)), t.p5, t.p20]); y = t.ex.values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta; s2 = res @ res / (len(y) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["trend_joint_p5_p20"] = f"b5 {beta[1]:.3f} t {beta[1]/se[1]:.2f}; b20 {beta[2]:.3f} t {beta[2]/se[2]:.2f}; n {len(y)}"
    t5 = g[g.reg == "trending"].dropna(subset=["p5"]).copy()
    t5["q"] = pd.qcut(t5.p5, 5, labels=False)
    out["trend_fwd10d_by_p5q"] = t5.groupby("q")["ex"].agg(["mean", "count", tt]).round(4)
    yrs = []
    for yv, s in t5.groupby("yr"):
        if len(s) > 20:
            r = stats.linregress(s.p5, s.ex); yrs.append((yv, len(s), round(r.slope, 3), round(r.slope / r.stderr, 2)))
    out["trend_p5_slope_by_year"] = pd.DataFrame(yrs, columns=["yr", "n", "slope", "t"])
    # C) next-day after large |move|: abs z quintile per year
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            cl = df["close"].values; n = len(cl); lr = np.diff(np.log(cl))
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(168, n - 24, 24):
                v = lr[i - 168:i].std()
                rows.append((yr[i], (cl[i] / cl[i - 24] - 1) / (v * np.sqrt(24)), (cl[i + 24] / cl[i] - 1) / (v * np.sqrt(24))))
    d = pd.DataFrame(rows, columns=["yr", "z", "fz"])
    d["aq"] = pd.qcut(d.z.abs(), 5, labels=False)
    out["next1d_by_absz_q"] = d.groupby("aq")["fz"].agg(["mean", "count", tt]).round(4)
    return out
