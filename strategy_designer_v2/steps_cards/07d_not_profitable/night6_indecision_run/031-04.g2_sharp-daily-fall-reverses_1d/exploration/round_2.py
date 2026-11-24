def explore(data):
    import pandas as pd, numpy as np
    out = {}
    coins = list(data["bars"].keys())
    B = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy()
            b["coin"] = c; b["wn"] = int(w[1:])
            b["r"] = b["close"].pct_change()
            b["nr"] = b["close"].shift(-1) / b["close"] - 1
            b["vol20"] = b["r"].rolling(20).std()
            b["vol_rank"] = b["vol20"] / b["vol20"].rolling(120, min_periods=40).mean()
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["pos"] = b["postRebalance_current_allocation"].fillna(0)
            b["prev"] = b["previous_allocation"].fillna(0)
            B.append(b)
    B = pd.concat(B)
    cm = B.groupby("coin")["nr"].mean()
    B["ex"] = B["nr"] - B["coin"].map(cm)
    B["sig"] = B["forecast"] > 0
    B["day"] = pd.to_datetime(B["timestamp"]).dt.floor("D")
    B = B.dropna(subset=["nr"])
    cost = 0.0019 / 2

    def book(mult, name):
        g = B.copy()
        g["p"] = g["pos"] * mult
        g = g.sort_values(["coin", "wn", "day"])
        g["pp"] = g.groupby(["coin", "wn"])["p"].shift(1).fillna(0)
        g["ret"] = g["p"] * g["nr"] - (g["p"] - g["pp"]).abs() * cost
        P = g.groupby(["wn", "day"])["ret"].mean().reset_index().sort_values(["wn", "day"])
        v = (1 + P["ret"]).cumprod()
        dd = (v / v.cummax() - 1).min()
        yrs = len(P) / 365
        yr = v.iloc[-1] ** (1 / yrs) - 1
        sh = P["ret"].mean() / P["ret"].std() * np.sqrt(365)
        inpos = (g["p"].abs() > 1e-9).mean()
        return {"yearly": yr, "maxdd": dd, "calmar": yr / -dd, "sharpe": sh, "in_pos": inpos}

    vr = B["vol_rank"].fillna(1.0)
    res = {}
    res["base"] = book(1.0, "base")
    res["vr>1"] = book((vr > 1).astype(float).values, "")
    res["vr>0.8"] = book((vr > 0.8).astype(float).values, "")
    res["fc>7"] = book((B["forecast"] > 7).astype(float).values, "")
    res["vr>1 & fc>4"] = book(((vr > 1) & (B["forecast"] > 4)).astype(float).values, "")
    res["scale vr clip(0,2)"] = book(np.clip(vr.values, 0, 2), "")
    res["scale (vr-0.6) clip 0..2"] = book(np.clip((vr.values - 0.6) / 0.6, 0, 2), "")
    out["book variants (after est. cost)"] = pd.DataFrame(res).T

    # day-clustered t of signal excess by vol_rank bucket; and slope of ex on forecast within
    S = B[B["sig"]].dropna(subset=["vol_rank", "ex"]).copy()
    S["vb"] = pd.cut(S["vol_rank"], [0, 0.8, 1.0, 1.25, 99], labels=["<.8", ".8-1", "1-1.25", ">1.25"])
    rows = {}
    for k, g in S.groupby("vb"):
        dsum = g.groupby("day")["ex"].apply(lambda x: (x - g["ex"].mean()).sum())
        se = np.sqrt((dsum ** 2).sum()) / len(g)
        q = g.copy(); q["fq"] = pd.qcut(q["forecast"], 3, labels=False)
        m = q.groupby("fq")["ex"].mean()
        rows[str(k)] = {"ex": g["ex"].mean(), "t_day": g["ex"].mean() / se, "n": len(g), "days": g["day"].nunique(),
                        "ex lowfc": m.iloc[0], "ex midfc": m.iloc[1], "ex hifc": m.iloc[2]}
    out["signal ex by volrank (day-clustered t)"] = pd.DataFrame(rows).T
    # condition alone: no-signal down days? compare non-signal bars by vol bucket
    N = B[~B["sig"]].dropna(subset=["vol_rank", "ex"]).copy()
    N["vb"] = pd.cut(N["vol_rank"], [0, 0.8, 1.0, 1.25, 99], labels=["<.8", ".8-1", "1-1.25", ">1.25"])
    out["no-signal ex by volrank"] = N.groupby("vb")["ex"].agg(["mean", "count"])
    # by window count: share of windows where high-vol signals positive
    S["hv"] = S["vol_rank"] > 1
    wv = S.groupby(["wn", "hv"])["ex"].mean().unstack()
    out["windows: share positive ex, low vs high vol"] = pd.Series({"lowvol share>0": (wv[False] > 0).mean(), "highvol share>0": (wv[True] > 0).mean(),
                                                                     "lowvol mean": wv[False].mean(), "highvol mean": wv[True].mean()})
    return out
