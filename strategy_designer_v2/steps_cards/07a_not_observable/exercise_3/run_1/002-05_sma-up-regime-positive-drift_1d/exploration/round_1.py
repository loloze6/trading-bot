def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            raw = b.get("debug_info.components.sma_cross_spread.last_history_value")
            c = b["close"]
            r = c.shift(-1) / c - 1
            f = b["forecast"]
            spread_pos = (raw > 0) if raw is not None else None
            runs = int(((spread_pos.astype(int).diff() == 1).sum()) + int(spread_pos.iloc[0])) if raw is not None else np.nan
            rows.append({
                "coin": coin, "window": w, "bars": len(b),
                "year": int(pd.to_datetime(b["timestamp"]).dt.year.mode()[0]),
                "fc>0": int((f > 0).sum()), "fc=0": int((f == 0).sum()), "fc<0": int((f < 0).sum()),
                "raw>0": int((raw > 0).sum()) if raw is not None else np.nan,
                "raw<0": int((raw < 0).sum()) if raw is not None else np.nan,
                "upcross_runs": runs,
                "raw_mean": float(raw.mean()), "raw_min": float(raw.min()), "raw_max": float(raw.max()),
                "fc_mean_pos": float(f[f > 0].mean()) if (f > 0).any() else np.nan,
                "fc_max": float(f.max()),
                "ret_sd": float(r.std()), "ret_mean": float(r.mean()),
                "ret_mean_in": float(r[f > 0].mean()), "ret_mean_out": float(r[f == 0].mean()),
                "first_pos_idx": int(np.argmax((f > 0).values)) if (f > 0).any() else -1,
            })
    out["per_window"] = pd.DataFrame(rows)
    return out
