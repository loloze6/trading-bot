def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    fb = []
    for coin, wins in data["bars"].items():
        # coin drift and usual move over non-overlapping 5-bar stretches
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(allr); usual = np.std(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; h = b["high"]; v = b["volume"]; l = b["low"]
            r1 = c.pct_change()
            f = pd.DataFrame({
                "ret5": c / c.shift(5) - 1,
                "ret20": c / c.shift(20) - 1,
                "ret1": r1,
                "vol20": r1.rolling(20).std(),
                "dist_hi20": c / h.shift(1).rolling(20).max() - 1,
                "dist_lo20": c / l.shift(1).rolling(20).min() - 1,
                "vratio": v / v.rolling(20).mean(),
                "range": (h - l) / c,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "fc": b["forecast"],
                "raw": b.get("debug_info.components.fb_vol.last_history_value"),
            })
            f["fwd"] = c.shift(-H) / c - 1
            f["unus"] = (f["fwd"] - drift) / usual
            f["fwd_raw"] = f["fwd"] - drift
            f["coin"] = coin; f["win"] = w
            grid = f.iloc[np.arange(0, len(f), H)].dropna(subset=["fwd"])
            rows.append(grid)
            # failed-breakout bars (forecast < 0), first in each grid cell
            act = f[(f["fc"] < 0) & f["fwd"].notna()].copy()
            act["cell"] = act.index // H
            act = act.groupby("cell").head(1)
            fb.append(act)
    g = pd.concat(rows); a = pd.concat(fb)
    out = {}
    def qtab(df, col, q=5):
        d = df.dropna(subset=[col, "unus"]).copy()
        d["q"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        t = d.groupby("q").agg(n=("unus", "size"), mean_col=(col, "mean"),
                               unus_mean=("unus", "mean"), fwd_pct=("fwd_raw", lambda x: x.mean()*100))
        t["t"] = d.groupby("q")["unus"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
        return t
    for col in ["ret5", "ret20", "ret1", "vol20", "dist_hi20", "dist_lo20", "vratio", "range", "clv"]:
        out["grid by " + col] = qtab(g, col)
    wt = g.groupby("wd")["unus"].agg(["size", "mean"])
    wt["t"] = g.groupby("wd")["unus"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x))))
    out["grid by weekday"] = wt
    out["fb cases n, mean unus, t"] = pd.Series({"n": len(a), "mean": a["unus"].mean(),
        "t": a["unus"].mean()/(a["unus"].std()/np.sqrt(len(a)))})
    for col in ["ret5", "ret20", "vol20", "dist_hi20", "vratio", "raw", "clv"]:
        out["fb by " + col] = qtab(a, col, 3)
    ct = a.groupby("coin")["unus"].agg(["size", "mean"])
    out["fb by coin"] = ct
    return out
