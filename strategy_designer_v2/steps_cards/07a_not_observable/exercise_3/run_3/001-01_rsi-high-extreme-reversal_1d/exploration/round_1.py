def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            f = b["forecast"]
            c = b["close"].values
            n = len(b)
            grid = list(range(0, n - 5, 5))
            fr = np.array([c[i+5]/c[i]-1 for i in range(n-5)])
            base = fr.mean()
            gf = f.iloc[grid].values
            gr = np.array([c[i+5]/c[i]-1 for i in grid])
            ext = gf <= -10
            rows.append({"coin": coin, "win": w, "bars": n, "grid_cases": len(grid),
                         "bars_f<0": int((f < 0).sum()), "bars_f<=-10": int((f <= -10).sum()),
                         "bars_f<=-5": int((f <= -5).sum()),
                         "grid_f<=-10": int(ext.sum()), "grid_f<0": int((gf < 0).sum()),
                         "share_bars_ext": float((f <= -10).mean()),
                         "fwd5_std_grid": float(gr.std(ddof=1)),
                         "fwd5_mean_all": float(base),
                         "excess_ext_mean": float((gr[ext]-base).mean()) if ext.any() else np.nan,
                         "excess_fneg_mean": float((gr[gf<0]-base).mean()) if (gf<0).any() else np.nan,
                         "year": int(pd.to_datetime(b["timestamp"]).dt.year.iloc[0])})
    out["per_window"] = pd.DataFrame(rows)
    allf = pd.concat([b["forecast"] for ws in data["bars"].values() for b in ws.values()])
    out["forecast_quantiles"] = allf.quantile([0, .05, .1, .25, .5, .75, .9, 1]).to_frame("forecast")
    out["forecast_bins"] = pd.cut(allf, [-20.01, -15, -10, -5, -1e-9, 0.0, 20]).value_counts().sort_index().to_frame("n")
    b = list(list(data["bars"].values())[0].values())[0]
    raw = b["debug_info.components.rsi_high.last_history_value"]
    out["raw_component_quantiles"] = raw.quantile([0, .05, .25, .5, .75, .95, 1]).to_frame("raw")
    out["share_raw_neg"] = float((raw < 0).mean())
    return out
