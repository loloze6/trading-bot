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
                              "regime": df["regime"].values, "z1": z1.values,
                              "f1": (c.shift(-1)/c-1).values, "f2": (c.shift(-2)/c-1).values,
                              "yr": ts.dt.year.values})
            rows.append(g)
    A = pd.concat(rows, ignore_index=True)
    for h in ["f1", "f2"]:
        A["x"+h] = A[h] - A["coin"].map(A.groupby("coin")[h].mean())
    def sl(d, x, y):
        d = d.dropna(subset=[x, y])
        if len(d) < 30: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(d)})
        r = stats.linregress(d[x], d[y]); return pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(d)})
    out = {}
    U = A[(A.regime != "trending") & (A.z1 < 0)]
    out["below-avg down days slope by coin"] = pd.DataFrame({c: sl(U[U.coin == c], "z1", "xf1") for c in A.coin.unique()}).T
    out["below-avg down days slope by year"] = pd.DataFrame({y: sl(U[U.yr == y], "z1", "xf1") for y in sorted(A.yr.unique())}).T
    out["below-avg down days excl 2020"] = sl(U[U.yr != 2020], "z1", "xf1")
    G2 = A[(A.pos % 2 == 0) & (A.regime != "trending") & (A.z1 < 0)]
    out["below-avg down days 2-day grid"] = sl(G2, "z1", "xf2")
    d = U.dropna(subset=["z1", "xf1"]).copy()
    d["b"] = pd.qcut(d["z1"], 5, labels=False)
    out["below-avg down days xf1 by z1 quintile"] = d.groupby("b")["xf1"].agg(["mean", "count", "std"]).assign(t=lambda s: s["mean"]/(s["std"]/np.sqrt(s["count"])))
    return out
