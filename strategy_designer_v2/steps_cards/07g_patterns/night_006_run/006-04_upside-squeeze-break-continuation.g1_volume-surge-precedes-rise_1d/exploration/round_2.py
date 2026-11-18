def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            n = len(b)
            vr = np.log(v.rolling(5).mean() / v.rolling(30).mean())
            r10 = c / c.shift(10) - 1
            r20 = c / c.shift(20) - 1
            r5 = c / c.shift(5) - 1
            vol20 = c.pct_change().rolling(20).std()
            hi20 = c / h.rolling(20).max() - 1
            pos = b["postRebalance_current_allocation"].astype(float)
            for i in range(0, n - 3, 3):
                rows.append(dict(coin=coin, win=w, fwd=c.iloc[i+3]/c.iloc[i]-1,
                                 vr=vr.iloc[i], r10=r10.iloc[i], r20=r20.iloc[i], r5=r5.iloc[i],
                                 vol=vol20.iloc[i], hi20=hi20.iloc[i], pos=pos.iloc[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}
    def pc_slope(col):
        res = {}
        d0 = g.dropna(subset=[col, "ex"])
        for coin, d in d0.groupby("coin"):
            x = (d[col] / d["vol"]).replace([np.inf, -np.inf], np.nan) if col.startswith("r") else d[col]
            m = x.notna()
            s = stats.linregress(x[m], d["ex"][m]); res[coin] = [round(s.slope, 5), round(s.slope / s.stderr, 2), int(m.sum())]
        x = d0[col] / d0["vol"] if col.startswith("r") else d0[col]
        m = x.notna() & np.isfinite(x)
        s = stats.linregress(x[m], d0["ex"][m]); res["POOLED"] = [round(s.slope, 5), round(s.slope / s.stderr, 2), int(m.sum())]
        return pd.DataFrame(res, index=["slope", "t", "n"]).T
    out["r10_volscaled_slope"] = pc_slope("r10")
    out["r20_volscaled_slope"] = pc_slope("r20")
    out["r5_volscaled_slope"] = pc_slope("r5")
    out["hi20_slope"] = pc_slope("hi20")
    d = g.dropna(subset=["vr", "r10", "vol", "ex"]).copy()
    d["z10"] = d["r10"] / d["vol"]
    out["corr_vr_z10"] = round(d[["vr", "z10"]].corr().iloc[0, 1], 3)
    X = np.column_stack([np.ones(len(d)), d["vr"], d["z10"]])
    beta, *_ = np.linalg.lstsq(X, d["ex"], rcond=None)
    resid = d["ex"] - X @ beta
    s2 = (resid ** 2).sum() / (len(d) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["joint_vr_z10_t"] = pd.Series({"t_vr": round(beta[1]/se[1], 2), "t_z10": round(beta[2]/se[2], 2), "n": len(d)})
    d["vq"] = d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    rr = {}
    for q, dq in d.groupby("vq"):
        s = stats.linregress(dq["z10"], dq["ex"]); rr[q] = [round(s.slope / s.stderr, 2), len(dq)]
    out["z10_t_by_vol_tercile"] = pd.DataFrame(rr, index=["t", "n"]).T
    d["zq"] = d.groupby("coin")["z10"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    t = d.groupby("zq")["ex"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["z10_bins_ex"] = t.round(4)
    # halves of windows
    d["half"] = d["win"].str[1:].astype(int) <= 12
    hh = {}
    for hf, dq in d.groupby("half"):
        s = stats.linregress(dq["z10"], dq["ex"]); hh["first12" if hf else "last12"] = [round(s.slope / s.stderr, 2), len(dq)]
    out["z10_t_by_half"] = pd.DataFrame(hh, index=["t", "n"]).T
    return out
