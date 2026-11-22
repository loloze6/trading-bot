def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            f = b["forecast"].astype(float).fillna(0)
            pos = b["postRebalance_current_allocation"].astype(float).fillna(0)
            nxt = c.shift(-1) / c - 1
            ret90 = c / c.shift(90) - 1
            ret30 = c / c.shift(30) - 1
            sig = (f < -2) & (f.shift(1).fillna(0) >= -2)
            idx = np.arange(len(b))
            last = pd.Series(np.where(sig.values, idx, np.nan)).ffill().values
            since = idx - last
            bars.append(pd.DataFrame({"coin": coin, "w": w, "pos": pos, "nxt": nxt,
                                      "since": since, "ret90": ret90, "ret30": ret30,
                                      "fneg": f < 0,
                                      "year": pd.to_datetime(b["timestamp"]).dt.year}))
    B = pd.concat(bars, ignore_index=True)
    drift = B.groupby("coin")["nxt"].mean()
    B["drift"] = B["coin"].map(drift)
    B["gain"] = B["pos"] * B["nxt"]
    B["mkt"] = B["pos"] * B["drift"]
    S = B[B["pos"] < 0].dropna(subset=["nxt"]).copy()
    out["short_bars_total"] = pd.Series({"n": len(S), "gain_mean": S["gain"].mean(),
                                         "mkt_part": S["mkt"].mean(),
                                         "timing": (S["gain"] - S["mkt"]).mean(),
                                         "share_forecast_neg": S["fneg"].mean()})
    S["since_b"] = pd.cut(S["since"], [-1, 4, 9, 19, 10000], labels=["0-4", "5-9", "10-19", "20+"])
    def agg(g):
        x = g["gain"]
        return pd.Series({"n": len(g), "gain": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))),
                          "timing": (g["gain"] - g["mkt"]).mean(), "sum_gain": x.sum()})
    out["short_by_days_since_signal"] = S.groupby("since_b").apply(agg)
    S["q90"] = pd.cut(S["ret90"], [-1, -0.43, -0.27, -0.13, 0, 10])
    out["short_by_ret90"] = S.groupby("q90").apply(agg)
    S["q30"] = pd.cut(S["ret30"], [-1, -0.23, -0.12, 0, 10])
    out["short_by_ret30"] = S.groupby("q30").apply(agg)
    out["short_by_year"] = S.groupby("year").apply(agg)
    # daily book: worst 5% days, what share from short positions
    return out
