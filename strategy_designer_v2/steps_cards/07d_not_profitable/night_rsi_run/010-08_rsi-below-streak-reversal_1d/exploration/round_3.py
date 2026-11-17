def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            pos = b["postRebalance_current_allocation"].fillna(0)
            nxt = c.shift(-1) / c - 1
            dd60 = c / c.rolling(60, min_periods=30).max() - 1
            vol20 = c.pct_change().rolling(20).std()
            ret7 = c / c.shift(7) - 1
            age = -b["debug_info.components.below_age.last_history_value"]
            fwd14 = c.shift(-14) / c - 1
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": pos, "nxt": nxt, "gain": pos * nxt,
                                      "dd60": dd60, "vol20": vol20, "ret7": ret7, "age": age,
                                      "fwd14": fwd14, "i": np.arange(len(b))}))
    d = pd.concat(rows)
    on = d[d["pos"] > 0].dropna(subset=["dd60", "nxt"]).copy()
    on["ddq"] = pd.qcut(on["dd60"], 3, labels=["deep", "mid", "shallow"])
    on["r7q"] = pd.qcut(on["ret7"], 3, labels=["fell7", "mid", "rose7"])
    for k in ["ddq", "r7q"]:
        out["long_gain_by_" + k] = on.groupby(k).agg(n=("gain", "size"), gain=("gain", "mean"), pos=("pos", "mean"),
                                                   nxt=("nxt", "mean"), sum_gain=("gain", "sum"))
    worst = on.nsmallest(40, "gain")
    out["worst40_long_bars_state"] = pd.Series({"mean_gain": worst["gain"].mean(), "mean_pos": worst["pos"].mean(),
        "mean_age": worst["age"].mean(), "all_age": on["age"].mean(),
        "mean_dd60": worst["dd60"].mean(), "all_dd60": on["dd60"].mean(),
        "mean_ret7": worst["ret7"].mean(), "all_ret7": on["ret7"].mean(),
        "share_sum": worst["gain"].sum() / on["gain"].sum()})
    grid = d[d["i"] % 14 == 0].copy()
    grid["ex"] = grid["fwd14"] - grid["coin"].map(grid.groupby("coin")["fwd14"].mean())
    g = grid[grid["age"] > 0].dropna(subset=["ex", "dd60", "age"]).copy()
    g["x"] = g["age"] * (-g["dd60"])
    res = {}
    for k in ["age", "x"]:
        sl = stats.linregress(g[k], g["ex"])
        res[k] = {"n": len(g), "slope": sl.slope, "t": sl.slope / sl.stderr}
    out["grid_age_vs_age_x_depth"] = pd.DataFrame(res).T
    g["xq"] = pd.qcut(g["x"], 3, labels=["low", "mid", "high"])
    out["grid_by_age_x_depth"] = g.groupby("xq").agg(n=("ex", "size"), ex=("ex", "mean"),
        t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    return out
