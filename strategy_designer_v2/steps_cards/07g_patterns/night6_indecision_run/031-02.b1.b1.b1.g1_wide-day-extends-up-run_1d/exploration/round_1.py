import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        grids = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, o, h, l = b["close"], b["open"], b["high"], b["low"]
            rng = (h - l)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w, "day": b["timestamp"].astype(str).str[:10],
                "ts": pd.to_datetime(b["timestamp"]),
                "ret6": c / c.shift(6) - 1,
                "ret20": c / c.shift(20) - 1,
                "ret1": r1,
                "rmult": rng / rng.rolling(20).mean(),
                "cloc": (c - l) / rng.replace(0, np.nan),
                "body": (c - o) / rng.replace(0, np.nan),
                "vol20": r1.rolling(20).std(),
                "fc": b["forecast"],
                "fwd": c.shift(-3) / c - 1,
            })
            df["volrel"] = df["vol20"] / r1.rolling(60, min_periods=30).std()
            g = df.iloc[::3]
            grids.append(g)
        G = pd.concat(grids)
        G = G[G["fwd"].notna()]
        drift = G["fwd"].mean(); usual = G["fwd"].std()
        G["adj"] = G["fwd"] - drift
        G["str"] = G["adj"] / usual
        G["drift"] = drift
        rows.append(G)
    A = pd.concat(rows)
    A["ret6z"] = A["ret6"] / (A["vol20"] * np.sqrt(6))
    A["ret20z"] = A["ret20"] / (A["vol20"] * np.sqrt(20))
    A["ret1z"] = A["ret1"] / A["vol20"]
    A["wd"] = A["ts"].dt.weekday
    A["yr"] = A["ts"].dt.year

    def summ(df, by):
        out = []
        for k, g in df.groupby(by, observed=True):
            x = g["adj"].dropna()
            gg = g.loc[x.index]
            m = x.mean()
            ds = (x - m).groupby(gg["day"]).sum()
            se = np.sqrt((ds ** 2).sum()) / len(x) if len(x) > 1 else np.nan
            out.append({"grp": str(k), "n": len(x), "days": ds.size,
                        "adj%": 100 * m, "t": m / se if se else np.nan,
                        "str": g["str"].mean(), "tot%": 100 * g["fwd"].mean()})
        return pd.DataFrame(out)

    res = {}
    B = A.dropna(subset=["ret6z", "rmult", "cloc"])
    B = B.copy()
    B["q6"] = pd.qcut(B["ret6z"], 5, labels=False)
    B["q20"] = pd.qcut(B["ret20z"], 5, labels=False)
    B["q1"] = pd.qcut(B["ret1z"], 5, labels=False)
    B["qr"] = pd.qcut(B["rmult"], 5, labels=False)
    B["qc"] = pd.qcut(B["cloc"], 3, labels=False)
    B["qv"] = pd.qcut(B["volrel"], 5, labels=False)
    B["up"] = (B["ret6"] > 0).astype(int)
    res["by ret6z quintile"] = summ(B, "q6")
    res["by ret20z quintile"] = summ(B, "q20")
    res["by ret1z quintile"] = summ(B, "q1")
    res["by range mult quintile"] = summ(B, "qr")
    res["up x range quintile"] = summ(B, ["up", "qr"])
    res["up x close-location tercile"] = summ(B, ["up", "qc"])
    res["up x wide(qr4) x cloc"] = summ(B[B["qr"] == 4], ["up", "qc"])
    res["vol rel quintile"] = summ(B, "qv")
    res["weekday"] = summ(B, "wd")
    res["year"] = summ(B, "yr")
    res["coin"] = summ(B, "coin")
    return res
