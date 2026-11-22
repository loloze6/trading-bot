def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []; hours = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float); hi = d["high"].astype(float); lo = d["low"].astype(float)
            r1 = np.log(c).diff()
            ret6 = c / c.shift(6) - 1
            ret42 = c / c.shift(42) - 1
            rng6 = hi.rolling(6).max() / lo.rolling(6).min() - 1
            rmult = rng6 / rng6.rolling(180).mean()
            ts = pd.to_datetime(d["timestamp"])
            base = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(d)), "year": ts.dt.year,
                                 "ret6": ret6, "ret42": ret42, "rmult": rmult,
                                 "rr": np.where(ret6 < 0, rmult, np.nan)})
            for h in (6, 18, 42, 84):
                f = c.shift(-h) / c - 1
                g = base[(base["pos"] % h == 0)].copy()
                g["h"] = h; g["fwd"] = f[g.index].values
                rows.append(g)
            hr = pd.DataFrame({"coin": coin, "year": ts.dt.year, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "r": c.shift(-1) / c - 1})
            hours.append(hr)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    st = A.groupby(["coin", "h"])["fwd"].agg(["mean", "std"]).rename(columns={"mean": "drift", "std": "sd"})
    A = A.join(st, on=["coin", "h"])
    A["s"] = (A["fwd"] - A["drift"]) / A["sd"]
    def topbot(feat, h, by):
        B = A[A["h"] == h].dropna(subset=[feat]).copy()
        B["q"] = B.groupby("coin")[feat].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        res = {}
        for k, G in B.groupby(by):
            t4 = G[G.q == 4]["s"]; t0 = G[G.q == 0]["s"]
            rho = stats.spearmanr(G[feat], G["s"])[0] if len(G) > 10 else np.nan
            res[k] = {"top_minus_bottom": t4.mean() - t0.mean(),
                      "welch_t": stats.ttest_ind(t4, t0, equal_var=False)[0] if len(t4) > 2 and len(t0) > 2 else np.nan,
                      "spearman": rho, "n": len(G)}
        return pd.DataFrame(res).T.round(4)
    for feat, h in (("ret6", 6), ("ret6", 18), ("rr", 6), ("rr", 18), ("ret42", 84), ("ret42", 42)):
        out[f"{feat} h{h} by coin"] = topbot(feat, h, "coin")
        out[f"{feat} h{h} by year"] = topbot(feat, h, "year")
    H = pd.concat(hours).dropna()
    H["h16"] = (H["hour"] == 16)
    H["fri"] = (H["wd"] == 4)
    for nm, col in (("hour16", "h16"), ("friday", "fri")):
        res = {}
        for by in ("coin", "year"):
            for k, G in H.groupby(by):
                a = G[G[col]]["r"]; b = G[~G[col]]["r"]
                res[f"{by}:{k}"] = {"diff": a.mean() - b.mean(), "welch_t": stats.ttest_ind(a, b, equal_var=False)[0], "n": len(a)}
        out[f"{nm} minus rest next-bar"] = pd.DataFrame(res).T.round(5)
    return out
