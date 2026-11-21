def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            if len(c) < 30: continue
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(c)),
                "fc": b["forecast"].astype(float).values,
                "alloc": b["postRebalance_current_allocation"].astype(float).values,
                "r1": r1, "r5p": c / c.shift(5) - 1, "r20p": c / c.shift(20) - 1,
                "vol20": r1.rolling(20).std(),
                "near": c / c.rolling(20, min_periods=10).max() - 1,
                "wd": ts.dt.weekday,
                "f1": c.shift(-1) / c - 1, "f5": c.shift(-5) / c - 1, "f20": c.shift(-20) / c - 1,
            })
            df["vol_rel"] = df["vol20"] / df["vol20"].rolling(60, min_periods=20).median()
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # coin drift and usual move per horizon, non-overlapping
    for h in (1, 5, 20):
        g = D[D["pos"] % h == 0]
        st = g.groupby("coin")["f%d" % h].agg(["mean", "std"])
        D["u%d" % h] = (D["f%d" % h] - D["coin"].map(st["mean"])) / D["coin"].map(st["std"])
    def grade(sig, h, nq=5):
        g = D[(D["pos"] % h == 0)].dropna(subset=[sig, "u%d" % h]).copy()
        g["z"] = g.groupby("coin")[sig].transform(lambda s: (s - s.mean()) / s.std())
        g["q"] = g.groupby("coin")["z"].transform(lambda s: pd.qcut(s.rank(method="first"), nq, labels=False))
        t = g.groupby("q")["u%d" % h].agg(["mean", "count"])
        t["t"] = g.groupby("q")["u%d" % h].apply(lambda s: s.mean() / s.std() * np.sqrt(len(s)))
        x = g["z"].clip(-3, 3) * g["u%d" % h]
        t.loc["slope_t", "mean"] = x.mean() / x.std() * np.sqrt(len(x))
        t.loc["slope_t", "count"] = len(x)
        return t
    for sig in ("r1", "r5p", "r20p", "vol20", "near", "vol_rel"):
        for h in (5, 20):
            out["%s_h%d" % (sig, h)] = grade(sig, h)
    # weekday of 1-day returns (standardised)
    wd = D.dropna(subset=["u1"]).groupby("wd")["u1"]
    out["weekday_u1"] = pd.DataFrame({"mean": wd.mean(), "n": wd.count(),
                                      "t": wd.mean() / wd.std() * np.sqrt(wd.count())})
    # forecast quintile on 20 grid, by forecast sign and vol regime
    g = D[D["pos"] % 20 == 0].dropna(subset=["fc", "u20", "vol_rel"]).copy()
    g["dir_u"] = np.sign(g["fc"]) * g["u20"]
    g["volhi"] = g["vol_rel"] > 1
    g["side"] = np.sign(g["fc"])
    out["fc_by_side_vol"] = g.groupby(["side", "volhi"])["dir_u"].agg(["mean", "count"])
    # book days: largest gains/losses context
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d[["book_return", "coin_return"]].astype(float).copy()
            x["coin"] = coin
            dd.append(x)
    B = pd.concat(dd).dropna()
    B["absb"] = B["book_return"].abs()
    q = B["book_return"].quantile([0.01, 0.99])
    out["book_tails"] = pd.DataFrame({
        "loss_days_coin_ret": [B[B.book_return <= q.iloc[0]]["coin_return"].mean()],
        "gain_days_coin_ret": [B[B.book_return >= q.iloc[1]]["coin_return"].mean()],
        "n_tail": [int((B.book_return <= q.iloc[0]).sum())],
        "corr_book_coin": [B["book_return"].corr(B["coin_return"])]})
    out["book_by_coin_mean_bps"] = (B.groupby("coin")["book_return"].mean() * 1e4).round(2)
    return out
