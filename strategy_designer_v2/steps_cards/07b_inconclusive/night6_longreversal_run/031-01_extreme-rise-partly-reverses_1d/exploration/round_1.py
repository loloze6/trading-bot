def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [5, 10, 20, 30]
    # normal drift per coin per horizon, on non-overlapping grid of all windows
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan

    def getz(row):
        d = row.get("debug_info.components")
        if isinstance(d, dict):
            try:
                return d["overreach"]["last_history_value"]
            except Exception:
                return np.nan
        if isinstance(d, str):
            import json
            try:
                dd = json.loads(d)
                return dd["overreach"]["last_history_value"]
            except Exception:
                return np.nan
        return np.nan

    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            zcol = [k for k in df.columns if "overreach" in k and "last_history" in k]
            n = len(df)
            for start in range(0, n, 30):
                cell = df.iloc[start:start + 30]
                m = cell[(cell["regime"] == "mean_reversion") & (cell["forecast"] < 0)]
                if len(m) == 0:
                    continue
                i = m.index[0]
                if zcol:
                    z = df.loc[i, zcol[0]]
                else:
                    z = getz(df.loc[i])
                r = {"coin": c, "win": w, "year": ts[i].year, "fc": df.loc[i, "forecast"], "z": z,
                     "past30": cl[i] / cl[i - 30] - 1 if i >= 30 else np.nan,
                     "past10": cl[i] / cl[i - 10] - 1 if i >= 10 else np.nan,
                     "day": ts[i].normalize()}
                for h in H:
                    if i + h < n:
                        tot = cl[i + h] / cl[i] - 1
                        r[f"u{h}"] = -(tot - drift[(c, h)])
                        r[f"t{h}"] = -tot
                    else:
                        r[f"u{h}"] = np.nan
                        r[f"t{h}"] = np.nan
                rows.append(r)
    d = pd.DataFrame(rows)

    def summ(g, col="u30"):
        x = g[col].dropna()
        if len(x) < 2:
            return pd.Series({"n": len(x), "mean": x.mean() if len(x) else np.nan, "t": np.nan, "share>0": np.nan})
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))), "share>0": (x > 0).mean()})

    out = {}
    out["horizons"] = pd.DataFrame({h: summ(d, f"u{h}") for h in H}).T
    out["horizons_total"] = pd.DataFrame({h: summ(d, f"t{h}") for h in H}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["zq"] = pd.qcut(d["z"].rank(method="first"), 3, labels=["low", "mid", "high"]) if d["z"].notna().sum() > 10 else "na"
    out["by_z_tercile"] = d.groupby("zq").apply(summ)
    out["z_means"] = d.groupby("zq")["z"].agg(["mean", "min", "max"]) if "zq" in d else 0
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 3, labels=["strong", "mid", "weak"])
    out["by_forecast_tercile"] = d.groupby("fq").apply(summ)
    d["p30"] = np.where(d["past30"] > 0, "last30 up", np.where(d["past30"] <= 0, "last30 down", "na"))
    out["by_past30"] = d.groupby("p30").apply(summ)
    out["by_past30_u10"] = d.groupby("p30").apply(lambda g: summ(g, "u10"))
    out["corr_z_u30"] = float(d[["z", "u30"]].dropna().corr().iloc[0, 1]) if d["z"].notna().sum() > 5 else np.nan
    out["corr_past30_u30"] = float(d[["past30", "u30"]].dropna().corr().iloc[0, 1])
    out["n_cases_z_nonnull"] = int(d["z"].notna().sum())
    return out
