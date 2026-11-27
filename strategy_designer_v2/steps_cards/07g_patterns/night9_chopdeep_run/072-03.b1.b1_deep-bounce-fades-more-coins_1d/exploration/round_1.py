import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            hi20 = c.rolling(20).max()
            depth = ((c - hi20) / hi20) / sd20
            lo20 = c.rolling(20).min()
            pos_in_range = (c - lo20) / (hi20 - lo20)
            reg = b["regime"].astype(str)
            prof = np.where(reg == "chop", "trend", "choppy")
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "win": w, "i": np.arange(len(b)),
                              "r1": r1, "z1": r1 / sd20.shift(1), "depth": depth,
                              "pir": pos_in_range, "prof": prof, "reg": reg,
                              "wd": ts.dt.weekday, "year": ts.dt.year,
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "volrank": sd20})
            for h in (1, 3, 10):
                d[f"f{h}"] = c.shift(-h) / c - 1
                d[f"g{h}"] = (d["i"] % h == 0) & d[f"f{h}"].notna()
            d["gain"] = d["alloc"] * d["f1"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 3, 10):
        drift = D[D[f"g{h}"]].groupby("coin")[f"f{h}"].mean()
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(drift)
    D["up"] = np.where(D["r1"] > 0, "up", "down")
    out = {}
    def summ(sub, col):
        x = sub[col].dropna()
        n = len(x)
        if n < 3: return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})
    ok = D["depth"].notna()
    D.loc[ok, "dq"] = D[ok].groupby("prof")["depth"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    for h in (1, 3, 10):
        g = D[D[f"g{h}"] & ok]
        out[f"depth quintile x prof x up, u{h}"] = g.groupby(["prof", "up", "dq"]).apply(lambda s: summ(s, f"u{h}")).unstack(level=[1]) if h != 1 else g.groupby(["prof", "up", "dq"]).apply(lambda s: summ(s, f"u{h}"))
    # large moves
    g = D[D["g1"] & D["z1"].notna()].copy()
    g["zq"] = pd.qcut(g["z1"].rank(method="first"), 7, labels=False)
    out["next day after 1d move z septile x prof"] = g.groupby(["prof", "zq"]).apply(lambda s: summ(s, "u1"))
    g3 = D[D["g3"] & D["z1"].notna()].copy()
    g3["zq"] = pd.qcut(g3["z1"].rank(method="first"), 7, labels=False)
    out["3d after 1d move z septile x prof"] = g3.groupby(["prof", "zq"]).apply(lambda s: summ(s, "u3"))
    out["weekday next day"] = D[D["g1"]].groupby("wd").apply(lambda s: summ(s, "u1"))
    # position in range
    g10 = D[D["g10"] & D["pir"].notna()].copy()
    g10["pq"] = pd.qcut(g10["pir"].rank(method="first"), 5, labels=False)
    out["10d after range position quintile x prof"] = g10.groupby(["prof", "pq"]).apply(lambda s: summ(s, "u10"))
    # book
    held = D[D["alloc"].abs() > 0]
    out["book bar gain by year"] = held.groupby("year").apply(lambda s: summ(s, "gain"))
    out["book bar gain by depth quintile"] = held.groupby("dq").apply(lambda s: summ(s, "gain"))
    out["held share by reg"] = D.groupby("reg")["alloc"].apply(lambda s: (s.abs() > 0).mean())
    return out
