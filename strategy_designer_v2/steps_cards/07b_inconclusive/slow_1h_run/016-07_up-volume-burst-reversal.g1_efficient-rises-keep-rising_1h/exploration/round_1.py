def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            f = df["forecast"].values.astype(float)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            absd = np.abs(np.diff(c, prepend=np.nan))
            for i in range(0, n, 72):
                rec = {"coin": coin, "win": w, "year": yr[i], "f": f[i]}
                for h in (24, 72, 120):
                    rec[f"r{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                if i >= 72:
                    s = np.nansum(absd[i-71:i+1])
                    rec["er_raw"] = (c[i]-c[i-72])/s if s > 0 else np.nan
                    rec["ret72"] = c[i]/c[i-72]-1
                    rec["rise48"] = c[i] > c[i-48]
                else:
                    rec["er_raw"] = np.nan; rec["ret72"] = np.nan; rec["rise48"] = False
                rows.append(rec)
    d = pd.DataFrame(rows)
    for h in (24, 72, 120):
        d[f"x{h}"] = d[f"r{h}"] - d.groupby("coin")[f"r{h}"].transform("mean")
    act = d[d.f > 0].copy()
    def slope(g, x, y):
        g = g.dropna(subset=[x, y])
        if len(g) < 10: return (np.nan, np.nan, len(g))
        r = stats.linregress(g[x], g[y])
        return (r.slope, r.slope/r.stderr, len(g))
    out = {}
    out["main_by_h"] = pd.DataFrame({h: slope(act, "f", f"x{h}") for h in (24, 72, 120)}, index=["slope", "t", "n"]).T
    out["by_coin"] = pd.DataFrame({c: slope(g, "f", "x72") for c, g in act.groupby("coin")}, index=["slope", "t", "n"]).T
    out["by_year"] = pd.DataFrame({y: slope(g, "f", "x72") for y, g in act.groupby("year")}, index=["slope", "t", "n"]).T
    act["fq"] = pd.qcut(act.f.rank(method="first"), 5, labels=False)
    out["by_fquint"] = act.groupby("fq").agg(f=("f", "mean"), x24=("x24", "mean"), x72=("x72", "mean"), x120=("x120", "mean"), n=("x72", "count"))
    # raw ER among rises (both 48 and 72)
    rise = d[(d.ret72 > 0) & d.rise48].copy()
    out["rawER_by_h"] = pd.DataFrame({h: slope(rise, "er_raw", f"x{h}") for h in (24, 72, 120)}, index=["slope", "t", "n"]).T
    rise = rise.dropna(subset=["er_raw", "x72"])
    rise["eq"] = pd.qcut(rise.er_raw, 5, labels=False)
    out["rawER_quint"] = rise.groupby("eq").agg(er=("er_raw", "mean"), ret72=("ret72", "mean"), x24=("x24", "mean"), x72=("x72", "mean"), x120=("x120", "mean"), n=("x72", "count"))
    # ER beyond size: multiple regression
    g = rise.dropna(subset=["er_raw", "ret72", "x72"])
    X = np.column_stack([np.ones(len(g)), g.er_raw, g.ret72])
    b, *_ = np.linalg.lstsq(X, g.x72.values, rcond=None)
    res = g.x72.values - X @ b
    s2 = res @ res / (len(g)-3)
    se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["multi_er_size"] = pd.DataFrame({"coef": b, "t": b/se}, index=["const", "er_raw", "ret72"])
    out["corr_f_er_raw"] = float(act[["f", "er_raw"]].corr().iloc[0, 1])
    # all bars incl. falls: signed ER
    a = d.dropna(subset=["er_raw", "x72"])
    out["signedER_all"] = pd.DataFrame({h: slope(d, "er_raw", f"x{h}") for h in (24, 72, 120)}, index=["slope", "t", "n"]).T
    return out
