def explore(data):
    import pandas as pd, numpy as np
    out = {}
    cr = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["s"] = np.log(b["close"]).diff().rolling(30).std()
            b["width"] = (b["high"] - b["low"]) / b["close"] / b["s"]
            b["r5s"] = (b["close"] / b["close"].shift(5) - 1) / (b["s"] * np.sqrt(5))
            b["a"] = b["postRebalance_current_allocation"]
            b["pa"] = b["previous_allocation"]
            b["coin"] = c; b["wn"] = int(w[1:])
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            cr.append(b)
    X = pd.concat(cr, ignore_index=True)
    X["nxt"] = X["nxt"].fillna(0)
    def book(mask_keep):
        a = X["a"].where(mask_keep, 0.0)
        # fees on entering and leaving: approx 0.0011 per unit changed
        g = X[["coin", "wn", "day"]].copy()
        g["a"] = a
        g["chg"] = g.groupby(["coin", "wn"])["a"].diff().abs().fillna(g["a"].abs())
        g["r"] = g["a"] * X["nxt"] - g["chg"] * 0.0011
        d = g.groupby(["wn", "day"])["r"].mean().sort_index()
        v = (1 + d).cumprod(); dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(d)) - 1
        sh = d.mean() / d.std() * np.sqrt(365)
        return pd.Series({"yearly": yr, "maxdd": dd, "calmar": yr / -dd, "sharpe": sh, "n_pos": int((a.abs() > 1e-9).sum())})
    inpos = X["a"].abs() > 1e-9
    side = np.sign(X["a"])
    res = {}
    res["all"] = book(inpos)
    res["long_only"] = book(inpos & (side > 0))
    res["short_only"] = book(inpos & (side < 0))
    res["no_short_against5"] = book(inpos & ~((side < 0) & (X["r5s"] < 0)))
    res["short_only_r5neg_removed"] = book(inpos & (side < 0) & (X["r5s"] >= 0))
    out["books"] = pd.DataFrame(res).T
    # condition alone check for long side: profile bars, low-close? next-day ex by r5s sign, no position
    drift = X.groupby("coin")["nxt"].mean()
    X["ex"] = X["nxt"] - X["coin"].map(drift)
    P = X[X["regime"] == "unknown"]
    out["prof_long_vs_nolong_ex"] = P.groupby(np.where(P["a"] > 1e-9, "long", np.where(P["a"] < -1e-9, "short", "flat")))["ex"].agg(["size", "mean"])
    return out
