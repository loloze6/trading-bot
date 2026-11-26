def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    recs = []
    for coin in bars:
        drift = {}
        for h in [5, 10, 20]:
            vals = []
            for w, df in bars[coin].items():
                c = df.sort_values("timestamp")["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals += list(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(vals)
        for w, df in bars[coin].items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values; n = len(c); s = pd.Series(c)
            r1 = s.pct_change()
            vol = r1.rolling(60, min_periods=30).std()
            up = np.r_[False, c[1:] > c[:-1]]
            streak = np.zeros(n, int)
            for i in range(1, n):
                streak[i] = streak[i-1] + 1 if up[i] else 0
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n),
                              "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                              "year": pd.to_datetime(df["timestamp"]).dt.year,
                              "alloc": df["postRebalance_current_allocation"].fillna(0).values,
                              "streak": streak})
            for L in [10, 30, 60, 90]:
                d[f"m{L}"] = (s.pct_change(L) / (vol * np.sqrt(L))).values
            d["ret30"] = s.pct_change(30).values
            d["r1n"] = np.r_[c[1:] / c[:-1] - 1, np.nan]
            for h in [5, 10, 20]:
                f = np.full(n, np.nan); f[:n-h] = c[h:] / c[:n-h] - 1
                d[f"u{h}"] = f - drift[h]
                d[f"usd{h}"] = d[f"u{h}"] / (vol.values * np.sqrt(h))
            recs.append(d)
    A = pd.concat(recs, ignore_index=True)

    def clt(x, k):
        x = np.asarray(x, float); m = x.mean(); n = len(x)
        s = pd.Series(x - m).groupby(np.asarray(k)).sum(); G = len(s)
        return m, m / (np.sqrt(G / (G - 1) * (s ** 2).sum()) / n), n, G

    def clslope(y, X, k):
        X = np.column_stack([np.ones(len(y))] + [np.asarray(v, float) for v in X]); y = np.asarray(y, float)
        XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ y; e = y - X @ b
        sc = pd.DataFrame(X * e[:, None]).groupby(np.asarray(k)).sum().values
        V = XtX @ (sc.T @ sc) @ XtX
        return b, b / np.sqrt(np.diag(V))
    out = {}
    rows = []
    for h in [5, 10, 20]:
        for L in [10, 30, 60, 90]:
            G_ = A[A["pos"] % h == 0].dropna(subset=[f"m{L}", f"usd{h}"])
            b, t = clslope(G_[f"usd{h}"], [G_[f"m{L}"]], G_["day"])
            # long-side: positive momentum only, graded
            P = G_[G_[f"m{L}"] > 0]
            bp, tp = clslope(P[f"usd{h}"], [P[f"m{L}"]], P["day"])
            m, tm, n, nd = clt(P[f"u{h}"], P["day"])
            rows.append({"h": h, "L": L, "slope_all": b[1], "t_all": t[1], "n": len(G_),
                         "slope_pos": bp[1], "t_pos": tp[1], "unusual_pos": m, "t_mean_pos": tm, "n_pos": n, "days_pos": nd})
    out["vol-scaled momentum -> vol-scaled unusual move"] = pd.DataFrame(rows)
    rows = []
    for h in [5, 10]:
        G_ = A[(A["pos"] % h == 0) & (A["ret30"] > 0)].dropna(subset=["m30", f"usd{h}"])
        b, t = clslope(G_[f"usd{h}"], [G_["m30"], G_["streak"].clip(upper=6)], G_["day"])
        rows.append({"h": h, "b_m30": b[1], "t_m30": t[1], "b_streak": b[2], "t_streak": t[2], "n": len(G_)})
    out["ret30>0: joint m30 + streak"] = pd.DataFrame(rows)
    # quintile of m30, 10d
    G_ = A[A["pos"] % 10 == 0].dropna(subset=["m30", "u10"]).copy()
    G_["q"] = pd.qcut(G_["m30"], 5, labels=False)
    out["m30 quintile -> unusual 10d"] = pd.DataFrame([dict(zip(["mean", "t", "n", "days"], clt(s["u10"], s["day"])), q=q, m30=s["m30"].mean()) for q, s in G_.groupby("q")])
    # by year: m30 slope at 10d, and book in-position gain by year from timing
    rows = []
    for y, s in G_.groupby("year"):
        if len(s) > 50:
            b, t = clslope(s["usd10"], [s["m30"]], s["day"]); rows.append({"year": y, "slope": b[1], "t": t[1], "n": len(s)})
    out["m30 slope 10d by year"] = pd.DataFrame(rows)
    # book: gain on days held vs counterfactual 'held whenever ret30>0'
    A["g"] = A["alloc"] * A["r1n"]
    A["cf"] = (A["ret30"] > 0) * A["r1n"]
    d = A.dropna(subset=["r1n"]).groupby("day")[["g", "cf"]].mean()
    out["book gain vs held-when-ret30>0 unit"] = pd.Series({"book": d["g"].mean(), "cf": d["cf"].mean(), "corr": d["g"].corr(d["cf"])})
    return out
