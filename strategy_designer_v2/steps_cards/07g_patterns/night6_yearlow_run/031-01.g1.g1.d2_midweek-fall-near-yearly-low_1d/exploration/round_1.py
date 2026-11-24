import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "ts": ts, "wd": ts.dt.weekday,
                              "ret": r, "next": c.shift(-1) / c - 1,
                              "next2": c.shift(-2) / c - 1,
                              "r3": c / c.shift(3) - 1,
                              "r1": r,
                              "vol20": r.rolling(20).std(),
                              "regime": b["regime"], "fc": b["forecast"],
                              "alloc": b["postRebalance_current_allocation"]})
            d["year"] = ts.dt.year
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["ret"].mean()
    D["nx"] = D["next"] - D["coin"].map(mu)
    D["z1"] = D["r1"] / D["vol20"]
    D["z3"] = D["r3"] / (D["vol20"] * np.sqrt(3))
    out = {}

    def tstat(s):
        s = s.dropna()
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan, "n": len(s)})

    # weekday of next-day excess return
    out["next-day excess by weekday of signal bar"] = D.groupby("wd")["nx"].apply(tstat).unstack()
    # correlation of 3-day z with next-day excess, by weekday
    res = {}
    for wd, g in D.groupby("wd"):
        g = g.dropna(subset=["z3", "nx"])
        rho, p = stats.spearmanr(g["z3"], g["nx"])
        x = g["z3"].clip(-3, 3)
        prod = x * g["nx"]
        res[wd] = {"spearman": rho, "p": p, "mean z3*nx": prod.mean(), "t": prod.mean() / (prod.std() / np.sqrt(len(prod))), "n": len(g)}
    out["z3 (3-day ending this bar) vs next excess, by weekday"] = pd.DataFrame(res).T
    # Lag-1 version: Mon->Thu analogue: r3 lagged one bar vs next day, by weekday
    D["z3l"] = D.groupby(["coin", "win"])["z3"].shift(1)
    res = {}
    for wd, g in D.groupby("wd"):
        g = g.dropna(subset=["z3l", "nx"])
        prod = g["z3l"].clip(-3, 3) * g["nx"]
        res[wd] = {"mean": prod.mean(), "t": prod.mean() / (prod.std() / np.sqrt(len(prod))), "n": len(g)}
    out["z3 lagged 1 vs next excess, by weekday"] = pd.DataFrame(res).T
    # deciles of 1-day z vs next day, all days
    D["q1"] = pd.qcut(D["z1"], 10, labels=False)
    out["next excess by decile of 1-day z"] = D.groupby("q1")["nx"].apply(tstat).unstack()
    D["q3"] = pd.qcut(D["z3"], 10, labels=False)
    out["next excess by decile of 3-day z"] = D.groupby("q3")["nx"].apply(tstat).unstack()
    # vol tercile per coin
    D["vq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["next excess by vol tercile"] = D.groupby("vq")["nx"].apply(tstat).unstack()
    # Friday: regime split
    F = D[D["wd"] == 4]
    out["Friday next excess by regime x sign z3l"] = F.assign(sg=np.sign(F["z3l"])).groupby(["regime", "sg"])["nx"].apply(tstat).unstack()
    # book: daily returns by weekday
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["win"] = w; bk.append(x)
    B = pd.concat(bk, ignore_index=True)
    B["wd"] = pd.to_datetime(B["day"]).dt.weekday
    out["book daily return by weekday"] = B.groupby("wd")["book_return"].apply(tstat).unstack()
    out["book by year"] = B.assign(y=pd.to_datetime(B["day"]).dt.year).groupby("y")["book_return"].apply(tstat).unstack()
    # Friday active: next excess vs abs forecast quintile
    Fa = F[F["fc"] != 0].copy()
    Fa["sgn_nx"] = np.sign(Fa["fc"]) * Fa["nx"]
    Fa["fq"] = pd.qcut(Fa["fc"].abs(), 5, labels=False, duplicates="drop")
    out["Friday active: signed next excess by |forecast| quintile"] = Fa.groupby("fq")["sgn_nx"].apply(tstat).unstack()
    out["Friday active by coin"] = Fa.groupby("coin")["sgn_nx"].apply(tstat).unstack()
    return out
