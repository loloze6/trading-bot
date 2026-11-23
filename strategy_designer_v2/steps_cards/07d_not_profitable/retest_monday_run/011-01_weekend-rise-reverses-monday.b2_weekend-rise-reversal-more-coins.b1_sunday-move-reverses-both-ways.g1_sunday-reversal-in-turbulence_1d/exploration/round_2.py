def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"]; r1 = cl.pct_change()
            nxt = cl.shift(-1) / cl - 1
            a = b["postRebalance_current_allocation"].fillna(0)
            vr = r1.rolling(20).std() / r1.rolling(60).std()
            r20 = cl / cl.shift(20) - 1
            # sunday that opened the current position: carry forward the Sunday state
            sun = ts.dt.weekday == 6
            sun_r1 = r1.where(sun).ffill(limit=2)
            sun_vr = vr.where(sun).ffill(limit=2)
            sun_tr = (np.sign(r1) == np.sign(r20 - r1)).where(sun).ffill(limit=2)
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            df = pd.DataFrame({"coin": c, "w": w, "day": ts.dt.floor("D"), "g": a * nxt - fee.shift(-1).fillna(0) * 0,
                               "fee": fee, "a": a, "sr": sun_r1, "svr": sun_vr, "str": sun_tr})
            rows.append(df)
    X = pd.concat(rows).dropna(subset=["g"])
    X["wn"] = X.w.str[1:].astype(int)
    out = {}
    def book(mask, feeuse=True):
        g = X.g.where(mask, 0) - (X.fee.where(mask.shift(1, fill_value=False) | mask, 0) if feeuse else 0)
        d = X.assign(gg=g).groupby(["wn", "coin", "day"]).gg.sum().groupby(["wn", "day"]).mean().sort_index()
        v = (1 + d).cumprod(); dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(d)) - 1
        return pd.Series({"mean": d.mean(), "sharpe": d.mean() / d.std() * np.sqrt(365), "yearly": yr, "maxdd": dd, "calmar": yr / -dd})
    allm = X.a != 0
    out["books"] = pd.DataFrame({
        "all": book(allm),
        "short_only": book(X.a < 0),
        "long_only": book(X.a > 0),
        "short+long_with_trend": book((X.a < 0) | ((X.a > 0) & (X["str"] == 1))),
        "vr_top40pct": book(allm & (X.svr > X.svr.quantile(0.6))),
    }).T
    # long side gains by vr
    L = X[(X.a > 0)]; S_ = X[X.a < 0]
    out["long_gain_by_trend"] = L.groupby("str").g.agg(["count", "mean"])
    out["short_gain_by_trend"] = S_.groupby("str").g.agg(["count", "mean"])
    return out
