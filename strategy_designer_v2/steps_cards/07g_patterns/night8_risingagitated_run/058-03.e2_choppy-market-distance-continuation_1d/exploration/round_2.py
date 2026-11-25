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
            d["pos"] = np.arange(len(b))
            vol = r1.rolling(20, min_periods=15).std()
            vol30 = r1.rolling(30, min_periods=25).std()
            d["vol"] = vol; d["vol30"] = vol30
            hl = (b["high"] - b["low"]).astype(float)
            d["clpos"] = ((c - b["low"]) / hl.replace(0, np.nan)) - 0.5
            d["rng"] = (hl / c) / vol
            d["r1s"] = r1 / vol
            d["ret60"] = c / c.shift(60) - 1
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            for h in (1, 2, 3):
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["agit"] = np.where(D.groupby("coin")["vol30"].rank(pct=True) > 0.5, "agit", "calm")
    D.loc[D.vol30.isna(), "agit"] = "na"
    D["tr"] = np.where(D["ret60"] > 0.10, "rising", np.where(D["ret60"] < -0.10, "falling", np.where(D["ret60"].notna(), "choppy", "na")))

    def clus(df, x, y):
        df = df[[x, y, "ts"]].dropna()
        if len(df) < 50: return (np.nan, np.nan, len(df), 0)
        X = df[x].values; X = (X - X.mean()) / X.std()
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
    for h in (1, 2):
        G = D[D["pos"] % h == 0].copy()
        G["ex"] = G[f"f{h}"] - G.groupby("coin")[f"f{h}"].transform("mean")
        # graded clpos interacted with range (wide day with high close)
        G["clxr"] = G["clpos"] * G["rng"]
        res = []
        for f in ["clpos", "clxr", "r1s"]:
            for (tr, ag), S in G.groupby(["tr", "agit"]):
                if tr == "na" or ag == "na": continue
                s, t, n, g = clus(S, f, "ex")
                res.append({"feat": f, "tr": tr, "ag": ag, "slope%": s, "t": t, "n": n, "days": g})
            for tr, S in G.groupby("tr"):
                if tr == "na": continue
                s, t, n, g = clus(S, f, "ex")
                res.append({"feat": f, "tr": tr, "ag": "any", "slope%": s, "t": t, "n": n, "days": g})
        out[f"h{h}_by_profile"] = pd.DataFrame(res).round(3)
        if h == 1:
            res = []
            for w, S in G.groupby("win"):
                s, t, n, g = clus(S, "clpos", "ex"); res.append({"win": w, "clpos_slope%": s, "t": t, "n": n})
            out["h1_clpos_by_window"] = pd.DataFrame(res).round(3)
            res = []
            for cn, S in G.groupby("coin"):
                s, t, n, g = clus(S, "clpos", "ex"); res.append({"coin": cn, "clpos_slope%": s, "t": t, "n": n})
            out["h1_clpos_by_coin"] = pd.DataFrame(res).round(3)
            G["q"] = pd.qcut(G["clpos"], 5, labels=False)
            out["h1_ex_by_clpos_quintile"] = G.groupby("q")["ex"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))]).round(5)
            G["rq"] = pd.qcut(G["rng"], 3, labels=False)
            G["hi"] = np.where(G.clpos > 0, "highclose", "lowclose")
            out["h1_ex_by_range_tercile_and_close_side"] = G.groupby(["rq", "hi"])["ex"].agg(["mean", "count"]).round(5)
            wd = G.groupby(["tr", "wd"])["f1"].agg(["mean", "count"])
            out["weekday_by_trend_f1"] = wd.unstack(0).round(4)
    return out
