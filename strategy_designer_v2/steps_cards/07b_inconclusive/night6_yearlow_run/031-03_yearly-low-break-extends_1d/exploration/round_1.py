def explore(data):
    import numpy as np, pandas as pd, json
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    drift = {}
    usual = {}
    def depth_of(v):
        try:
            d = v if isinstance(v, dict) else json.loads(v) if isinstance(v, str) else None
            if d is None: return np.nan
            x = d.get("depth", {})
            return x.get("last_history_value", np.nan)
        except Exception:
            return np.nan
    for coin, ws in bars.items():
        r10 = []
        for w, df in ws.items():
            c = df["close"].values
            n = len(c)
            for i in range(0, n - 10, 10):
                r10.append(c[i + 10] / c[i] - 1)
        drift[coin] = np.mean(r10); usual[coin] = np.std(r10, ddof=1)
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            act = (df["regime"] == "trending").values
            dep = df["debug_info.components"].apply(depth_of).values if "debug_info.components" in df else np.full(n, np.nan)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(n):
                if not act[i]: continue
                rec = {"coin": coin, "w": w, "i": i, "grid": i % 10 == 0, "cell": i // 10,
                       "year": ts.iloc[i].year, "depth": dep[i], "fc": df["forecast"].iloc[i],
                       "first": (i == 0) or (not act[i - 1]),
                       "day": ts.iloc[i].normalize()}
                # count of active in previous 10 bars
                rec["prev_act"] = act[max(0, i - 10):i].sum()
                for h in H:
                    rec[f"r{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    A = pd.DataFrame(rows)
    A["u10"] = -(A["r10"] - A["coin"].map(drift))  # short side unusual
    A["s10"] = A["u10"] / A["coin"].map(usual)
    out = {}
    out["n_active_bars"] = len(A)
    out["drift_usual"] = pd.DataFrame({"drift10": drift, "usual10": usual})
    # first active bar per (coin,w,cell)
    F = A.dropna(subset=["r10"]).sort_values("i").groupby(["coin", "w", "cell"]).first().reset_index()
    def tday(s, days):
        g = s.groupby(days).sum()
        m = s.mean(); n = len(s)
        dev = (s - m).groupby(days).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return m, m / se if se > 0 else np.nan, n, days.nunique()
    m, t, n, d = tday(F["u10"], F["day"])
    out["first_per_cell_u10"] = pd.Series({"mean": m, "t_day": t, "cases": n, "days": d, "mean_strength": F["s10"].mean()})
    # by horizon, short-side raw returns on all active bars (overlapping, informative), first-per-cell
    hz = {}
    for h in H:
        x = -F[f"r{h}"].dropna()
        hz[h] = {"mean_short_raw": x.mean(), "t": stats.ttest_1samp(x, 0).statistic, "n": len(x)}
    out["by_horizon_first_cell"] = pd.DataFrame(hz).T
    out["by_coin"] = F.groupby("coin")["u10"].agg(["mean", "count", "median"])
    out["by_year"] = F.groupby("year")["u10"].agg(["mean", "count", "median"])
    out["by_window"] = F.groupby("w")["u10"].agg(["mean", "count"])
    F["fresh"] = F["prev_act"] == 0
    out["fresh_vs_continuing"] = F.groupby("fresh")["u10"].agg(["mean", "count", "median"])
    F["dq"] = pd.qcut(F["depth"].rank(method="first"), 3, labels=["shallow", "mid", "deep"]) if F["depth"].notna().sum() > 5 else "na"
    out["by_depth_tercile"] = F.groupby("dq")[["u10", "depth", "r1", "r3", "r5", "r20"]].mean()
    out["depth_nonnull"] = int(F["depth"].notna().sum())
    out["fc_desc"] = F["fc"].describe()
    out["corr_depth_u10"] = F[["depth", "fc", "u10"]].corr(method="spearman")
    return out
