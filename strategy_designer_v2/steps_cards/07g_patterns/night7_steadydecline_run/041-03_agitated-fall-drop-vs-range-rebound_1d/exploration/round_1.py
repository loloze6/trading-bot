import numpy as np
import pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            rng = (b["high"] - b["low"])
            mr = rng.shift(1).rolling(30, min_periods=20).mean()
            r0 = c.pct_change()
            sm = (c - c.shift(1)) / mr
            cl = (b["close"] - b["low"]) / rng.replace(0, np.nan)
            vol30 = r0.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "w": w, "ts": b["timestamp"],
                "inprof": (b["regime"] == "unknown").astype(int),
                "sm": sm, "r0": r0, "cl": cl,
                "r1": c.shift(-1) / c - 1,
                "r2": c.shift(-2) / c.shift(-1) - 1,
                "r3": c.shift(-3) / c.shift(-2) - 1,
                "absz": r0.abs() / vol30,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    cm = d.groupby("coin")["r0"].mean()
    for k in ["r1", "r2", "r3"]:
        d[k + "x"] = d[k] - d["coin"].map(cm)

    def ct(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 10:
            return pd.Series({"n": len(s), "mean%": np.nan, "t": np.nan, "days": 0})
        dev = s[col] - s[col].mean()
        g = dev.groupby(s["ts"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(s)
        return pd.Series({"n": len(s), "mean%": 100 * s[col].mean(),
                          "t": s[col].mean() / se if se > 0 else np.nan, "days": g.size})

    d["smbin"] = pd.cut(d["sm"], [-99, -1.5, -0.8, -0.4, -0.1, 0.1, 0.4, 0.8, 1.5, 99])
    out = {}
    for p in [1, 0]:
        sub = d[d["inprof"] == p]
        out[f"r1x by scaled move, inprof={p}"] = sub.groupby("smbin", observed=True).apply(lambda s: ct(s, "r1x"))
    ip = d[d["inprof"] == 1]
    out["inprof falls: r2x,r3x by bin"] = pd.concat({
        "r2x": ip[ip.sm < 0].groupby("smbin", observed=True).apply(lambda s: ct(s, "r2x"))["mean%"],
        "r3x": ip[ip.sm < 0].groupby("smbin", observed=True).apply(lambda s: ct(s, "r3x"))["mean%"]}, axis=1)
    d["clbin"] = pd.cut(d["cl"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    for p in [1, 0]:
        out[f"r1x by close location, inprof={p}"] = d[d.inprof == p].groupby("clbin", observed=True).apply(lambda s: ct(s, "r1x"))
    out["inprof falls r1x by weekday"] = ip[ip.sm < 0].groupby("wd").apply(lambda s: ct(s, "r1x"))
    out["inprof falls r1x by coin"] = ip[ip.sm < 0].groupby("coin").apply(lambda s: ct(s, "r1x"))
    out["inprof falls r1x by year"] = ip[ip.sm < 0].groupby("yr").apply(lambda s: ct(s, "r1x"))
    out["share inprof"] = float(d["inprof"].mean())
    # slope of r1x on sm in profile vs out
    for p in [1, 0]:
        s = d[(d.inprof == p)].dropna(subset=["sm", "r1x"])
        out[f"corr sm,r1x inprof={p}"] = float(np.corrcoef(s.sm, s.r1x)[0, 1])
    return out
