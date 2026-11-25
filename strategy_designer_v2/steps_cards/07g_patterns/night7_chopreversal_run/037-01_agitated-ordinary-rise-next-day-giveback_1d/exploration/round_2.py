import pandas as pd
import numpy as np

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c / c.shift(1) - 1
            vol = r.rolling(30, min_periods=20).std()
            z = r / vol
            f1 = c.shift(-1) / c - 1
            f2 = c.shift(-2) / c - 1
            hl = (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "win": w, "day": ts.dt.floor("D"),
                "year": ts.dt.year, "r": r, "z": z, "f1": f1, "f2": f2,
                "pos2": (np.arange(len(b)) % 2 == 0),
                "agit": b["regime"] != "chop",
                "cp": (c - b["low"]) / hl,
                "wick_up": (b["high"] - np.maximum(c, b["open"])) / hl,
                "rngz": (hl / c) / (hl / c).rolling(30, min_periods=20).mean(),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "ret_next": f1}))
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["f1"] - D["coin"].map(D.groupby("coin")["f1"].mean())
    D["x2"] = D["f2"] - D["coin"].map(D[D.pos2].groupby("coin")["f2"].mean())
    D["cps"] = 0.5 - D["cp"]  # positive when close near low

    def ct(df, col):
        df = df.dropna(subset=[col])
        if len(df) < 10: return pd.Series({"n": len(df)})
        m = df[col].mean(); s = (df[col] - m).groupby(df["day"]).sum(); G = len(s)
        se = np.sqrt((s ** 2).sum() * G / max(G - 1, 1)) / len(df)
        return pd.Series({"n": len(df), "days": G, "mean%": 100 * m, "t": m / se})

    def slope(df, xcol, ycol):
        df = df.dropna(subset=[xcol, ycol])
        x = df[xcol] - df[xcol].mean(); y = df[ycol]
        b = (x * y).sum() / (x * x).sum()
        e = y - y.mean() - b * x
        s = (x * e).groupby(df["day"]).sum(); G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (x * x).sum()
        return pd.Series({"n": len(df), "slope%": 100 * b, "t": b / se})

    out = {}
    D["cpb"] = pd.cut(D["cp"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    D["sgn"] = np.where(D["r"] > 0, "up", "down")
    out["agit x day sign x close pos, next-day"] = D[D.agit].groupby(["sgn", "cpb"], observed=True).apply(lambda g: ct(g, "x1"))
    sl = []
    for (a, y), g in D.groupby(["agit", "year"]):
        s = slope(g, "cps", "x1"); s["agit"] = a; s["year"] = y; sl.append(s)
    out["slope next-day on (0.5-closepos), agit x year"] = pd.DataFrame(sl).set_index(["agit", "year"])
    out["slope next-day on (0.5-closepos), by agit"] = D.groupby("agit").apply(lambda g: slope(g, "cps", "x1"))
    # partial: residualise on z
    def partial(g):
        g = g.dropna(subset=["cps", "z", "x1"])
        X = np.column_stack([np.ones(len(g)), g["z"].clip(-3, 3), g["cps"]])
        beta = np.linalg.lstsq(X, g["x1"].values, rcond=None)[0]
        return pd.Series({"b_z%": 100 * beta[1], "b_cps%": 100 * beta[2], "n": len(g)})
    out["joint regression z and close pos"] = D.groupby("agit").apply(partial)
    out["slope 2-day on cps, grid"] = D[D.pos2].groupby("agit").apply(lambda g: slope(g, "cps", "x2"))
    out["agit by coin, slope cps"] = D[D.agit].groupby("coin").apply(lambda g: slope(g, "cps", "x1"))
    # book: realised short position vs next-day
    P = D[D.alloc < 0]
    out["held short bars: next-day coin ret%, n"] = pd.Series({"n": len(P), "mean raw%": 100 * P["f1"].mean(), "mean excess short%": -100 * P["x1"].mean()})
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    tr["dur_d"] = tr["duration_minutes"] / 1440
    tr["db"] = pd.cut(tr["dur_d"], [0, 1.5, 2.5, 5, 1000])
    out["trades by duration"] = tr.groupby("db", observed=True)["profit_loss_percent"].agg(["count", "mean"])
    return out
