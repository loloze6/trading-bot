import numpy as np, pandas as pd

def explore(data):
    days = data["days"]; bars = data["bars"]
    out = {}
    D = pd.concat([df.assign(coin=c, win=w) for c, ws in days.items() for w, df in ws.items()])
    D = D.dropna(subset=["coin_return"])
    D["d"] = pd.to_datetime(D["day"])
    D["wd"] = D["d"].dt.weekday
    D["yr"] = D["d"].dt.year
    # day-clustered: one mean per calendar day across coins
    M = D.groupby("d").agg(r=("coin_return", "mean")).reset_index()
    M["wd"] = M["d"].dt.weekday; M["yr"] = M["d"].dt.year
    g = M.groupby("wd")["r"]
    out["weekday_daymean"] = pd.DataFrame(dict(mean=g.mean(), n_days=g.count(),
                                               t=g.mean() / (g.std() / np.sqrt(g.count()))))
    # Welch t: each weekday vs the other days
    res = {}
    for wd in range(7):
        a = M.loc[M["wd"] == wd, "r"]; b = M.loc[M["wd"] != wd, "r"]
        res[wd] = dict(diff=a.mean() - b.mean(),
                       t=(a.mean() - b.mean()) / np.sqrt(a.var() / len(a) + b.var() / len(b)))
    out["weekday_vs_rest"] = pd.DataFrame(res).T
    # stability by year: mean per weekday per year (day-mean)
    out["weekday_by_year"] = M.pivot_table(index="yr", columns="wd", values="r", aggfunc="mean")
    # per coin: Sat minus rest and Thu minus rest
    pc = {}
    for c, s in D.groupby("coin"):
        pc[c] = dict(sat_minus_rest=s.loc[s["wd"] == 5, "coin_return"].mean() - s.loc[s["wd"] != 5, "coin_return"].mean(),
                     thu_minus_rest=s.loc[s["wd"] == 3, "coin_return"].mean() - s.loc[s["wd"] != 3, "coin_return"].mean())
    out["weekday_by_coin"] = pd.DataFrame(pc).T
    # by window halves for weekday 5
    D["wn"] = D["win"].str[1:].astype(int)
    D["wgrp"] = pd.cut(D["wn"], [0, 6, 12, 18, 24], labels=["w1-6", "w7-12", "w13-18", "w19-24"])
    out["sat_minus_rest_by_wgrp"] = D.groupby("wgrp").apply(
        lambda s: s.loc[s["wd"] == 5, "coin_return"].mean() - s.loc[s["wd"] != 5, "coin_return"].mean())
    # 90-day up momentum: quintiles of z90 on 30-day grid, by year halves
    rows = []
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 30, 30):
                rs.append(c[i + 30] / c[i] - 1)
        mu, sd = np.mean(rs), np.std(rs, ddof=1)
        for w, df in wins.items():
            c = df["close"].values; n = len(c)
            ts = pd.to_datetime(df["timestamp"]).values
            for i in range(90, n - 10):
                rows.append(dict(coin=coin, pos=i, d=ts[i], p90=c[i] / c[i - 90] - 1,
                                 f10=c[i + 10] / c[i] - 1,
                                 f30=(c[i + 30] / c[i] - 1 - mu) / sd if i + 30 < n else np.nan))
    X = pd.DataFrame(rows)
    X["z"] = X.groupby("coin")["p90"].transform(lambda s: (s - s.mean()) / s.std())
    X["yr"] = pd.to_datetime(X["d"]).dt.year
    S = X[X["pos"] % 10 == 0].copy()
    S["q"] = pd.qcut(S["z"], 5, labels=False)
    out["z90_quint_f10"] = S.groupby("q").agg(n=("f10", "size"), mean_f10=("f10", "mean"), zmean=("z", "mean"))
    S["half"] = np.where(S["yr"] <= 2021, "<=2021", ">=2022")
    out["z90_top_vs_mid_by_half"] = S.groupby(["half", "q"])["f10"].mean().unstack()
    return out
