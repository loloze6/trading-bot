def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"]; h = df["high"]; l = df["low"]; o = df["open"]
            r1 = c.pct_change()
            v30 = r1.rolling(30).std()
            feat = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(df["timestamp"]),
                "rec": (df["regime"] == "unknown").astype(int),
                "tr60": c / c.shift(60) - 1,
                "calm": (v30 <= v30.expanding(60).median()).astype(float).where(v30.expanding(60).count() >= 60),
                "ret1": r1, "ret3p": c / c.shift(3) - 1, "ret5p": c / c.shift(5) - 1,
                "clv": ((c - l) / (h - l)).where(h > l),
                "depth": ((c - h.rolling(20).max()) / h.rolling(20).max()) / r1.rolling(20).std(),
                "uplow": ((c - l.rolling(20).min()) / l.rolling(20).min()) / r1.rolling(20).std(),
                "rng_vol": ((h - l) / c) / r1.rolling(20).std(),
            })
            for hz in (1, 3, 5):
                feat[f"f{hz}"] = c.shift(-hz) / c - 1
            feat["pos"] = np.arange(len(df))
            rows.append(feat)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    A["fall"] = (A["tr60"] < -0.10).astype(int)
    out = {}
    out["recorded_vs_rebuilt"] = pd.crosstab(A["rec"], [A["fall"], A["calm"].fillna(-1)])
    def clust_t(G, x, y="ex"):
        d = G[[x, y, "day"]].dropna()
        if len(d) < 30: return np.nan, np.nan, len(d)
        X = d[x] - d[x].mean(); b = (X * d[y]).sum() / (X**2).sum()
        e = d[y] - d[y].mean() - b * X
        s = (X * e).groupby(d["day"]).sum(); g = len(s)
        se = np.sqrt((s**2).sum() * g / (g - 1)) / (X**2).sum()
        return b, b / se, len(d)
    res = []
    for hz in (1, 3, 5):
        G = A[A["pos"] % hz == 0].copy()
        mu = G.groupby("coin")[f"f{hz}"].mean()
        G["ex"] = G[f"f{hz}"] - G["coin"].map(mu)
        for lab, P in [("fall", G[G["fall"] == 1]), ("fallcalm", G[(G["fall"] == 1) & (G["calm"] == 1)])]:
            for f in ["ret1", "ret3p", "ret5p", "clv", "depth", "uplow", "rng_vol"]:
                b, t, n = clust_t(P, f)
                res.append({"set": lab, "hz": hz, "feat": f, "t": round(t, 2), "n": n})
            if hz == 3:
                out[f"{lab}_mean_ex3"] = float(P["ex"].mean()); out[f"{lab}_n3"] = len(P)
    out["slopes_rebuilt"] = pd.DataFrame(res).pivot_table(index=["set", "feat"], columns="hz", values="t")
    # book's largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x["coin"] = coin; dd.append(x)
    D = pd.concat(dd, ignore_index=True).dropna(subset=["book_return"])
    D = D[D["book_return"] != 0]
    q = D["book_return"].quantile([0.05, 0.95])
    out["active_days"] = len(D)
    out["top5pct_sum"] = float(D[D["book_return"] >= q[0.95]]["book_return"].sum())
    out["bot5pct_sum"] = float(D[D["book_return"] <= q[0.05]]["book_return"].sum())
    out["all_sum"] = float(D["book_return"].sum())
    out["coin_ret_on_top_bot"] = pd.Series({
        "coin_ret_top": D[D["book_return"] >= q[0.95]]["coin_return"].mean(),
        "coin_ret_bot": D[D["book_return"] <= q[0.05]]["coin_return"].mean()})
    return out
