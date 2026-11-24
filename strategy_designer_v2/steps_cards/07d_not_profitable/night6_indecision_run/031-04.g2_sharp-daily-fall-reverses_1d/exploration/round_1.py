def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    # portfolio daily returns per window
    rows = []
    for c in coins:
        for w, d in data["days"][c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    P = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index().sort_values(["wn", "day"])
    P = P.dropna()
    P["val"] = (1 + P["book"]).cumprod()
    P["peak"] = P["val"].cummax()
    P["dd"] = P["val"] / P["peak"] - 1
    P["hval"] = (1 + P["hold"]).cumprod()
    P["hdd"] = P["hval"] / P["hval"].cummax() - 1
    out["max dd book, hold"] = pd.Series({"book": P["dd"].min(), "hold": P["hdd"].min()})
    # drawdown episodes
    P = P.reset_index(drop=True)
    ep = []
    i = 0
    n = len(P)
    inn = False
    for k in range(n):
        if P.loc[k, "dd"] < 0 and not inn:
            inn = True; start = k
        if inn and P.loc[k, "dd"] == 0:
            seg = P.loc[start:k - 1]
            ep.append((start, k - 1, seg["dd"].min(), seg["dd"].idxmin()))
            inn = False
    if inn:
        seg = P.loc[start:]
        ep.append((start, n - 1, seg["dd"].min(), seg["dd"].idxmin()))
    ep = sorted(ep, key=lambda x: x[2])[:6]
    er = []
    for s, e, m, t in ep:
        seg = P.loc[s:t]
        er.append({"depth": m, "days_to_trough": t - s + 1, "windows": "%s-%s" % (P.loc[s, "wn"], P.loc[t, "wn"]),
                   "hold_ret_during": (1 + seg["hold"]).prod() - 1, "book_ret_during": (1 + seg["book"]).prod() - 1})
    out["deepest falls"] = pd.DataFrame(er)
    # bar-level analysis
    B = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy()
            b["coin"] = c; b["wn"] = int(w[1:])
            b["r"] = b["close"].pct_change()
            b["nr"] = b["close"].shift(-1) / b["close"] - 1
            b["vol20"] = b["r"].rolling(20).std()
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["ret5"] = b["close"] / b["close"].shift(5) - 1
            b["ma50"] = b["close"].rolling(50).mean()
            b["below50"] = (b["close"] < b["ma50"]).astype(float)
            b.loc[b["ma50"].isna(), "below50"] = np.nan
            b["vol_rank"] = b["vol20"] / b["vol20"].rolling(120, min_periods=40).mean()
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["nr"]
            b["rng"] = (b["high"] - b["low"]) / b["close"]
            b["bodyfrac"] = (b["close"] - b["open"]).abs() / (b["high"] - b["low"])
            B.append(b)
    B = pd.concat(B)
    cm = B.groupby("coin")["nr"].mean()
    B["ex"] = B["nr"] - B["coin"].map(cm)
    B["sig"] = B["forecast"] > 0
    # gains in drawdown episodes vs others: tag bars with the date in deepest episode
    B["day"] = pd.to_datetime(B["timestamp"]).dt.floor("D")
    P["day"] = pd.to_datetime(P["day"])
    s, e, m, t = ep[0]
    epset = P.loc[s:t, ["wn", "day"]]
    epset["inep"] = 1
    B = B.merge(epset, on=["wn", "day"], how="left")
    E = B[B["inep"] == 1]
    out["deepest fall: bars"] = pd.Series({"n_bars": len(E), "share signal": E["sig"].mean(), "mean pos": E["pos"].mean(),
        "mean ret20 at bar": E["ret20"].mean(), "share below ma50": E["below50"].mean(), "vol_rank": E["vol_rank"].mean(),
        "all bars ret20": B["ret20"].mean(), "all below50": B["below50"].mean(), "all vol_rank": B["vol_rank"].mean(),
        "gain sum": E["gain"].sum()})
    # conditional next-day excess on signal vs no signal by trend state
    def tab(col, bins, labels):
        g = B.dropna(subset=[col, "ex"]).copy()
        g["bk"] = pd.cut(g[col], bins, labels=labels)
        r = g.groupby(["bk", "sig"])["ex"].agg(["mean", "count"]).unstack()
        return r
    out["ex by ret20 x sig"] = tab("ret20", [-9, -0.15, -0.05, 0.05, 0.15, 9], ["<-15", "-15..-5", "-5..5", "5..15", ">15"])
    out["ex by below50 x sig"] = B.dropna(subset=["below50", "ex"]).groupby(["below50", "sig"])["ex"].agg(["mean", "count"]).unstack()
    out["ex by volrank x sig"] = tab("vol_rank", [0, 0.8, 1.0, 1.25, 1.6, 99], ["<.8", ".8-1", "1-1.25", "1.25-1.6", ">1.6"])
    S = B[B["sig"]].dropna(subset=["ex"]).copy()
    S["fq"] = pd.qcut(S["forecast"], 5, labels=False)
    out["signal by forecast quintile"] = S.groupby("fq").agg(fc=("forecast", "mean"), ex=("ex", "mean"), nr=("nr", "mean"), n=("ex", "size"), pos=("pos", "mean"), gain=("gain", "mean"))
    # book gain on signal vs held-without-signal bars
    out["gain by sig, pos>0"] = B[B["pos"].abs() > 1e-6].groupby("sig")["gain"].agg(["mean", "count", "sum"])
    # yearly book
    P["year"] = P["day"].dt.year
    out["book by year"] = P.groupby("year").agg(book=("book", "mean"), hold=("hold", "mean"), minval=("dd", "min"))
    # forward 3/5 day excess on signal, non overlapping not essential: use grid
    for h in [1, 3, 5]:
        rr = []
        for (c, wn), g in B.groupby(["coin", "wn"]):
            g = g.reset_index(drop=True)
            fr = g["close"].shift(-h) / g["close"] - 1
            rr.append(pd.DataFrame({"fr": fr, "sig": g["sig"], "coin": c}))
        R = pd.concat(rr).dropna()
        out["fwd %dd by sig" % h] = R.groupby("sig")["fr"].agg(["mean", "count"])
    return out
