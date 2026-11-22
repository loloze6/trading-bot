def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            mv = v.rolling(720, min_periods=240).mean()
            zr = r / sd; vr = v / mv
            yr = pd.to_datetime(df["timestamp"]).dt.year
            fwd = c.shift(-2) / c - 1
            idx = np.arange(0, len(df), 2)
            rows.append(pd.DataFrame({"coin": coin, "win": w, "zr": zr.values[idx], "vr": vr.values[idx],
                                      "fwd": fwd.values[idx], "fc": df["forecast"].values[idx], "year": yr.values[idx]}))
    A = pd.concat(rows).dropna(subset=["zr", "vr", "fwd"])
    A["u"] = A["fwd"] - A.groupby("coin")["fwd"].transform("mean")
    out = {}
    C = A[A["fc"] >= 2].copy()
    def slope(x, y):
        s = stats.linregress(x, y); return s.slope, s.slope / s.stderr
    sl, st = slope(C["fc"], C["u"])
    q = C["u"].quantile([0.01, 0.99]).values
    sw, swt = slope(C["fc"], C["u"].clip(q[0], q[1]))
    rho, prho = stats.spearmanr(C["fc"], C["u"])
    out["fc>=2 cases slope"] = pd.Series({"n": len(C), "mean_u_bp": C["u"].mean()*1e4,
        "t": C["u"].mean()/(C["u"].std()/np.sqrt(len(C))), "ols_slope_bp_per_pt": sl*1e4, "ols_t": st,
        "wins_slope_bp": sw*1e4, "wins_t": swt, "spearman": rho, "spearman_p": prho})
    C["fcb"] = pd.cut(C["fc"], [1.99, 5, 10, 15, 19.99, 20.01])
    def summ(g):
        n = len(g); m = g["u"].mean(); s = g["u"].std()
        return pd.Series({"n": n, "mean_u_bp": m*1e4, "t": m/(s/np.sqrt(n)) if n > 1 else np.nan,
                          "median_u_bp": g["u"].median()*1e4, "share_pos": (g["u"] > 0).mean()})
    out["fc>=2 by fc bin"] = C.groupby("fcb").apply(summ).reset_index()
    P = A[(A["zr"] < 0) & (A["vr"] >= 1)].copy()
    P["prod"] = -P["zr"] * P["vr"]
    P["pb"] = pd.cut(P["prod"], [0, 5, 10, 20, 40, np.inf])
    out["fall x vol product bins"] = P.groupby("pb").apply(summ).reset_index()
    E = A[(A["zr"] <= -4) & (A["vr"] >= 3)]
    out["z<=-4,vr>=3 by coin"] = E.groupby("coin").apply(summ).reset_index()
    out["z<=-4,vr>=3 by year"] = E.groupby("year").apply(summ).reset_index()
    return out
