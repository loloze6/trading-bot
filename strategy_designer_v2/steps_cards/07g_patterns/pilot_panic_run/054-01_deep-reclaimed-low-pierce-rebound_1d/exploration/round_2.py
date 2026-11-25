def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            n = len(b)
            if n < 40: continue
            c = b["close"].values; lo = b["low"].values; hi = b["high"].values
            fwd = np.full(n, np.nan); fwd[:n-H] = c[H:] / c[:n-H] - 1
            f1 = np.full(n, np.nan); f1[:n-1] = c[1:] / c[:-1] - 1
            r1 = np.full(n, np.nan); r1[1:] = c[1:] / c[:-1] - 1
            prevlow = pd.Series(lo).shift(1).rolling(30, min_periods=30).min().values
            prevhigh = pd.Series(hi).shift(1).rolling(30, min_periods=30).max().values
            tr60 = np.full(n, np.nan); tr60[60:] = c[60:] / c[:-60] - 1
            vol30 = pd.Series(r1).rolling(30, min_periods=25).std().values
            clv = np.where(hi > lo, (c - lo) / (hi - lo), np.nan)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n), "fwd": fwd, "f1": f1, "r1": r1,
                "tr60": tr60, "vol30": vol30, "clv": clv,
                "reclaim": (lo < prevlow) & (c >= prevlow),
                "rdepth": np.where((lo < prevlow) & (c >= prevlow), (prevlow - lo) / prevlow, np.nan),
                "ufail": (hi > prevhigh) & (c <= prevhigh),
                "udepth": np.where((hi > prevhigh) & (c <= prevhigh), (hi - prevhigh) / prevhigh, np.nan),
                "upclose": c > prevhigh,
                "regime": b["regime"].values, "day": ts.dt.floor("D").values,
                "year": ts.dt.year.values,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["fwd"])
    grid = D[D.pos % H == 0]
    drift = grid.groupby("coin")["fwd"].mean(); sd = grid.groupby("coin")["fwd"].std()
    D["un"] = D["fwd"] - D["coin"].map(drift)
    D["inprof"] = D["regime"].isin(["mean_reversion", "unknown"])
    D["trend"] = np.where(D.tr60 > 0.10, "rising", np.where(D.tr60 < -0.10, "falling", np.where(D.tr60.notna(), "choppy", "na")))

    def dedup(E):
        # first event per coin/window, then skip events within H bars of the last kept
        keep = []
        for (cn, w), g in E.sort_values("pos").groupby(["coin", "win"]):
            last = -10**9
            for i, p in zip(g.index, g.pos):
                if p - last >= H:
                    keep.append(i); last = p
        return E.loc[keep]

    def ct(E, col="un"):
        E = E.dropna(subset=[col])
        if len(E) < 3: return pd.Series({"n": len(E), "days": np.nan, "mean": np.nan, "t_day": np.nan})
        m = E[col].mean()
        s = (E[col] - m).groupby(E["day"]).sum()
        Dn = len(s)
        se = np.sqrt((s**2).sum() * Dn / max(Dn - 1, 1)) / len(E)
        return pd.Series({"n": len(E), "days": Dn, "mean": m, "t_day": m / se if se > 0 else np.nan})

    out = {}
    R = dedup(D[D.reclaim])
    U = dedup(D[D.ufail])
    UC = dedup(D[D.upclose])
    tab = {}
    tab["reclaim_all"] = ct(R)
    tab["reclaim_inprof"] = ct(R[R.inprof]); tab["reclaim_outprof"] = ct(R[~R.inprof])
    for tr in ["rising", "choppy", "falling", "na"]:
        tab["reclaim_" + tr] = ct(R[R.trend == tr])
    tab["reclaim_out_clv_hi"] = ct(R[(~R.inprof) & (R.clv > 0.5)])
    tab["reclaim_out_clv_lo"] = ct(R[(~R.inprof) & (R.clv <= 0.5)])
    tab["ufail_all"] = ct(U)
    for tr in ["rising", "choppy", "falling", "na"]:
        tab["ufail_" + tr] = ct(U[U.trend == tr])
    tab["upclose_all"] = ct(UC)
    tab["reclaim_f1"] = ct(R, "f1"); tab["ufail_f1"] = ct(U, "f1")
    out["events_dedup_cluster"] = pd.DataFrame(tab).T
    Ro = R[~R.inprof].copy()
    if len(Ro) > 9:
        Ro["dq"] = pd.qcut(Ro["rdepth"].rank(method="first"), 3, labels=False)
        out["reclaim_out_by_depth"] = Ro.groupby("dq").apply(lambda g: pd.concat([ct(g), pd.Series({"depth": g.rdepth.mean()})]))
        out["reclaim_out_by_year"] = Ro.groupby("year").apply(ct)
        out["reclaim_out_by_coin"] = Ro.groupby("coin").apply(ct)
        out["reclaim_out_slope_t"] = float(np.polyfit(Ro.rdepth, Ro.un, 1)[0])
        from scipy import stats
        out["reclaim_out_spearman"] = str(stats.spearmanr(Ro.rdepth, Ro.un))
    U2 = U.copy()
    if len(U2) > 9:
        U2["dq"] = pd.qcut(U2["udepth"].rank(method="first"), 3, labels=False)
        out["ufail_by_depth"] = U2.groupby("dq").apply(lambda g: pd.concat([ct(g), pd.Series({"depth": g.udepth.mean()})]))
        out["ufail_by_year"] = U2.groupby("year").apply(ct)
        out["ufail_by_coin"] = U2.groupby("coin").apply(ct)
    return out
