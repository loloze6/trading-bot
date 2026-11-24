def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "r": r, "z": r / vol, "vol": vol,
                "nxt": c.shift(-1) / c - 1,
                "n3": c.shift(-3) / c - 1,
                "clpos": (c - l) / (h - l).replace(0, np.nan),
                "rngz": ((h - l) / c) / vol,
                "ret5z": (c / c.shift(5) - 1) / (vol * np.sqrt(5)),
                "fc": b["forecast"].astype(float),
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    drift3 = d[d["pos"] % 3 == 0].groupby("coin")["n3"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d["ex3"] = d["n3"] - d["coin"].map(drift3)
    d["day"] = d["ts"].dt.floor("D")
    d["wnum"] = d["win"].str[1:].astype(int)

    def clt(s, col):
        s = s.dropna(subset=[col]); n = len(s)
        if n < 10: return (np.nan, np.nan, n, np.nan)
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / n
        return (m * 100, m / se, n, s["day"].nunique())

    def clreg(s, ycol, xcols):
        s = s.dropna(subset=[ycol] + xcols)
        X = np.column_stack([np.ones(len(s))] + [s[x].values for x in xcols])
        y = s[ycol].values
        XtXi = np.linalg.inv(X.T @ X)
        b = XtXi @ X.T @ y
        e = y - X @ b
        U = pd.DataFrame(X * e[:, None]).groupby(s["day"].values).sum().values
        G = U.shape[0]; N, K = X.shape
        V = XtXi @ (U.T @ U) @ XtXi * G / (G - 1) * (N - 1) / (N - K)
        se = np.sqrt(np.diag(V))
        return pd.DataFrame({"coef": b, "t": b / se}, index=["const"] + xcols).assign(n=N, days=G)

    d["clc"] = d["clpos"] - 0.5
    out["reg next ex on clpos-0.5 & z (day-clustered)"] = clreg(d, "ex", ["clc", "z"])
    out["reg next ex on clpos, rngz, z"] = clreg(d, "ex", ["clc", "rngz", "z"])
    d["clr"] = d["clc"] * d["rngz"]
    out["reg next ex on clpos x range interaction"] = clreg(d, "ex", ["clc", "clr", "z"])
    g3 = d[d["pos"] % 3 == 0]
    out["reg next-3d ex on clpos, z (grid 3)"] = clreg(g3, "ex3", ["clc", "z"])
    # per coin slope of clpos
    res = []
    for k, s in d.groupby("coin"):
        r_ = clreg(s, "ex", ["clc", "z"])
        res.append({"coin": k, "coef_cl%": r_.loc["clc", "coef"] * 100, "t": r_.loc["clc", "t"], "n": r_["n"].iloc[0]})
    out["clpos slope per coin"] = pd.DataFrame(res)
    d["half"] = np.where(d["wnum"] <= 12, "w1-w12", "w13-w24")
    res = []
    for k, s in d.groupby("half"):
        r_ = clreg(s, "ex", ["clc", "z"])
        res.append({"half": k, "coef_cl%": r_.loc["clc", "coef"] * 100, "t": r_.loc["clc", "t"]})
    out["clpos slope per half"] = pd.DataFrame(res)
    # clpos within up days and down days
    res = []
    for side, s in [("down", d[d["z"] < 0]), ("up", d[d["z"] > 0])]:
        r_ = clreg(s, "ex", ["clc"])
        res.append({"side": side, "coef_cl%": r_.loc["clc", "coef"] * 100, "t": r_.loc["clc", "t"], "n": r_["n"].iloc[0]})
    out["clpos slope on down/up days"] = pd.DataFrame(res)
    # tested idea's slope on z, controlling clpos, among down days
    out["down days: next ex on fall size & clpos"] = clreg(d[d["z"] < 0].assign(fall=lambda x: -x["z"]), "ex", ["fall", "clc"])
    # 5d z continuation per coin
    res = []
    for k, s in d.groupby("coin"):
        r_ = clreg(s, "ex", ["ret5z"])
        res.append({"coin": k, "coef%": r_.loc["ret5z", "coef"] * 100, "t": r_.loc["ret5z", "t"]})
    out["5d z slope per coin"] = pd.DataFrame(res)
    out["5d z slope pooled"] = clreg(d, "ex", ["ret5z", "z"])
    return out
