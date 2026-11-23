def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            idx = np.arange(0, len(c) - 3, 3)
            rs.extend((c.values[idx + 3] / c.values[idx] - 1).tolist())
        drift[coin] = np.mean(rs)
    ncoins = {}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            ncoins[w] = ncoins.get(w, 0) + 1
            b = b.reset_index(drop=True).copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                              "sun": ts.dt.dayofweek == 6, "fc": b["forecast"].astype(float),
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "fwd3": c.shift(-3) / c - 1, "mon": c.shift(-1) / c - 1,
                              "tuewed": c.shift(-3) / c.shift(-1) - 1,
                              "r20": c / c.shift(20) - 1, "vol20": r1.rolling(20, min_periods=10).std(),
                              "vol60": r1.rolling(60, min_periods=20).std(),
                              "sunret": r1})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["ex3"] = A["fwd3"] - A["coin"].map(drift)
    S = A[A["sun"]].dropna(subset=["fwd3", "vol20", "r20"])
    cases = S[S["fc"] >= 2].copy()
    cases["pnl"] = cases["alloc"] * cases["fwd3"] - 0.0022 * cases["alloc"].abs()
    out["alloc_by_vol20_q"] = cases.groupby(pd.qcut(cases["vol20"], 4, labels=False)).agg(
        n=("ex3", "size"), alloc=("alloc", "mean"), ex3=("ex3", "mean"), fwd3=("fwd3", "mean"), pnl=("pnl", "mean"), pnl_sum=("pnl", "sum"))
    out["pnl_by_fc"] = cases.groupby(pd.cut(cases["fc"], [2, 4, 6, 8, 12, 21])).agg(
        n=("pnl", "size"), alloc=("alloc", "mean"), pnl=("pnl", "mean"), pnl_sum=("pnl", "sum"))
    # Monday continuation: within case, Monday fall then Tue-Wed
    cases["monq"] = pd.qcut(cases["mon"], 4, labels=False)
    out["tuewed_by_monday_q"] = cases.groupby("monq").agg(n=("mon", "size"), mon=("mon", "mean"), tuewed=("tuewed", "mean"))
    # condition-alone checks: vol20 relative to vol60
    S2 = S.copy(); S2["vr"] = S2["vol20"] / S2["vol60"]
    # weekly book chain variants
    def chain(df, wcol=None):
        d = df.copy()
        if wcol is not None:
            d["p"] = d[wcol] * d["fwd3"] - 0.0022 * d[wcol].abs()
        else:
            d["p"] = d["pnl"]
        g = d.groupby(["wn", "pos"]).agg(s=("p", "sum"), win=("win", "first")).reset_index()
        # one row per window-week: group by window and week index approx by pos//7
        g["wk"] = g["pos"] // 7
        wk = g.groupby(["wn", "wk"]).agg(s=("s", "sum"), win=("win", "first")).reset_index()
        wk["r"] = wk["s"] / wk["win"].map(ncoins)
        wk = wk.sort_values(["wn", "wk"])
        v = (1 + wk["r"]).cumprod().values
        dd = (v / np.maximum.accumulate(v) - 1).min()
        yrs = len(wk) / 52.0
        ann = v[-1] ** (1 / yrs) - 1
        return pd.Series({"weeks": len(wk), "ann": ann, "maxdd": dd, "calmar": ann / abs(dd) if dd < 0 else np.nan})
    V = {}
    V["as_tested"] = chain(cases)
    V["fc_ge8"] = chain(cases[cases["fc"] >= 8])
    v50 = cases["vol20"].median()
    V["vol20_above_median"] = chain(cases[cases["vol20"] > v50])
    V["r20_below_median"] = chain(cases[cases["r20"] < cases["r20"].median()])
    cases["fixed"] = 1.0
    V["unit_size"] = chain(cases, "fixed")
    cases["fcsz"] = cases["fc"] / 10
    V["forecast_size_novol"] = chain(cases, "fcsz")
    out["weekly_chain_variants"] = pd.DataFrame(V).T
    # condition alone vs with signal
    nos = S[S["fc"] <= 0]
    out["cond_check"] = pd.DataFrame({
        "vol20_hi_case": [cases[cases["vol20"] > v50]["ex3"].mean(), (cases["vol20"] > v50).sum()],
        "vol20_hi_nosig": [nos[nos["vol20"] > v50]["ex3"].mean(), (nos["vol20"] > v50).sum()],
        "vol20_lo_case": [cases[cases["vol20"] <= v50]["ex3"].mean(), (cases["vol20"] <= v50).sum()],
        "vol20_lo_nosig": [nos[nos["vol20"] <= v50]["ex3"].mean(), (nos["vol20"] <= v50).sum()],
    }, index=["ex3", "n"]).T
    # deepest-fall windows w1-w9: pnl by vol quartile
    f = cases[cases["wn"] <= 9]
    out["fall_w1_9_by_vol20_q"] = f.groupby(pd.qcut(f["vol20"], 4, labels=False)).agg(n=("pnl", "size"), alloc=("alloc", "mean"), ex3=("ex3", "mean"), pnl_sum=("pnl", "sum"))
    out["fall_w1_9_by_fc"] = f.groupby(pd.cut(f["fc"], [2, 8, 21])).agg(n=("pnl", "size"), ex3=("ex3", "mean"), pnl_sum=("pnl", "sum"))
    return out
