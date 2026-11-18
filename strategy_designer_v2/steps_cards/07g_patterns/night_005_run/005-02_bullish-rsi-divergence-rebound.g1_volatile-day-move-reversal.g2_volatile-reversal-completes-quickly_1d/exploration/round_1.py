def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            mad = r1.abs().shift(1).rolling(60, min_periods=20).mean()
            z = r1 / mad
            vol20 = r1.rolling(20).std()
            vrank = vol20.rolling(100, min_periods=50).apply(lambda x: (x[:-1] < x[-1]).mean() if len(x) > 1 else np.nan, raw=True)
            r5 = c / c.shift(5) - 1
            ts = pd.to_datetime(b["timestamp"])
            for h in (1, 3, 7):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b), h):
                    if pd.isna(fwd.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, z=z.iloc[i], vr=vrank.iloc[i],
                                     reg=b["regime"].iloc[i], fwd=fwd.iloc[i], r5=r5.iloc[i],
                                     wd=ts.iloc[i].dayofweek, r1=r1.iloc[i]))
    df = pd.DataFrame(rows)
    mean_h = df.groupby(["coin", "h"])["fwd"].mean().rename("mh")
    df = df.join(mean_h, on=["coin", "h"])
    df["ex"] = df["fwd"] - df["mh"]
    df = df.dropna(subset=["z", "vr"])
    df["zb"] = pd.cut(df["z"], [-np.inf, -2, -1, -0.5, 0.5, 1, 2, np.inf])
    df["volhi"] = df["vr"] >= 0.8
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g["ex"].mean(),
                          "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    out["fwd_ex_by_zbin_volhi_h"] = df.groupby(["h", "volhi", "zb"], observed=True).apply(summ).round(4)
    # 5-day return quintile vs next 3/7 days by vol regime
    d3 = df[df.h.isin([3, 7])].dropna(subset=["r5"]).copy()
    d3["r5q"] = d3.groupby(["coin", "h"])["r5"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["fwd_ex_by_r5q"] = d3.groupby(["h", "volhi", "r5q"]).apply(summ).round(4)
    # weekday on daily returns
    d1 = df[df.h == 1]
    out["weekday_next1d"] = d1.groupby("wd").apply(summ).round(4)
    # book
    drows = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            drows.append(d)
    D = pd.concat(drows)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std", "count"]).round(5)
    out["book_by_weekday"] = D.groupby("wd")["book_return"].agg(["mean", "count"]).round(5)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades_by_side"] = T.groupby(["coin", "side"]).agg(n=("net_profit_loss_percent", "size"),
        mean_pl=("net_profit_loss_percent", "mean"), med_dur=("dur_d", "median"),
        win=("net_profit_loss_percent", lambda x: (x > 0).mean())).round(3)
    T["durb"] = pd.cut(T["dur_d"], [0, 1.5, 3.5, 7.5, 1000])
    out["trades_by_dur"] = T.groupby("durb", observed=True)["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
    return out
