def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n),
                "fwd": c.shift(-H) / c - 1, "fwd1": c.shift(-1) / c - 1, "r1": r1,
                "lo20": c / c.rolling(20).min() - 1, "dist50": c / c.rolling(50).mean() - 1,
                "past20": c / c.shift(20) - 1,
                "wd": ts.dt.weekday, "yr": ts.dt.year,
                "fc": b["forecast"].astype(float)})
            recs.append(df)
    A = pd.concat(recs, ignore_index=True)
    # per-coin drift and sd, on each grid
    for col in ["fwd", "fwd1"]:
        g = A[(A["pos"] % (H if col == "fwd" else 1) == 0) & A[col].notna()]
        st = g.groupby("coin")[col].agg(["mean", "std"])
        A = A.join(st.rename(columns={"mean": col + "_m", "std": col + "_s"}), on="coin")
        A[col + "_st"] = (A[col] - A[col + "_m"]) / A[col + "_s"]
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s)))})
    out = {}
    # 1-day forward return by weekday (all bars, non-overlapping at h=1)
    out["wd_1d"] = A.groupby("wd")["fwd1_st"].apply(tt).unstack().round(4)
    out["wd_1d_raw_mean"] = A.groupby("wd")["fwd1"].mean().round(5)
    # weekday 1d effect by year
    A["mon_minus"] = np.nan
    yy = {}
    for y, s in A.groupby("yr"):
        yy[y] = {d: s.loc[s["wd"] == d, "fwd1_st"].mean() for d in range(7)}
        yy[y]["n"] = len(s)
    out["wd_1d_by_year"] = pd.DataFrame(yy).T.round(3)
    cc = {}
    for co, s in A.groupby("coin"):
        cc[co] = {d: s.loc[s["wd"] == d, "fwd1_st"].mean() for d in range(7)}
    out["wd_1d_by_coin"] = pd.DataFrame(cc).T.round(3)
    # lo20 effect on 5-day grid, split by regime
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    for nm, sub in [("lo20_below50", G[G["dist50"] < 0]), ("lo20_above50", G[G["dist50"] >= 0])]:
        x = sub.dropna(subset=["lo20"]).copy()
        x["b"] = pd.qcut(x["lo20"].rank(method="first"), 4, labels=False)
        out[nm] = x.groupby("b").agg(lo=("lo20", "min"), hi=("lo20", "max"), n=("fwd_st", "size"),
                    st=("fwd_st", "mean"), t=("fwd_st", lambda s: s.mean() / (s.std() / np.sqrt(len(s))))).round(4)
    # lo20 bottom quintile by year
    x = G.dropna(subset=["lo20"]).copy()
    x["q"] = pd.qcut(x["lo20"].rank(method="first"), 5, labels=False)
    out["lo20_q0_by_year"] = x[x["q"] == 0].groupby("yr")["fwd_st"].apply(tt).unstack().round(3)
    # after large 1-day moves (all bars, 1d forward)
    A["absr"] = A["r1"] / A.groupby("coin")["r1"].transform("std")
    A["mb"] = pd.cut(A["absr"], [-99, -2, -1, 1, 2, 99])
    out["after_move_1d"] = A.groupby("mb")["fwd1_st"].apply(tt).unstack().round(4)
    return out
