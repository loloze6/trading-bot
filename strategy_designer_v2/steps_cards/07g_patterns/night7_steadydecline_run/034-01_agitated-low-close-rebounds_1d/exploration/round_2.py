import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            allr.append(pd.Series(b["close"].astype(float).values).pct_change().dropna())
        mu = pd.concat(allr).mean()
        sd1 = pd.concat(allr).std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l)
            clv = (c - l) / rng.replace(0, np.nan)
            r0 = c.pct_change()
            r1 = c.shift(-1) / c - 1
            r3 = c.shift(-3) / c - 1
            vol30 = r0.rolling(30, min_periods=20).std()
            relrng = (rng / c) / ((rng / c).rolling(30, min_periods=20).mean())
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)), "ts": ts,
                "clv": clv, "z0": r0 / vol30.shift(1), "x1": r1 - mu, "x3": r3 - 3 * mu,
                "x1n": (r1 - mu) / sd1,
                "relrng": relrng, "tr60": c / c.shift(60) - 1,
                "ag": (b["regime"] != "chop").astype(int),
                "wd": ts.dt.dayofweek, "year": ts.dt.year,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["s"] = 0.5 - D["clv"]
    D["trend"] = pd.cut(D["tr60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out = {}

    def dayt(sub, col):
        g = sub.dropna(subset=[col]).groupby("day")[col].sum()
        return pd.Series({"mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(len(g))), "days": len(g)})

    # graded strength: s * relrng (wide low close) in agitated
    D["sw"] = D["s"] * D["relrng"]
    D["swx1"] = D["sw"] * D["x1"]
    D["sx1"] = D["s"] * D["x1"]
    A = D[D.ag == 1].copy()
    out["ag: s*x1 vs (s*relrng)*x1"] = pd.DataFrame({"s": dayt(A, "sx1"), "s*relrng": dayt(A, "swx1")}).T
    # multiple regression per-obs: x1 on s, z0, s*relrng in agitated
    R = A.dropna(subset=["x1", "s", "z0", "relrng"])
    X = np.column_stack([np.ones(len(R)), R["s"], R["z0"].clip(-5, 5), R["s"] * (R["relrng"] - 1)])
    y = R["x1"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    cov = np.linalg.inv(X.T @ X) * res.var(ddof=X.shape[1])
    out["ag OLS x1 ~ s + z0 + s*(relrng-1)"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["c", "s", "z0", "s_x_wide"])
    # signed size per case when |s| large and wide, in agitated non-rising
    A["side"] = np.sign(A["s"])
    A["gain"] = A["side"] * A["x1"]
    A["wide"] = pd.qcut(A["relrng"], 3, labels=["narrow", "mid", "wide"])
    A["sbin"] = pd.cut(A["s"].abs(), [0, 0.2, 0.35, 0.51], labels=["weak", "mid", "strong"])
    out["ag: signed next-day gain % by |s| x width"] = (A.groupby(["wide", "sbin"])["gain"].agg(["mean", "count"]).assign(mean=lambda t: 100 * t["mean"]).unstack())
    out["ag: signed gain % by trend x |s|"] = (A.groupby(["trend", "sbin"])["gain"].agg(["mean", "count"]).assign(mean=lambda t: 100 * t["mean"]).unstack())
    # big down day rebound graded by z, agitated, by trend
    A["zq"] = pd.qcut(A["z0"], 5, labels=["bigdown", "down", "mid", "up", "bigup"])
    A["x3g"] = A["x3"].where(A["pos"] % 3 == 0)
    out["ag: 3d excess % by z x trend"] = (A.groupby(["trend", "zq"])["x3g"].mean() * 100).unstack().round(3)
    A["zx3"] = (-A["z0"].clip(-5, 5)) * A["x3g"]
    A["zx1"] = (-A["z0"].clip(-5, 5)) * A["x1"]
    out["ag: -z*x per-day t (1d, 3d grid)"] = pd.DataFrame({"1d": dayt(A, "zx1"), "3d": dayt(A, "zx3")}).T
    D["zx1"] = (-D["z0"].clip(-5, 5)) * D["x1"]
    out["all: -z*x1 by ag x trend"] = D.groupby(["ag", "trend"]).apply(lambda s: dayt(s, "zx1")).round(4)
    out["ag: -z*x1 by year"] = A.groupby("year").apply(lambda s: dayt(s, "zx1")).round(4)
    out["ag: -z*x1 by coin"] = A.groupby("coin").apply(lambda s: dayt(s, "zx1")).round(4)
    # weekday next-day excess by year
    out["next-day excess % by weekday x year"] = (D.groupby(["year", "wd"])["x1"].mean() * 100).unstack().round(3)
    return out
