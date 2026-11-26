def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l)
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ret1": c / c.shift(1) - 1,
                "ret5": c / c.shift(5) - 1,
                "ret20": c / c.shift(20) - 1,
                "rm": rng / rng.rolling(20).mean().shift(1),
                "body": (c - o) / rng.replace(0, np.nan),
                "cloc": (c - l) / rng.replace(0, np.nan),
                "vol20": c.pct_change().rolling(20).std(),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    dr1 = D.groupby("coin")["f1"].mean()
    g3 = D[D["pos"] % 3 == 0]
    dr3 = g3.groupby("coin")["f3"].mean()
    D["u1"] = D["f1"] - D["coin"].map(dr1)
    D["u3"] = D["f3"] - D["coin"].map(dr3)
    D["vrank"] = D.groupby("coin")["vol20"].rank(pct=True)
    G = D[D["pos"] % 3 == 0].copy()

    def tab(df, col, key, q=5):
        df = df.dropna(subset=[col, key]).copy()
        df["b"] = pd.qcut(df[key].rank(method="first"), q, labels=False)
        a = df.groupby("b")[col].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["keymean"] = df.groupby("b")[key].mean()
        return a.drop(columns="std").round(5)

    out = {}
    out["u3 by ret5 quintile"] = tab(G, "u3", "ret5")
    out["u3 by ret20 quintile"] = tab(G, "u3", "ret20")
    out["u3 by range multiple"] = tab(G, "u3", "rm")
    out["u3 by close location"] = tab(G, "u3", "cloc")
    out["u3 by vol rank"] = tab(G, "u3", "vrank")
    out["u1 by ret1 quintile"] = tab(D, "u1", "ret1", 10)
    # brief's own: after 5d run, flat wide day, move against run
    R = G.dropna(subset=["ret5", "rm", "body", "u3"]).copy()
    R["sgn"] = np.sign(R["ret5"])
    R["against"] = -R["sgn"] * R["u3"]
    R["flat"] = R["body"].abs() < 0.3
    Rf = R[R["flat"]]
    out["flat days: against-run u3 by rm"] = tab(Rf, "against", "rm", 3)
    Rn = R[~R["flat"]]
    out["nonflat days: against-run u3 by rm"] = tab(Rn, "against", "rm", 3)
    # signed body direction after wide days
    W = R[R["rm"] > R["rm"].quantile(0.8)].copy()
    W["sb"] = np.sign(W["body"])
    out["wide days u3 by body sign"] = W.groupby("sb")["u3"].agg(["mean", "count"]).round(5)
    # weekday
    a = D.groupby("wd")["u1"].agg(["mean", "count", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["u1 by weekday"] = a.drop(columns="std").round(5)
    # forecast-held vs not
    G["held"] = G["alloc"].abs() > 1e-6
    out["u3 by held"] = G.groupby("held")["u3"].agg(["mean", "count"]).round(5)
    out["u3 held, by fc quintile"] = tab(G[G["held"]], "u3", "fc")
    # by year
    out["u3 by year, ret5 top quintile"] = G[G["ret5"] > G["ret5"].quantile(0.8)].groupby("yr")["u3"].agg(["mean", "count"]).round(4)
    return out
