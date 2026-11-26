def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # coin drift per horizon over all visible windows (non-overlapping grid)
        for h in [1,3,5,10,15]:
            pass
        allret = {h: [] for h in [1,3,5,10,15]}
        for w, df in wins.items():
            c = df["close"].values
            for h in allret:
                idx = np.arange(0, len(c)-h, h)
                allret[h] += list(c[idx+h]/c[idx]-1)
        drift = {h: np.mean(v) for h, v in allret.items()}
        usual = {h: np.std(v, ddof=1) for h, v in allret.items()}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            ret60 = pd.Series(c).pct_change(60).values
            raw = df.get("debug_info.components.stretch.last_history_value")
            for i in range(0, n-5, 5):
                f = df["forecast"].iloc[i]
                if not (f < 0): continue
                r = {"coin": coin, "win": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                     "depth": -f, "raw": raw.iloc[i] if raw is not None else np.nan,
                     "t60": ret60[i]}
                for h in [1,3,5,10,15]:
                    if i+h < n:
                        r[f"y{h}"] = c[i+h]/c[i]-1-drift[h]
                        r[f"z{h}"] = r[f"y{h}"]/usual[h]
                rows.append(r)
    d = pd.DataFrame(rows)
    def slope(sub, y="y5", x="depth"):
        s = sub.dropna(subset=[y, x])
        if len(s) < 10: return pd.Series({"n": len(s)})
        X = s[x].values; Y = s[y].values
        b = np.polyfit(X, Y, 1)[0]
        e = Y - np.polyval(np.polyfit(X, Y, 1), X)
        xc = X - X.mean()
        g = pd.DataFrame({"u": xc*e, "day": s["day"].values}).groupby("day")["u"].sum()
        se = np.sqrt((g**2).sum())/ (xc**2).sum()
        dm = pd.DataFrame({"y": Y, "day": s["day"].values}).groupby("day")["y"].sum()
        mt = Y.mean()/(np.sqrt(((dm - dm.size and 0) ).pow(0).sum()) if False else 1)
        # mean y, day-clustered t
        dev = pd.DataFrame({"e": Y - Y.mean(), "day": s["day"].values}).groupby("day")["e"].sum()
        tm = Y.mean()/(np.sqrt((dev**2).sum())/len(Y))
        return pd.Series({"n": len(s), "days": s["day"].nunique(), "slope": b, "t_slope": b/se,
                          "mean_y_short_dir": -Y.mean(), "t_mean": -tm})
    out = {}
    out["all_by_horizon"] = pd.DataFrame({h: slope(d, f"y{h}") for h in [1,3,5,10,15]}).T
    out["by_coin_h5"] = d.groupby("coin").apply(lambda s: slope(s))
    out["by_year_h5"] = d.groupby("year").apply(lambda s: slope(s))
    d["trend"] = np.where(d.t60 > 0.10, "rising", np.where(d.t60 < -0.10, "falling", np.where(d.t60.isna(), "na", "choppy")))
    out["by_trend_h5"] = d.groupby("trend").apply(lambda s: slope(s))
    out["by_trend_h10"] = d.groupby("trend").apply(lambda s: slope(s, "y10"))
    d["q"] = pd.qcut(d.depth, 4, labels=["q1", "q2", "q3", "q4"])
    out["by_depth_q"] = d.groupby("q").agg(n=("y5", "size"), depth=("depth", "mean"), raw=("raw", "mean"),
                                          y5_short=("y5", lambda v: -v.mean()), y10_short=("y10", lambda v: -v.mean()),
                                          y1_short=("y1", lambda v: -v.mean()))
    out["raw_slope_h5"] = slope(d, "y5", "raw")
    out["zslope_h5"] = slope(d, "z5")
    return out
