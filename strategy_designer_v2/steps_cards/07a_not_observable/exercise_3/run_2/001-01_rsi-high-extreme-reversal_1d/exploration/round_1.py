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
            fg = f.iloc[grid]
            fwd = np.array([c[i+5]/c[i]-1 for i in grid])
            allfwd = c[5:]/c[:-5]-1
            ext = (fg <= -10).values
            rows.append({"coin": coin, "win": w, "bars": n, "grid_cases": len(grid),
                         "bars_fc<=-10": int((f <= -10).sum()),
                         "bars_fc<0": int((f < 0).sum()),
                         "bars_fc==0": int((f == 0).sum()),
                         "grid_fc<=-10": int(ext.sum()),
                         "grid_fc<0": int((fg < 0).sum()),
                         "mean_fwd5_all": float(allfwd.mean()),
                         "sd_fwd5_grid": float(fwd.std(ddof=1)),
                         "mean_excess_ext": float((fwd[ext]-allfwd.mean()).mean()) if ext.any() else np.nan,
                         "first_ts_year": int(pd.to_datetime(b["timestamp"].iloc[0]).year),
                         "last_ts_year": int(pd.to_datetime(b["timestamp"].iloc[-1]).year)})
            out["fc_quantiles_"+coin+w] = f.quantile([0,0.05,0.1,0.25,0.5,0.75,1]).round(3)
            raw = b["debug_info.components.rsi_high.last_history_value"]
            out["raw_quantiles_"+coin+w] = raw.quantile([0,0.05,0.1,0.25,0.5,0.75,0.9,1]).round(3)
            # runs of forecast <= -10
            e = (f <= -10).astype(int).values
            runs = []; r = 0
            for x in e:
                if x: r += 1
                else:
                    if r: runs.append(r)
                    r = 0
            if r: runs.append(r)
            out["runs_fc<=-10_"+coin+w] = pd.Series(runs).describe() if runs else "none"
    out["summary"] = pd.DataFrame(rows)
    return out
