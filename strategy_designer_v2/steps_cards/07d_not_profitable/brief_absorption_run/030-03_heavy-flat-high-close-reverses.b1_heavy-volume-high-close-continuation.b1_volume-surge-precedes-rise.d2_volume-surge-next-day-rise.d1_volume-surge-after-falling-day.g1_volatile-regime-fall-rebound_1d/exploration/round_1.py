def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    wins = sorted(set(w for c in coins for w in data["days"][c].keys()), key=lambda x: int(x[1:]))
    # book daily returns: mean over coins per day within window
    chain = []
    for w in wins:
        frames = []
        for c in coins:
            if w in data["days"][c]:
                d = data["days"][c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        df = pd.concat(frames)
        g = df.groupby("day").agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna()
        g["win"] = w
        chain.append(g.reset_index())
    ch = pd.concat(chain, ignore_index=True)
    ch["val"] = (1 + ch["br"]).cumprod()
    ch["peak"] = ch["val"].cummax()
    ch["dd"] = ch["val"] / ch["peak"] - 1
    ch["hval"] = (1 + ch["cr"]).cumprod()
    # find top drawdown episodes
    eps = []
    i = 0
    n = len(ch)
    dd = ch["dd"].values
    while i < n:
        if dd[i] < 0:
            j = i
            while j < n and dd[j] < 0:
                j += 1
            seg = ch.iloc[i:j]
            k = seg["dd"].idxmin()
            eps.append({"start_pos": i, "trough_pos": k, "len_days": j - i, "depth": seg["dd"].min(),
                        "wins": ",".join(sorted(set(seg.loc[:k, "win"]), key=lambda x: int(x[1:]))),
                        "hold_ret_to_trough": ch.loc[k, "hval"] / ch.loc[max(i - 1, 0), "hval"] - 1})
            i = j
        else:
            i += 1
    eps = pd.DataFrame(eps).sort_values("depth").head(6)
    out["deepest_falls"] = eps
    out["maxdd"] = float(ch["dd"].min())

    # per-bar analysis
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy()
            r = b["close"].pct_change()
            sd20 = r.rolling(20).std()
            b["ret1"] = r
            b["z"] = r / sd20
            b["vr"] = sd20 / sd20.rolling(120, min_periods=40).mean()
            b["ret5"] = b["close"] / b["close"].shift(5) - 1
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["ret60"] = b["close"] / b["close"].shift(60) - 1
            b["fwd"] = b["close"].shift(-1) / b["close"] - 1
            b["gain"] = b["postRebalance_current_allocation"] * b["fwd"]
            b["coin"] = c; b["win"] = w
            b["ma50"] = b["close"] / b["close"].rolling(50).mean() - 1
            b["dn5"] = (r < 0).astype(float).rolling(5).sum()
            rows.append(b[["coin", "win", "forecast", "postRebalance_current_allocation", "ret1", "z", "vr",
                           "ret5", "ret20", "ret60", "fwd", "gain", "ma50", "dn5"]])
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["fwd"].mean()
    B["ex"] = B["fwd"] - B["coin"].map(mu)
    B["sig"] = B["forecast"] > 0
    out["held_share_on_sig_vs_not"] = B.groupby("sig")["postRebalance_current_allocation"].apply(lambda x: (x.abs() > 0).mean())

    def summ(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})

    # gain by states, signal vs no signal
    res = {}
    for name, col in [("ret20", "ret20"), ("ret60", "ret60"), ("ma50", "ma50"), ("vr", "vr"), ("z", "z")]:
        q = pd.qcut(B[col], 4, labels=False, duplicates="drop")
        tab = B.assign(q=q).groupby(["q", "sig"])["ex"].apply(summ).unstack()
        res[name] = tab
    for k, v in res.items():
        out["ex_by_" + k + "_quartile_x_sig"] = v
    # book bar gain by state on held bars
    H = B[B["postRebalance_current_allocation"].abs() > 0]
    out["bookgain_by_ma50_q"] = H.assign(q=pd.qcut(H["ma50"], 4, labels=False)).groupby("q")["gain"].apply(summ)
    out["bookgain_by_ret20_q"] = H.assign(q=pd.qcut(H["ret20"], 4, labels=False)).groupby("q")["gain"].apply(summ)
    out["held_share_all"] = float((B["postRebalance_current_allocation"].abs() > 0).mean())
    out["held_share_nosig_bars"] = float((B.loc[~B["sig"], "postRebalance_current_allocation"].abs() > 0).mean())
    out["gain_sig_vs_nosig_held"] = H.groupby("sig")["gain"].apply(summ).unstack()
    return out
