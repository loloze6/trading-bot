def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    fc_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            f = b["forecast"]
            c = b["close"]
            n = len(b)
            fwd = c.shift(-5) / c - 1
            grid = b.index[(b.index % 5 == 0)]
            g = grid[fwd.loc[grid].notna()]
            ext_all = int((f <= -10).sum())
            ext_grid = int((f.loc[g] <= -10).sum())
            # recompute RSI14 (Wilder) from closes
            d = c.diff()
            up = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
            dn = (-d.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
            rsi = 100 - 100 / (1 + up / dn)
            rows.append({"coin": coin, "window": w, "bars": n, "grid_cases": len(g),
                         "share_f_lt0": float((f < 0).mean()),
                         "share_f_le_-5": float((f <= -5).mean()),
                         "share_f_le_-10": float((f <= -10).mean()),
                         "n_f_le_-10_allbars": ext_all, "n_f_le_-10_grid": ext_grid,
                         "share_rsi_gt70": float((rsi > 70).mean()),
                         "share_rsi_gt50": float((rsi > 50).mean()),
                         "fwd5_std_grid": float(fwd.loc[g].std()),
                         "fwd5_mean_grid": float(fwd.loc[g].mean()),
                         "years": str(sorted(set(pd.to_datetime(b["timestamp"]).dt.year)))})
            fc_rows.append(f.describe(percentiles=[.01, .05, .1, .25, .5]))
            # runs of forecast <= -10
            m = (f <= -10).astype(int)
            runs = m.groupby((m != m.shift()).cumsum()).sum()
            runs = runs[runs > 0]
            out[f"{coin}_{w}_extreme_run_lengths"] = runs.value_counts().sort_index()
            # excess on extreme grid bars
            base = fwd.dropna().mean()
            ex = fwd.loc[g][f.loc[g] <= -10] - base
            out[f"{coin}_{w}_extreme_grid_excess"] = ex.reset_index(drop=True)
            # forecast quantiles by recomputed rsi bins
            bins = pd.cut(rsi, [0, 50, 60, 65, 70, 75, 80, 100])
            out[f"{coin}_{w}_forecast_by_rsi"] = f.groupby(bins).agg(["count", "mean", "min"])
    out["per_window"] = pd.DataFrame(rows)
    out["forecast_dist"] = pd.DataFrame(fc_rows)
    return out
