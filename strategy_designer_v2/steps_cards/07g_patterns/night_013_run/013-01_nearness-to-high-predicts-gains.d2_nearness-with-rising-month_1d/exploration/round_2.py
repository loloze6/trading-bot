import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float); r1 = cl.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": c, "w": w, "yr": ts.dt.year,
                "regime": b["regime"],
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "ret30": cl / cl.shift(30) - 1,
                "near": cl / cl.rolling(364, min_periods=91).max() - 1,
                "vrat": b["volume"] / b["volume"].rolling(20).mean(),
                "lvrat": np.log(b["volume"].rolling(5).mean() / b["volume"].rolling(30).mean()),
                "fwd7": cl.shift(-7) / cl - 1,
                "fwd1": cl.shift(-1) / cl - 1,
                "wd": ts.dt.weekday,
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
    for col in ["vrat", "lvrat", "ret30", "near"]:
        t = {}
        for c, s in g.groupby("coin"): t[c] = slope(s, col)
        for y, s in g.groupby("yr"): t[f"y{y}"] = slope(s, col)
        t["ALL"] = slope(g, col)
        out[f"slope {col} (std x) by coin/year"] = pd.DataFrame(t, index=["slope", "t", "n"]).T
    # vrat within ret30 sign
    t = {}
    for sgn, s in g.dropna(subset=["ret30"]).groupby(g["ret30"] > 0):
        t[f"ret30>0={sgn} vrat"] = slope(s, "vrat")
        t[f"ret30>0={sgn} near"] = slope(s, "near")
        t[f"ret30>0={sgn} ret30"] = slope(s, "ret30")
    out["within ret30 sign"] = pd.DataFrame(t, index=["slope", "t", "n"]).T
    # near x vrat: heavy volume near high
    s = g.dropna(subset=["near", "vrat"]).copy()
    s["nearq"] = pd.qcut(s["near"].rank(method="first"), 3, labels=["far", "mid", "close"])
    s["vq"] = pd.qcut(s["vrat"].rank(method="first"), 3, labels=["lowV", "midV", "hiV"])
    out["ex7 near x vol"] = s.pivot_table(index="nearq", columns="vq", values="ex7", aggfunc="mean").round(4)
    # weekday by year (Friday & Wednesday)
    d1 = df.dropna(subset=["fwd1"]).copy()
    d1["ex1"] = d1["fwd1"] - d1.groupby("coin")["fwd1"].transform("mean")
    out["weekday x year next-day excess"] = d1.pivot_table(index="yr", columns="wd", values="ex1", aggfunc="mean").round(4)
    # book gain by regime and side
    d1["gain"] = d1["alloc"] * d1["fwd1"]
    d1["side"] = np.sign(d1["alloc"].round(3))
    out["gain by regime x side"] = d1.groupby(["regime", "side"])["gain"].agg(["mean", "count"]).round(5)
    # short side by year
    out["short-side gain by year"] = d1[d1.side < 0].groupby("yr")["gain"].agg(["mean", "count"]).round(5)
    return out
