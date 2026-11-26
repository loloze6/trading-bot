def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w})
            d["r1"] = c.pct_change()
            d["std30"] = d["r1"].rolling(30, min_periods=20).std()
            d["z"] = d["r1"] / d["std30"]
            d["r5p"] = c / c.shift(5) - 1
            d["z5"] = d["r5p"] / (d["std30"] * np.sqrt(5))
            d["fwd5"] = c.shift(-5) / c - 1
            d["fwd1"] = c.shift(-1) / c - 1
            d["ret60"] = c / c.shift(60) - 1
            d["dist20"] = c / c.rolling(20, min_periods=10).max() - 1
            d["calmchop"] = (b["regime"] == "unknown").values
            d["fc"] = b["forecast"].astype(float).values
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday.values
            d["grid"] = (np.arange(len(b)) % 5) == 0
            d["pos"] = b["postRebalance_current_allocation"].astype(float).values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    g = D[D["grid"]].copy()
    cm = g.groupby("coin")["fwd5"].mean()
    D["ex5"] = D["fwd5"] - D["coin"].map(cm)
    g = D[D["grid"]].dropna(subset=["ex5"]).copy()
    out = {}
    def summ(x):
        x = x.dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(n)) if n > 2 else np.nan})
    gz = g.dropna(subset=["z"]).copy()
    gz["zb"] = pd.cut(gz["z"], [-99, -2, -1, 0, 1, 2, 99])
    gz["tr"] = pd.cut(gz["ret60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    out["A_ex5_by_z_calmchop"] = gz.groupby(["calmchop", "zb"], observed=True)["ex5"].apply(summ).unstack()
    out["C_ex5_by_z_trend"] = gz.groupby(["tr", "zb"], observed=True)["ex5"].apply(summ).unstack()
    # signed follow-through slope by group
    res = {}
    for k, s in gz.groupby("calmchop"):
        sl = stats.linregress(s["z"], s["ex5"]); res[f"calmchop={k}"] = (sl.slope, sl.slope/sl.stderr, len(s))
    for k, s in gz.dropna(subset=["tr"]).groupby("tr", observed=True):
        sl = stats.linregress(s["z"], s["ex5"]); res[f"tr={k}"] = (sl.slope, sl.slope/sl.stderr, len(s))
    out["B_slope_ex5_on_z"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    # 5-day past move
    g5 = gz.dropna(subset=["z5"]).copy()
    g5["z5b"] = pd.cut(g5["z5"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    out["D_ex5_by_past5z_trend"] = g5.groupby(["tr", "z5b"], observed=True)["ex5"].apply(summ).unstack()
    # vol level within coin
    gz["volt"] = gz.groupby("coin")["std30"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=["low", "mid", "high"]))
    out["E_ex5_by_vol_tercile"] = gz.groupby("volt", observed=True)["ex5"].apply(summ).unstack()
    out["E2_slope_by_vol"] = pd.DataFrame({k: (lambda sl: (sl.slope, sl.slope/sl.stderr, len(s)))(stats.linregress(s["z"], s["ex5"])) for k, s in gz.groupby("volt", observed=True)}, index=["slope", "t", "n"]).T
    # distance to 20d high
    gd = g.dropna(subset=["dist20"]).copy()
    gd["db"] = pd.cut(gd["dist20"], [-9, -0.2, -0.1, -0.05, -0.0001, 0.01])
    out["F_ex5_by_dist20"] = gd.groupby("db", observed=True)["ex5"].apply(summ).unstack()
    # weekday next-day return excess
    cm1 = D.groupby("coin")["fwd1"].mean()
    D["ex1"] = D["fwd1"] - D["coin"].map(cm1)
    out["G_ex1_by_weekday"] = D.groupby("wd")["ex1"].apply(summ).unstack()
    # forecast in calm-chop
    gf = g[(g["calmchop"]) & (g["fc"] > 0)].copy()
    gf["fq"] = pd.qcut(gf["fc"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["H_ex5_by_forecast_q"] = gf.groupby("fq", observed=True)["ex5"].apply(summ).unstack()
    out["H2_calmchop_fc0"] = summ(g[(g["calmchop"]) & (g["fc"] <= 0)]["ex5"])
    # trades
    tl = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tl.append(t.assign(coin=coin))
    if tl:
        T = pd.concat(tl, ignore_index=True)
        T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 3, labels=["low", "mid", "high"])
        out["I_trades_by_entry_fc"] = T.groupby("fq", observed=True)["net_profit_loss_percent"].apply(summ).unstack()
        out["I2_trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].apply(summ).unstack()
    return out
