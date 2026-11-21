import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            allr.append(c.pct_change().dropna())
        drift1 = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(c)),
                               "z": r1 / sd,
                               "z3": (c / c.shift(3) - 1) / (sd * np.sqrt(3)),
                               "z5": (c / c.shift(5) - 1) / (sd * np.sqrt(5)),
                               "year": ts.dt.year, "wnum": int(w[1:])})
            for h in (5, 10):
                df[f"f{h}"] = c.shift(-h) / c - 1
                df[f"x{h}"] = df[f"f{h}"] - drift1 * h
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)

    def qtab(g, key, col, nq=5):
        g = g.dropna(subset=[key, col]).copy()
        g["q"] = g.groupby("coin")[key].transform(lambda s: pd.qcut(s, nq, labels=False, duplicates="drop"))
        return g

    # robustness over grid offsets, 10d excess
    for key in ("z", "z3", "z5"):
        res = []
        for off in range(10):
            g = d[d["pos"] % 10 == off]
            g = qtab(g, key, "x10")
            m = g.groupby("q")["x10"].agg(["mean", "std", "count"])
            m["t"] = m["mean"] / (m["std"] / np.sqrt(m["count"]))
            slope = stats.linregress(g[key], g["x10"])
            res.append({"off": off, "q0": m.loc[0, "mean"], "t0": m.loc[0, "t"],
                        "q4": m.loc[4, "mean"], "t4": m.loc[4, "t"], "n0": m.loc[0, "count"],
                        "slope_t": slope.slope / slope.stderr})
        out[f"{key} 10d excess by grid offset"] = pd.DataFrame(res).round(4)
    # 5d after top z by offset
    res = []
    for off in range(5):
        g = qtab(d[d["pos"] % 5 == off], "z", "x5")
        m = g.groupby("q")["x5"].agg(["mean", "std", "count"])
        m["t"] = m["mean"] / (m["std"] / np.sqrt(m["count"]))
        res.append({"off": off, "q0": m.loc[0, "mean"], "t0": m.loc[0, "t"], "q4": m.loc[4, "mean"], "t4": m.loc[4, "t"]})
    out["z 5d excess by offset"] = pd.DataFrame(res).round(4)
    # z3 lowest quintile 10d by coin and by window half, offset 0
    g = qtab(d[d["pos"] % 10 == 0], "z3", "x10")
    g["half"] = np.where(g["wnum"] <= 12, "w1-12", "w13-24")
    out["z3 q x coin 10d"] = g.groupby(["coin", "q"])["x10"].mean().unstack().round(4)
    out["z3 q x half 10d"] = g.groupby(["half", "q"])["x10"].mean().unstack().round(4)
    out["z3 q x year 10d (q0,q4)"] = g[g["q"].isin([0, 4])].groupby(["year", "q"])["x10"].mean().unstack().round(4)
    return out
