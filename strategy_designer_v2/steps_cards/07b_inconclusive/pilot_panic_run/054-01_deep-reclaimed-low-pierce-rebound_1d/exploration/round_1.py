def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []
    drift = {}
    usual = {}
    for coin, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
            usual[(coin, h)] = np.std(rs, ddof=1)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            lo = df["low"].values; c = df["close"].values
            prior = pd.Series(lo).shift(1).rolling(30, min_periods=30).min().values
            tr60 = pd.Series(c) / pd.Series(c).shift(60) - 1
            for t in range(len(df)):
                if np.isnan(prior[t]): continue
                if lo[t] < prior[t] and c[t] >= prior[t]:
                    r = {"coin": coin, "win": w, "t": t,
                         "day": str(pd.Timestamp(df["timestamp"].iloc[t]).date()),
                         "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                         "depth": (prior[t] - lo[t]) / prior[t] * 100,
                         "regime": df["regime"].iloc[t],
                         "fc": df["forecast"].iloc[t],
                         "tr60": tr60.iloc[t]}
                    for h in H:
                        if t + h < len(df):
                            r[f"u{h}"] = c[t + h] / c[t] - 1 - drift[(coin, h)]
                            r[f"s{h}"] = r[f"u{h}"] / usual[(coin, h)]
                        else:
                            r[f"u{h}"] = np.nan; r[f"s{h}"] = np.nan
                    rows.append(r)
    ev = pd.DataFrame(rows)
    # one per 5-bar grid cell
    ev["cell"] = ev["t"] // 5
    ev1 = ev.drop_duplicates(["coin", "win", "cell"])
    ev1 = ev1.assign(inprof=ev1["regime"] == "mean_reversion",
                     falling=ev1["tr60"] < -0.10)
    def summ(g, col):
        x = g[["day", col]].dropna()
        if len(x) < 3: return pd.Series({"n": len(x), "mean": np.nan, "t": np.nan, "days": x["day"].nunique()})
        d = x.groupby("day")[col].sum() - x[col].mean() * x.groupby("day")[col].size()
        D = len(d); se = np.sqrt((d ** 2).sum() * D / (D - 1)) / len(x)
        return pd.Series({"n": len(x), "mean": x[col].mean(), "t": x[col].mean() / se, "days": D})
    out = {}
    out["by_profile_horizon"] = pd.DataFrame({(p, h): summ(ev1[ev1.inprof == p], f"u{h}") for p in [True, False] for h in H}).T
    out["by_trend_h5"] = pd.DataFrame({k: summ(g, "u5") for k, g in ev1.groupby("falling")}).T
    inp = ev1[ev1.inprof].copy()
    out["inprof_by_coin_h5"] = pd.DataFrame({k: summ(g, "u5") for k, g in inp.groupby("coin")}).T
    out["inprof_by_year_h5"] = pd.DataFrame({k: summ(g, "u5") for k, g in inp.groupby("year")}).T
    inp["dq"] = pd.qcut(inp["depth"], 3, labels=["shallow", "mid", "deep"])
    out["inprof_by_depth_h5"] = pd.DataFrame({k: summ(g, "u5") for k, g in inp.groupby("dq")}).T
    ev1c = ev1.copy(); ev1c["dq"] = pd.qcut(ev1c["depth"], 3, labels=["shallow", "mid", "deep"])
    out["all_by_depth_h5"] = pd.DataFrame({k: summ(g, "u5") for k, g in ev1c.groupby("dq")}).T
    out["inprof_strength_h5"] = inp["s5"].mean()
    out["inprof_median_u5"] = inp["u5"].median()
    out["inprof_share_pos_u5"] = (inp["u5"] > 0).mean()
    return out
