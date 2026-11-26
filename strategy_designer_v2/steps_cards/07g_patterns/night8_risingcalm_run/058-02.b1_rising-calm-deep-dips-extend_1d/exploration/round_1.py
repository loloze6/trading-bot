def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            hi5 = c.rolling(5).max()
            pb = (c - hi5) / hi5 / sd30
            ret5 = c.pct_change(5)
            ret60 = c / c.shift(60) - 1 if len(c) > 60 else pd.Series(np.nan, index=c.index)
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            g = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)),
                              "rc": (df["regime"] == "unknown").astype(int),
                              "pb": pb, "r1z": r1 / sd30, "ret5z": ret5 / (sd30 * np.sqrt(5)),
                              "sd30": sd30, "ret60": ret60, "fwd5": fwd5, "fwd1": fwd1,
                              "wd": ts.dt.weekday, "day": ts.dt.floor("D"),
                              "alloc": df["postRebalance_current_allocation"].astype(float)})
            rows.append(g)
    A = pd.concat(rows, ignore_index=True)
    drift5 = A.groupby("coin")["fwd5"].apply(lambda s: s[A.loc[s.index, "pos"] % 5 == 0].mean())
    drift1 = A.groupby("coin")["fwd1"].mean()
    A["ex5"] = A["fwd5"] - A["coin"].map(drift5)
    A["ex1"] = A["fwd1"] - A["coin"].map(drift1)
    G = A[(A["pos"] % 5 == 0)].dropna(subset=["ex5"])
    out = {}
    def summ(df, key, col="ex5"):
        t = df.groupby(key)[col].agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.round(4)
    Gp = G.dropna(subset=["pb"]).copy()
    Gp["pbq"] = pd.qcut(Gp["pb"], 5, labels=False, duplicates="drop")
    out["pb quintile x regime (ex5)"] = summ(Gp, ["rc", "pbq"])
    Gz = G.dropna(subset=["r1z"]).copy()
    Gz["r1q"] = pd.qcut(Gz["r1z"], 5, labels=False)
    out["1d move z quintile x regime (ex5)"] = summ(Gz, ["rc", "r1q"])
    Gr = G.dropna(subset=["ret5z"]).copy()
    Gr["r5q"] = pd.qcut(Gr["ret5z"], 5, labels=False)
    out["5d ret z quintile (ex5) all"] = summ(Gr, "r5q")
    Gv = G.dropna(subset=["sd30"]).copy()
    Gv["volq"] = Gv.groupby("coin")["sd30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["vol tercile in coin (ex5)"] = summ(Gv, "volq")
    G6 = G.dropna(subset=["ret60"]).copy()
    G6["trend"] = np.where(G6["ret60"] > 0.1, "rising", np.where(G6["ret60"] < -0.1, "falling", "choppy"))
    out["trend60 (ex5)"] = summ(G6, "trend")
    out["weekday (ex1, all bars)"] = summ(A.dropna(subset=["ex1"]), "wd", "ex1")
    Az = A.dropna(subset=["r1z", "ex1"]).copy()
    Az["r1q"] = pd.qcut(Az["r1z"], 5, labels=False)
    out["1d move z quintile -> next day ex1"] = summ(Az, "r1q", "ex1")
    out["share rising calm"] = float(A["rc"].mean())
    out["share in position"] = float((A["alloc"].abs() > 1e-6).mean())
    return out
