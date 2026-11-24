def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    wins = sorted(data["days"][coins[0]].keys(), key=lambda w: int(w[1:]))
    # book daily returns
    rows = []
    for c in coins:
        for w in wins:
            d = data["days"][c].get(w)
            if d is None: continue
            d = d.copy(); d["coin"] = c; d["win"] = w
            rows.append(d[["day","win","coin","book_return","coin_return"]])
    D = pd.concat(rows)
    B = D.groupby(["win","day"]).agg(book=("book_return","mean"), hold=("coin_return","mean")).reset_index()
    B["wn"] = B["win"].str[1:].astype(int)
    B = B.sort_values(["wn","day"]).dropna(subset=["book"]).reset_index(drop=True)
    v = (1+B["book"]).cumprod()
    dd = v/v.cummax()-1
    B["dd"] = dd.values
    # deepest fall episodes
    peak_idx = None
    trough = dd.idxmin()
    pk = v[:trough+1].idxmax()
    out["deepest fall"] = pd.Series({"depth": dd.min(), "days": trough-pk, "win_peak": B.loc[pk,"win"], "win_trough": B.loc[trough,"win"],
                                     "hold_chain_during": (1+B.loc[pk+1:trough,"hold"]).prod()-1})
    # drawdown by window: worst within-window fall
    out["per window"] = B.groupby("wn").agg(book_mean=("book","mean"), hold_mean=("hold","mean"), book_sd=("book","std"), min_dd=("dd","min"), n=("book","size")).round(5)
    # per bar analysis
    br = []
    for c in coins:
        for w in wins:
            b = data["bars"][c].get(w)
            if b is None or len(b) < 5: continue
            b = b.copy()
            r = b["close"].pct_change()
            b["r"] = r
            b["fwd"] = b["close"].shift(-1)/b["close"]-1
            b["sd60"] = r.rolling(60, min_periods=20).std()
            b["z"] = r/b["sd60"]
            b["ret20"] = b["close"]/b["close"].shift(20)-1
            b["ret5"] = b["close"]/b["close"].shift(5)-1
            b["vol_ratio"] = r.rolling(10).std()/b["sd60"]
            b["pos"] = b["postRebalance_current_allocation"]
            b["coin"] = c; b["wn"] = int(w[1:])
            br.append(b[["coin","wn","r","fwd","z","forecast","ret20","ret5","vol_ratio","pos","sd60"]])
    X = pd.concat(br).dropna(subset=["fwd"])
    mu = X.groupby("coin")["fwd"].transform("mean")
    X["ex"] = X["fwd"]-mu
    X["gain"] = X["pos"]*X["fwd"]
    S = X[X["forecast"]>0].copy()
    out["pos mean on signal vs not"] = pd.Series({"pos_sig": S["pos"].mean(), "pos_nosig": X.loc[X.forecast<=0,"pos"].mean(),
        "gain_sig": S["gain"].mean(), "gain_nosig": X.loc[X.forecast<=0,"gain"].mean(), "n_sig": len(S), "n_nosig": (X.forecast<=0).sum()})
    def tab(df, col, q=4):
        df = df.dropna(subset=[col]).copy()
        df["b"] = pd.qcut(df[col], q, labels=False, duplicates="drop")
        g = df.groupby("b").agg(lo=(col,"min"), hi=(col,"max"), ex=("ex","mean"), fwd=("fwd","mean"), gain=("gain","mean"), sdfwd=("fwd","std"), n=("ex","size"))
        g["t_ex"] = g["ex"]/(g["sdfwd"]/np.sqrt(g["n"]))
        return g.round(5)
    out["signal bars by z depth"] = tab(S, "z", 5)
    out["signal bars by ret20"] = tab(S, "ret20", 4)
    out["NON-signal bars by ret20"] = tab(X[X.forecast<=0], "ret20", 4)
    out["signal bars by vol_ratio"] = tab(S, "vol_ratio", 4)
    out["NON-signal by vol_ratio"] = tab(X[X.forecast<=0], "vol_ratio", 4)
    out["signal bars by ret5"] = tab(S, "ret5", 4)
    out["signal by coin"] = S.groupby("coin").agg(ex=("ex","mean"), gain=("gain","mean"), n=("ex","size")).round(5)
    # bars in the deepest fall
    return out
