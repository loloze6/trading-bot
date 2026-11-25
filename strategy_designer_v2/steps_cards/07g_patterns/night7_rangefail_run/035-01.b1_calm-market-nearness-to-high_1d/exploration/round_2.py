import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi = c.shift(1).rolling(20).max()
            sd = r1.rolling(20).std()
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(n), "day": ts.dt.floor("D"),
                "dist": (c - hi) / hi / sd, "z1": r1 / sd.shift(1), "r1": r1,
                "r3z": (c / c.shift(3) - 1) / sd,
                "fwd5": c.shift(-5) / c - 1, "fwd1": c.shift(-1) / c - 1, "fwd2": c.shift(-2)/c-1,
                "calm": (b["regime"] != "chop").astype(int),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": ts.dt.weekday, "yr": ts.dt.year,
            }))
    A = pd.concat(rows, ignore_index=True)
    drift5 = A[A.pos % 5 == 0].groupby("coin")["fwd5"].mean()
    A["ex5"] = A["fwd5"] - A["coin"].map(drift5)
    out = {}
    def dayt(g, col, key):
        # per-day sum of deviations, t over days
        res = {}
        for k, gg in g.groupby(key):
            s = gg.groupby("day")[col].sum()
            m = gg[col].mean()
            se = s.std() * np.sqrt(len(s)) / len(gg) if len(s) > 1 else np.nan
            res[k] = {"mean": m, "cases": len(gg), "days": len(s), "t_day": m / se}
        return pd.DataFrame(res).T.round(4)
    G = A[A.pos % 5 == 0].dropna(subset=["ex5", "dist", "z1"]).copy()
    C = G[G.calm == 1].copy()
    C["dt"] = pd.qcut(C["dist"], 3, labels=False)
    C["zt"] = C.groupby("dt")["z1"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["calm: dist tercile x 1d z tercile within"] = dayt(C, "ex5", ["dt", "zt"])
    C["rt"] = C.groupby("dt")["r3z"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["calm: dist tercile x 3d z tercile within"] = dayt(C, "ex5", ["dt", "rt"])
    Ag = G[G.calm == 0].copy()
    Ag["zq"] = pd.qcut(Ag["z1"], 5, labels=False)
    out["agitated: 1d z quintile, 5d ex"] = dayt(Ag, "ex5", "zq")
    Ag["dq"] = pd.qcut(Ag["dist"], 5, labels=False)
    out["agitated: dist quintile by year-half"] = dayt(Ag, "ex5", "dq")
    # weekday, day-clustered, 1d grid is every bar
    D = A.dropna(subset=["fwd1"]).copy()
    d1 = D.groupby("coin")["fwd1"].mean()
    D["ex1"] = D["fwd1"] - D["coin"].map(d1)
    out["weekday next-day ex, day-clustered"] = dayt(D, "ex1", "wd")
    D["thfr"] = D.wd.isin([3, 4]).astype(int)
    out["Thu/Fri vs other by year"] = dayt(D, "ex1", ["yr", "thfr"])
    # book: long vs short contribution
    A["g"] = A["alloc"] * A["fwd1"]
    A["side"] = np.sign(A["alloc"]).fillna(0)
    out["bar gain by side x calm"] = A.groupby(["side"])["g"].agg(["mean", "count", "sum"]).round(5)
    return out
