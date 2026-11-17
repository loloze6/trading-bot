def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 3
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); hi = df["high"].astype(float); v = df["volume"].astype(float)
            prevhi = hi.shift(1).rolling(30, min_periods=10).max()
            near = c / hi.rolling(30, min_periods=10).max() - 1
            vrel = v / v.rolling(30, min_periods=10).mean()
            vrel5 = v.rolling(5).mean() / v.rolling(30, min_periods=10).mean()
            brk = (c > prevhi).astype(float)
            brk_size = c / prevhi - 1
            r7 = c / c.shift(7) - 1
            fwd = c.shift(-H) / c - 1
            # breakout holds: close 3 days later still above prev high
            hold = (c.shift(-H) > prevhi).astype(float)
            ts = pd.to_datetime(df["timestamp"])
            wn = int(w[1:])
            for i in range(0, len(df), H):
                if pd.isna(fwd.iloc[i]): continue
                rows.append(dict(coin=coin, wn=wn, fwd=fwd.iloc[i], near=near.iloc[i], vrel=vrel.iloc[i],
                                 vrel5=vrel5.iloc[i], brk=brk.iloc[i], bsz=brk_size.iloc[i], hold=hold.iloc[i],
                                 r7=r7.iloc[i], yr=ts.iloc[i].year))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g = g.dropna(subset=["near", "vrel", "r7"])
    for col in ["near", "vrel", "r7", "vrel5"]:
        g[col + "_r"] = g.groupby("coin")[col].rank(pct=True) - 0.5
    out = {}
    # top-quintile vs rest per coin
    res = {}
    for col in ["near", "vrel"]:
        for coin, d in g.groupby("coin"):
            top = d[d[col + "_r"] > 0.3]["ex"]; rest = d[d[col + "_r"] <= 0.3]["ex"]
            res[(col, coin)] = top.mean() - rest.mean()
    out["top_minus_rest_by_coin"] = pd.Series(res).unstack()
    # multiple regression pooled
    X = np.column_stack([np.ones(len(g)), g["near_r"], g["vrel_r"], g["r7_r"], g["near_r"] * g["vrel_r"]])
    y = g["ex"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    s2 = resid @ resid / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["reg"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "near", "vrel", "r7", "near_x_vrel"])
    # early vs late windows
    g["half"] = np.where(g["wn"] <= 12, "w1-12", "w13-24")
    hh = {}
    for h, d in g.groupby("half"):
        for col in ["near", "vrel"]:
            top = d[d[col + "_r"] > 0.3]["ex"]; rest = d[d[col + "_r"] <= 0.3]["ex"]
            hh[(h, col)] = (top.mean() - rest.mean(), stats.ttest_ind(top, rest, equal_var=False)[1 * 0], len(top))
    out["half_top_minus_rest"] = pd.DataFrame(hh, index=["diff", "t", "n_top"]).T
    # breakouts
    b = g[g["brk"] == 1]
    out["breakout"] = pd.Series({"n": len(b), "mean_ex": b["ex"].mean(),
                                 "t": b["ex"].mean() / (b["ex"].std() / np.sqrt(len(b))),
                                 "share_holding_above": b["hold"].mean(),
                                 "nonbrk_mean_ex": g[g["brk"] == 0]["ex"].mean()})
    bb = b.copy(); bb["vb"] = pd.qcut(bb["vrel"].rank(method="first"), 3, labels=False)
    out["breakout_by_vol_tercile"] = bb.groupby("vb")["ex"].agg(["mean", "count"])
    # vrel by year: top quintile minus rest
    yy = {}
    for yr, d in g.groupby("yr"):
        top = d[d["vrel_r"] > 0.3]["ex"]; rest = d[d["vrel_r"] <= 0.3]["ex"]
        yy[yr] = top.mean() - rest.mean()
    out["vrel_top_minus_rest_by_year"] = pd.Series(yy)
    # vrel within near tercile, deciles of vrel
    g["vd"] = pd.qcut(g["vrel_r"].rank(method="first"), 10, labels=False)
    out["vrel_decile"] = g.groupby("vd")["ex"].agg(["mean", "count"])
    return out
