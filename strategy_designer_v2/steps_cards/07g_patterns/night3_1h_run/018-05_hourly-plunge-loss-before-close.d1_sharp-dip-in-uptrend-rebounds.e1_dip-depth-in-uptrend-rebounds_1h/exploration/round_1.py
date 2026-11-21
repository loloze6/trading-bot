def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    H = {24: [], 72: [], 144: [], 240: []}
    for coin, wins in bars.items():
        recs = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            ma = r24.abs().rolling(720, min_periods=360).mean()
            z = r24 / ma
            r720 = c / c.shift(720) - 1
            r168 = c / c.shift(168) - 1
            vol = c.pct_change().rolling(720, min_periods=360).std()
            for h in (24, 72, 144, 240):
                idx = np.arange(0, len(c) - h, h)
                fr = (c.shift(-h) / c - 1).iloc[idx]
                recs.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "fr": fr.values,
                                          "z": z.iloc[idx].values, "r720": r720.iloc[idx].values,
                                          "r168": r168.iloc[idx].values, "vol": vol.iloc[idx].values,
                                          "hour": ts.iloc[idx].dt.hour.values,
                                          "wd": ts.iloc[idx].dt.weekday.values}))
        d = pd.concat(recs)
        for h in (24, 72, 144, 240):
            m = d["h"] == h
            mu = d.loc[m, "fr"].mean(); sd = d.loc[m, "fr"].std()
            d.loc[m, "u"] = d.loc[m, "fr"] - mu
            d.loc[m, "s"] = (d.loc[m, "fr"] - mu) / sd
        rows.append(d)
    A = pd.concat(rows).dropna(subset=["fr", "z", "r720"])
    A["zb"] = pd.cut(A["z"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    A["up"] = np.where(A["r720"] > 0, "up30", "down30")
    def agg(g):
        n = len(g); m = g["u"].mean(); t = m / (g["u"].std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean_u": round(m, 4), "t": round(t, 2), "strength": round(g["s"].mean(), 3)})
    out = {}
    for h in (24, 72, 144, 240):
        out[f"h{h}_by_z_regime"] = A[A.h == h].groupby(["up", "zb"], observed=True).apply(agg)
    a72 = A[A.h == 72].copy()
    a72["volq"] = a72.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=["lo", "mid", "hi"]))
    dip = a72[(a72.z < -1)]
    out["dip_by_regime_vol"] = dip.groupby(["up", "volq"], observed=True).apply(agg)
    a72["wb"] = pd.qcut(a72["r168"], 5)
    out["h72_by_7d_return_regime"] = a72.groupby(["up", "wb"], observed=True).apply(agg)
    out["dip_by_coin"] = dip[dip.up == "up30"].groupby("coin").apply(agg)
    # book
    dd = []
    for coin, wins in days.items():
        for w, df in wins.items():
            dd.append(df.assign(coin=coin, w=w))
    D = pd.concat(dd).dropna(subset=["book_return"])
    D["absb"] = D["book_return"].abs()
    out["book_by_window_sum"] = D.groupby("w")["book_return"].agg(["mean", "count"]).round(5).T
    q = D["book_return"].quantile([0.01, 0.99])
    out["book_tail_share"] = pd.Series({"sum_all": D.book_return.sum(),
                                        "sum_top1pct": D.book_return[D.book_return > q[0.99]].sum(),
                                        "sum_bot1pct": D.book_return[D.book_return < q[0.01]].sum()})
    return out
