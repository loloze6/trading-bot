import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            r7b = c / c.shift(7) - 1
            r60b = c / c.shift(60) - 1
            r3b = c / c.shift(3) - 1
            f7 = c.shift(-7) / c - 1
            f3 = c.shift(-3) / c - 1
            f1 = c.shift(-1) / c - 1
            rng = (df["high"] - df["low"]) / c
            pos_in_rng = (c - df["low"]) / (df["high"] - df["low"]).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(df)),
                "inprof": (df["regime"] == "unknown").astype(int),
                "s7": r7b / (vol30 * np.sqrt(7)), "s1": r1 / vol30,
                "s3": r3b / (vol30 * np.sqrt(3)),
                "tr60": r60b, "f7": f7, "f3": f3, "f1": f1,
                "rngs": rng / vol30, "clpos": pos_in_rng,
                "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
                "fc": df["forecast"], "alloc": df["postRebalance_current_allocation"],
            })
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin (7d on grid, all windows) and 1d
    g7 = A[A["pos"] % 7 == 0].copy()
    dr7 = g7.groupby("coin")["f7"].mean()
    g7["x7"] = g7["f7"] - g7["coin"].map(dr7)
    dr1 = A.groupby("coin")["f1"].mean()
    A["x1"] = A["f1"] - A["coin"].map(dr1)
    g3 = A[A["pos"] % 3 == 0].copy()
    dr3 = g3.groupby("coin")["f3"].mean()
    g3["x3"] = g3["f3"] - g3["coin"].map(dr3)

    def summ(df, col, by):
        g = df.dropna(subset=[col, by[-1]]).groupby(by)[col]
        out = g.agg(["count", "mean", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        return out.round(4)

    res = {}
    # 1: s7 quintiles in/out of profile, next 7d excess
    g7["s7q"] = pd.qcut(g7["s7"], 5, labels=False, duplicates="drop")
    res["7d excess by s7 quintile x inprof"] = summ(g7, "x7", ["inprof", "s7q"])
    # trend 60 buckets (crude: choppy/rising/falling) x s7 sign
    g7["trend"] = pd.cut(g7["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    g7["s7sign"] = np.sign(g7["s7"])
    res["7d excess by trend x s7 sign"] = summ(g7, "x7", ["trend", "s7sign"])
    # 2: 1-day scaled move quintiles -> next 3d excess, in/out
    g3["s1q"] = pd.qcut(g3["s1"], 5, labels=False, duplicates="drop")
    res["3d excess by s1 quintile x inprof"] = summ(g3, "x3", ["inprof", "s1q"])
    # 3: range/close pos
    g3["rngq"] = pd.qcut(g3["rngs"], 3, labels=False, duplicates="drop")
    g3["clq"] = pd.cut(g3["clpos"], [-0.01, 0.33, 0.67, 1.01], labels=["low", "mid", "high"])
    res["3d excess by range tercile x close pos"] = summ(g3, "x3", ["rngq", "clq"])
    # 4: weekday next-day excess, by trend
    A["trend"] = pd.cut(A["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    res["1d excess by weekday"] = summ(A, "x1", ["wd"])
    # 5: book: days data
    dl = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            x = dd[["book_return", "coin_return"]].copy(); x["coin"] = coin; x["win"] = w
            dl.append(x)
    D = pd.concat(dl)
    res["book by window"] = D.groupby("win")[["book_return", "coin_return"]].mean().mul(1e4).round(2)
    # trades
    tl = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): tt = t.copy(); tt["coin"] = coin; tl.append(tt)
    T = pd.concat(tl)
    T["efq"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    res["trades by entry forecast quartile"] = T.groupby("efq")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    res["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
    res["share inprof"] = float(A["inprof"].mean())
    return res
