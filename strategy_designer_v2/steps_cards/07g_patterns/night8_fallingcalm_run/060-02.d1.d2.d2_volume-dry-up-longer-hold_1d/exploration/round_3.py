def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            m30 = v.rolling(30).mean()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                "ret20": c / c.shift(20) - 1, "ret60": c / c.shift(60) - 1,
                "vr": np.log(m30 / m30.shift(30)), "r1": r1,
                "sdrat": np.log(r1.rolling(30).std() / r1.rolling(90).std()),
                "day": ts.dt.floor("D"), "wd": ts.dt.weekday,
                "fwd1": c.shift(-1) / c - 1,
                "alloc": b["postRebalance_current_allocation"]})
            for H in (10, 15, 20):
                df["fwd%d" % H] = c.shift(-H) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    def ctt(d, col):
        d = d.dropna(subset=[col])
        s = d.groupby("day")[col].sum(); n = len(s)
        if n < 3: return pd.Series({"cases": len(d), "days": n, "mean": np.nan, "t": np.nan})
        m = d[col].mean()
        se = np.sqrt((s - s.mean()).pow(2).sum() * n / (n - 1)) / len(d)
        return pd.Series({"cases": len(d), "days": n, "mean": m, "t": m / se})
    out = {}
    res = {}; resq = {}
    for H in (10, 15, 20):
        for off in (0, H // 2):
            G = A[((A["pos"] - off) % H == 0) & (A["pos"] >= off) & A["fwd%d" % H].notna()].copy()
            drift = G.groupby("coin")["fwd%d" % H].mean()
            G["ex"] = G["fwd%d" % H] - G["coin"].map(drift)
            F = G[G["ret60"] < -0.1].dropna(subset=["vr"]).copy()
            F["g"] = F["vr"] * F["ex"]
            res["H%d_off%d_all" % (H, off)] = ctt(F, "g")
            res["H%d_off%d_r20ge-10" % (H, off)] = ctt(F[F["ret20"] >= -0.1], "g")
            res["H%d_off%d_calm" % (H, off)] = ctt(F[F["sdrat"] <= 0], "g")
            res["H%d_off%d_agit" % (H, off)] = ctt(F[F["sdrat"] > 0], "g")
            Rr = G[G["ret60"] > 0.1].dropna(subset=["vr"]).copy(); Rr["g"] = Rr["vr"] * Rr["ex"]
            res["H%d_off%d_rising" % (H, off)] = ctt(Rr, "g")
            if H == 20 and off == 0:
                F["vq"] = pd.qcut(F["vr"], 3, labels=False)
                out["H20_falling_vr_tercile_ex_dryup_short_side"] = F.groupby("vq").apply(lambda d: ctt(d, "ex"))
                out["H20_falling_coin_graded"] = F.groupby("coin").apply(lambda d: ctt(d, "g"))
    out["graded_vr_x_ex"] = pd.DataFrame(res).T
    A["ex1"] = A["fwd1"] - A.groupby("coin")["fwd1"].transform("mean")
    out["weekday_next1_dayclustered"] = A.groupby("wd").apply(lambda d: ctt(d, "ex1"))
    A["trend"] = np.where(A["ret60"] > .1, "rising", np.where(A["ret60"] < -.1, "falling", "choppy"))
    A["r1z"] = A["r1"] / A.groupby(["coin", "w"])["r1"].transform(lambda s: s.rolling(30).std())
    A["gr"] = -A["r1z"] * A["ex1"]
    out["fall_rebound_graded_by_trend"] = A.dropna(subset=["ret60"]).groupby("trend").apply(lambda d: ctt(d, "gr"))
    return out
