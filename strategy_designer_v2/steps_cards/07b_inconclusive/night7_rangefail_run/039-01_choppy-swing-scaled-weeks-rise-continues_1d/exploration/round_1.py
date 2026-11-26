def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 3, 5, 10, 20]
    # normal drift per coin per horizon (non-overlapping grid, all windows)
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, b in ws.items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else 0.0
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            r = pd.Series(cl).pct_change()
            sd30 = r.rolling(30).std()
            # agitation: 30d sd vs past-year median (approx; within window only)
            agit = sd30 > sd30.rolling(365, min_periods=60).median()
            ret60 = pd.Series(cl) / pd.Series(cl).shift(60) - 1
            raw = b.get("debug_info.components.swing_move.last_history_value")
            fc = b["forecast"].values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for i in range(0, len(cl), 5):
                if fc[i] == 0 or np.isnan(fc[i]):
                    continue
                d = {"coin": c, "win": w, "year": yr[i], "fc": fc[i],
                     "raw": raw.iloc[i] if raw is not None else np.nan,
                     "agit": agit.iloc[i], "ret60": ret60.iloc[i], "pos": i,
                     "ts": b["timestamp"].iloc[i]}
                for h in H:
                    if i + h < len(cl):
                        d[f"ex{h}"] = cl[i + h] / cl[i] - 1 - drift[(c, h)]
                    else:
                        d[f"ex{h}"] = np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    df["side"] = np.sign(df["raw"].fillna(df["fc"]))
    out = {}

    def slope_t(g, col):
        g = g.dropna(subset=[col])
        p = g.groupby("ts").agg(fc=("fc", "mean"), y=(col, "mean"))
        if len(p) < 10:
            return pd.Series({"n_days": len(p), "slope": np.nan, "t": np.nan, "dirmean": np.nan})
        res = stats.linregress(p["fc"], p["y"])
        dm = (np.sign(g["fc"]) * g[col]).mean()
        return pd.Series({"n_days": len(p), "slope": res.slope, "t": res.slope / res.stderr, "dirmean": dm})

    out["by_horizon"] = pd.DataFrame({h: slope_t(df, f"ex{h}") for h in H}).T
    out["by_side_h5"] = pd.DataFrame({s: slope_t(df[df.side == s], "ex5") for s in [-1, 1]}).T
    out["by_side_h10"] = pd.DataFrame({s: slope_t(df[df.side == s], "ex10") for s in [-1, 1]}).T
    df["absq"] = pd.qcut(df["fc"].abs(), 5, labels=False)
    df["dir5"] = np.sign(df["fc"]) * df["ex5"]
    df["dir10"] = np.sign(df["fc"]) * df["ex10"]
    out["by_absfc_quint"] = df.groupby(["absq"]).agg(n=("dir5", "count"), absfc=("fc", lambda x: x.abs().mean()),
                                                     dir5=("dir5", "mean"), dir10=("dir10", "mean"))
    out["by_side_absq_dir5"] = df.groupby(["side", "absq"])["dir5"].mean().unstack()
    out["by_agit"] = df.groupby("agit").apply(lambda g: slope_t(g, "ex5"))
    out["by_agit_side_dir5"] = df.groupby(["agit", "side"])["dir5"].agg(["count", "mean"])
    out["by_window"] = df.groupby("win").apply(lambda g: slope_t(g, "ex5"))
    out["by_coin"] = df.groupby("coin").apply(lambda g: slope_t(g, "ex5"))
    out["by_year"] = df.groupby("year").apply(lambda g: slope_t(g, "ex5"))
    return out
