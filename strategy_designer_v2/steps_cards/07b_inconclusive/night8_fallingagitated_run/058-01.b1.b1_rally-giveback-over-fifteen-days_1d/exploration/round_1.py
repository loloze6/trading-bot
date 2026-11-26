import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for H in [5, 10, 15, 20, 30]:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rr.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = np.mean(rr) if rr else np.nan
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            r = pd.Series(c).pct_change()
            sd30 = r.rolling(30).std().values
            r3 = pd.Series(c).pct_change(3).values
            for i in range(0, len(c), 15):
                if not (f[i] < 0):
                    continue
                d = dict(coin=coin, win=w, year=ts.iloc[i].year, f=f[i],
                         s=r3[i] / sd30[i] if sd30[i] > 0 else np.nan, r3=r3[i])
                for H in [5, 10, 15, 20, 30]:
                    if i + H < len(c):
                        d["x%d" % H] = c[i + H] / c[i] - 1 - drift[(coin, H)]
                rows.append(d)
    t = pd.DataFrame(rows)
    out = {}

    def slope(sub, col="x15", xcol="f"):
        s = sub.dropna(subset=[col, xcol])
        if len(s) < 5:
            return (len(s), np.nan, np.nan, np.nan)
        res = stats.linregress(s[xcol], s[col])
        m = s[col].mean()
        tm = m / (s[col].std() / np.sqrt(len(s)))
        return (len(s), res.slope, res.slope / res.stderr, -m, -tm)

    hz = {}
    for H in [5, 10, 15, 20, 30]:
        hz["H%d" % H] = slope(t, "x%d" % H)
    out["by horizon (n, slope, t, mean short move, t)"] = pd.DataFrame(
        hz, index=["n", "slope", "t", "short_mean", "t_mean"]).T
    out["by coin"] = pd.DataFrame(
        {c: slope(g) for c, g in t.groupby("coin")},
        index=["n", "slope", "t", "short_mean", "t_mean"]).T
    out["by year"] = pd.DataFrame(
        {y: slope(g) for y, g in t.groupby("year")},
        index=["n", "slope", "t", "short_mean", "t_mean"]).T
    t["q"] = pd.qcut(t["f"].rank(method="first"), 4, labels=["q1_largest", "q2", "q3", "q4_smallest"])
    out["by forecast quartile: mean x15 and x5"] = t.groupby("q")[["x5", "x10", "x15", "x20", "f", "s"]].agg(["mean", "count"])
    out["slope on scaled rise s (x15)"] = str(slope(t, "x15", "s"))
    out["forecast desc"] = t["f"].describe()
    return out
