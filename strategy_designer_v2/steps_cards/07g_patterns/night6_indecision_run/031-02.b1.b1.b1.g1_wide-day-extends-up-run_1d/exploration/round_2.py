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
                "coin": coin, "win": w, "day": b["timestamp"].astype(str).str[:10].values,
                "ts": pd.to_datetime(b["timestamp"]).values,
                "ret6": (c / c.shift(6) - 1).values,
                "ret20": (c / c.shift(20) - 1).values,
                "ret1": r1.values,
                "rmult": (rng / rng.rolling(20).mean()).values,
                "cloc": ((c - l) / rng.replace(0, np.nan)).values,
                "absbody": ((c - o).abs() / rng.replace(0, np.nan)).values,
                "vol20": r1.rolling(20).std().values,
                "volrel": (r1.rolling(20).std() / r1.rolling(60, min_periods=30).std()).values,
                "fc": b["forecast"].values,
                "alloc": b["postRebalance_current_allocation"].values,
                "fwd": (c.shift(-3) / c - 1).values,
            })
            grids.append(df.iloc[::3])
        G = pd.concat(grids, ignore_index=True)
        G = G[G["fwd"].notna()].copy()
        drift = G["fwd"].mean(); usual = G["fwd"].std()
        G["adj"] = G["fwd"] - drift
        G["str"] = G["adj"] / usual
        rows.append(G)
    A = pd.concat(rows, ignore_index=True)
    A["ret6z"] = A["ret6"] / (A["vol20"] * np.sqrt(6))
    A["ret20z"] = A["ret20"] / (A["vol20"] * np.sqrt(20))
    A["ret1z"] = A["ret1"] / A["vol20"]
    A["wd"] = pd.to_datetime(A["ts"]).dt.weekday
    A["yr"] = pd.to_datetime(A["ts"]).dt.year

    def summ(df, by):
        out = []
        for k, g in df.groupby(by, observed=True):
            g = g[g["adj"].notna()]
            x = g["adj"].values
            if len(x) < 2: continue
            m = x.mean()
            ds = pd.Series(x - m).groupby(g["day"].values).sum()
            se = np.sqrt((ds ** 2).sum()) / len(x)
            out.append({"grp": str(k), "n": len(x), "days": ds.size,
                        "adj%": round(100 * m, 3), "t": round(m / se, 2) if se > 0 else np.nan,
                        "str": round(g["str"].mean(), 4), "tot%": round(100 * g["fwd"].mean(), 3)})
        return pd.DataFrame(out)

    res = {}
    B = A.dropna(subset=["ret6z", "rmult", "cloc", "ret20z", "ret1z"]).copy()
    B["q6"] = pd.qcut(B["ret6z"], 5, labels=False)
    B["q20"] = pd.qcut(B["ret20z"], 5, labels=False)
    B["q1"] = pd.qcut(B["ret1z"], 5, labels=False)
    B["qr"] = pd.qcut(B["rmult"], 5, labels=False)
    B["qr3"] = pd.qcut(B["rmult"], 3, labels=False)
    B["qc"] = pd.qcut(B["cloc"], 3, labels=False)
    B["qb"] = pd.qcut(B["absbody"], 3, labels=False)
    B["qv"] = pd.qcut(B["volrel"], 5, labels=False)
    B["up"] = (B["ret6"] > 0).astype(int)
    res["ret6z quintile"] = summ(B, "q6")
    res["ret20z quintile"] = summ(B, "q20")
    res["ret1z quintile"] = summ(B, "q1")
    res["range mult quintile"] = summ(B, "qr")
    res["up x range quintile"] = summ(B, ["up", "qr"])
    res["up x close-location tercile"] = summ(B, ["up", "qc"])
    res["up x range3 x absbody3"] = summ(B, ["up", "qr3", "qb"])
    res["up x range3 x cloc3"] = summ(B, ["up", "qr3", "qc"])
    res["vol rel quintile"] = summ(B, "qv")
    res["up x volrel quintile"] = summ(B, ["up", "qv"])
    res["weekday"] = summ(B, "wd")
    res["year"] = summ(B, "yr")

    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            dd.append(d)
    D = pd.concat(dd, ignore_index=True)
    D["day"] = pd.to_datetime(D["day"])
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    bk["wd"] = bk["day"].dt.weekday
    bk["yr"] = bk["day"].dt.year
    res["book by weekday"] = bk.groupby("wd")[["book_return", "coin_return"]].agg(["mean", "count"]).round(5)
    res["book by year"] = bk.groupby("yr")[["book_return", "coin_return"]].mean().round(5)
    s = bk["book_return"].sort_values(ascending=False).values
    tot = s.sum()
    res["book gain share top 5% days"] = round(s[: len(s) // 20].sum() / tot, 3)
    res["book gain share bottom 5% days"] = round(s[-len(s) // 20:].sum() / tot, 3)
    bk["cq"] = pd.qcut(bk["coin_return"], 5, labels=False)
    res["book by market day quintile"] = bk.groupby("cq")[["book_return", "coin_return"]].mean().round(5)
    return res
