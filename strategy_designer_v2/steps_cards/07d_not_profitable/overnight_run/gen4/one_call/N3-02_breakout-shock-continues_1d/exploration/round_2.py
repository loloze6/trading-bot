def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; f = b["forecast"].values
            ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(cl).pct_change()
            vol = r1.rolling(20, min_periods=10).std().values
            mom = pd.Series(cl).pct_change(20).values
            n = len(cl); last = -100
            for i in range(1, n):
                if f[i] > 0 and i - last >= 10:
                    last = i
                    r = {"coin": c, "fc": f[i], "vol": vol[i], "mom": mom[i], "year": ts.iloc[i].year}
                    for h in [1, 5, 10]:
                        r[f"r{h}"] = cl[i + h] / cl[i] - 1 if i + h < n else np.nan
                    # exit after 1 day: return from i+1 to i+11 when forecast at i+1 is 0
                    if i + 11 < n and f[i + 1] == 0:
                        r["after_exit10"] = cl[i + 11] / cl[i + 1] - 1
                    else:
                        r["after_exit10"] = np.nan
                    rows.append(r)
    R = pd.DataFrame(rows)
    def st(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan})
    out["sep10_overall"] = pd.DataFrame({k: st(R[k]) for k in ["r1", "r5", "r10", "after_exit10"]}).T
    out["share_exit_next_day"] = float(R.after_exit10.notna().mean())
    R["volq"] = R.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=["low", "mid", "high"]))
    out["r10_by_vol"] = R.groupby("volq")["r10"].apply(st).unstack()
    R["momq"] = pd.cut(R.mom, [-10, 0.1, 0.25, 0.5, 100])
    out["r10_by_mom20"] = R.groupby("momq")["r10"].apply(st).unstack()
    R["fcq"] = pd.cut(R.fc, [0, 10, 19.99, 20.01])
    out["r10_by_fc"] = R.groupby("fcq")["r10"].apply(st).unstack()
    out["r10_by_year"] = R.groupby("year")["r10"].apply(st).unstack()
    out["r10_by_coin"] = R.groupby("coin")["r10"].apply(st).unstack()
    return out
