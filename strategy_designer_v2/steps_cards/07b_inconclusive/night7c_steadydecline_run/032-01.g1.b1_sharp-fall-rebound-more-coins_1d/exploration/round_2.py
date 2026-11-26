def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    drift = {}
    for coin, wins in data["bars"].items():
        for h in (1, 2):
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    vals.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(vals)
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; r = c.pct_change()
            z_ex = r / r.rolling(20).std().shift(1)
            z_in = r / r.rolling(20).std()
            f = df["forecast"].fillna(0).values
            pp = df.get("debug_info.components.fall.post_pipeline_value")
            n = len(c)
            for i in range(n):
                zi, ze = z_in.iloc[i], z_ex.iloc[i]
                if pd.isna(zi) and pd.isna(ze):
                    continue
                inr = (not pd.isna(zi)) and zi <= -2
                exr = (not pd.isna(ze)) and ze <= -2
                if not (inr or exr or f[i] > 0):
                    continue
                rec = {"coin": coin, "win": w, "day": pd.Timestamp(df["timestamp"].iloc[i]).floor("D"),
                       "z_in": zi, "z_ex": ze, "fc": f[i], "pp": pp.iloc[i] if pp is not None else np.nan,
                       "grid2": i % 2 == 0, "inr": inr, "exr": exr, "rec": f[i] > 0}
                for h in (1, 2):
                    if i + h < n:
                        rec[f"u{h}"] = c.iloc[i + h] / c.iloc[i] - 1 - drift[(coin, h)]
                if i + 2 < n:
                    rec["u_d2only"] = c.iloc[i + 2] / c.iloc[i + 1] - 1 - drift[(coin, 1)]
                rows.append(rec)
    ev = pd.DataFrame(rows)

    def summ(g, col):
        g = g.dropna(subset=[col])
        if len(g) < 3:
            return pd.Series({"n": len(g), "days": np.nan, "mean%": np.nan, "t": np.nan})
        d = g.groupby("day")[col].sum(); nd = len(d)
        mean = g[col].mean(); se = d.std(ddof=1) * np.sqrt(nd) / len(g)
        return pd.Series({"n": len(g), "days": nd, "mean%": 100 * mean, "t": mean / se})

    out = {}
    tab = {}
    for name, m in [("recorded fc>0", ev.rec), ("z_in<=-2", ev.inr), ("z_ex<=-2", ev.exr),
                    ("z_ex only, not recorded", ev.exr & ~ev.rec), ("recorded, grid2", ev.rec & ev.grid2)]:
        g = ev[m]
        for col in ("u1", "u2", "u_d2only"):
            tab[f"{name} | {col}"] = summ(g, col)
    out["case sets"] = pd.DataFrame(tab).T
    rc = ev[ev.rec].copy()
    out["recorded: fc stats"] = rc["fc"].describe()
    rc["fcb"] = pd.qcut(rc["fc"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["recorded by fc quartile u1"] = rc.groupby("fcb", observed=True).apply(lambda g: summ(g, "u1"))
    rc["zb"] = pd.cut(rc.z_in, [-np.inf, -4, -3, -2.5, -2, np.inf])
    out["recorded by z_in bucket u1"] = rc.groupby("zb", observed=True).apply(lambda g: summ(g, "u1"))
    out["recorded by z_in bucket u2"] = rc.groupby("zb", observed=True).apply(lambda g: summ(g, "u2"))
    s = rc.dropna(subset=["u1", "z_in"])
    a = stats.linregress(-s.z_in, s.u1); b = stats.linregress(s.fc, s.u1)
    out["recorded slopes u1"] = f"on -z_in {a.slope:.5f} t {a.slope/a.stderr:.2f}; on fc {b.slope:.6f} t {b.slope/b.stderr:.2f}; n {len(s)}"
    s = rc.dropna(subset=["u2", "z_in"])
    a = stats.linregress(-s.z_in, s.u2); b = stats.linregress(s.fc, s.u2)
    out["recorded slopes u2"] = f"on -z_in {a.slope:.5f} t {a.slope/a.stderr:.2f}; on fc {b.slope:.6f} t {b.slope/b.stderr:.2f}; n {len(s)}"
    out["corr fc vs -z_in (recorded)"] = float(np.corrcoef(rc.dropna(subset=['z_in']).fc, -rc.dropna(subset=['z_in']).z_in)[0, 1])
    out["recorded consecutive share (fc>0 bars that follow fc>0)"] = float(rc.shape[0])
    return out
