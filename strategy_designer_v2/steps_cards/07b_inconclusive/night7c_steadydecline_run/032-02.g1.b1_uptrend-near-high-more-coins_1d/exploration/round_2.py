def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for H in [5, 10]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rs.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = np.mean(rs) if rs else np.nan
        sd5 = None
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            s = pd.Series(c)
            ret28 = s.pct_change(28).values
            hi28 = s.rolling(28, min_periods=28).max().values
            dist = (hi28 - c) / hi28
            vol30 = s.pct_change().rolling(30).std().values
            for i in range(0, n, 5):
                r = {"coin": coin, "w": w, "regime": df["regime"].iloc[i], "fc": df["forecast"].iloc[i],
                     "ret28": ret28[i], "dist": dist[i], "vol30": vol30[i],
                     "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "day": pd.Timestamp(df["timestamp"].iloc[i]).normalize()}
                for H in [5, 10]:
                    r[f"x{H}"] = (c[i + H] / c[i] - 1 - drift[(coin, H)]) if i + H < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    t = d[(d.regime == "trending") & d.x5.notna()].copy()
    t["prox"] = -t["dist"]
    t["prox_vol"] = -t["dist"] / t["vol30"]
    t["at_high"] = (t["dist"] <= 1e-12).astype(int)
    out = {}
    def tert(col, sub, y="x5"):
        s = sub.dropna(subset=[col, y]).sort_values(col, kind="stable")
        k = len(s) // 3
        if k < 5:
            return pd.Series({"n3": k})
        lo, hi = s.iloc[:k][y], s.iloc[-k:][y]
        tt = stats.ttest_ind(hi, lo, equal_var=False)
        return pd.Series({"n3": k, "lo": lo.mean(), "mid": s.iloc[k:-k][y].mean(), "hi": hi.mean(),
                          "diff": hi.mean() - lo.mean(), "t": tt.statistic})
    out["prox_by_window"] = pd.DataFrame({w: tert("prox", g) for w, g in t.groupby("w")}).T
    out["prox_by_year"] = pd.DataFrame({y: tert("prox", g) for y, g in t.groupby("year")}).T
    out["prox_by_coin"] = pd.DataFrame({c: tert("prox", g) for c, g in t.groupby("coin")}).T
    out["proxvol_horizons"] = pd.DataFrame({y: tert("prox_vol", t, y) for y in ["x5", "x10"]}).T
    out["corr_fc_prox_spearman"] = stats.spearmanr(t.fc, t.prox, nan_policy="omit").correlation
    out["share_at_high"] = t["at_high"].mean()
    out["at_high_vs_not_x5"] = t.groupby("at_high")["x5"].agg(["count", "mean"])
    t["pq"] = pd.qcut(t["prox"].rank(method="first"), 5, labels=False)
    out["prox_quintiles"] = t.groupby("pq").agg(n=("x5", "size"), x5=("x5", "mean"), x10=("x10", "mean"), dist=("dist", "mean"))
    # day-clustered slope t of x5 on prox
    s = t.dropna(subset=["prox", "x5"])
    X = s["prox"] - s["prox"].mean()
    b = (X * (s["x5"] - s["x5"].mean())).sum() / (X ** 2).sum()
    e = s["x5"] - s["x5"].mean() - b * X
    g = (X * e).groupby(s["day"]).sum()
    se = np.sqrt((g ** 2).sum()) / (X ** 2).sum()
    out["slope_prox_x5_dayclustered"] = pd.Series({"slope": b, "t": b / se, "days": g.size, "n": len(s)})
    # does leaving out w18 keep it
    out["prox_without_w18"] = tert("prox", t[t.w != "w18"])
    out["fc_without_w18"] = tert("fc", t[t.w != "w18"])
    return out
