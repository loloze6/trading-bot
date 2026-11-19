def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cl = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(cl).pct_change()
            v7 = r1.rolling(168).std()
            v60 = r1.rolling(1440, min_periods=720).std()
            vr = (v7 / v60).values
            n = len(b)
            idx = np.arange(0, n - 24, 24)
            idx = idx[idx >= 24]
            fr = cl[idx + 24] / cl[idx] - 1
            past = cl[idx] / cl[idx - 24] - 1
            vol = v7.values[idx] * np.sqrt(24)
            rows.append(pd.DataFrame({"coin": c, "w": w, "year": ts.dt.year.values[idx], "fr": fr, "past": past,
                                      "vol": vol, "vr": vr[idx]}))
    D = pd.concat(rows).dropna()
    D["ex"] = D["fr"] - D.groupby("coin")["fr"].transform("mean")
    D["pz"] = D["past"] / D["vol"]
    D["exz"] = D["ex"] / D["vol"]
    def slope(s):
        if len(s) < 30: return pd.Series({"n": len(s), "slope": np.nan, "t": np.nan})
        l = stats.linregress(s["pz"], s["exz"])
        return pd.Series({"n": len(s), "slope": l.slope, "t": l.slope / l.stderr})
    D["vrq"] = pd.qcut(D["vr"].rank(method="first"), 3, labels=False)
    out["rev_by_causal_volratio_tercile"] = D.groupby("vrq").apply(slope)
    H = D[D.vrq == 2]
    out["highvr_by_coin"] = H.groupby("coin").apply(slope)
    out["highvr_by_year"] = H.groupby("year").apply(slope)
    H = H.copy()
    H["q"] = pd.qcut(H["pz"].rank(method="first"), 5, labels=False)
    g = H.groupby("q").agg(n=("ex", "size"), mean_pz=("pz", "mean"), mean_ex=("ex", "mean"), sd=("ex", "std"))
    g["t"] = g.mean_ex / (g.sd / np.sqrt(g.n))
    out["highvr_quintiles"] = g.drop(columns="sd")
    # interaction: slope of exz on pz*vr
    D["inter"] = D["pz"] * (D["vr"] - D["vr"].mean())
    X = np.column_stack([np.ones(len(D)), D["pz"], D["vr"] - D["vr"].mean(), D["inter"]])
    y = D["exz"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    s2 = res @ res / (len(y) - 4)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["interaction"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "pz", "vr", "pz_x_vr"])
    return out
