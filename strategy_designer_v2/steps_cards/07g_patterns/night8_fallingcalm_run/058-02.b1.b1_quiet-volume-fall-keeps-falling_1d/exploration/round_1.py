def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            b["fwd5"] = c.shift(-5) / c - 1
            b["ret30"] = c / c.shift(30) - 1
            b["ret60"] = c / c.shift(60) - 1
            b["ret1"] = r1
            b["ret5"] = c / c.shift(5) - 1
            b["std30"] = r1.rolling(30).std()
            b["std10"] = r1.rolling(10).std()
            b["vr"] = np.log(v.rolling(10).mean() / v.rolling(60).mean())
            b["vr5"] = np.log(v.rolling(5).mean() / v.rolling(30).mean())
            b["rawvol"] = b.get("debug_info.components.quiet_volume.last_history_value")
            b["coin"] = coin; b["win"] = w
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            g = b.iloc[::5].copy()
            rows.append(g)
    G = pd.concat(rows, ignore_index=True)
    G = G[G["fwd5"].notna()]
    drift = G.groupby("coin")["fwd5"].mean()
    usual = G.groupby("coin")["fwd5"].std()
    G["adj"] = G["fwd5"] - G["coin"].map(drift)
    G["z1"] = G["ret1"] / G["std30"]
    G["z30"] = G["ret30"] / (G["std30"] * np.sqrt(30))

    def st(x, days):
        x = pd.Series(x).astype(float); d = pd.Series(days).values
        m = x.mean(); n = len(x)
        if n < 5: return pd.Series({"n": n, "mean%": np.nan, "t": np.nan, "days": 0})
        s = (x - m).groupby(d).sum()
        se = np.sqrt((s ** 2).sum()) / n
        return pd.Series({"n": n, "mean%": 100 * m, "t": m / se if se > 0 else np.nan, "days": len(s)})

    def tab(df, key):
        return df.groupby(key, observed=True).apply(lambda q: st(q["adj"], q["day"]))

    out = {}
    T = G[G["regime"] == "trending"].copy()
    T["fb"] = pd.cut(T["forecast"], [-21, -10, -5, -2, -0.01, 0.01])
    out["fall regime: adj fwd5 by forecast"] = tab(T, "fb")
    T["dq"] = pd.qcut(T["ret30"], 5, labels=False)
    out["fall regime: adj fwd5 by 30d return quintile (0=deepest)"] = tab(T, "dq")
    T["vq"] = pd.qcut(T["vr"], 3, labels=False)
    out["fall regime: depth tercile x short vol ratio tercile"] = T.assign(dt=pd.qcut(T["ret30"], 3, labels=False)).groupby(["dt", "vq"]).apply(lambda q: st(q["adj"], q["day"]))
    A = G[G["ret60"].notna()].copy()
    A["trend"] = np.where(A["ret60"] > 0.10, "rising", np.where(A["ret60"] < -0.10, "falling", "choppy"))
    out["all: adj fwd5 by 60d trend"] = tab(A, "trend")
    A["zq"] = pd.qcut(A["z1"], 5, labels=False)
    out["all: adj fwd5 by 1d move z quintile"] = tab(A, "zq")
    A["z30q"] = pd.qcut(A["z30"], 5, labels=False)
    out["all: adj fwd5 by 30d scaled return quintile, by trend"] = A.groupby(["trend", "z30q"]).apply(lambda q: st(q["adj"], q["day"]))
    A["volq"] = pd.qcut(A["std10"] / A["std30"], 3, labels=False)
    out["all: adj fwd5 by 10d/30d vol ratio tercile"] = tab(A, "volq")
    A["vrq"] = pd.qcut(A["vr5"], 5, labels=False)
    out["all: adj fwd5 by 5d/30d volume ratio quintile"] = tab(A, "vrq")
    # weekday on daily returns
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; D.append(dd)
    D = pd.concat(D, ignore_index=True)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    D["adj"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    out["daily coin return by weekday"] = D.dropna(subset=["adj"]).groupby("wd").apply(lambda q: st(q["adj"], q["day"]))
    out["book return by weekday (mean% ,n)"] = D.dropna(subset=["book_return"]).groupby("wd")["book_return"].agg(["mean", "count"]) * [100, 1]
    return out
