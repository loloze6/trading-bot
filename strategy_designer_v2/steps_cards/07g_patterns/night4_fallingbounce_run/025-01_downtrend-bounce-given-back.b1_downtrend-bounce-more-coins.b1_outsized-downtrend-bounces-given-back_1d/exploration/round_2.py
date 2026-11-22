def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        vals = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 5, 5)
            vals.append(c[idx + 5] / c[idx] - 1)
        v = np.concatenate(vals)
        dm, ds = np.nanmean(v), np.nanstd(v)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            z = r1 / sd20
            r30 = c / c.shift(30) - 1
            z30 = r30 / (sd20 * np.sqrt(30))
            r3 = c / c.shift(3) - 1
            z3 = r3 / (sd20 * np.sqrt(3))
            n = len(df)
            fwd = c.shift(-5) / c - 1
            idx = np.arange(0, n - 5, 5)
            ts = pd.to_datetime(df["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "z": z.values[idx], "z3": z3.values[idx],
                "z30": z30.values[idx], "un": fwd.values[idx] - dm,
                "str": (fwd.values[idx] - dm) / ds,
                "fall": np.where(df["regime"].values[idx] == "mean_reversion", "fall90", "notfall"),
                "year": ts.dt.year.values[idx], "fc": df["forecast"].values[idx]}))
    A = pd.concat(rows).dropna(subset=["z", "un"])
    lo, hi = A["un"].quantile([0.01, 0.99])
    A["unw"] = A["un"].clip(lo, hi)
    def rob(g):
        n = len(g)
        return pd.Series({"n": n, "mean": g["un"].mean(), "median": g["un"].median(),
                          "share_pos": (g["un"] > 0).mean(), "wins_mean": g["unw"].mean(),
                          "wins_t": g["unw"].mean() / (g["unw"].std() / np.sqrt(n)) if n > 2 else np.nan,
                          "strength": g["str"].mean()})
    out = {}
    A["zb"] = pd.cut(A["z"], [-99, 0, 1, 1.5, 2, 3, 99])
    out["robust h5 by z bucket x regime"] = A.groupby(["fall", "zb"]).apply(rob)
    up = A[A.z > 1]
    out["z>1 by regime x year (winsorised)"] = up.groupby(["fall", "year"]).apply(
        lambda g: pd.Series({"n": len(g), "wins_mean": g["unw"].mean(), "strength": g["str"].mean()}))
    pc = up.groupby(["fall", "coin"])["unw"].mean().reset_index()
    out["z>1 coins with positive mean by regime"] = pc.groupby("fall")["unw"].agg(
        n_coins="count", share_pos=lambda s: (s > 0).mean(), mean="mean")
    sp = {}
    for f in ("fall90", "notfall"):
        g = A[(A.fall == f) & (A.z > 0)]
        r, p = stats.spearmanr(g["z"], g["un"])
        sp[f + " up days: spearman z vs fwd5"] = (round(r, 4), round(p, 4), len(g))
    out["graded up-day relation"] = pd.DataFrame(sp, index=["rho", "p", "n"]).T
    a = A[(A.fall == "fall90") & (A.z > 2)]["unw"]; b = A[(A.fall == "notfall") & (A.z > 2)]["unw"]
    out["z>2 fall minus notfall welch t"] = round(stats.ttest_ind(a, b, equal_var=False).statistic, 3)
    A["z30b"] = pd.qcut(A["z30"], 5)
    out["h5 by z30 quintile x regime"] = A.dropna(subset=["z30"]).groupby(["fall", "z30b"]).apply(rob)
    A["z3b"] = pd.qcut(A["z3"], 5)
    out["h5 by z3 quintile x regime"] = A.dropna(subset=["z3"]).groupby(["fall", "z3b"]).apply(rob)
    # forecast-based buckets in falling regime
    F = A[A.fall == "fall90"].copy()
    F["fcb"] = pd.cut(F["fc"], [-21, -10, -2, -0.001, 0.001])
    out["fall90 by forecast bucket"] = F.groupby("fcb").apply(rob)
    # book extremes
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            b2 = bars[coin][w].copy()
            b2["day"] = pd.to_datetime(b2["timestamp"]).dt.floor("D")
            al = b2.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            d = df.copy(); d["day"] = pd.to_datetime(d["day"]).dt.floor("D")
            d["alloc_prev"] = d["day"].map(al)
            D.append(d)
    D = pd.concat(D).dropna(subset=["book_return"])
    D["state"] = np.where(D["alloc_prev"] < -0.01, "short", "flat")
    out["book by state"] = D.groupby("state").agg(n=("book_return", "size"), book=("book_return", "mean"),
                                                   coin=("coin_return", "mean"))
    q = D["book_return"].quantile([0.01, 0.99])
    out["coin ret on book worst/best 1%"] = pd.Series({
        "worst_n": (D.book_return <= q.iloc[0]).sum(), "worst_coin_mean": D[D.book_return <= q.iloc[0]].coin_return.mean(),
        "best_n": (D.book_return >= q.iloc[1]).sum(), "best_coin_mean": D[D.book_return >= q.iloc[1]].coin_return.mean(),
        "share_book_from_worst1pct": D[D.book_return <= q.iloc[0]].book_return.sum() / D.book_return.sum()})
    return out
