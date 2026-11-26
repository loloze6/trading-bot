def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            sd = r.rolling(30).std()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "rng": ((b["high"] - b["low"]) / c) / sd,
                "z1": r / sd,
                "tr60": c / c.shift(60) - 1,
                "tr20": c / c.shift(20) - 1,
                "cl": (c - b["low"]) / (b["high"] - b["low"]),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "f7": c.shift(-7) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos": np.arange(len(b)),
                "fc": b["forecast"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    for h, col in [(3, "f3"), (7, "f7"), (1, "f1")]:
        g = D[D.pos % h == 0].copy()
        drift = g.groupby("coin")[col].transform("mean")
        g["u"] = g[col] - drift
        D.loc[g.index, "u%d" % h] = g["u"]

    def summ(df, col, by):
        x = df.dropna(subset=[col, by] if isinstance(by, str) else [col] + by)
        res = x.groupby(by)[col].agg(["mean", "count", "std"])
        res["t"] = res["mean"] / (res["std"] / np.sqrt(res["count"]))
        return res.drop(columns="std").round(5)

    D["rngq"] = pd.qcut(D["rng"], 5, labels=False, duplicates="drop")
    D["z1q"] = pd.qcut(D["z1"], 5, labels=False)
    D["trend"] = np.where(D.tr60 < -0.10, "fall", np.where(D.tr60 > 0.10, "rise", "chop"))
    D.loc[D.tr60.isna(), "trend"] = np.nan
    fall = D[D.trend == "fall"]
    out["fall: u3 by range quintile"] = summ(fall, "u3", "rngq")
    out["all: u3 by range quintile"] = summ(D, "u3", "rngq")
    out["u3 by trend x range>=2"] = summ(D.assign(w2=(D.rng >= 2)), "u3", ["trend", "w2"])
    fw = fall[fall.rng >= 2].copy()
    fw["dn"] = np.where(fw.z1 < 0, "down", "up")
    out["fall wide: u3 by close dir"] = summ(fw, "u3", "dn")
    out["fall wide: u7 by close dir"] = summ(fw, "u7", "dn")
    out["fall: u3 by 1d z quintile"] = summ(fall, "u3", "z1q")
    out["all: u3 by 1d z quintile"] = summ(D, "u3", "z1q")
    out["all: u3 by trend x z1q"] = summ(D, "u3", ["trend", "z1q"])
    out["all: u7 by z1q"] = summ(D, "u7", "z1q")
    out["all: u1 by weekday"] = summ(D, "u1", "wd")
    # trend20 quintile
    D["t20q"] = pd.qcut(D["tr20"], 5, labels=False)
    out["all: u7 by 20d return quintile"] = summ(D, "u7", "t20q")
    out["corr rng vs u3 in fall"] = float(fall[["rng", "u3"]].dropna().corr().iloc[0, 1])
    return out
