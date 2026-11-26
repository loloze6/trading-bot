def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r": r, "rn": c.shift(-1)/c - 1,
                "r2": c/c.shift(2) - 1, "r3": c/c.shift(3) - 1,
                "rng": (b["high"]-b["low"])/c.shift(1),
                "low_d": b["low"]/c.shift(1) - 1,
                "clo": (c-b["low"])/(b["high"]-b["low"]),
                "inp": (b["regime"] != "chop").astype(int),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            ma = r.abs().rolling(60, min_periods=20).mean()
            d["z"] = r / ma
            d["zr"] = d["rng"] / ((b["high"]-b["low"])/c.shift(1)).rolling(60, min_periods=20).mean()
            d["zl"] = d["low_d"] / ma
            d["z3"] = d["r3"] / (ma*np.sqrt(3))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["rn"].mean()
    D["xn"] = D["rn"] - D["coin"].map(drift)
    D = D.dropna(subset=["z", "xn", "zr", "zl"])

    def reg(g, xs):
        g = g.dropna(subset=xs + ["xn"])
        X = np.column_stack([np.ones(len(g))] + [g[x].values for x in xs])
        y = g["xn"].values
        XtXi = np.linalg.inv(X.T @ X)
        bta = XtXi @ X.T @ y
        e = y - X @ bta
        S = np.zeros((X.shape[1], X.shape[1]))
        for _, idx in g.reset_index(drop=True).groupby("day").indices.items():
            s = (X[idx] * e[idx, None]).sum(0)
            S += np.outer(s, s)
        V = XtXi @ S @ XtXi
        G = g["day"].nunique(); N = len(g); K = X.shape[1]
        V *= G/(G-1)*(N-1)/(N-K)
        se = np.sqrt(np.diag(V))
        return pd.DataFrame({"coef%": 100*bta, "t": bta/se}, index=["const"] + xs).assign(n=N, days=G)

    out = {}
    F = D[(D.inp == 1) & (D.z < 0)]
    out["fall_z_only"] = reg(F, ["z"])
    out["fall_z_range"] = reg(F, ["z", "zr"])
    out["fall_z_range_clo"] = reg(F, ["z", "zr", "clo"])
    out["fall_z_lowdepth"] = reg(F, ["z", "zl"])
    U = D[(D.inp == 1) & (D.z > 0)]
    out["rise_z_only"] = reg(U, ["z"])
    out["rise_z_range_clo"] = reg(U, ["z", "zr", "clo"])
    A = D[D.inp == 1]
    out["all_inprofile_z_z3"] = reg(A, ["z", "z3"])
    out["all_inprofile_range_only"] = reg(A, ["zr"])
    O = D[(D.inp == 0) & (D.z < 0)]
    out["outprofile_fall_z_range"] = reg(O, ["z", "zr"])
    # book: largest gain/loss days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin, win=w))
    DD = pd.concat(dd).dropna(subset=["book_return"])
    bk = DD.groupby(["win", "day"])["book_return"].mean()
    q = bk.quantile([0.02, 0.98])
    out["book_tail_counts"] = pd.Series({"top2%_mean%": 100*bk[bk >= q[0.98]].mean(),
                                          "bot2%_mean%": 100*bk[bk <= q[0.02]].mean(),
                                          "share_gain_from_top2%": bk[bk >= q[0.98]].sum()/bk.sum(),
                                          "share_lost_bot2%": bk[bk <= q[0.02]].sum()/bk.sum()})
    out["book_by_window_mean%"] = (100*bk.groupby(level=0).mean()).round(4)
    return out
