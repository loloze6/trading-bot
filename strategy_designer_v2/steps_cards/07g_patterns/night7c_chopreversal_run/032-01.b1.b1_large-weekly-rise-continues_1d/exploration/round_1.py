import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            z7 = r7 / (sd30 * np.sqrt(7))
            z30 = r30 / (sd30 * np.sqrt(30))
            er14 = (c - c.shift(14)).abs() / (c.diff().abs().rolling(14).sum())
            fwd7 = c.shift(-7) / c - 1
            fwd1 = c.shift(-1) / c - 1
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n), "z7": z7, "z30": z30,
                               "er14": er14, "sd30": sd30, "fwd7": fwd7, "fwd1": fwd1,
                               "z1": r1 / sd30, "fc": b["forecast"].astype(float),
                               "day": ts.dt.floor("D"), "wd": ts.dt.dayofweek,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % 7 == 0) & A["fwd7"].notna()].copy()
    drift = G.groupby("coin")["fwd7"].mean()
    G["u7"] = G["fwd7"] - G["coin"].map(drift)
    G["sd30r"] = G.groupby("coin")["sd30"].rank(pct=True)
    G = G.dropna(subset=["z7", "sd30", "er14"])

    def summ(g):
        m = g["u7"].mean(); s = g["u7"].std(); k = len(g)
        dd = g.groupby("day")["u7"].sum(); D = len(dd)
        se = np.sqrt((dd - dd.mean() * 0).pow(2).sum() * 0 + ((g.groupby("day")["u7"].apply(lambda x: (x - m).sum())) ** 2).sum()) / k
        return pd.Series({"n": k, "days": D, "mean_u7": m, "t_clu": m / se if se > 0 else np.nan})

    out = {}
    G["z7bin"] = pd.cut(G["z7"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out["u7 by z7 bin"] = G.groupby("z7bin", observed=True).apply(summ)
    G["volt"] = pd.cut(G["sd30r"], [0, 1/3, 2/3, 1], labels=["lowvol", "midvol", "hivol"])
    G["side"] = np.sign(G["z7"])
    G["sz"] = G["z7"].abs() > 1
    out["u7 by vol x z7 sign (|z7|>1)"] = G[G["sz"]].groupby(["volt", "side"], observed=True).apply(summ)
    G["ert"] = pd.cut(G["er14"], [0, 0.15, 0.35, 1.01], labels=["chop", "mid", "trend"])
    out["u7 by er14 x z7 sign (|z7|>1)"] = G[G["sz"]].groupby(["ert", "side"], observed=True).apply(summ)
    G["z30bin"] = pd.cut(G["z30"], [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf])
    out["u7 by z30 bin"] = G.groupby("z30bin", observed=True).apply(summ)
    # slopes
    sl = {}
    for nm, sub in [("all", G), ("z7>0", G[G.z7 > 0]), ("z7<0", G[G.z7 < 0])]:
        r = stats.linregress(sub["z7"], sub["u7"]); sl[nm] = pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(sub)})
    out["slope u7 on z7"] = pd.DataFrame(sl).T
    # daily: large 1d moves, next day
    D1 = A.dropna(subset=["z1", "fwd1"]).copy()
    D1["z1bin"] = pd.cut(D1["z1"], [-np.inf, -2, -1, 1, 2, np.inf])
    out["next1d by z1"] = D1.groupby("z1bin", observed=True)["fwd1"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["next1d by weekday"] = D1.groupby("wd")["fwd1"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # book: gain on long-held bars by z7 bin at entry
    H = A[A["alloc"] > 0].dropna(subset=["fwd1"])
    H["g"] = H["alloc"] * H["fwd1"]
    H["z7bin"] = pd.cut(H["z7"], [2, 2.5, 3, 4, np.inf])
    out["book gain held bars by z7"] = H.groupby("z7bin", observed=True)["g"].agg(["count", "mean", "sum"])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)], ignore_index=True)
    T["ef"] = pd.cut(T["entry_forecast"], [0, 5, 10, 15, 20.1])
    out["trades by entry fc"] = T.groupby("ef", observed=True)["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
