def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            rng = (b["high"] - b["low"]) / c
            ratio = rng / sd30
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                "fwd3": c.shift(-3) / c - 1, "fwd1": c.shift(-1) / c - 1, "r1": r1,
                "ratio": ratio, "ret60": c / c.shift(60) - 1,
                "falling": (b["regime"] == "unknown").astype(int),
                "wd": ts.dt.weekday, "year": ts.dt.year,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % 3 == 0].groupby("coin")["fwd3"].mean()
    A["ex3"] = A["fwd3"] - A["coin"].map(drift)
    G = A[(A.pos % 3 == 0) & A.ex3.notna() & A.ratio.notna()].copy()
    G["q"] = G.groupby(["coin", "falling"])["ratio"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out = {}
    def dayt(d, v="ex3"):
        s = d.groupby("day")[v].sum()
        n = d.groupby("day")[v].count()
        m = d[v].mean()
        dev = (d[v] - m).groupby(d["day"]).sum()
        se = np.sqrt((dev**2).sum()) / len(d)
        return pd.Series({"mean": m, "cases": len(d), "days": len(s), "t_day": m / se})
    F = G[G.falling == 1]; N = G[G.falling == 0]
    out["fall_narrowQ0_dayt"] = dayt(F[F.q == 0])
    out["fall_narrowQ0_by_coin"] = F[F.q == 0].groupby("coin")["ex3"].agg(["mean", "count"])
    out["fall_narrowQ0_by_year"] = F[F.q == 0].groupby("year")["ex3"].agg(["mean", "count"])
    out["fall_narrowQ0_by_window"] = F[F.q == 0].groupby("w")["ex3"].agg(["mean", "count"])
    # ret60 depth within falling: deeper falls vs narrow
    F2 = F.copy(); F2["deep"] = F2["ret60"] < F2.groupby("coin")["ret60"].transform("median")
    out["fall_q_by_deep"] = F2.groupby(["deep", "q"])["ex3"].mean().unstack()
    # wide days not falling, split by day direction
    Nw = N[N.q == 4]
    out["notfall_wideQ4_dayt"] = dayt(Nw)
    out["notfall_wideQ4_by_dir"] = Nw.groupby(np.sign(Nw["r1"]))["ex3"].agg(["mean", "count"])
    out["notfall_wideQ4_by_coin"] = Nw.groupby("coin")["ex3"].agg(["mean", "count"])
    out["notfall_wideQ4_by_year"] = Nw.groupby("year")["ex3"].agg(["mean", "count"])
    N2 = N.copy(); N2["up"] = N2["ret60"] > 0.10
    out["notfall_q_by_rising"] = N2.groupby(["up", "q"])["ex3"].mean().unstack()
    # weekday robustness
    D = A.dropna(subset=["fwd1"]).copy()
    D["thfr"] = D.wd.isin([3, 4]).astype(int)
    out["thfr_by_year"] = D.groupby(["year", "thfr"])["fwd1"].mean().unstack()
    out["thfr_by_coin"] = D.groupby(["coin", "thfr"])["fwd1"].mean().unstack()
    out["thfr_dayt"] = dayt(D[D.thfr == 1].assign(ex3=D.fwd1 - D.fwd1.mean()))
    return out
