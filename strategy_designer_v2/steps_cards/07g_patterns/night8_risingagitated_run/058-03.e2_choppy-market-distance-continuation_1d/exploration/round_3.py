def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]).dt.floor("D").astype("int64")})
            vol = r1.rolling(20, min_periods=15).std()
            vol30 = r1.rolling(30, min_periods=25).std()
            d["vol30"] = vol30
            hl = (b["high"] - b["low"]).astype(float)
            d["clpos"] = ((c - b["low"]) / hl.replace(0, np.nan)) - 0.5
            d["rng"] = (hl / c) / vol
            d["ret60"] = c / c.shift(60) - 1
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["f1"] = c.shift(-1) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["ex"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")
    D["agit"] = np.where(D.groupby("coin")["vol30"].rank(pct=True) > 0.5, "agit", "calm")
    D.loc[D.vol30.isna(), "agit"] = "na"
    D["tr"] = np.where(D["ret60"] > 0.10, "rising", np.where(D["ret60"] < -0.10, "falling", np.where(D["ret60"].notna(), "choppy", "na")))

    def clus(df, x, y="ex"):
        df = df[[x, y, "ts"]].dropna()
        if len(df) < 50: return (np.nan, np.nan, len(df), 0)
        X = df[x].values.astype(float)
        Y = df[y].values
        A = np.column_stack([np.ones(len(X)), X])
        beta, *_ = np.linalg.lstsq(A, Y, rcond=None)
        e = Y - A @ beta
        inv = np.linalg.inv(A.T @ A)
        g = pd.DataFrame(A * e[:, None]).groupby(df["ts"].values).sum().values
        G = len(g)
        V = inv @ (g.T @ g) @ inv * G / (G - 1)
        return (beta[1] * 100, beta[1] / np.sqrt(V[1, 1]), len(df), G)

    out = {}
    D["hiX"] = D["clpos"].clip(lower=0) * D["rng"]   # strength of a high close on a wide day
    D["loX"] = (-D["clpos"]).clip(lower=0) * D["rng"]
    res = []
    for nm, S in [("agit_all", D[D.agit == "agit"]), ("calm_all", D[D.agit == "calm"]),
                  ("agit_hiclose_only", D[(D.agit == "agit") & (D.clpos > 0)]),
                  ("calm_hiclose_only", D[(D.agit == "calm") & (D.clpos > 0)]),
                  ("agit_choppy_hi", D[(D.agit == "agit") & (D.tr == "choppy") & (D.clpos > 0)]),
                  ("agit_falling_hi", D[(D.agit == "agit") & (D.tr == "falling") & (D.clpos > 0)]),
                  ("agit_rising_hi", D[(D.agit == "agit") & (D.tr == "rising") & (D.clpos > 0)])]:
        for f in ["hiX", "loX"]:
            s, t, n, g = clus(S, f); res.append({"set": nm, "feat": f, "slope%perunit": s, "t": t, "n": n, "days": g})
    out["graded_hi_lo"] = pd.DataFrame(res).round(3)
    A = D[(D.agit == "agit") & (D.clpos > 0)].copy()
    A["q"] = pd.qcut(A["hiX"], 4, labels=False)
    out["agit_hiclose_quartile_ex1"] = A.groupby("q")["ex"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))]).round(5)
    res = []
    for w, S in A.groupby("win"):
        s, t, n, g = clus(S, "hiX"); res.append({"win": w, "slope%": s, "t": t, "n": n})
    out["agit_hiX_by_window"] = pd.DataFrame(res).round(3)
    res = []
    for cn, S in A.groupby("coin"):
        s, t, n, g = clus(S, "hiX"); res.append({"coin": cn, "slope%": s, "t": t, "n": n})
    out["agit_hiX_by_coin"] = pd.DataFrame(res).round(3)
    return out
