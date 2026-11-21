def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            dist = b.get("debug_info.components.beyond_high.last_history_value")
            pp = b.get("debug_info.components.beyond_high.post_pipeline_value")
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            past20 = c / c.shift(20) - 1
            past5 = c / c.shift(5) - 1
            lo60 = c.rolling(60, min_periods=60).min().shift(1)
            dlow = (c / lo60 - 1) * 100
            n = len(b)
            for h in (5, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                        fwd=c.iloc[i + h] / c.iloc[i] - 1,
                        dist=float(dist.iloc[i]) if dist is not None else np.nan,
                        pp=float(pp.iloc[i]) if pp is not None else np.nan,
                        vol=vol20.iloc[i], past20=past20.iloc[i], past5=past5.iloc[i],
                        dlow=dlow.iloc[i]))
            ts = pd.to_datetime(b["timestamp"])
            for i in range(1, n - 1):
                daily.append(dict(coin=coin, w=w, r=r1.iloc[i], nxt=r1.iloc[i + 1],
                                  wd=ts.iloc[i].dayofweek, vol=vol20.iloc[i]))
    R = pd.DataFrame(rows)
    # drift-adjust per coin & h
    R["adj"] = R["fwd"] - R.groupby(["coin", "h"])["fwd"].transform("mean")
    def summ(g):
        return pd.Series({"n": len(g), "mean_adj": g["adj"].mean(),
                          "t": g["adj"].mean() / (g["adj"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    for h in (5, 20):
        S = R[R.h == h].copy()
        S["dbin"] = pd.cut(S["dist"], [-1000, -40, -25, -15, -8, -3, 0, 5, 15, 1000])
        out[f"h{h}_by_dist90high"] = S.groupby("dbin", observed=True).apply(summ)
        S["vbin"] = S.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
        out[f"h{h}_by_volq"] = S.groupby("vbin").apply(summ)
        S["p20bin"] = S.groupby("coin")["past20"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
        out[f"h{h}_by_past20q"] = S.groupby("p20bin").apply(summ)
        S["lowbin"] = pd.cut(S["dlow"], [-1, 5, 15, 30, 60, 1e6])
        out[f"h{h}_by_dist60low"] = S.groupby("lowbin", observed=True).apply(summ)
    D = pd.DataFrame(daily).dropna()
    D["nadj"] = D["nxt"] - D.groupby("coin")["nxt"].transform("mean")
    D["z"] = D["r"] / D["vol"]
    D["zbin"] = pd.cut(D["z"], [-100, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 100])
    out["next_day_by_today_z"] = D.groupby("zbin", observed=True)["nadj"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["next_day_by_weekday"] = D.groupby("wd")["nadj"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; bk.append(d)
    B = pd.concat(bk)
    out["book_by_year"] = B.assign(y=pd.to_datetime(B["day"]).dt.year).groupby("y")[["book_return", "coin_return"]].agg(["mean", "count"])
    out["book_by_coin"] = B.groupby("coin")[["book_return", "coin_return"]].mean()
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    out["trades"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
