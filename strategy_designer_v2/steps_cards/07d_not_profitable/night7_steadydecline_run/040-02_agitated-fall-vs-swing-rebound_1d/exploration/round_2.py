def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "wn": int(w[1:]), "pos": b["postRebalance_current_allocation"].astype(float).fillna(0),
                              "fc": b["forecast"].astype(float), "regime": b["regime"].astype(str),
                              "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            d["r1"] = c.pct_change()
            d["fwd"] = c.shift(-1) / c - 1
            d["fwd2"] = c.shift(-2) / c - 1
            d["ret60"] = c / c.shift(60) - 1
            d["ret7"] = c / c.shift(7) - 1
            d["z"] = d["r1"] / d["r1"].rolling(30).std()
            d["i"] = np.arange(len(d))
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A = A[A["fwd"].notna()].copy()
    mean_all = A.groupby("coin")["r1"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(mean_all)
    cost = 0.00095

    def book(posname):
        g = []
        for (coin, wn), x in A.groupby(["coin", "wn"]):
            p = x[posname].values
            ch = np.abs(np.diff(np.concatenate([[0.0], p])))
            r = p * x["fwd"].values - cost * ch
            g.append(pd.DataFrame({"wn": wn, "day": x["day"].values, "r": r, "inpos": p > 0}))
        g = pd.concat(g)
        bk = g.groupby(["wn", "day"]).agg(r=("r", "mean")).reset_index().sort_values(["wn", "day"])
        v = (1 + bk["r"]).cumprod()
        dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(bk)) - 1
        return pd.Series({"mean": bk["r"].mean(), "sharpe": bk["r"].mean() / bk["r"].std() * np.sqrt(365),
                          "yearly": yr, "maxdd": dd, "calmar": yr / -dd, "inpos_share": g["inpos"].mean()})

    A["p_base"] = A["pos"]
    A["p_z1"] = np.where(A["z"] <= -1.0, A["pos"], 0)
    A["p_z15"] = np.where(A["z"] <= -1.5, A["pos"], 0)
    A["p_nochop"] = np.where((A["ret60"] > -0.10) & (A["ret60"] < 0.10), 0, A["pos"])
    A["p_r7"] = np.where(A["ret7"] < -0.10, A["pos"], 0)
    A["p_z1_r7"] = np.where((A["z"] <= -1.0) & (A["ret7"] < -0.10), A["pos"], 0)
    A["p_notrise"] = np.where(A["ret60"] > 0.10, 0, A["pos"])
    out["variant books (approx, cost 0.095% per side)"] = pd.DataFrame({k: book(k) for k in
        ["p_base", "p_z1", "p_z15", "p_nochop", "p_r7", "p_z1_r7", "p_notrise"]}).T

    # drawdown spans: book base by window, find worst windows' peak-to-trough, what was held
    g = []
    for (coin, wn), x in A.groupby(["coin", "wn"]):
        p = x["pos"].values
        g.append(x.assign(gain=p * x["fwd"].values))
    G = pd.concat(g)
    bk = G.groupby(["wn", "day"])["gain"].mean().reset_index().sort_values(["wn", "day"])
    res = []
    G["indd"] = False
    for wn in [13, 16, 17]:
        s = bk[bk["wn"] == wn].reset_index(drop=True)
        v = (1 + s["gain"]).cumprod()
        dd = v / v.cummax() - 1
        t = dd.idxmin(); pk = v.iloc[:t + 1].idxmax()
        days = set(s.loc[pk + 1:t, "day"])
        m = (G["wn"] == wn) & G["day"].isin(days)
        G.loc[m, "indd"] = True
    H = G[(G["pos"] > 0)].copy()
    H["zb"] = pd.cut(H["z"], [-99, -1.5, -1, -0.5, 0, 99])
    H["trend"] = np.where(H["ret60"].isna(), "na", np.where(H["ret60"] > 0.10, "rising", np.where(H["ret60"] < -0.10, "falling", "choppy")))
    H["r7b"] = pd.cut(H["ret7"], [-9, -0.2, -0.1, 0, 9])
    for k in ["zb", "trend", "r7b"]:
        out["held in falls (w13,w16,w17) by " + k] = H[H["indd"]].groupby(k).agg(n=("gain", "size"), gain_sum=("gain", "sum"),
                                                                              fwd_mean=("fwd", "mean"), pos=("pos", "mean"))
        out["held outside falls by " + k] = H[~H["indd"]].groupby(k).agg(n=("gain", "size"), gain_sum=("gain", "sum"),
                                                                       fwd_mean=("fwd", "mean"))
    # condition check: agitated bars, ret7<-0.1, with signal (down day) vs without (up day)
    ag = A[(A["regime"] != "chop") & A["z"].notna()].copy()
    ag["sig"] = np.where(ag["z"] <= -1, "z<=-1", np.where(ag["r1"] < 0, "small down", "up"))
    ag["r7c"] = np.where(ag["ret7"] < -0.10, "r7<-10%", "r7>=-10%")
    def tt(s):
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / s.std() * np.sqrt(len(s))})
    out["agitated next-day ex by signal x 7d fall"] = ag.groupby(["r7c", "sig"])["ex"].apply(tt).unstack()
    ag["ex2"] = ag["fwd2"] - 2 * ag["coin"].map(mean_all)
    out["agitated 2-day ex by signal x 7d fall"] = ag.dropna(subset=["ex2"]).groupby(["r7c", "sig"])["ex2"].apply(tt).unstack()
    return out
