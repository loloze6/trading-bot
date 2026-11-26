def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [10, 30]
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs)
    out = {}
    for h in H:
        rows = []
        for c, ws in bars.items():
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                cl = df["close"].values
                ts = pd.to_datetime(df["timestamp"])
                n = len(df)
                for start in range(0, n, h):
                    cell = df.iloc[start:start + h]
                    m = cell[(cell["regime"] == "mean_reversion") & (cell["forecast"] < 0)]
                    if len(m) == 0:
                        continue
                    i = m.index[0]
                    if i + h >= n:
                        continue
                    tot = cl[i + h] / cl[i] - 1
                    rows.append({"coin": c, "year": ts[i].year, "day": ts[i].normalize(),
                                 "u": -(tot - drift[(c, h)]),
                                 "past30": cl[i] / cl[i - 30] - 1 if i >= 30 else np.nan,
                                 "past10": cl[i] / cl[i - 10] - 1 if i >= 10 else np.nan})
        d = pd.DataFrame(rows)

        def clus(g):
            s = g.groupby("day")["u"].sum()
            G = len(s); N = len(g)
            if G < 3:
                return pd.Series({"n": N, "days": G, "mean": g["u"].mean(), "median": g["u"].median(), "t_day": np.nan})
            mu = g["u"].mean()
            dev = g.assign(e=g["u"] - mu).groupby("day")["e"].sum()
            se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / N
            return pd.Series({"n": N, "days": G, "mean": mu, "median": g["u"].median(),
                              "t_day": mu / se, "share>0": (g["u"] > 0).mean()})
        out[f"h{h}_all"] = clus(d).to_frame().T
        lo, hi = d["u"].quantile([0.05, 0.95])
        dw = d.assign(u=d["u"].clip(lo, hi))
        out[f"h{h}_winsor5"] = clus(dw).to_frame().T
        out[f"h{h}_by_coin"] = d.groupby("coin").apply(clus)
        d["yb"] = pd.cut(d["year"], [2017, 2020, 2022, 2026], labels=["2018-20", "2021-22", "2023-25"])
        out[f"h{h}_by_yearblock"] = d.groupby("yb").apply(clus)
        dd = d.dropna(subset=["past30"])
        dd = dd.assign(pq=pd.qcut(dd["past30"].rank(method="first"), 3, labels=["p30 low", "p30 mid", "p30 high"]))
        out[f"h{h}_by_past30_tercile"] = dd.groupby("pq").apply(clus)
        out[f"h{h}_past30_mean_by_tercile"] = dd.groupby("pq")["past30"].mean()
    return out
