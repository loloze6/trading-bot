def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r = pd.Series(c).pct_change()
            sd = r.rolling(20, min_periods=20).std().shift(1)
            z = r / sd
            vol20 = r.rolling(20, min_periods=20).std()
            ret5p = pd.Series(c).pct_change(5)
            ret20p = pd.Series(c).pct_change(20)
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(n), "z": z, "vol": vol20,
                               "reg": b["regime"].values, "ret5p": ret5p, "ret20p": ret20p,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
                               "r": r, "pos": b["postRebalance_current_allocation"].values})
            for h in (1, 5, 20):
                f = np.full(n, np.nan)
                f[:n-h] = c[h:] / c[:n-h] - 1
                df[f"f{h}"] = f
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["down"] = (A["reg"] == "mean_reversion")
    # coin drifts (non-overlapping)
    drift = {}
    for h in (5, 20):
        g = A[(A["i"] % h == 0)]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
    def cases(mask, h):
        # first event bar in each grid cell of h
        S = A[mask & A[f"f{h}"].notna()].copy()
        S["cell"] = S["i"] // h
        S = S.groupby(["coin", "w", "cell"]).head(1)
        S["u"] = S[f"f{h}"] - S["coin"].map(drift[h])
        return S
    def summ(S, col="u"):
        x = S[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    # 1. z buckets x regime, 20d and 5d
    res = []
    bins = [(-99, -2), (-2, -1), (-1, 0), (0, 1), (1, 2), (2, 99)]
    for h in (5, 20):
        for lo, hi in bins:
            for d in (False, True):
                S = cases((A["z"] >= lo) & (A["z"] < hi) & (A["down"] == d), h)
                s = summ(S); s["h"] = h; s["zbin"] = f"{lo},{hi}"; s["down90"] = d
                res.append(s)
    out["z_by_regime_unusual"] = pd.DataFrame(res)
    # 2. regime alone (grid bars)
    res = []
    for h in (5, 20):
        for d in (False, True):
            S = cases(A["down"] == d, h)
            s = summ(S); s["h"] = h; s["down90"] = d; res.append(s)
    out["regime_alone"] = pd.DataFrame(res)
    # 3. past 20d return quintile -> next 20d (within coin quintiles)
    A["q20"] = A.groupby("coin")["ret20p"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    A["qv"] = A.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    A["q5"] = A.groupby("coin")["ret5p"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    res = []
    for q in range(5):
        for h in (5, 20):
            S = cases(A["q20"] == q, h); s = summ(S); s["q"] = q; s["h"] = h; s["by"] = "ret20"; res.append(s)
            S = cases(A["q5"] == q, h); s = summ(S); s["q"] = q; s["h"] = h; s["by"] = "ret5"; res.append(s)
    for q in range(3):
        for h in (5, 20):
            S = cases(A["qv"] == q, h); s = summ(S); s["q"] = q; s["h"] = h; s["by"] = "vol"; res.append(s)
    out["quantiles"] = pd.DataFrame(res)
    # 4. weekday daily return
    out["weekday"] = A.groupby("wd")["f1"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    # 5. book by regime / position sign
    A["bk"] = A["pos"] * A["f1"]
    A["side"] = np.sign(A["pos"].fillna(0))
    out["book_by_side_regime"] = A.groupby(["down", "side"])["bk"].agg(["count", "mean", "sum"])
    # 6. book daily returns by window and coin
    D = []
    for coin in days:
        for w, d in days[coin].items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D, ignore_index=True)
    bw = D.groupby("w")[["book_return", "coin_return"]].sum()
    out["book_sum_by_window"] = bw
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean"])
    # 7. trades
    T = []
    for coin in data["trades"]:
        for w, t in data["trades"][coin].items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T, ignore_index=True)
    out["trades"] = T.groupby(["side"])["net_profit_loss_percent"].agg(["count", "mean", "median", lambda x: (x > 0).mean()])
    out["trades_coin_side"] = T.groupby(["coin", "side"])["net_profit_loss_percent"].agg(["count", "mean"])
    return out
