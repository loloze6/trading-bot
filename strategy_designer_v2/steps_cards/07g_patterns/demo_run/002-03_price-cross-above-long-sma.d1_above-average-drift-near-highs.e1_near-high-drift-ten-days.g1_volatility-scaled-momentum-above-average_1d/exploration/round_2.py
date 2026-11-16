import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std().shift(1)
            z1 = r1 / vol20
            ts = pd.to_datetime(df["timestamp"])
            g = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)),
                              "regime": df["regime"].values, "r1": r1.values, "z1": z1.values,
                              "f1": (c.shift(-1)/c-1).values, "f3": (c.shift(-3)/c-1).values,
                              "wd": ts.dt.weekday.values, "yr": ts.dt.year.values})
            rows.append(g)
    A = pd.concat(rows, ignore_index=True)
    for h in ["f1", "f3"]:
        A["x"+h] = A[h] - A["coin"].map(A.groupby("coin")[h].mean())
    out = {}
    def tbin(df, col, q, y):
        d = df.dropna(subset=[col, y]).copy()
        d["b"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        s = d.groupby("b")[y].agg(["mean", "count", "std"])
        s["t"] = s["mean"] / (s["std"] / np.sqrt(s["count"]))
        return s
    def sl(d, x, y):
        d = d.dropna(subset=[x, y])
        r = stats.linregress(d[x], d[y]); return pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(d)})
    dn = A[A.z1 < 0]; up = A[A.z1 > 0]
    out["next-day xret by z1 decile"] = tbin(A, "z1", 10, "xf1")
    out["down days: slope xf1 on z1"] = pd.DataFrame({"all": sl(dn, "z1", "xf1"),
        "trend": sl(dn[dn.regime == "trending"], "z1", "xf1"),
        "unknown": sl(dn[dn.regime != "trending"], "z1", "xf1"),
        "up days all": sl(up, "z1", "xf1")}).T
    out["down days slope by coin"] = pd.DataFrame({c: sl(dn[dn.coin == c], "z1", "xf1") for c in A.coin.unique()}).T
    out["down days slope by year"] = pd.DataFrame({y: sl(dn[dn.yr == y], "z1", "xf1") for y in sorted(A.yr.unique())}).T
    G3 = A[A.pos % 3 == 0]
    dn3 = G3[G3.z1 < 0]
    out["down days 3-day grid slope"] = sl(dn3, "z1", "xf3")
    out["bottom z1 decile next-day by regime"] = A[A.z1 <= A.z1.quantile(0.1)].groupby("regime")["xf1"].agg(["mean", "count", "std"]).assign(t=lambda s: s["mean"]/(s["std"]/np.sqrt(s["count"])))
    out["weekday xf1 by year sign (Fri)"] = A[A.wd == 4].groupby("yr")["xf1"].mean()
    out["weekday xf1 by coin (Fri)"] = A[A.wd == 4].groupby("coin")["xf1"].agg(["mean", "count"])
    return out
