def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["win"] = w
            tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["year"] = pd.to_datetime(T["entry_time"]).dt.year
    T["days_held"] = T["duration_minutes"] / 1440
    T["fbin"] = pd.cut(T["entry_forecast"], [-0.1, 2, 5, 10, 15, 19.99, 20.1])
    def agg(g):
        return pd.Series({"n": len(g), "gross_mean": g["profit_loss_percent"].mean(),
                          "net_mean": g["net_profit_loss_percent"].mean(),
                          "comm_mean": g["total_commission"].mean(),
                          "days_held": g["days_held"].mean(),
                          "win_gross": (g["profit_loss_percent"] > 0).mean()})
    out["trades_all"] = agg(T).to_frame().T
    out["trades_by_side"] = T.groupby("side").apply(agg)
    out["trades_by_fbin"] = T.groupby("fbin").apply(agg)
    out["trades_by_coin"] = T.groupby("coin").apply(agg)
    out["trades_by_year"] = T.groupby("year").apply(agg)
    out["days_held_quantiles"] = T["days_held"].describe()
    # event study, non-overlapping
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            r1 = pd.Series(cl).pct_change()
            vol = r1.abs().rolling(20).mean().shift(1)
            mom20 = pd.Series(cl).pct_change(20)
            ma50 = pd.Series(cl).rolling(50).mean()
            f = b["forecast"].fillna(0).values
            n = len(b); last = -99
            for i in range(n - 5):
                if f[i] >= 5 and i - last > 5:
                    last = i
                    rows.append({"coin": c, "win": w, "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 "f": f[i], "r5": cl[i+5]/cl[i]-1, "r1": cl[i+1]/cl[i]-1,
                                 "r10": (cl[i+10]/cl[i]-1) if i+10 < n else np.nan,
                                 "vol": vol.iloc[i], "mom20": mom20.iloc[i],
                                 "abovema": (cl[i] > ma50.iloc[i]) if not np.isnan(ma50.iloc[i]) else np.nan,
                                 "dayret": r1.iloc[i]})
    E = pd.DataFrame(rows)
    def es(g, col="r5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan,
                          "hit": (x > 0).mean()})
    E["fb"] = pd.cut(E["f"], [4.99, 10, 19.99, 20.1])
    out["ev_r5_by_f"] = E.groupby("fb").apply(es)
    out["ev_r1_by_f"] = E.groupby("fb").apply(lambda g: es(g, "r1"))
    out["ev_r10_by_f"] = E.groupby("fb").apply(lambda g: es(g, "r10"))
    E["volq"] = E.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=["lowvol","mid","highvol"]))
    out["ev_r5_by_vol"] = E.groupby("volq").apply(es)
    E["momsign"] = np.where(E["mom20"] > 0, "up20", "down20")
    out["ev_r5_by_mom"] = E.groupby("momsign").apply(es)
    out["ev_r5_by_ma50"] = E.groupby("abovema").apply(es)
    out["ev_r5_by_coin"] = E.groupby("coin").apply(es)
    out["ev_r5_by_year"] = E.groupby("year").apply(es)
    return out
