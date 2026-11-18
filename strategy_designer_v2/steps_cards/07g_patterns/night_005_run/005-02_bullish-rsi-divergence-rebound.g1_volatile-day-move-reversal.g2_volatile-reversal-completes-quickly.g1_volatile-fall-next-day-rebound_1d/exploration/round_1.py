import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            mad = r.abs().rolling(60, min_periods=20).mean().shift(1)
            z = r / mad
            vol20 = r.rolling(20, min_periods=10).std()
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "r": r, "z": z,
                "nx1": c.shift(-1)/c - 1,
                "nx3": c.shift(-3)/c - 1,
                "nx5": c.shift(-5)/c - 1,
                "r5": c/c.shift(5) - 1,
                "r20": c/c.shift(20) - 1,
                "vol20": vol20,
                "regime": b["regime"].values,
                "fc": b["forecast"].astype(float).values,
                "pos": b["postRebalance_current_allocation"].astype(float).values,
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek.values,
                "yr": pd.to_datetime(b["timestamp"]).dt.year.values,
                "range": ((b["high"]-b["low"])/c).values,
                "clv": ((c-b["low"])/(b["high"]-b["low"])).values,
                "pos_in_w": np.arange(len(b)),
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    mean_coin = D.groupby("coin")["nx1"].mean()
    D["ex1"] = D["nx1"] - D["coin"].map(mean_coin)
    D["mr"] = (D["regime"] == "mean_reversion")
    D["zb"] = pd.cut(D["z"], [-np.inf, -2, -1.2, -0.6, 0, 0.6, 1.2, 2, np.inf])

    def agg(g, col="ex1"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out["nextday_by_zbin_regime"] = D.groupby(["mr", "zb"], observed=True).apply(agg).round(4)
    out["regime_counts"] = D["regime"].value_counts()
    # close location in bar
    D["clvb"] = pd.cut(D["clv"], [0, .2, .4, .6, .8, 1.0], include_lowest=True)
    out["nextday_by_closeloc"] = D.groupby(["mr", "clvb"], observed=True).apply(agg).round(4)
    # 20-day return grade
    D["r20q"] = pd.qcut(D["r20"], 5)
    out["nextday_by_r20q"] = D.groupby("r20q", observed=True).apply(agg).round(4)
    # range relative
    D["rngq"] = D.groupby("coin")["range"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["nextday_by_rangeq"] = D.groupby("rngq").apply(agg).round(4)
    out["nextday_by_weekday"] = D.groupby("wd").apply(agg).round(4)
    out["nextday_by_year"] = D.groupby("yr").apply(agg).round(4)
    # 5-day non overlapping grid: r5 -> nx5
    G = D[D["pos_in_w"] % 5 == 0].copy()
    G["ex5"] = G["nx5"] - G["coin"].map(D.groupby("coin")["nx5"].mean())
    G["r5q"] = pd.qcut(G["r5"], 5)
    out["next5_by_r5q_grid"] = G.groupby("r5q", observed=True).apply(lambda g: agg(g, "ex5")).round(4)
    # book
    days = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w; days.append(dd)
    DD = pd.concat(days, ignore_index=True)
    DD["wd"] = pd.to_datetime(DD["day"]).dt.dayofweek
    daily_book = DD.groupby(["w", "day"])["book_return"].mean().dropna()
    daily_hold = DD.groupby(["w", "day"])["coin_return"].mean().dropna()
    out["book_stats"] = pd.Series({"book_mean": daily_book.mean(), "book_sd": daily_book.std(),
                                   "hold_mean": daily_hold.mean(), "hold_sd": daily_hold.std(),
                                   "share_days_in": (D["pos"].abs() > 1e-6).mean(),
                                   "mean_pos_when_in": D.loc[D["pos"].abs() > 1e-6, "pos"].mean()})
    # gain decomposition
    D["g"] = D["pos"] * D["nx1"]
    D["mkt"] = D["pos"] * D["coin"].map(mean_coin)
    out["gain_decomp_by_coin"] = D.groupby("coin")[["g", "mkt"]].mean().assign(timing=lambda x: x.g - x.mkt)
    out["book_gain_by_regime"] = D.groupby("mr")["g"].agg(["count", "mean", "sum"])
    # trades
    T = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            tt = t.copy(); tt["coin"] = coin; T.append(tt)
    T = pd.concat(T, ignore_index=True)
    T["days"] = T["duration_minutes"]/1440
    out["trades"] = T.groupby("coin").agg(n=("days", "size"), med_days=("days", "median"),
                                          mean_pl=("profit_loss_percent", "mean"),
                                          mean_net=("net_profit_loss_percent", "mean"),
                                          win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
    return out
