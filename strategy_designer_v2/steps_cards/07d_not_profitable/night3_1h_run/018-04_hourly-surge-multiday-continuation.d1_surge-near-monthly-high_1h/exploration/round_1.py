def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    wins = sorted({w for c in coins for w in data["days"][c].keys()}, key=lambda s: int(s[1:]))
    # book daily return: mean over coins per day, per window
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            if w in data["days"][c]:
                d = data["days"][c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day").agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
        g["window"] = w
        rows.append(g)
    B = pd.concat(rows, ignore_index=True).dropna(subset=["book"])
    B["eq"] = (1 + B["book"]).cumprod()
    B["peak"] = B["eq"].cummax()
    B["dd"] = B["eq"] / B["peak"] - 1
    # per-window summary
    pw = B.groupby("window", sort=False).agg(
        n=("book", "size"), book_mean=("book", "mean"), hold_mean=("hold", "mean"),
        book_tot=("book", lambda x: (1 + x).prod() - 1), hold_tot=("hold", lambda x: (1 + x).prod() - 1),
        min_dd=("dd", "min"))
    out["per_window"] = pw
    # drawdown episodes
    B["idx"] = np.arange(len(B))
    eps = []
    in_dd = False
    for i, r in B.iterrows():
        if r["dd"] < 0 and not in_dd:
            in_dd = True; start = r["idx"]
        if in_dd and r["dd"] == 0:
            seg = B.iloc[int(start):int(r["idx"])]
            eps.append((start, seg["dd"].min(), len(seg), seg["window"].iloc[0], seg["window"].iloc[-1],
                        (1 + seg["hold"]).prod() - 1))
            in_dd = False
    if in_dd:
        seg = B.iloc[int(start):]
        eps.append((start, seg["dd"].min(), len(seg), seg["window"].iloc[0], seg["window"].iloc[-1],
                    (1 + seg["hold"]).prod() - 1))
    E = pd.DataFrame(eps, columns=["start", "depth", "days", "w_from", "w_to", "hold_ret"]).sort_values("depth").head(8)
    out["deepest_falls"] = E.drop(columns="start").reset_index(drop=True)
    yrs = len(B) / 365
    out["yearly_ret"] = B["eq"].iloc[-1] ** (1 / yrs) - 1
    out["max_dd"] = B["dd"].min()
    # Deepest fall: per coin contribution (trough path from peak)
    E1 = E.iloc[0]
    k0 = int(E1["start"]); k1 = int(B.iloc[k0:][B.iloc[k0:]["dd"] == E1["depth"]].index[0])
    seg = B.loc[k0:k1]
    contrib = {}
    for c in coins:
        s = 0
        for w in seg["window"].unique():
            dd_ = data["days"][c].get(w)
            if dd_ is None: continue
            m = dd_[dd_["day"].isin(seg[seg.window == w]["day"])]
            s += m["book_return"].sum()
        contrib[c] = s / len(coins)
    out["deepest_fall_by_coin_sum"] = pd.Series(contrib)
    # Cases: per coin, signal bars (forecast rise from 0), features at entry, 120h outcome
    cs = []
    for c in coins:
        drift_l = []
        for w, b in data["bars"][c].items():
            cl = b["close"].values
            r = cl[120::120] / cl[:-120:120] - 1 if len(cl) > 120 else []
            drift_l.extend(list(r))
        drift = np.mean(drift_l)
        for w, b in data["bars"][c].items():
            cl = b["close"].values; fc = b["forecast"].fillna(0).values
            al = b["postRebalance_current_allocation"].fillna(0).values
            n = len(cl)
            s = pd.Series(cl)
            r24 = s / s.shift(24) - 1
            r720 = s / s.shift(720) - 1
            r168 = s / s.shift(168) - 1
            hi = s.rolling(720, min_periods=200).max()
            prox = s / hi - 1
            lr = np.log(s).diff()
            vol = lr.rolling(168).std() / lr.rolling(1440, min_periods=500).std()
            for g0 in range(0, n - 120, 120):
                seg = fc[g0:g0 + 120]
                idx = np.where(seg > 2)[0]
                if len(idx) == 0: continue
                t = g0 + idx[0]
                if t + 120 >= n: continue
                fwd = cl[t + 120] / cl[t] - 1
                mae = cl[t:t + 121].min() / cl[t] - 1
                cs.append(dict(coin=c, window=w, year=pd.Timestamp(b["timestamp"].iloc[t]).year,
                               fc=fc[t], alloc=al[t], unus=fwd - drift, fwd=fwd, mae=mae,
                               r24=r24[t], r168=r168[t], r720=r720[t], prox=prox[t], vol=vol[t],
                               hour=pd.Timestamp(b["timestamp"].iloc[t]).hour))
    C = pd.DataFrame(cs)
    out["n_cases"] = len(C)

    def grp(col, q=4):
        x = C.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col], q, duplicates="drop")
        g = x.groupby("b", observed=True)
        res = g.agg(n=("unus", "size"), unus=("unus", "mean"), fwd=("fwd", "mean"),
                    mae=("mae", "mean"), loss_share=("fwd", lambda v: (v < -0.1).mean()))
        res["t"] = g["unus"].apply(lambda v: v.mean() / (v.std() / np.sqrt(len(v))))
        res.index = res.index.astype(str)
        return res
    for col in ["r720", "r168", "r24", "prox", "vol", "fc"]:
        out["by_" + col] = grp(col)
    out["by_coin"] = C.groupby("coin").agg(n=("unus", "size"), unus=("unus", "mean"), mae=("mae", "mean"))
    out["by_year"] = C.groupby("year").agg(n=("unus", "size"), unus=("unus", "mean"), mae=("mae", "mean"))
    # book exposure share: average |alloc| per window
    return out
