def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"]).dropna()
    B["val"] = (1 + B["book_return"]).cumprod()
    B["peak"] = B["val"].cummax()
    B["dd"] = B["val"] / B["peak"] - 1
    out["by_window"] = B.groupby("wn").agg(n=("book_return", "size"), mean=("book_return", "mean"),
                                           sd=("book_return", "std"), coin=("coin_return", "mean"),
                                           mindd=("dd", "min")).round(5)
    # per bar cases with features
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r = cl.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            z = r / sd30
            nxt = cl.shift(-1) / cl - 1
            nxt3 = cl.shift(-3) / cl - 1
            r3 = cl / cl.shift(3) - 1
            r10 = cl / cl.shift(10) - 1
            rng = (b["high"] - b["low"])
            clv = (cl - b["low"]) / rng.replace(0, np.nan)
            alloc = b["postRebalance_current_allocation"]
            pos = alloc.fillna(0)
            gain = pos * nxt
            df = pd.DataFrame({"coin": c, "w": w, "z": z, "r": r, "nxt": nxt, "nxt3": nxt3, "r3": r3 / sd30,
                               "r10": r10 / sd30, "clv": clv, "alloc": pos, "gain": gain,
                               "fc": b["forecast"], "inprof": b["regime"] == "unknown",
                               "volr": b["volume"] / b["volume"].rolling(30, min_periods=10).mean(),
                               "sd30": sd30})
            recs.append(df)
    X = pd.concat(recs)
    mu = X.groupby("coin")["nxt"].mean()
    X["drift"] = X["coin"].map(mu)
    X["unus_short"] = -(X["nxt"] - X["drift"])
    P = X[X["inprof"] & (X["r"] > 0)].dropna(subset=["nxt", "z"])
    out["n_profile_up"] = len(P)
    P["zq"] = pd.qcut(P["z"], 4, labels=False)
    def ag(g):
        return pd.Series({"n": len(g), "unus": g["unus_short"].mean(),
                          "t": g["unus_short"].mean() / (g["unus_short"].std() / np.sqrt(len(g))),
                          "gain": g["gain"].mean(), "alloc": g["alloc"].mean()})
    out["by_z_quartile"] = P.groupby("zq").apply(ag).round(4)
    P["r10q"] = pd.qcut(P["r10"], 3, labels=False)
    out["by_prior10d_scaled"] = P.groupby("r10q").apply(ag).round(4)
    P["clvq"] = pd.qcut(P["clv"], 3, labels=False)
    out["by_close_in_range"] = P.groupby("clvq").apply(ag).round(4)
    P["volq"] = pd.qcut(P["volr"], 3, labels=False)
    out["by_volume_ratio"] = P.groupby("volq").apply(ag).round(4)
    out["by_window_cases"] = P.groupby("w").apply(ag).round(4)
    # whole profile, any day, and out-of-profile up days
    Q = X[(~X["inprof"]) & (X["r"] > 0)].dropna(subset=["nxt", "z"])
    Q["zq"] = pd.qcut(Q["z"], 4, labels=False)
    out["outside_profile_up_by_z"] = Q.groupby("zq").apply(ag).round(4)
    A = X[X["inprof"]].dropna(subset=["nxt"])
    out["profile_all_days_unus_short"] = round(A["unus_short"].mean(), 5)
    out["profile_down_days_unus_short"] = round(A[A["r"] <= 0]["unus_short"].mean(), 5)
    # 3-day horizon
    P["u3"] = -(P["nxt3"] - 3 * P["drift"])
    out["by_z_q_3day"] = P.groupby("zq")["u3"].agg(["mean", "count"]).round(4)
    # worst book days: what held
    worst = B.nsmallest(15, "book_return")
    out["worst_days_mean_coinret"] = round(worst["coin_return"].mean(), 4)
    out["worst15_book_sum"] = round(worst["book_return"].sum(), 4)
    out["book_total_logsum"] = round(np.log1p(B["book_return"]).sum(), 4)
    return out
