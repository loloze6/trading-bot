def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]

    def grid_cases(h, featfun):
        rows = []
        for coin, ws in bars.items():
            # drift over grid of all windows
            fr_all = []
            per = []
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                n = len(c)
                feats = featfun(df)
                for i in range(0, n - h, h):
                    r = c[i + h] / c[i] - 1
                    fr_all.append(r)
                    d = {"coin": coin, "w": w, "day": str(pd.Timestamp(df["timestamp"].iloc[i]).date()), "r": r,
                         "wd": pd.Timestamp(df["timestamp"].iloc[i]).weekday(),
                         "yr": pd.Timestamp(df["timestamp"].iloc[i]).year}
                    for k, v in feats.items():
                        d[k] = v[i]
                    per.append(d)
            if not fr_all:
                continue
            drift = np.mean(fr_all); sd = np.std(fr_all, ddof=1)
            for d in per:
                d["ex"] = d["r"] - drift
                d["exz"] = (d["r"] - drift) / sd if sd > 0 else np.nan
            rows += per
        return pd.DataFrame(rows)

    def feats(df):
        c = df["close"]
        lr = np.log(c).diff()
        f = {}
        f["ret5"] = (c / c.shift(5) - 1).values
        f["ret10"] = (c / c.shift(10) - 1).values
        f["ret20"] = (c / c.shift(20) - 1).values
        f["ret1"] = (c / c.shift(1) - 1).values
        f["vol20"] = lr.rolling(20).std().values
        f["rng20"] = ((c - c.rolling(20).min()) / (c.rolling(20).max() - c.rolling(20).min())).values
        col = "debug_info.components.low_prox.last_history_value"
        f["lowprox"] = df[col].values if col in df else np.full(len(df), np.nan)
        f["fc"] = df["forecast"].values
        f["alloc"] = df["postRebalance_current_allocation"].values
        return f

    def clustered_t(g):
        s = g.groupby("day")["exz"].sum()
        nd = len(s); n = g["exz"].notna().sum()
        m = g["exz"].mean()
        if nd < 3: return np.nan
        se = np.sqrt((s - g.groupby("day")["exz"].count() * m).pow(2).sum()) / n
        return m / se

    for h in (5, 10, 20, 40):
        df = grid_cases(h, feats)
        for k in ["ret5", "ret10", "ret20", "vol20", "rng20", "lowprox"]:
            g = df.dropna(subset=[k, "exz"]).copy()
            if len(g) < 50: continue
            g["z"] = g.groupby("coin")[k].rank(pct=True)
            g["q"] = pd.cut(g["z"], [0, .2, .4, .6, .8, 1.0], labels=False, include_lowest=True)
            res = g.groupby("q").apply(lambda x: pd.Series({"n": len(x), "ex_mean%": 100 * x["ex"].mean(), "exz": x["exz"].mean(), "t_day": clustered_t(x)}))
            sp = stats.spearmanr(g["z"], g["exz"])
            res.loc["spearman"] = [len(g), np.nan, sp.correlation, sp.pvalue]
            out[f"h{h}_{k}"] = res.round(4)
        if h == 10:
            g = df.dropna(subset=["exz"])
            out["h10_weekday"] = g.groupby("wd").apply(lambda x: pd.Series({"n": len(x), "exz": x["exz"].mean(), "t": clustered_t(x)})).round(3)
    # book decomposition
    rows = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            rows.append(pd.DataFrame({"coin": coin, "w": w, "br": d["book_return"].values, "cr": d["coin_return"].values}))
    D = pd.concat(rows)
    out["book_by_coin"] = D.groupby("coin").agg(br_mean_bp=("br", lambda x: 1e4 * x.mean()), cr_mean_bp=("cr", lambda x: 1e4 * x.mean()), n=("br", "count")).round(2)
    # allocation sign stats
    al = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            a = df["postRebalance_current_allocation"]; r = df["close"].shift(-1) / df["close"] - 1
            al.append(pd.DataFrame({"a": a, "g": a * r, "fc": df["forecast"]}))
    A = pd.concat(al).dropna()
    A["side"] = np.sign(A["a"])
    out["by_side"] = A.groupby("side").agg(n=("g", "count"), mean_gain_bp=("g", lambda x: 1e4 * x.mean()), mean_alloc=("a", "mean")).round(3)
    return out
