def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns: mean over coins per (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, df in ws.items():
            d = df[["day", "book_return", "coin_return"]].copy()
            d["coin"] = c; d["window"] = w
            rows.append(d)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().sort_values(["wn", "day"])
    B = B.dropna(subset=["br"])
    v = (1 + B["br"]).cumprod()
    dd = v / v.cummax() - 1
    B["dd"] = dd.values
    out["max_dd"] = float(dd.min())
    wstats = B.groupby("wn").agg(mean=("br", "mean"), sum=("br", "sum"), n=("br", "size"), worst=("br", "min"), coin=("cr", "mean"))
    wstats["sharpe"] = B.groupby("wn")["br"].apply(lambda x: x.mean() / x.std() * np.sqrt(365))
    out["per_window"] = wstats
    # worst days of book
    worst = B.nsmallest(15, "br")[["wn", "br", "cr"]].reset_index(drop=True)
    out["worst15_days"] = worst
    out["share_loss_in_worst15"] = float(worst["br"].sum() / B.loc[B.br < 0, "br"].sum())

    # cases: per bar features
    cases = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            nxt = cl.shift(-1) / cl - 1
            nxt2 = cl.shift(-2) / cl - 1
            nxt3 = cl.shift(-3) / cl - 1
            sd30 = r.rolling(30).std()
            rng = (b["high"] - b["low"]) / cl / sd30
            ret_z = r / sd30
            prev_z = r.shift(1) / sd30
            r5 = cl / cl.shift(5) - 1
            r60 = cl / cl.shift(60) - 1
            clpos = (cl - b["low"]) / (b["high"] - b["low"])
            upper_wick = (b["high"] - np.maximum(cl, b["open"])) / (b["high"] - b["low"])
            act = b["forecast"] < 0
            df = pd.DataFrame({"coin": c, "wn": int(w[1:]), "f": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "nxt": nxt, "nxt2": nxt2, "nxt3": nxt3, "rng": rng, "retz": ret_z, "prevz": prev_z,
                               "r5": r5 / sd30, "r60": r60, "clpos": clpos, "wick": upper_wick, "sd30": sd30,
                               "act": act, "up": r > 0, "prevdown": r.shift(1) <= 0})
            df["gain"] = -df["nxt"]
            cases.append(df)
    C = pd.concat(cases, ignore_index=True)
    A = C[C.act].dropna(subset=["nxt"])
    out["n_cases"] = len(A)
    out["case_short_gain_mean_t"] = pd.Series({"mean": A.gain.mean(), "t": stats.ttest_1samp(A.gain, 0).statistic,
                                               "share_pos": (A.gain > 0).mean(), "p5": A.gain.quantile(0.05), "p95": A.gain.quantile(0.95)})
    def qtab(col, q=4, df=A):
        g = pd.qcut(df[col], q, duplicates="drop")
        t = df.groupby(g, observed=True)["gain"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["mean2d"] = df.groupby(g, observed=True)["nxt2"].mean() * -1
        t["mean3d"] = df.groupby(g, observed=True)["nxt3"].mean() * -1
        t.index = t.index.astype(str)
        return t
    for col in ["rng", "retz", "prevz", "r5", "r60", "clpos", "wick", "sd30"]:
        out["by_" + col] = qtab(col)
    out["by_window"] = A.groupby("wn")["gain"].agg(["mean", "count"])
    out["by_coin"] = A.groupby("coin")["gain"].agg(["mean", "count"])
    # horizon on cases
    out["horizon"] = pd.Series({"1d": A.gain.mean(), "2d": -A.nxt2.mean(), "3d": -A.nxt3.mean()})
    # biggest losing cases' features
    L = A.nsmallest(30, "gain")
    out["worst30_cases_feat_mean_vs_all"] = pd.DataFrame({"worst30": L[["gain", "rng", "retz", "prevz", "r5", "r60", "clpos", "wick", "alloc"]].mean(),
                                                         "all": A[["gain", "rng", "retz", "prevz", "r5", "r60", "clpos", "wick", "alloc"]].mean()})
    return out
