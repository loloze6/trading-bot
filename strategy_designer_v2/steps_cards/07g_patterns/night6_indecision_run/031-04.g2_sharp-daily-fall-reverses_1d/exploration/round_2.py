def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; o = b["open"]; h = b["high"]; l = b["low"]
            r1 = c / c.shift(1) - 1
            vol = r1.rolling(20, min_periods=20).std()
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]), "pos_i": np.arange(len(b))})
            d["z"] = r1 / vol
            d["volrank"] = vol / vol.rolling(60, min_periods=20).mean()
            d["rngz"] = ((h - l) / c) / vol
            d["clv"] = ((c - l) / (h - l)).where(h > l)
            d["f1"] = c.shift(-1) / c - 1
            d["vol"] = vol
            d["alloc"] = b["postRebalance_current_allocation"].values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["yr"] = D["ts"].dt.year
    m = D.groupby("coin")["f1"].mean()
    D["e1"] = D["f1"] - D["coin"].map(m)
    D["e1s"] = D["e1"] / D["vol"]
    D["clvc"] = 0.5 - D["clv"]  # positive = close near low

    def ols_cl(s, ycol, xcols):
        s = s.dropna(subset=[ycol] + xcols)
        X = np.column_stack([np.ones(len(s))] + [s[x].values for x in xcols])
        y = s[ycol].values
        XtX = np.linalg.inv(X.T @ X)
        beta = XtX @ X.T @ y
        u = y - X @ beta
        g = pd.DataFrame(X * u[:, None]).groupby(s["day"].values).sum().values
        G = len(g); n, k = X.shape
        V = XtX @ (g.T @ g) @ XtX * G / (G - 1) * (n - 1) / (n - k)
        t = beta / np.sqrt(np.diag(V))
        return pd.DataFrame({"beta": beta, "t": t}, index=["const"] + xcols).assign(n=n, days=G)

    res = {}
    D["zneg"] = (-D["z"]).clip(lower=0)
    D["zpos"] = D["z"].clip(lower=0)
    res["all days: e1s on clv-centred, zneg, zpos"] = ols_cl(D, "e1s", ["clvc", "zneg", "zpos"])
    res["all days: e1s on clvc only"] = ols_cl(D, "e1s", ["clvc"])
    D["lvr"] = np.log(D["volrank"])
    D["zneg_x_lvr"] = D["zneg"] * D["lvr"]
    res["falls: e1 (raw) on zneg, lvr, zneg*lvr"] = ols_cl(D[D["z"] < 0], "e1", ["zneg", "lvr", "zneg_x_lvr"])
    D["clvc_x_lvr"] = D["clvc"] * D["lvr"]
    res["all: e1 on clvc, lvr, clvc*lvr"] = ols_cl(D, "e1", ["clvc", "lvr", "clvc_x_lvr"])
    D["clvc_x_rng"] = D["clvc"] * np.log(D["rngz"])
    D["lrng"] = np.log(D["rngz"])
    res["all: e1s on clvc, lrng, clvc*lrng"] = ols_cl(D.replace([np.inf, -np.inf], np.nan), "e1s", ["clvc", "lrng", "clvc_x_rng"])
    # stability of clv effect by year and by coin
    out = {}
    for y, s in D.groupby("yr"):
        r = ols_cl(s, "e1s", ["clvc"]); out[str(y)] = r.loc["clvc", ["beta", "t", "n"]]
    for cn, s in D.groupby("coin"):
        r = ols_cl(s, "e1s", ["clvc"]); out[cn] = r.loc["clvc", ["beta", "t", "n"]]
    res["clvc slope by year and coin"] = pd.DataFrame(out).T
    out = {}
    F = D[D["z"] < 0].copy()
    F["vb"] = pd.qcut(F["volrank"], 3, labels=["low", "mid", "high"])
    for y, s in F.groupby("yr"):
        hv = s[s["vb"] == "high"]; r = ols_cl(hv, "e1", ["zneg"]); out[str(y)] = r.loc["zneg", ["beta", "t", "n"]]
    res["high-vol falls slope by year"] = pd.DataFrame(out).T
    # book: largest gain/loss days context
    bk = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            x = dd[["day", "book_return", "coin_return"]].copy(); x["coin"] = coin; bk.append(x)
    B = pd.concat(bk).dropna()
    B["prev_cr"] = B.groupby("coin")["coin_return"].shift(1)
    q = B["book_return"].quantile([0.01, 0.99])
    res["book coin-days worst 1% vs best 1%"] = pd.DataFrame({
        "worst": B[B["book_return"] <= q.iloc[0]][["coin_return", "prev_cr"]].mean(),
        "best": B[B["book_return"] >= q.iloc[1]][["coin_return", "prev_cr"]].mean()})
    return res
