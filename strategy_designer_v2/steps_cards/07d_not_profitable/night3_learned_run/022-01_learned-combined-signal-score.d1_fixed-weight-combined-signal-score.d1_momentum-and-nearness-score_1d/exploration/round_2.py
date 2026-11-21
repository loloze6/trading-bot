def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["ret1"]
            b["r28"] = b["close"] / b["close"].shift(28) - 1
            b["r90"] = b["close"] / b["close"].shift(90) - 1
            b["lr"] = np.log(b["close"]).diff()
            b["vol30_rel"] = b["lr"].rolling(30).std() / b["lr"].expanding(30).std()
            b["dd90"] = b["close"] / b["close"].rolling(90, min_periods=20).max() - 1
            b["coin"] = coin; b["wn"] = int(w[1:])
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["side"] = np.sign(B["pos"]).map({1: "long", -1: "short", 0: "flat"})
    S = B[B["side"] != "flat"].copy()
    S["r90q"] = S.groupby("coin")["r90"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    out["side_by_r90q"] = S.groupby(["r90q", "side"]).agg(n=("gain", "size"), gain=("gain", "mean"),
                                                        ret1=("ret1", "mean")).unstack()
    S["ddq"] = S.groupby("coin")["dd90"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    out["side_by_dd90q"] = S.groupby(["ddq", "side"]).agg(n=("gain", "size"), gain=("gain", "mean"),
                                                        ret1=("ret1", "mean")).unstack()
    # short gain t-stat, non-overlapping 5-day grid
    B["pos5"] = B.groupby(["coin", "wn"]).cumcount()
    g = B[(B["pos5"] % 5 == 0)].copy()
    g["r5"] = B.groupby(["coin", "wn"])["close"].shift(-5).loc[g.index] / g["close"] - 1
    mu5 = g.groupby("coin")["r5"].mean()
    g["ex5"] = g["r5"] - g["coin"].map(mu5)
    g = g.dropna(subset=["r5"])
    def tt(x):
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    g["sgn"] = np.sign(g["forecast"])
    out["grid_long"] = tt(g.loc[g["sgn"] > 0, "r5"])
    out["grid_short_signed"] = tt(-g.loc[g["sgn"] < 0, "r5"])
    out["grid_short_excess_signed"] = tt(-g.loc[g["sgn"] < 0, "ex5"])
    g["r90q"] = g.groupby("coin")["r90"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    out["grid_short_by_r90q"] = g[g["sgn"] < 0].groupby("r90q")["r5"].apply(lambda x: tt(-x)).unstack()
    out["grid_long_by_r90q"] = g[g["sgn"] > 0].groupby("r90q")["r5"].apply(tt).unstack()
    # book daily: long-only vs short-only contribution per window ordering in deepest fall
    B["gl"] = np.where(B["pos"] > 0, B["gain"], 0.0)
    B["gs"] = np.where(B["pos"] < 0, B["gain"], 0.0)
    daily = B.groupby(["wn", "day", "coin"])[["gl", "gs"]].sum().groupby(["wn", "day"]).mean().reset_index()
    out["contrib_by_window"] = daily.groupby("wn")[["gl", "gs"]].sum()
    # yearly return / deepest fall long-only chain
    for k in ["gl", "gs"]:
        eq = (1 + daily[k]).cumprod(); dd = (eq / eq.cummax() - 1).min()
        out["chain_" + k] = pd.Series({"mean": daily[k].mean(), "maxdd": dd, "yearly": eq.iloc[-1] ** (365 / len(daily)) - 1})
    return out
