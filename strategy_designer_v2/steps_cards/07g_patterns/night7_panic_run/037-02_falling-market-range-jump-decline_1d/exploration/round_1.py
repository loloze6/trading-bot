def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 40: continue
            rng = (b.high - b.low) / b.close.shift(1)
            rr = (b.high - b.low) / (b.high - b.low).rolling(30, min_periods=20).mean()
            clv = ((b.close - b.low) / (b.high - b.low)).replace([np.inf, -np.inf], np.nan)
            r1 = b.close.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            z1 = r1 / vol30
            r5 = b.close / b.close.shift(5) - 1
            z5 = r5 / (vol30 * np.sqrt(5))
            fwd = b.close.shift(-H) / b.close - 1
            fwd1 = b.close.shift(-1) / b.close - 1
            falling = (b.regime != "chop")
            volrank = vol30.rolling(90, min_periods=30).rank(pct=True)
            idx = np.arange(0, len(b), H)
            for i in idx:
                rows.append(dict(coin=coin, w=w, day=b.timestamp.iloc[i], rr=rr.iloc[i], clv=clv.iloc[i],
                                 z1=z1.iloc[i], z5=z5.iloc[i], fwd=fwd.iloc[i], falling=falling.iloc[i],
                                 volrank=volrank.iloc[i], wd=pd.Timestamp(b.timestamp.iloc[i]).dayofweek,
                                 pos=b.postRebalance_current_allocation.iloc[i]))
    d = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = d.groupby("coin").fwd.mean()
    sd = d.groupby("coin").fwd.std()
    d["ex"] = d.fwd - d.coin.map(drift)
    d["exz"] = d.ex / d.coin.map(sd)
    def summ(g):
        n = len(g); m = g.ex.mean(); s = g.ex.std()
        return pd.Series({"n": n, "mean_ex": m, "t": m / (s / np.sqrt(n)) if n > 1 else np.nan, "strength": g.exz.mean()})
    out = {}
    out["drift_sd"] = pd.DataFrame({"drift": drift, "sd": sd})
    d["rrq"] = pd.qcut(d.rr, 5, labels=False)
    out["rr_x_falling"] = d.groupby(["falling", "rrq"]).apply(summ)
    d["z1q"] = pd.qcut(d.z1, 5, labels=False)
    out["z1_x_falling"] = d.groupby(["falling", "z1q"]).apply(summ)
    d["z5q"] = pd.qcut(d.z5, 5, labels=False)
    out["z5_x_falling"] = d.groupby(["falling", "z5q"]).apply(summ)
    wide = d[d.rr >= 1.5].copy()
    wide["clvq"] = pd.cut(wide.clv, [0, .33, .67, 1.0001], labels=["low", "mid", "high"], include_lowest=True)
    out["wide_clv_x_falling"] = wide.groupby(["falling", "clvq"]).apply(summ)
    d["vq"] = pd.qcut(d.volrank, 3, labels=False)
    out["volrank"] = d.groupby(["falling", "vq"]).apply(summ)
    out["weekday"] = d.groupby("wd").apply(summ)
    out["by_window_falling"] = d[d.falling].groupby("w").apply(summ)
    out["corr_z5_ex_all"] = pd.Series({"rho": stats.spearmanr(d.z5, d.ex, nan_policy="omit")[0], "n": d.z5.notna().sum()})
    return out
