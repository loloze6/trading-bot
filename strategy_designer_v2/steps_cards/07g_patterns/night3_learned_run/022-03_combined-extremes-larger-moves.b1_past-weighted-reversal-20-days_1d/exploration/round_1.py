def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 20
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # coin drift and usual move over H on non-overlapping grid
        fr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            fr += list(c[idx + H] / c[idx] - 1)
        fr = np.array(fr)
        drift, usual = fr.mean(), fr.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fc": b["forecast"],
                "raw": b["debug_info.components.rev_weighted.last_history_value"],
                "pos": b["postRebalance_current_allocation"],
                "r1": r1, "r5": c.pct_change(5), "r10": c.pct_change(10), "r20": c.pct_change(20),
                "vol10": r1.rolling(10).std(),
                "vol20": r1.rolling(20).std(),
                "near20": c / c.rolling(20).max() - 1,
                "rng": (b["high"] - b["low"]) / c,
                "vchg": np.log(b["volume"].replace(0, np.nan) / b["volume"].rolling(20).mean()),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "fwd": c.shift(-H) / c - 1,
            })
            df["ex"] = df["fwd"] - drift
            df["str"] = df["ex"] / usual
            df = df.iloc[np.arange(0, len(df), H)]
            df = df[df["fwd"].notna()]
            rows.append(df)
    A = pd.concat(rows)
    out = {}
    out["n_grid"] = len(A)
    res = []
    for s in ["fc", "raw", "r1", "r5", "r10", "r20", "vol10", "vol20", "near20", "rng", "vchg"]:
        d = A[["coin", s, "ex", "str"]].dropna()
        d = d.copy()
        d["q"] = d.groupby("coin")[s].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False) if len(x) >= 10 else np.nan)
        d = d.dropna()
        g = d.groupby("q")["str"].mean()
        hi = d[d.q == 4]["str"]; lo = d[d.q == 0]["str"]
        t = stats.ttest_ind(hi, lo, equal_var=False).statistic
        rc = stats.spearmanr(d[s], d["str"]).correlation
        res.append([s, len(d)] + list(g.round(3)) + [round(t, 2), round(rc, 3)])
    out["quintile_strength"] = pd.DataFrame(res, columns=["sig", "n", "q0", "q1", "q2", "q3", "q4", "t_q4_q0", "spearman"])
    out["weekday_str"] = A.groupby("wd")["str"].agg(["mean", "count"]).round(3)
    # per window-year view of r20 effect sign
    d = A.dropna(subset=["r20"]).copy()
    d["s"] = np.sign(d["r20"]) * d["str"]
    out["r20_signed_by_coin"] = d.groupby("coin")["s"].agg(["mean", "count"]).round(3)
    # daily: book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w
            dd.append(x)
    D = pd.concat(dd)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_year"] = D.groupby("yr").agg(book=("book_return", "mean"), hold=("coin_return", "mean"), n=("book_return", "count"))
    out["book_by_coin"] = D.groupby("coin").agg(book=("book_return", "mean"), hold=("coin_return", "mean"))
    # daily-bar next-day after large moves, by r1 quintile, pooled
    nd = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            c = b["close"].reset_index(drop=True); r = c.pct_change()
            z = r / r.rolling(20).std().shift(1)
            nd.append(pd.DataFrame({"z": z, "n1": r.shift(-1), "n5": c.shift(-5) / c - 1}).iloc[::5])
        pass
    N = pd.concat(nd).dropna()
    N["q"] = pd.qcut(N["z"], 10, labels=False)
    out["after_move_decile"] = N.groupby("q")[["n1", "n5"]].mean().round(4).assign(n=N.groupby("q").size())
    return out
