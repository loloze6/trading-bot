import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "r": r, "z": r / sd, "sd": sd,
                "r5p": (c.shift(1) / c.shift(6) - 1) / (sd * np.sqrt(5)),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "regime": b["regime"].values,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "rng": (b["high"] - b["low"]) / c,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A.groupby("coin")["f1"].mean()
    A["d1"] = A["f1"] - A["coin"].map(drift)
    A["d3"] = A["f3"] - 3 * A["coin"].map(drift)
    A["prof"] = np.where(A["regime"] == "chop", "out", "in")

    def ct(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 10:
            return pd.Series({"n": len(s), "mean": np.nan, "t_day": np.nan})
        g = s.groupby("day")[col].sum()
        m = s[col].mean()
        dev = s[col] - m
        gd = dev.groupby(s["day"]).sum()
        se = np.sqrt((gd ** 2).sum()) / len(s)
        return pd.Series({"n": len(s), "days": s["day"].nunique(), "mean": m, "t_day": m / se})

    out = {}
    # next-day after scaled move, by profile and z bucket
    A["zb"] = pd.cut(A["z"], [-np.inf, -2, -1, -0.3, 0, 0.3, 1, 2, np.inf])
    out["next1_by_z_profile"] = A.groupby(["prof", "zb"], observed=True).apply(lambda s: ct(s, "d1")).round(4)
    # 3-day, non-overlapping grid pos%3==0
    G3 = A[A["pos"] % 3 == 0]
    out["next3_by_z_profile_grid"] = G3.groupby(["prof", "zb"], observed=True).apply(lambda s: ct(s, "d3")).round(4)
    # in profile rise days: by prior 5d scaled
    ins = A[(A["prof"] == "in") & (A["r"] > 0)].copy()
    ins["pb"] = pd.qcut(ins["r5p"], 4, duplicates="drop")
    out["in_rise_next1_by_prior5"] = ins.groupby("pb", observed=True).apply(lambda s: ct(s, "d1")).round(4)
    # in profile, by close position in range
    inn = A[A["prof"] == "in"].copy()
    inn["cb"] = pd.cut(inn["clpos"], [0, 0.2, 0.4, 0.6, 0.8, 1.0001], include_lowest=True)
    out["in_next1_by_closepos"] = inn.groupby("cb", observed=True).apply(lambda s: ct(s, "d1")).round(4)
    out["all_next1_by_weekday"] = A.groupby(["prof", "wd"]).apply(lambda s: ct(s, "d1")).round(4)
    # range scaled
    inn["rngz"] = inn["rng"] / inn["sd"]
    inn["rb"] = pd.qcut(inn["rngz"], 4, duplicates="drop")
    out["in_next1_by_rangez"] = inn.groupby("rb", observed=True).apply(lambda s: ct(s, "d1")).round(4)
    # book day returns: largest gains/losses context
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    out["book_by_window"] = D.groupby("win").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count")).round(5)
    out["share_in_profile_by_coin"] = A.groupby("coin")["prof"].apply(lambda s: (s == "in").mean()).round(3)
    return out
