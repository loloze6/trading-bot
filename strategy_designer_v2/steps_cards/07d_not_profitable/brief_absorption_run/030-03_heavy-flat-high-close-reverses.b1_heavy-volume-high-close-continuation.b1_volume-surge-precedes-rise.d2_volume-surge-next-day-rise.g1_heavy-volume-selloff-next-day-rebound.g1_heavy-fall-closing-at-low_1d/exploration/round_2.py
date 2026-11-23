def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            b["coin"] = coin; b["wn"] = int(w[1:]); b["pos"] = np.arange(len(b))
            b["nxt"] = c.shift(-1) / c - 1
            b["ret1"] = c.pct_change()
            b["ret20"] = c / c.shift(20) - 1
            b["vol_ratio"] = b["ret1"].rolling(20).std() / b["ret1"].rolling(60).std()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["cl_low"] = (b["high"] - c) / rng
            b["vr"] = b["volume"] / b["volume"].shift(1).rolling(20).mean()
            b["alloc"] = b["postRebalance_current_allocation"].fillna(0)
            b["fc"] = b["forecast"].fillna(0)
            b["ts"] = pd.to_datetime(b["timestamp"]); b["year"] = b["ts"].dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["nxt"].mean()
    B["ex"] = B["nxt"] - B["coin"].map(mu)
    out = {}
    # condition alone: vol_ratio on all bars and on down days by signal strength
    Bv = B.dropna(subset=["vol_ratio", "nxt"]).copy()
    edges = Bv["vol_ratio"].quantile([0.2, 0.4, 0.6, 0.8]).values
    Bv["qv"] = np.digitize(Bv["vol_ratio"], edges)
    Bv["down"] = Bv["ret1"] < 0
    Bv["sig"] = Bv["cl_low"] * Bv["vr"]
    thr = Bv.loc[Bv["down"], "sig"].quantile(0.8)
    Bv["strong"] = Bv["down"] & (Bv["sig"] >= thr)
    def tt(x): return pd.Series({"n": len(x), "ex": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x))})
    out["vol_ratio quintile: all bars"] = Bv.groupby("qv")["ex"].apply(tt).unstack().round(4)
    out["vol_ratio quintile: not-signal bars (not strong)"] = Bv[~Bv["strong"]].groupby("qv")["ex"].apply(tt).unstack().round(4)
    out["vol_ratio quintile: strong-signal bars"] = Bv[Bv["strong"]].groupby("qv")["ex"].apply(tt).unstack().round(4)
    # slope of ex on sig within down days by vol_ratio half
    Dn = Bv[Bv["down"]].copy()
    res = {}
    for k, g in Dn.groupby(Dn["qv"] >= 2):
        x = g["sig"]; y = g["ex"]
        bb = np.polyfit(x, y, 1)[0]; r = y - np.polyval(np.polyfit(x, y, 1), x)
        se = np.sqrt((r ** 2).sum() / (len(x) - 2) / ((x - x.mean()) ** 2).sum())
        res["vol_ratio upper60=" + str(k)] = {"n": len(g), "slope": bb, "t": bb / se}
    out["down days slope by vol regime"] = pd.DataFrame(res).T.round(5)
    # simulated variants of the book
    B["dalloc"] = B.groupby(["coin", "wn"])["alloc"].diff().fillna(B["alloc"]).abs()
    B["fc_strong"] = B["fc"] >= B.loc[B["fc"] > 0, "fc"].quantile(0.8)
    B["lowvr"] = B["vol_ratio"] < edges[0]
    variants = {
        "as run": B["alloc"],
        "only top fifth forecast": B["alloc"] * B["fc_strong"],
        "out when vol_ratio lowest fifth": B["alloc"] * (~B["lowvr"]),
        "alloc x (fc/10)": B["alloc"] * (B["fc"] / 10).clip(0, 2),
        "alloc x vol_ratio": B["alloc"] * B["vol_ratio"].fillna(1).clip(0, 2),
    }
    res = {}
    for name, a in variants.items():
        X = B[["coin", "wn", "pos", "nxt"]].copy(); X["a"] = a.fillna(0)
        X["da"] = X.groupby(["coin", "wn"])["a"].diff().fillna(X["a"]).abs()
        X["g"] = (X["a"] * X["nxt"]).fillna(0) - X["da"] * 0.00095
        d = X.groupby(["wn", "pos"])["g"].mean().sort_index()
        v = (1 + d).cumprod().values; dd = v / np.maximum.accumulate(v) - 1
        yrs = len(d) / 365
        yr = v[-1] ** (1 / yrs) - 1
        res[name] = {"sharpe": d.mean() / d.std() * np.sqrt(365), "yearly": yr, "maxdd": dd.min(), "calmar": yr / -dd.min(), "in_share": (X["a"].abs() > 1e-6).mean()}
    out["variants (approx, cost 0.095%/side)"] = pd.DataFrame(res).T.round(4)
    # what the book held in deepest fall (w1-w3)
    F = B[B["wn"] <= 3]
    out["w1-3 by vol_ratio fifth: gain"] = F.assign(qv=np.digitize(F["vol_ratio"].fillna(1), edges)).groupby("qv").apply(lambda g: pd.Series({"n": (g["alloc"] > 0).sum(), "gain": (g["alloc"] * g["nxt"]).sum()})).round(3)
    return out
