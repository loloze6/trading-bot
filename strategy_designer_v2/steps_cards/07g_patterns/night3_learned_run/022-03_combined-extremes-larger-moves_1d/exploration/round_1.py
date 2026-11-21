def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            fwd = c.shift(-H) / c - 1
            mom28 = c / c.shift(28) - 1
            mom7 = c / c.shift(7) - 1
            mom3 = c / c.shift(3) - 1
            hi90 = c / c.rolling(90, min_periods=30).max() - 1
            vol30 = r1.rolling(30, min_periods=15).std()
            vol7 = r1.rolling(7, min_periods=5).std()
            rng = (b["high"] - b["low"]) / b["close"]
            ts = pd.to_datetime(b["timestamp"])
            f = b["forecast"]
            comb = b.get("debug_info.components.combined.last_history_value")
            pos = b["postRebalance_current_allocation"]
            gain = pos * (c.shift(-1) / c - 1)
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=fwd[i], r1=r1[i], mom28=mom28[i], mom7=mom7[i],
                                 mom3=mom3[i], hi90=hi90[i], vol30=vol30[i], vol7=vol7[i],
                                 vratio=vol7[i] / vol30[i] if vol30[i] and vol30[i] > 0 else np.nan,
                                 rng=rng[i], wd=ts[i].weekday(), yr=ts[i].year, f=f[i],
                                 comb=comb[i] if comb is not None else np.nan, pos=pos[i],
                                 g5=gain[i:i + H].sum()))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby("coin")["fwd"].transform("mean")
    d["usual"] = d.groupby("coin")["fwd"].transform("std")
    d["un"] = d["fwd"] - d["drift"]
    d["z"] = d["un"] / d["usual"]
    out = {}
    def quint(col, q=5):
        x = d.dropna(subset=[col, "z"]).copy()
        x["q"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = x.groupby("q")["z"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["un_mean_pct"] = x.groupby("q")["un"].mean() * 100
        sl = stats.spearmanr(x[col], x["z"])
        g.loc["rho", "mean"] = sl.correlation
        g.loc["rho", "t"] = sl.correlation * np.sqrt(len(x))
        return g.round(4)
    for col in ["r1", "mom3", "mom7", "mom28", "hi90", "vol30", "vol7", "vratio", "rng", "f", "comb"]:
        out["q_" + col] = quint(col)
    g = d.groupby("wd")["z"].agg(["mean", "count", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["weekday"] = g.round(4)
    g = d.groupby("yr")["z"].agg(["mean", "count"])
    out["year_z"] = g.round(4)
    # book: position sign vs forward
    d["possign"] = np.sign(d["pos"])
    out["by_possign"] = d.groupby("possign").agg(n=("z", "count"), z=("z", "mean"), g5=("g5", "mean")).round(5)
    # per coin rho of mom28 and r1
    pc = {}
    for coin, x in d.groupby("coin"):
        pc[coin] = {k: stats.spearmanr(x[k], x["z"], nan_policy="omit").correlation for k in ["r1", "mom28", "hi90", "vol30", "f"]}
    out["percoin_rho"] = pd.DataFrame(pc).T.round(3)
    return out
