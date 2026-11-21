import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        g3 = []; h1 = []
        for w, b in wins.items():
            c = b["close"].values
            n = (len(c) - 1) // 3
            g3.append(c[3:3*n+1:3] / c[0:3*n:3] - 1)
            h1.append(c[1:] / c[:-1] - 1)
        m3 = np.nanmean(np.concatenate(g3)); m1 = np.nanmean(np.concatenate(h1))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r72 = c / c.shift(72) - 1
            sc = r72.abs().rolling(72, min_periods=20).mean().shift(1)
            sig = (-r72 / sc).clip(-2, 2)
            r1 = c / c.shift(1) - 1
            sc1 = r1.abs().rolling(72, min_periods=20).mean().shift(1)
            d = pd.DataFrame({"coin": coin, "w": w, "hour": ts.dt.hour, "year": ts.dt.year,
                              "sig": sig, "f3": c.shift(-3) / c - 1 - m3,
                              "f1": c.shift(-1) / c - 1 - m1, "z1": (r1 / sc1).clip(-5, 5),
                              "rv": r1.abs().rolling(24, min_periods=12).mean()})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def tab(G, x, y, key):
        res = []
        for k, g in G.dropna(subset=[x, y]).groupby(key):
            s = stats.linregress(g[x], g[y])
            res.append({key: str(k), "n": len(g), "slope_bp": s.slope * 1e4, "t": s.slope / s.stderr})
        return pd.DataFrame(res).round(3)

    # 15:00-bar 3h trend continuation (sig negative = uptrend); slope negative = continuation
    G = D[D.hour == 14]
    out["14h bar 3h fwd on sig, by coin"] = tab(G, "sig", "f3", "coin")
    out["14h bar 3h fwd on sig, by year"] = tab(G, "sig", "f3", "year")
    # by volatility tercile (rv known at close), within-coin terciles
    G = G.copy()
    G["rvq"] = G.groupby("coin")["rv"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["14h bar 3h fwd on sig, by vol tercile"] = tab(G, "sig", "f3", "rvq")
    # by sig quintile mean of f3 at 14h
    G2 = G.dropna(subset=["sig", "f3"]).copy()
    G2["q"] = pd.qcut(G2["sig"], 5, labels=False, duplicates="drop")
    out["14h bar f3 by sig quintile"] = G2.groupby("q")["f3"].agg(["count", "mean"]).assign(mean_bp=lambda x: x["mean"] * 1e4)
    # noon 1h reversal: bar stamped 12 (closes 13:00) next-1h on its own scaled 1h move
    G = D[D.hour == 12]
    out["12h bar next1h on z1, by coin"] = tab(G, "z1", "f1", "coin")
    out["12h bar next1h on z1, by year"] = tab(G, "z1", "f1", "year")
    # evening 20-22 continuation by year
    G = D[D.hour == 21]
    out["21h bar 3h fwd on sig, by year"] = tab(G, "sig", "f3", "year")
    out["21h bar 3h fwd on sig, by coin"] = tab(G, "sig", "f3", "coin")
    return out
