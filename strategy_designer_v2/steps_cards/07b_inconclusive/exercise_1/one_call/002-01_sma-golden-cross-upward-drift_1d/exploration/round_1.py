def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].fillna(0).values
            raw = b["debug_info.components.sma_cross.last_history_value"].values
            n = len(b)
            # days since raw spread turned positive (within window)
            since = np.full(n, np.nan); cnt = np.nan
            for i in range(n):
                if np.isnan(raw[i]): cnt = np.nan
                elif raw[i] > 0:
                    if i > 0 and not np.isnan(raw[i-1]) and raw[i-1] <= 0: cnt = 0
                    elif not np.isnan(cnt): cnt += 1
                else: cnt = np.nan
                since[i] = cnt
            lr = np.log(c)
            for i in range(0, n - 10, 10):
                past20 = lr[i] - lr[i-20] if i >= 20 else np.nan
                vol20 = np.std(np.diff(lr[max(0,i-20):i+1])) if i >= 5 else np.nan
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 f=f[i], raw=raw[i], since=since[i],
                                 fwd=c[i+10]/c[i]-1, past20=past20, vol=vol20))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d["pos"] = (d.fwd > 0).astype(float) - d.groupby("coin")["fwd"].transform(lambda x: (x > 0).mean())
    def summ(g):
        s = g["ex"]
        return pd.Series({"n": len(s), "mean_ex": s.mean(), "t": s.mean()/s.std()*np.sqrt(len(s)) if len(s) > 2 else np.nan,
                          "pos_minus": g["pos"].mean(), "sd": s.std()})
    out = {}
    d["fb"] = pd.cut(d.f, [-0.1, 0, 5, 10, 15, 20.1], labels=["0", "0-5", "5-10", "10-15", "15-20"])
    out["by_forecast"] = d.groupby("fb").apply(summ)
    a = d[d.f > 0]
    out["active_by_coin"] = a.groupby("coin").apply(summ)
    out["flat_by_coin"] = d[d.f == 0].groupby("coin").apply(summ)
    out["active_by_year"] = a.groupby("year").apply(summ)
    out["all_by_year"] = d.groupby("year").apply(summ)
    a2 = d[d.raw > 0].copy()
    a2["sb"] = pd.cut(a2.since, [-1, 20, 60, 120, 10000])
    out["by_days_since_cross"] = a2.groupby("sb").apply(summ)
    a2["rawq"] = pd.qcut(a2.raw, 5, duplicates="drop")
    out["by_raw_spread_q"] = a2.groupby("rawq").apply(summ)
    a["p20"] = np.sign(a.past20)
    out["active_by_past20_sign"] = a.groupby("p20").apply(summ)
    a["vq"] = pd.qcut(a.vol, 3, labels=["lowvol", "mid", "hivol"])
    out["active_by_vol"] = a.groupby("vq").apply(summ)
    d["p20"] = np.sign(d.past20)
    out["all_by_past20_sign"] = d.groupby("p20").apply(summ)
    return out
