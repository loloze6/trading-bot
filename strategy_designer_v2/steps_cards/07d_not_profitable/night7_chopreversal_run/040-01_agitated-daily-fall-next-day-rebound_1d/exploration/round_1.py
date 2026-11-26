def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- book daily returns, per window, mean over coins
    rows = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = coin; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index().sort_values(["wn", "day"])
    v = (1 + B["book_return"]).cumprod()
    dd_ = v / v.cummax() - 1
    B["dd"] = dd_.values
    out["deepest_fall"] = float(dd_.min())
    yrs = len(B) / 365
    out["yearly_return"] = float(v.iloc[-1] ** (1 / yrs) - 1)
    # drawdown by window
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["by_window"] = B.groupby("wn").agg(book_sum=("book_return", "sum"), coin_sum=("coin_return", "sum"),
                                           min_dd=("dd", "min"), n=("book_return", "size"))
    # worst 15 book days: what coin did
    worst = B.nsmallest(20, "book_return")
    out["worst20_days_mean"] = worst[["book_return", "coin_return"]].mean()
    out["worst20_by_window"] = worst.groupby("wn").size()
    # ---- bar-level: signals and next-day returns, with state
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            nxt = c.shift(-1) / c - 1
            absm = r1.abs().rolling(60, min_periods=20).mean()
            z = -r1 / absm
            ret7 = c / c.shift(7) - 1
            ret30 = c / c.shift(30) - 1
            rng = (b["high"] - b["low"]) / c
            df = pd.DataFrame({"coin": coin, "w": w, "r1": r1, "z": z, "nxt": nxt,
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "agit": b["regime"] != "chop", "ret7": ret7, "ret30": ret30,
                               "rng_rel": rng / rng.rolling(30, min_periods=10).mean(),
                               "gain": b["postRebalance_current_allocation"] * nxt})
            recs.append(df)
    X = pd.concat(recs).dropna(subset=["nxt", "r1"])
    mu = X.groupby("coin")["nxt"].mean()
    X["ex"] = X["nxt"] - X["coin"].map(mu)
    S = X[X["fc"] > 0]
    out["n_signal"] = len(S)
    S = S.copy()
    S["zbin"] = pd.qcut(S["z"], 4, labels=False)
    def summ(g):
        return pd.Series({"n": len(g), "ex_mean": g["ex"].mean(), "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))),
                          "gain_mean": g["gain"].mean(), "alloc": g["alloc"].mean()})
    out["by_fall_quartile"] = S.groupby("zbin").apply(summ)
    S["r7bin"] = pd.qcut(S["ret7"], 3, labels=False)
    out["by_prior7d_tercile"] = S.groupby("r7bin").apply(summ)
    S["r30bin"] = pd.cut(S["ret30"], [-9, -0.15, 0, 0.15, 9])
    out["by_prior30d"] = S.groupby("r30bin").apply(summ)
    S["rngbin"] = pd.qcut(S["rng_rel"], 3, labels=False)
    out["by_range_vs_usual"] = S.groupby("rngbin").apply(summ)
    # condition alone (no signal) in agitated: by prior 30d
    N = X[(X["fc"] <= 0) & X["agit"]].copy()
    N["r30bin"] = pd.cut(N["ret30"], [-9, -0.15, 0, 0.15, 9])
    out["nosignal_agit_by_prior30d"] = N.groupby("r30bin").apply(summ)
    # by year
    S2 = S.copy()
    out["by_window_signal"] = S2.groupby("w").apply(summ)
    return out
