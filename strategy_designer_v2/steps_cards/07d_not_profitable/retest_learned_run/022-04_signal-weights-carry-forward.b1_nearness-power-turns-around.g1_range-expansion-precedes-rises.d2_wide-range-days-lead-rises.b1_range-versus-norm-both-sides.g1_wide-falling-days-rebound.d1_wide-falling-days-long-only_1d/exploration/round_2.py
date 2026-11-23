def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["days"].keys())
    wins = sorted(data["days"][coins[0]].keys(), key=lambda w: int(w[1:]))
    H = 3
    # condition-alone vs with-signal on 3-bar grid
    grid = []
    for c in coins:
        allr = []
        for w in wins:
            b = data["bars"][c].get(w)
            if b is None: continue
            cl = b["close"].values
            idx = np.arange(0, len(cl) - H, H)
            allr.append(cl[idx + H] / cl[idx] - 1)
        drift = np.concatenate(allr).mean()
        for w in wins:
            b = data["bars"][c].get(w)
            if b is None: continue
            b = b.reset_index(drop=True)
            cl = b["close"]
            ma50 = cl / cl.rolling(50, min_periods=20).mean() - 1
            r30 = cl / cl.shift(30) - 1
            down = cl.pct_change() < 0
            f = b["forecast"].fillna(0)
            fwd = cl.shift(-H) / cl - 1
            for t in range(0, len(b) - H, H):
                grid.append({"coin": c, "w": w, "u": fwd[t] - drift, "ma50": ma50[t], "r30": r30[t],
                             "sig": f[t] >= 2, "down": bool(down[t])})
    G = pd.DataFrame(grid).dropna()
    G["up"] = G["ma50"] > 0
    def agg(x):
        return pd.Series({"n": len(x), "mean_u": x["u"].mean(), "t": x["u"].mean() / x["u"].std() * np.sqrt(len(x))})
    out["grid_by_up_sig"] = G.groupby(["up", "sig"]).apply(agg)
    out["grid_by_up_down_nosig"] = G[~G["sig"]].groupby(["up", "down"]).apply(agg)
    # book contributions by coin state; filtered book
    rows = []
    for w in wins:
        per = []
        for c in coins:
            b = data["bars"][c].get(w); d = data["days"][c].get(w)
            if b is None or d is None: continue
            b = b.reset_index(drop=True)
            cl = b["close"]
            ma50 = (cl / cl.rolling(50, min_periods=20).mean() - 1).shift(1)  # known at prior close
            r30 = (cl / cl.shift(30) - 1).shift(1)
            alloc_prev = b["postRebalance_current_allocation"].shift(1).fillna(0)
            x = pd.DataFrame({"br": d["book_return"].values, "ma50": ma50.values, "r30": r30.values,
                              "pos": alloc_prev.values, "cr": d["coin_return"].values})
            x["coin"] = c; x["w"] = w; x["i"] = np.arange(len(x))
            per.append(x)
        rows.append(pd.concat(per))
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["br"])
    D["inpos"] = D["pos"].abs() > 1e-9
    D["state"] = np.where(D["ma50"] > 0, "above_ma50", np.where(D["ma50"] <= 0, "below_ma50", "na"))
    out["book_by_state_inpos"] = D[D["inpos"]].groupby("state").agg(n=("br", "size"), mean=("br", "mean"),
                                                                   std=("br", "std"), sum=("br", "sum"))
    def book_stats(col):
        bk = D.groupby(["w", "i"])[col].mean().reset_index()
        bk["wn"] = bk["w"].str[1:].astype(int)
        bk = bk.sort_values(["wn", "i"])
        r = bk[col].values
        v = np.cumprod(1 + r)
        dd = (v / np.maximum.accumulate(v) - 1).min()
        yr = v[-1] ** (365 / len(r)) - 1
        sh = r.mean() / r.std() * np.sqrt(365)
        return {"sharpe": sh, "yearly": yr, "maxdd": dd, "calmar": yr / -dd}
    D["br_f"] = np.where(D["ma50"] <= 0, 0.0, D["br"])
    D["br_r30"] = np.where(D["r30"] <= 0, 0.0, D["br"])
    out["book_orig"] = pd.Series(book_stats("br"))
    out["book_only_above_ma50"] = pd.Series(book_stats("br_f"))
    out["book_only_r30_pos"] = pd.Series(book_stats("br_r30"))
    # year of ma50 effect for cases
    return out
