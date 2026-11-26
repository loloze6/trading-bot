def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r3 = c / c.shift(3) - 1
            r20 = c / c.shift(20) - 1
            f3 = c.shift(-3) / c - 1
            f2 = c.shift(-2) / c - 1
            fc = b["forecast"].astype(float)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "inprof": (b["regime"] == "unknown").values,
                               "s3": (r3 / sd30).values, "r20s": (r20 / sd30).values,
                               "f3": f3.values, "f2": f2.values, "fc": fc.values,
                               "alloc": b["postRebalance_current_allocation"].astype(float).values,
                               "ts": pd.to_datetime(b["timestamp"]).values})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = pd.to_datetime(A["ts"]).dt.floor("D")

    def summ(d, col):
        d = d.dropna(subset=[col])
        n = len(d)
        if n < 5:
            return pd.Series({"n": n, "mean": np.nan, "t_day": np.nan, "days": 0})
        m = d[col].mean(); G = d["day"].nunique()
        sdev = (d[col] - m).groupby(d["day"]).sum()
        se = np.sqrt((sdev ** 2).sum() * G / max(G - 1, 1)) / n
        return pd.Series({"n": n, "mean": m, "t_day": m / se, "days": G})

    def slope(d, x, y):
        d = d.dropna(subset=[x, y])
        X = d[x] - d[x].mean(); Y = d[y]
        beta = (X * (Y - Y.mean())).sum() / (X ** 2).sum()
        e = (Y - Y.mean()) - beta * X
        G = d["day"].nunique()
        sc = (X * e).groupby(d["day"]).sum()
        se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (X ** 2).sum()
        return pd.Series({"n": len(d), "slope": beta, "t_day": beta / se, "days": G})

    out = {}
    g3 = A[A["pos"] % 3 == 0].copy()
    drift = g3.groupby("coin")["f3"].mean()
    g3["u3"] = g3["f3"] - g3["coin"].map(drift)
    g3 = g3.dropna(subset=["s3", "u3"])
    P = g3[g3["inprof"]]; O = g3[~g3["inprof"]]
    out["slope u3 on s3: in prof all/rises/falls, out all/rises/falls"] = pd.DataFrame({
        "in_all": slope(P, "s3", "u3"), "in_rise": slope(P[P.s3 > 0], "s3", "u3"),
        "in_fall": slope(P[P.s3 < 0], "s3", "u3"), "out_all": slope(O, "s3", "u3"),
        "out_rise": slope(O[O.s3 > 0], "s3", "u3"), "out_fall": slope(O[O.s3 < 0], "s3", "u3")}).T.round(4)
    # per-window consistency of in-profile slope sign
    ws = {}
    for w, d in P.groupby("w"):
        if len(d) >= 15:
            ws[w] = slope(d, "s3", "u3")
    out["in-prof slope by window"] = pd.DataFrame(ws).T.round(4)
    wso = {}
    for w, d in O.groupby("w"):
        if len(d) >= 15:
            wso[w] = slope(d, "s3", "u3")
    out["out-prof slope by window"] = pd.DataFrame(wso).T.round(4)
    # out of profile by local 20-day trend sign
    O2 = O.dropna(subset=["r20s"]).copy()
    O2["tr"] = np.where(O2["r20s"] > 0, "up20", "down20")
    out["out-prof slope by 20d trend"] = O2.groupby("tr").apply(lambda d: slope(d, "s3", "u3")).round(4)
    # rank of forecast vs s3 in profile: does forecast track s3?
    Pr = P[P.s3 > 0]
    out["corr forecast vs s3 on in-prof rises"] = float(np.corrcoef(Pr["fc"].fillna(0), Pr["s3"])[0, 1])
    Pr = Pr.copy(); Pr["s3t"] = pd.qcut(Pr["s3"], 3, labels=["small", "mid", "large"])
    out["in-prof rises by s3 tercile: u3 and mean forecast"] = Pr.groupby("s3t").apply(
        lambda d: pd.concat([summ(d, "u3"), pd.Series({"mean_fc": d["fc"].mean()})])).round(4)
    Pf = P[P.s3 < 0].copy(); Pf["s3t"] = pd.qcut(Pf["s3"], 3, labels=["large_fall", "mid", "small_fall"])
    out["in-prof falls by s3 tercile"] = Pf.groupby("s3t").apply(lambda d: summ(d, "u3")).round(4)
    # book's biggest days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D, ignore_index=True).dropna(subset=["book_return"])
    act = D[D["book_return"].abs() > 0]
    q = act["book_return"].quantile([0.05, 0.95])
    out["active coin-days, n / mean coin_return on book's worst5% / best5%"] = pd.Series({
        "n_active": len(act), "worst5_coinret": act[act.book_return <= q.iloc[0]]["coin_return"].mean(),
        "best5_coinret": act[act.book_return >= q.iloc[1]]["coin_return"].mean(),
        "share_book_sum_from_best5": act[act.book_return >= q.iloc[1]]["book_return"].sum() / act["book_return"].sum()}).round(4)
    return out
