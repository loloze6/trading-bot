def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book-level: gross vs fees
    rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = b["close"].shift(-1) / b["close"] - 1
            gross = (pos * r1).sum()
            turn = (b["postRebalance_current_allocation"].fillna(0) - b["previous_allocation"].fillna(0)).abs().sum()
            rows.append(dict(coin=coin, w=w, gross=gross, turnover=turn, bars=len(b),
                             share_in=(pos.abs() > 0).mean(), mean_abs_pos=pos.abs().mean()))
    g = pd.DataFrame(rows)
    out["gross_and_turnover_by_coin"] = g.groupby("coin")[["gross", "turnover", "bars", "share_in", "mean_abs_pos"]].agg(
        {"gross": "sum", "turnover": "sum", "bars": "sum", "share_in": "mean", "mean_abs_pos": "mean"})
    out["est_fee_drag_total_at_0.0011_per_roundtrip"] = float(g["turnover"].sum() * 0.00055)
    out["gross_total_summed"] = float(g["gross"].sum())

    # event study: hour's return in typical moves (720-bar mean abs), volume ratio (720-bar mean vol)
    ev = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            c = b["close"].astype(float)
            r = c.pct_change()
            typ = r.abs().rolling(720, min_periods=240).mean()
            z = r / typ
            vr = b["volume"] / b["volume"].rolling(720, min_periods=240).mean()
            f3 = c.shift(-3) / c - 1
            f6 = c.shift(-6) / c - 1
            f1 = c.shift(-1) / c - 1
            hr = pd.to_datetime(b["timestamp"]).dt.hour
            yr = pd.to_datetime(b["timestamp"]).dt.year
            d = pd.DataFrame(dict(coin=coin, w=w, z=z, vr=vr, f1=f1, f3=f3, f6=f6, hr=hr, yr=yr,
                                  fc=b["forecast"]))
            ev.append(d)
    E = pd.concat(ev).dropna(subset=["z", "vr", "f3"])
    drift3 = E["f3"].mean()
    E["zbin"] = pd.cut(E["z"], [-np.inf, -6, -4, -3, -2, -1.5, -1, 0, 1, 1.5, 2, 3, 4, 6, np.inf])
    def agg(x):
        return pd.Series(dict(n=len(x), f1=x.f1.mean(), f3=x.f3.mean(), f6=x.f6.mean(),
                              t3=x.f3.mean() / (x.f3.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out["fwd_by_hour_z_in_typical_moves"] = E.groupby("zbin", observed=True).apply(agg)
    D = E[E["z"] < -2].copy()
    D["vbin"] = pd.qcut(D["vr"], 4, labels=["v1low", "v2", "v3", "v4high"])
    out["falls_below_-2_by_volume_quartile"] = D.groupby("vbin", observed=True).apply(agg)
    U = E[E["z"] > 2].copy()
    U["vbin"] = pd.qcut(U["vr"], 4, labels=["v1low", "v2", "v3", "v4high"])
    out["rises_above_+2_by_volume_quartile"] = U.groupby("vbin", observed=True).apply(agg)
    out["share_bars_forecast_pos"] = float((E["fc"] > 0).mean())
    out["falls_below_-2_by_year"] = D.groupby("yr").apply(agg)
    return out
