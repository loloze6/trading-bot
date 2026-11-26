import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            o = b["open"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": c / c.shift(1) - 1,
                "s4": c.shift(1) / c.shift(5) - 1,
                "s10": c / c.shift(10) - 1,
                "nxt": c.shift(-1) / c - 1,
                "nxt3": c.shift(-3) / c - 1,
                "pos": b["postRebalance_current_allocation"].astype(float),
                "inprof": (b["regime"] == "unknown").astype(int),
                "fc": b["forecast"].astype(float),
                "clpos": (c - l) / (h - l).replace(0, np.nan),
                "rng": (h - l) / c.shift(1),
            })
            d["vol20"] = d["r1"].rolling(20).std()
            d["pos3"] = (np.arange(len(d)) % 3 == 0)
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    A["wd"] = A["ts"].dt.dayofweek
    A["year"] = A["ts"].dt.year
    drift = A.groupby("coin")["nxt"].mean()
    A["ex"] = A["nxt"] - A["coin"].map(drift)
    sd = A.groupby("coin")["nxt"].std()
    A["z1"] = A["r1"] / A["coin"].map(sd)
    A["zs4"] = A["s4"] / (A["coin"].map(sd) * 2)

    def dt(g, col="ex"):
        g = g.dropna(subset=[col])
        m = g.groupby("day")[col].sum()
        n = len(g)
        if n < 5: return pd.Series({"n": n, "days": len(m), "mean%": np.nan, "t": np.nan})
        mean = g[col].mean()
        se = np.sqrt(((m - g.groupby("day").size() * mean) ** 2).sum()) / n
        return pd.Series({"n": n, "days": len(m), "mean%": 100 * mean, "t": mean / se if se > 0 else np.nan})

    out = {}
    A["s4q"] = pd.qcut(A["zs4"], 5, labels=False)
    A["r1q"] = pd.qcut(A["z1"], 5, labels=False)
    out["by_slide_quintile_x_profile"] = A.groupby(["inprof", "s4q"]).apply(dt)
    out["by_lastday_quintile_x_profile"] = A.groupby(["inprof", "r1q"]).apply(dt)
    out["inprof_lastday_x_slide_(lo/hi)"] = A[A.inprof == 1].assign(
        s=lambda x: x.zs4 < x.zs4.median(), r=lambda x: x.z1 < x.z1.median()).groupby(["s", "r"]).apply(dt)
    out["weekday_x_profile"] = A.groupby(["inprof", "wd"]).apply(dt)
    A["volq"] = A.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["vol_tercile_x_profile"] = A.groupby(["inprof", "volq"]).apply(dt)
    A["clq"] = pd.cut(A["clpos"], [0, .2, .4, .6, .8, 1.0001], labels=False, include_lowest=True)
    out["closepos_x_profile"] = A.groupby(["inprof", "clq"]).apply(dt)
    A["s10q"] = pd.qcut(A["s10"], 5, labels=False)
    out["10d_return_quintile_x_profile"] = A.groupby(["inprof", "s10q"]).apply(dt)
    G = A[A.pos3].copy(); G["ex3"] = G["nxt3"] - G["coin"].map(A.groupby("coin")["nxt3"].mean())
    out["3d_after_slide_quintile_inprof"] = G[G.inprof == 1].groupby("s4q").apply(lambda g: dt(g, "ex3"))
    out["inprof_by_year"] = A[A.inprof == 1].groupby("year").apply(dt)
    out["share_inprof"] = float(A.inprof.mean())
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D)
    bk = D.groupby("day")["book_return"].mean().dropna()
    out["book_days_top_bottom"] = pd.Series({
        "n_days": len(bk), "mean%": 100 * bk.mean(),
        "top10_sum%": 100 * bk.nlargest(10).sum(), "bot10_sum%": 100 * bk.nsmallest(10).sum(),
        "share_total_from_top10": bk.nlargest(10).sum() / bk.sum()})
    return out
