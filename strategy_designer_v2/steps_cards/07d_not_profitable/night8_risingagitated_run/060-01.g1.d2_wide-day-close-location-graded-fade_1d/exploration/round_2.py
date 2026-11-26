def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            rng = b["high"] - b["low"]
            b["cpos"] = np.where(rng > 0, 2 * (b["close"] - b["low"]) / rng - 1, 0)
            b["rr"] = rng / rng.rolling(20, min_periods=20).mean()
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["r2"] = b["close"].shift(-2) / b["close"] - 1
            b["dret"] = b["close"] / b["close"].shift(1) - 1
            b["alloc"] = b["postRebalance_current_allocation"]
            b["ts"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["coin"] = coin; b["win"] = w
            rows.append(b[["coin","win","ts","forecast","regime","cpos","rr","r1","r2","dret","alloc"]])
    A = pd.concat(rows, ignore_index=True)
    drift = A.groupby("coin")["r1"].mean()
    A["s1"] = -(A["r1"]); A["ex1"] = A["s1"] + A["coin"].map(drift)
    def summ(g):
        g = g.dropna(subset=["s1"])
        return pd.Series({"n": len(g), "s1": g["s1"].mean(),
                          "t1": stats.ttest_1samp(g["s1"], 0).statistic if len(g) > 2 else np.nan,
                          "s2": (-g["r2"]).mean(), "share_neg": (g["s1"] < 0).mean()})
    P = A[A["regime"].isin(["mean_reversion", "unknown"])].dropna(subset=["r1"]).copy()
    P["case"] = P["forecast"] < 0
    # condition alone: big up day
    q = P["dret"].quantile([1/3, 2/3]).values
    P["updayBig"] = P["dret"] > 0.10
    P["wide"] = P["rr"] >= 1
    P["hi"] = P["cpos"] > 0
    P["rrBig"] = P["rr"] > 1.57
    out["bigup_by_case"] = P.groupby(["updayBig", "case"]).apply(summ)
    out["bigup_wide_hi"] = P[P["wide"]].groupby(["updayBig", "hi"]).apply(summ)
    out["rrBig_hi"] = P[P["rr"].notna()].groupby(["rrBig", "hi"]).apply(summ)
    out["upday_noSignal_terciles"] = P[~P["case"]].groupby(pd.cut(P[~P["case"]]["dret"], [-1, 0, 0.05, 0.10, 5])).apply(summ)
    # cases: cpos x rr grid
    C = P[P["case"]].copy()
    C["cb"] = pd.cut(C["cpos"], [-1.01, 0.33, 1.01], labels=["low", "midhigh"])
    C["rb"] = pd.cut(C["rr"], [0, 1.3, 99], labels=["rr<1.3", "rr>=1.3"])
    out["case_cpos_rr"] = C.groupby(["cb", "rb"], observed=True).apply(summ)
    C["db"] = pd.cut(C["dret"], [-1, 0.05, 5], labels=["up<5%", "up>=5%"])
    out["case_cpos_dret"] = C.groupby(["cb", "db"], observed=True).apply(summ)
    # variant books: daily pnl from cases, weighted by abs alloc, mean over coins (6)
    def book(mask, name):
        d = C[mask].copy()
        d["pnl"] = d["alloc"].abs() * d["s1"] - d["alloc"].abs() * 0.0019
        res = {}
        tot = 0; vals = []
        for w in sorted(A["win"].unique(), key=lambda s: int(s[1:])):
            days = A[A["win"] == w]["ts"].drop_duplicates().sort_values()
            ncoin = A[A["win"] == w]["coin"].nunique()
            dd = d[d["win"] == w].groupby("ts")["pnl"].sum() / ncoin
            s = dd.reindex(days, fill_value=0.0)
            vals.append(s.values)
        r = np.concatenate(vals)
        v = np.cumprod(1 + r); mdd = (v / np.maximum.accumulate(v) - 1).min()
        yr = v[-1] ** (365 / len(r)) - 1
        return pd.Series({"n_cases": int(mask.sum()), "yearly": yr, "maxDD": mdd, "calmar": yr / -mdd if mdd < 0 else np.nan,
                          "sharpe": r.mean() / r.std(ddof=1) * np.sqrt(365)})
    out["variant_books"] = pd.DataFrame({
        "all": book(C["cpos"].notna() | True, "all"),
        "cpos>0.33": book(C["cpos"] > 0.33, ""),
        "cpos>0": book(C["cpos"] > 0, ""),
        "rr>=1.3": book(C["rr"] >= 1.3, ""),
        "up>=5%": book(C["dret"] >= 0.05, ""),
        "cpos>0.33&rr>=1.3": book((C["cpos"] > 0.33) & (C["rr"] >= 1.3), ""),
    }).T
    out["case_cpos_quantiles"] = C["cpos"].describe()
    return out
