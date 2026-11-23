def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; v = b["volume"]
            rng = (h - l).replace(0, np.nan)
            r0 = c / c.shift(1) - 1
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "cl": (h - c) / rng,
                "vr": v / v.shift(1).rolling(20, min_periods=20).mean(),
                "r0": r0,
                "vol20": r0.shift(1).rolling(20, min_periods=20).std(),
                "rr": (rng / c) / (rng / c).shift(1).rolling(20, min_periods=20).mean(),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "i": np.arange(len(b)),
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")
    D["z"] = D["r0"] / D["vol20"]
    out = {}
    def tab(df, key, val):
        r = df.dropna(subset=[key, val]).groupby(key)[val].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.drop(columns="std")
    D["zq"] = pd.cut(D["z"], [-100, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 2, 100])
    out["x1 by z of day return"] = tab(D, "zq", "x1")
    # joint regression
    J = D.dropna(subset=["x1", "z", "cl", "vr", "rr"]).copy()
    J["neg_z"] = (-J["z"]).clip(lower=0)
    J["clvr"] = J["cl"] * J["vr"]
    J["clvr2"] = J["clvr"] ** 2
    X = np.column_stack([np.ones(len(J)), J["neg_z"], J["cl"], J["clvr"], J["rr"]])
    beta, *_ = np.linalg.lstsq(X, J["x1"].values, rcond=None)
    res = J["x1"].values - X @ beta
    s2 = res @ res / (len(J) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["joint OLS x1"] = pd.DataFrame({"beta": beta, "t": beta / se},
                                       index=["const", "neg_z", "cl", "cl*vr", "rangeratio"])
    # drop reversal by coin and by year
    big = D[D["z"] < -1.5]
    out["z<-1.5 by coin"] = tab(big, "coin", "x1")
    out["z<-1.5 by year"] = tab(big, "yr", "x1")
    # within drop days, closeloc and volume
    big = big.copy()
    big["clh"] = np.where(big["cl"] > 0.7, "low close", "not low")
    big["vrh"] = np.where(big["vr"] > 1.5, "heavy", "normal")
    g = big.dropna(subset=["x1"]).groupby(["vrh", "clh"])["x1"].agg(["mean", "count", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"])); out["drop days by vol x close"] = g.drop(columns="std")
    # range expansion split by direction
    D["rrq"] = pd.qcut(D["rr"], 5, labels=False, duplicates="drop")
    D["dir"] = np.where(D["r0"] < 0, "down", "up")
    g = D.dropna(subset=["x1", "rrq"]).groupby(["rrq", "dir"])["x1"].agg(["mean", "count", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"])); out["range ratio x dir"] = g.drop(columns="std")
    # 3-day horizon after drops, non-overlapping grid
    D3 = D[D["i"] % 3 == 0].copy()
    D3["x3"] = D3["f3"] - D3.groupby("coin")["f3"].transform("mean")
    D3["zq"] = pd.cut(D3["z"], [-100, -2, -1, 0, 1, 2, 100])
    out["x3 by z (3d grid)"] = tab(D3, "zq", "x3")
    # heavy+low-close cell over 3 days (grid)
    D3["cv"] = D3["cl"] * D3["vr"]
    D3["cvq"] = pd.qcut(D3["cv"], 5, labels=False, duplicates="drop")
    out["x3 by cl*vr quintile (grid)"] = tab(D3, "cvq", "x3")
    return out
