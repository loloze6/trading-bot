def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            f = b["forecast"]
            raw = b.get("debug_info.components.sma_cross_spread.last_history_value")
            r = b["close"].shift(-1) / b["close"] - 1
            on = f > 0
            runs = int(((on) & (~on.shift(1, fill_value=False))).sum())
            rawpos = (raw > 0) if raw is not None else pd.Series(False, index=b.index)
            rawruns = int(((rawpos) & (~rawpos.shift(1, fill_value=False))).sum())
            rows.append({"coin": coin, "window": w, "bars": len(b),
                         "year": int(pd.to_datetime(b["timestamp"]).dt.year.iloc[0]),
                         "in_bars": int(on.sum()), "out_bars": int((f == 0).sum()),
                         "fc_runs": runs, "raw_pos_bars": int(rawpos.sum()), "raw_runs": rawruns,
                         "fc_mean_in": float(f[on].mean()) if on.any() else np.nan,
                         "fc_max": float(f.max()),
                         "raw_min": float(raw.min()) if raw is not None else np.nan,
                         "raw_max": float(raw.max()) if raw is not None else np.nan,
                         "ret_sd": float(r.std()), "ret_mean_in": float(r[on].mean()),
                         "ret_mean_out": float(r[f == 0].mean()),
                         "first_in_pos": int(np.argmax(on.values)) if on.any() else -1})
    out["per_window"] = pd.DataFrame(rows)
    b = data["bars"]["BTCUSD"]["w1"].sort_values("timestamp").reset_index(drop=True)
    b["pos"] = np.arange(len(b))
    b["blk"] = b["pos"] // 20
    out["by_block20"] = b.groupby("blk").agg(fc_mean=("forecast", "mean"),
        in_share=("forecast", lambda x: (x > 0).mean()),
        raw_mean=("debug_info.components.sma_cross_spread.last_history_value", "mean"))
    return out
