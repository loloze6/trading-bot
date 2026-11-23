def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            b["ret1"] = c.shift(-1) / c - 1
            b["r0"] = c / c.shift(1) - 1
            b["r20"] = c / c.shift(20) - 1
            b["ma50"] = c / c.rolling(50, min_periods=30).mean() - 1
            b["vol20"] = b["r0"].rolling(20).std()
            b["volrel"] = b["vol20"] / b["r0"].rolling(120, min_periods=60).std()
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["ret1"]
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
        for w, d in data["days"][coin].items():
            d = d[["day", "book_return", "coin_return"]].copy()
            d["win"] = w; d["coin"] = coin
            daily.append(d)
    B = pd.concat(rows, ignore_index=True)
    D = pd.concat(daily, ignore_index=True)
    drift = B.groupby("coin")["r0"].mean()
    B["drift"] = B["coin"].map(drift)
    B["ex1"] = B["ret1"] - B["drift"]
    B["sig"] = B["forecast"] > 0
    B["inpos"] = B["pos"].abs() > 1e-9
    out["pos_vs_signal"] = pd.crosstab(B["sig"], B["inpos"])
    out["mean_pos_by_signal"] = B.groupby("sig")["pos"].mean()
    out["gain_by_signal_inpos"] = B[B.inpos].groupby("sig")["gain"].agg(["mean", "count", "sum"])

    # book daily
    P = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
    P["wn"] = P["win"].str[1:].astype(int)
    P = P.sort_values(["wn", "day"]).dropna(subset=["book"])
    v = (1 + P["book"]).cumprod()
    dd = v / v.cummax() - 1
    P["dd"] = dd.values
    i = int(np.argmin(P["dd"].values))
    peak = int(np.argmax(v.values[: i + 1]))
    out["deepest_fall"] = pd.Series({"depth": P["dd"].iloc[i], "days_peak_to_trough": i - peak,
                                     "win_peak": P["win"].iloc[peak], "win_trough": P["win"].iloc[i],
                                     "hold_chain_in_fall": float((1 + P["hold"].iloc[peak + 1:i + 1]).prod() - 1),
                                     "book_chain_in_fall": float((1 + P["book"].iloc[peak + 1:i + 1]).prod() - 1)})
    # per window book result
    pw = P.groupby("wn").agg(book=("book", lambda x: (1 + x).prod() - 1), hold=("hold", lambda x: (1 + x).prod() - 1),
                             mindd=("dd", "min"))
    out["per_window"] = pw

    # gain by market state, in-position bars
    X = B[B.inpos & B.ret1.notna() & B.r20.notna()].copy()
    X["trend"] = pd.qcut(X["r20"], 4, labels=["q1low", "q2", "q3", "q4high"])
    out["gain_by_r20"] = X.groupby("trend")["gain"].agg(["mean", "count", "sum"])
    X["above"] = X["ma50"] > 0
    out["gain_by_ma50"] = X.groupby("above")["gain"].agg(["mean", "count", "sum"])
    X["vq"] = pd.qcut(X["volrel"], 3, labels=["calm", "mid", "wild"])
    out["gain_by_volrel"] = X.groupby("vq")["gain"].agg(["mean", "count", "sum"])
    # signal effect by state: ex1 on signal vs non-signal bars, by ma50
    Y = B[B.ret1.notna() & B.ma50.notna()].copy()
    Y["above"] = Y["ma50"] > 0
    out["ex1_sig_by_ma50"] = Y.groupby(["above", "sig"])["ex1"].agg(["mean", "count"])
    Y["trend"] = pd.qcut(Y["r20"], 4, labels=["q1low", "q2", "q3", "q4high"])
    out["ex1_sig_by_r20"] = Y.groupby(["trend", "sig"])["ex1"].agg(["mean", "count"])
    out["gain_by_year"] = B[B.inpos].groupby("year")["gain"].agg(["mean", "sum", "count"])
    return out
