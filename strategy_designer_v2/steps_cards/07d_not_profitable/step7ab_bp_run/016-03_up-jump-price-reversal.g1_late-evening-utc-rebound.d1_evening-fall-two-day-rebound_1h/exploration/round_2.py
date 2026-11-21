def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            g.extend(list(c[idx + 48] / c[idx] - 1))
        m, s = np.mean(g), np.std(g)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lr = np.log(c).diff()
            absum = lr.abs().rolling(24).sum()
            jump = lr.abs().rolling(24).max() / absum
            vol24 = lr.rolling(24).std()
            vol30 = lr.rolling(720, min_periods=200).std()
            ma30 = c.rolling(720, min_periods=200).mean()
            act = b.index[b["regime"] == "mean_reversion"]
            for k, i in enumerate(act):
                if i + 48 >= len(c):
                    continue
                tr = c[i + 48] / c[i] - 1
                rows.append({"coin": coin, "k": k, "fc": b.loc[i, "forecast"],
                             "jump": jump[i], "volr": vol24[i] / vol30[i] if vol30[i] else np.nan,
                             "above": c[i] > ma30[i] if not np.isnan(ma30[i]) else np.nan,
                             "year": pd.Timestamp(b.loc[i, "timestamp"]).year,
                             "x": tr - m, "t": tr, "s": (tr - m) / s,
                             "alloc": b.loc[i, "postRebalance_current_allocation"]})
    df = pd.DataFrame(rows)
    f = df[(df["fc"] > 0) & (df["k"] % 2 == 0)].dropna(subset=["volr", "jump"]).copy()

    def summ(gd):
        x = gd["x"]; t = gd["t"]
        return pd.Series({"n": len(x), "excess": x.mean(), "t_ex": x.mean() / (x.std() / np.sqrt(len(x))),
                          "total": t.mean(), "strength": gd["s"].mean()})

    f["volr_q"] = pd.qcut(f["volr"], 5, labels=False)
    out["falls by volr quintile"] = f.groupby("volr_q").apply(summ)
    f["deep"] = f["fc"] >= f["fc"].median()
    f["volr_t"] = pd.qcut(f["volr"], 3, labels=["low", "mid", "high"])
    f["jump_t"] = pd.qcut(f["jump"], 3, labels=["low", "mid", "high"])
    out["deep x volr"] = f.groupby(["deep", "volr_t"]).apply(summ)
    out["volr x jump"] = f.groupby(["volr_t", "jump_t"]).apply(summ)
    out["high volr by year"] = f[f["volr_t"] == "high"].groupby("year").apply(summ)
    out["low volr by year"] = f[f["volr_t"] == "low"].groupby("year").apply(summ)
    out["falls by above 30d mean"] = f.dropna(subset=["above"]).groupby("above").apply(summ)
    nf = df[(df["fc"] == 0) & (df["k"] % 2 == 0)].dropna(subset=["volr"]).copy()
    nf["volr_t"] = pd.qcut(nf["volr"], 3, labels=["low", "mid", "high"])
    out["non-fall evenings by volr"] = nf.groupby("volr_t").apply(summ)
    # book exposure
    out["mean alloc on fall evenings by volr"] = f.groupby("volr_t")["alloc"].mean()
    tb = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            a = b["postRebalance_current_allocation"].astype(float)
            r = b["close"].astype(float).pct_change().shift(-1)
            tb.append(pd.DataFrame({"a": a, "r": r, "inpos": a.abs() > 0}))
    T = pd.concat(tb).dropna()
    out["share of bars in position"] = float(T["inpos"].mean())
    out["mean alloc when in position"] = float(T.loc[T["inpos"], "a"].mean())
    return out
