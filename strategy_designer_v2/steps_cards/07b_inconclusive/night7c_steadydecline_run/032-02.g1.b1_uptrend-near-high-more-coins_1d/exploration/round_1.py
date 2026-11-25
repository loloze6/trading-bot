def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for H in [1, 3, 5, 10, 20]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rs.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = np.mean(rs) if rs else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ret28 = pd.Series(c).pct_change(28).values
            hi28 = pd.Series(c).rolling(28, min_periods=28).max().values
            dist = (hi28 - c) / hi28
            rng = ((df["high"] - df["low"]) / df["close"]).values
            vol30 = pd.Series(c).pct_change().rolling(30).std().values
            for i in range(0, n, 5):
                r = {"coin": coin, "w": w, "i": i, "regime": df["regime"].iloc[i],
                     "fc": df["forecast"].iloc[i], "ret28": ret28[i], "dist": dist[i],
                     "vol30": vol30[i], "year": pd.Timestamp(df["timestamp"].iloc[i]).year}
                for H in [1, 3, 5, 10, 20]:
                    r[f"x{H}"] = (c[i + H] / c[i] - 1 - drift[(coin, H)]) if i + H < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    t = d[(d.regime == "trending") & d.x5.notna()].copy()
    out = {}
    out["n_trending"] = len(t)
    def tert(col, sub, y="x5"):
        s = sub.dropna(subset=[col, y]).sort_values(col, kind="stable")
        k = len(s) // 3
        lo, hi = s.iloc[:k][y], s.iloc[-k:][y]
        mid = s.iloc[k:-k][y]
        tt = stats.ttest_ind(hi, lo, equal_var=False)
        return pd.Series({"n3": k, "lo": lo.mean(), "mid": mid.mean(), "hi": hi.mean(), "diff": hi.mean() - lo.mean(), "t": tt.statistic})
    out["by_forecast_horizon"] = pd.DataFrame({f"x{H}": tert("fc", t, f"x{H}") for H in [1, 3, 5, 10, 20]}).T
    t["prox_raw"] = -t["dist"]
    out["by_rawprox_horizon"] = pd.DataFrame({f"x{H}": tert("prox_raw", t, f"x{H}") for H in [1, 3, 5, 10, 20]}).T
    out["by_ret28_horizon"] = pd.DataFrame({f"x{H}": tert("ret28", t, f"x{H}") for H in [1, 3, 5, 10, 20]}).T
    out["fc_by_window"] = pd.DataFrame({w: tert("fc", g) for w, g in t.groupby("w") if len(g) > 30}).T
    out["fc_by_coin"] = pd.DataFrame({c: tert("fc", g) for c, g in t.groupby("coin") if len(g) > 30}).T
    out["fc_by_year"] = pd.DataFrame({y: tert("fc", g) for y, g in t.groupby("year") if len(g) > 30}).T
    t["volq"] = t.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s.rank(method="first"), 2, labels=["lowvol", "highvol"]))
    out["fc_by_vol"] = pd.DataFrame({v: tert("fc", g) for v, g in t.groupby("volq")}).T
    out["rawprox_by_vol"] = pd.DataFrame({v: tert("prox_raw", g) for v, g in t.groupby("volq")}).T
    t["r28q"] = pd.qcut(t["ret28"], 3, labels=["r28lo", "r28mid", "r28hi"])
    out["fc_by_ret28"] = pd.DataFrame({v: tert("fc", g) for v, g in t.groupby("r28q")}).T
    # outside regime
    o = d[(d.regime != "trending") & d.x5.notna()]
    out["nontrend_mean_x5"] = pd.Series({"n": len(o), "mean": o.x5.mean(), "trend_mean": t.x5.mean()})
    out["corr_fc_x5_spearman"] = stats.spearmanr(t.fc, t.x5, nan_policy="omit").correlation
    return out
