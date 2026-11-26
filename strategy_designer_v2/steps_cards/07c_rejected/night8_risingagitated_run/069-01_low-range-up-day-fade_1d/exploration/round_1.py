def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float)
            hi = d["high"].astype(float).rolling(20, min_periods=20).max()
            lo = d["low"].astype(float).rolling(20, min_periods=20).min()
            pos = (c - lo) / (hi - lo)
            r1 = c.pct_change()
            tr60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30).std()
            out = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(d)), "pos": pos, "r1": r1,
                                "fc": d["forecast"].astype(float), "tr60": tr60, "vol30": vol30,
                                "day": pd.to_datetime(d["timestamp"]).dt.floor("D").astype(str)})
            for h in (1, 3, 5):
                out[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    res = {}
    # coin mean returns per horizon (non-overlapping)
    means = {}
    for h in (1, 3, 5):
        g = A[A["i"] % h == 0]
        means[h] = g.groupby("coin")[f"f{h}"].mean()
    for h in (1, 3, 5):
        A[f"x{h}"] = A[f"f{h}"] - A["coin"].map(means[h])
    up = A[(A["r1"] > 0) & A["pos"].notna()].copy()
    dn = A[(A["r1"] < 0) & A["pos"].notna()].copy()
    up["q"] = pd.cut(up["pos"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["0-.2", ".2-.4", ".4-.6", ".6-.8", ".8-1"])
    dn["q"] = pd.cut(dn["pos"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["0-.2", ".2-.4", ".4-.6", ".6-.8", ".8-1"])
    def tab(df, h):
        g = df[df["i"] % h == 0].dropna(subset=[f"x{h}"])
        t = g.groupby("q", observed=True)[f"x{h}"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t[["mean", "count", "t"]]
    for h in (1, 3, 5):
        res[f"up days by range pos, excess fwd {h}d"] = tab(up, h)
    res["down days by range pos, excess fwd 1d"] = tab(dn, 1)
    low = up[up["pos"] < 0.4].dropna(subset=["x1"])
    t = low.groupby("coin")["x1"].agg(["mean", "count"]); res["up low-range by coin x1"] = t
    t = low.groupby("w")["x1"].agg(["mean", "count"]); res["up low-range by window x1"] = t
    low = low.copy()
    low["trend"] = np.where(low["tr60"] > 0.1, "rising", np.where(low["tr60"] < -0.1, "falling", "choppy"))
    t = low.groupby("trend")["x1"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    res["up low-range by trend x1"] = t
    # size of up day
    low["rq"] = pd.qcut(low["r1"], 3, labels=["small", "mid", "big"])
    t = low.groupby("rq", observed=True)["x1"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    res["up low-range by size of up day x1"] = t
    # forecast bins
    sh = A[A["fc"] < 0].dropna(subset=["x1"]).copy()
    sh["fb"] = pd.cut(sh["fc"], [-21, -15, -10, -5, 0], labels=["<-15", "-15..-10", "-10..-5", "-5..0"])
    t = sh.groupby("fb", observed=True)["x1"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    res["short cases by forecast bin x1"] = t
    res["corr pos vs x1 on up days"] = float(up[["pos", "x1"]].dropna().corr().iloc[0, 1])
    return res
