def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            r7 = c / c.shift(7) - 1
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "i": np.arange(len(b)),
                "regime": b["regime"], "r7": r7, "r1": r1,
                "volz": v / v.rolling(30, min_periods=20).mean(),
                "volz7": v.rolling(7).mean() / v.rolling(30, min_periods=20).mean(),
                "fwd7": c.shift(-7) / c - 1, "fwd3": c.shift(-3) / c - 1, "fwd1": c.shift(-1) / c - 1,
                "yr": ts.dt.year, "day": ts.dt.floor("D")})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["inprof"] = A.regime.isin(["trending", "unknown"])
    out = {}
    d7 = A.loc[A.i % 7 == 0, "fwd7"].mean()
    d3 = A.loc[A.i % 3 == 0, "fwd3"].mean()
    d1 = A["fwd1"].mean()
    def pooled_t(g, col):
        s = g.groupby("day")[col].sum()
        n = g.groupby("day")[col].count().sum()
        m = g[col].mean()
        se = np.sqrt(((s - g.groupby("day")[col].count() * m) ** 2).sum()) / n
        return m / se, s.size
    # robustness across grid offsets, in profile, volz and volz7
    res = []
    for off in range(7):
        G = A[(A.i % 7 == off) & A.fwd7.notna() & A.inprof].copy()
        G["ex"] = G.fwd7 - d7
        for nm in ["volz", "volz7"]:
            g = G[[nm, "ex"]].dropna()
            rr, pv = stats.spearmanr(g[nm], g.ex)
            q = pd.qcut(G[nm], 2, labels=False)
            hi = G.ex[q == 1]; lo = G.ex[q == 0]
            t = stats.ttest_ind(hi, lo, equal_var=False).statistic
            res.append({"off": off, "var": nm, "rho": rr, "p": pv, "n": len(g),
                        "hi_minus_lo": hi.mean() - lo.mean(), "welch_t": t})
    out["offsets_inprof"] = pd.DataFrame(res)
    G = A[(A.i % 7 == 0) & A.fwd7.notna()].copy()
    G["ex"] = G.fwd7 - d7
    P = G[G.inprof].copy()
    P["vq"] = pd.qcut(P.volz, 3, labels=False)
    P["up"] = P.r7 > 0
    out["inprof_volz_by_up"] = P.groupby(["up", "vq"]).ex.agg(["count", "mean"])
    P["top"] = P.vq == 2
    out["inprof_topvol_by_year"] = P[P.top].groupby("yr").ex.agg(["count", "mean"])
    out["inprof_botvol_by_year"] = P[P.vq == 0].groupby("yr").ex.agg(["count", "mean"])
    out["inprof_topvol_by_coin"] = P[P.top].groupby("coin").ex.agg(["count", "mean"])
    # pooled-day t of excess weighted by standardized volz rank (graded)
    P2 = P.dropna(subset=["volz"]).copy()
    P2["z"] = P2.volz.rank(pct=True) - 0.5
    P2["sig"] = P2.z * P2.ex
    tt, nd = pooled_t(P2, "sig")
    out["graded_volrank_x_ex_pooled_t"] = f"t {tt:.2f} days {nd}"
    # 3-day and 1-day horizons in profile
    for H, col, dr in [(3, "fwd3", d3), (1, "fwd1", d1)]:
        Q = A[(A.i % H == 0) & A[col].notna() & A.inprof].dropna(subset=["volz"]).copy()
        Q["ex"] = Q[col] - dr
        rr, pv = stats.spearmanr(Q.volz, Q.ex)
        out[f"spearman_volz_h{H}_in"] = f"rho {rr:.3f} p {pv:.4f} n {len(Q)}"
    # same out of profile over offsets (mean rho)
    rs = []
    for off in range(7):
        Q = A[(A.i % 7 == off) & A.fwd7.notna() & ~A.inprof].dropna(subset=["volz"])
        rs.append(stats.spearmanr(Q.volz, Q.fwd7)[0])
    out["outprof_volz_rho_offsets_mean"] = float(np.mean(rs))
    # weekday in profile 1d
    Q = A[A.inprof & A.fwd1.notna()].copy()
    Q["ex"] = Q.fwd1 - d1
    Q["wd"] = Q.day.dt.weekday
    out["inprof_wd_1d"] = Q.groupby("wd").ex.agg(["count", "mean"])
    return out
