def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float); op = b["open"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-H) / c - 1,
                "r1": r1,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "vol20": r1.rolling(20).std(),
                "dist_hi20": c / c.shift(1).rolling(20).max() - 1,
                "dist_lo20": c / c.shift(1).rolling(20).min() - 1,
                "range1": (hi - lo) / c,
                "clv": (c - lo) / (hi - lo).replace(0, np.nan),
                "upwick": (hi - np.maximum(op, c)) / c,
                "volz": (b["volume"] - b["volume"].rolling(20).mean()) / b["volume"].rolling(20).std(),
                "fc": b["forecast"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "pos": np.arange(len(b)),
            })
            f["brk"] = (c > c.shift(1).rolling(20).max()).astype(float)
            rows.append(f[f["pos"] % H == 0])
    d = pd.concat(rows, ignore_index=True)
    d = d.dropna(subset=["fwd"])
    drift = d.groupby("coin")["fwd"].mean()
    sd = d.groupby("coin")["fwd"].std()
    d["ex"] = d["fwd"] - d["coin"].map(drift)
    d["exz"] = d["ex"] / d["coin"].map(sd)
    out = {}
    feats = ["r1", "r5", "r20", "vol20", "dist_hi20", "dist_lo20", "range1", "clv", "upwick", "volz"]
    res = []
    for ft in feats:
        x = d.dropna(subset=[ft])
        # z within coin
        z = x.groupby("coin")[ft].transform(lambda s: (s - s.mean()) / s.std())
        rho, p = stats.spearmanr(x[ft], x["exz"])
        sl = stats.linregress(z, x["exz"])
        q = pd.qcut(z.rank(method="first"), 5, labels=False)
        qm = x.groupby(q)["ex"].mean()
        per_coin = x.groupby("coin").apply(lambda g: stats.spearmanr(g[ft], g["exz"])[0])
        res.append({"feat": ft, "n": len(x), "spearman": rho, "p": p, "slope_t": sl.slope / sl.stderr,
                    "q1_ex%": qm.iloc[0]*100, "q5_ex%": qm.iloc[-1]*100,
                    "coins_pos_rho": int((per_coin > 0).sum())})
    out["features_vs_fwd5_excess"] = pd.DataFrame(res).round(4)
    # breakout states
    def grp(g):
        return pd.Series({"n": len(g), "mean_ex%": g["ex"].mean()*100,
                          "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    d["state"] = np.where(d["brk"] == 1, "breakout_now", np.where(d["fc"] < 0, "failed_active", "other"))
    out["by_state"] = d.groupby("state").apply(grp).round(3)
    out["by_weekday"] = d.groupby("wd").apply(grp).round(3)
    out["by_year"] = d.groupby("year").apply(grp).round(3)
    d["volq"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d["r20q"] = d.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["by_vol_tercile"] = d.groupby("volq").apply(grp).round(3)
    out["r20_x_vol"] = d.groupby(["r20q", "volq"]).apply(grp).round(3)
    out["by_coin"] = d.groupby("coin").apply(grp).round(3)
    return out
