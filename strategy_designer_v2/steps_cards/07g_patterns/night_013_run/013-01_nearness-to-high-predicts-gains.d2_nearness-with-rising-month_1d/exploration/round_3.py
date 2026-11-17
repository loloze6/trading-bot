import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": c, "w": w, "yr": ts.dt.year,
                "ret30": cl / cl.shift(30) - 1,
                "near60": cl / cl.rolling(60, min_periods=60).max() - 1,
                "near364": cl / cl.rolling(364, min_periods=91).max() - 1,
                "vrat": b["volume"] / b["volume"].rolling(20).mean(),
                "fwd7": cl.shift(-7) / cl - 1,
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    g = df[df["pos"] % 7 == 0].dropna(subset=["fwd7"]).copy()
    g["ex7"] = g["fwd7"] - g.groupby("coin")["fwd7"].transform("mean")
    out = {}
    def slope(s, col):
        s = s.dropna(subset=[col, "ex7"])
        if len(s) < 20: return (np.nan, np.nan, len(s))
        x = (s[col] - s[col].mean()) / s[col].std()
        r = stats.linregress(x, s["ex7"])
        return (round(r.slope, 5), round(r.slope / r.stderr, 2), len(s))
    fall = g[g.ret30 <= 0]; rise = g[g.ret30 > 0]
    for nm, sub in [("falling", fall), ("rising", rise)]:
        for col in ["near60", "ret30", "vrat"]:
            t = {}
            for c, s in sub.groupby("coin"): t[c] = slope(s, col)
            for y, s in sub.groupby("yr"): t[f"y{y}"] = slope(s, col)
            t["ALL"] = slope(sub, col)
            out[f"{nm}: slope {col}"] = pd.DataFrame(t, index=["slope", "t", "n"]).T
    s = fall.dropna(subset=["near60"]).copy()
    s["q"] = pd.qcut(s["near60"].rank(method="first"), 5, labels=False)
    q = s.groupby("q")["ex7"].agg(["mean", "count", "std"]); q["t"] = q["mean"]/(q["std"]/np.sqrt(q["count"]))
    out["falling: near60 quintiles"] = q.round(4)
    return out
