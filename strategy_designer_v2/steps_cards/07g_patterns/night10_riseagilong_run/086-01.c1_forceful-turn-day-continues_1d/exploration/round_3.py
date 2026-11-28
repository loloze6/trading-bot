def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    for H in [1, 3, 5]:
        rows = []; drift = {}
        for coin, wins in data["bars"].items():
            rr = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c)-H, H):
                    rr.append(c[i+H]/c[i]-1)
            drift[coin] = (np.mean(rr), np.std(rr))
            for w, b in wins.items():
                b = b.reset_index(drop=True).copy()
                c = b["close"]; r1 = c.pct_change()
                vol = r1.rolling(30, min_periods=20).std()
                rng = b["high"]-b["low"]
                b["rngz"] = (rng/c.shift(1))/vol
                b["lrng"] = np.log(b["rngz"])
                b["up"] = r1 > 0
                b["clv"] = (c-b["low"])/rng.replace(0, np.nan)
                down = (r1 < 0).astype(int).values
                run = np.zeros(len(b)); s = 0
                for i in range(len(b)):
                    s = s+1 if down[i] == 1 else 0; run[i] = s
                b["brk"] = (r1 > 0) & (pd.Series(run).shift(1).values >= 2)
                b["inprof"] = b["regime"].isin(["trending", "unknown"])
                b["fwd"] = c.shift(-H)/c-1
                b["pos"] = np.arange(len(b)); b["coin"] = coin; b["win"] = w
                b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
                b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
                rows.append(b[(b["pos"] % H == 0) & b["fwd"].notna()])
        df = pd.concat(rows)
        df["unu"] = df["fwd"]-df["coin"].map(lambda k: drift[k][0])
        df["us"] = df["unu"]/df["coin"].map(lambda k: drift[k][1])
        P = df[df["inprof"]].dropna(subset=["rngz"])
        def cslope(x, col):
            X = np.column_stack([np.ones(len(x)), x[col].values]); y = x["unu"].values
            beta = np.linalg.lstsq(X, y, rcond=None)[0]; e = y-X@beta
            XtXi = np.linalg.inv(X.T@X)
            sc = pd.DataFrame(X*e[:, None]).groupby(x["day"].values).sum().values
            G = len(sc); V = XtXi@(sc.T@sc)@XtXi*G/(G-1)
            return pd.Series({"slope": beta[1], "t_day": beta[1]/np.sqrt(V[1, 1]), "n": len(x), "days": G})
        res = {"all in-profile": cslope(P, "lrng"),
               "up days": cslope(P[P["up"]], "lrng"),
               "up days close top half": cslope(P[P["up"] & (P["clv"] > 0.5)], "lrng"),
               "down days": cslope(P[~P["up"]], "lrng"),
               "break days": cslope(P[P["brk"]], "lrng"),
               "out of profile": cslope(df[~df["inprof"]].dropna(subset=["rngz"]), "lrng")}
        out[f"H{H} log range slope, day-clustered"] = pd.DataFrame(res).T
        if H == 3:
            U = P[P["up"]]
            q = pd.qcut(U["rngz"].rank(method="first"), 3, labels=False)
            out["H3 up days by range tercile"] = U.groupby(q).agg(mean=("unu", "mean"), strength=("us", "mean"), n=("unu", "size"))
            out["H3 up days slope by year"] = U.groupby("yr").apply(lambda x: cslope(x, "lrng") if len(x) > 10 else pd.Series(dtype=float))
            out["H3 up days slope by coin"] = U.groupby("coin").apply(lambda x: cslope(x, "lrng"))
    return out
