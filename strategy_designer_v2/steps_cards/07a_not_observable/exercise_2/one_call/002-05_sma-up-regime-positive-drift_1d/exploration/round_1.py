def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            raw = b["debug_info.components.sma_cross_spread.last_history_value"]
            f = b["forecast"]
            r = b["close"].pct_change().shift(-1)
            pos = raw > 0
            runs = int(((pos) & (~pos.shift(1, fill_value=False))).sum())
            dn = int(((~pos) & (pos.shift(1, fill_value=False))).sum())
            span_days = (b["timestamp"].iloc[-1] - b["timestamp"].iloc[0]).total_seconds() / 86400 if hasattr(b["timestamp"].iloc[0], "year") else np.nan
            rows.append({"coin": coin, "window": w, "bars": len(b), "span_days": span_days,
                         "raw_pos_bars": int(pos.sum()), "raw_neg_bars": int((~pos).sum()),
                         "fc_pos_bars": int((f > 0).sum()), "fc_zero_bars": int((f == 0).sum()),
                         "up_runs": runs, "down_crosses": dn,
                         "raw_first": float(raw.iloc[0]), "raw_last": float(raw.iloc[-1]),
                         "raw_min": float(raw.min()), "raw_max": float(raw.max()),
                         "fc_mean_pos": float(f[f > 0].mean()) if (f > 0).any() else 0.0,
                         "fc_max": float(f.max()),
                         "ret_mean_in": float(r[f > 0].mean()), "ret_sd_in": float(r[f > 0].std()),
                         "ret_mean_out": float(r[f == 0].mean()), "ret_sd_out": float(r[f == 0].std()),
                         "coin_total_ret": float(b["close"].iloc[-1] / b["close"].iloc[0] - 1)})
            # position of in-stretch bars
            idx = np.where(f.values > 0)[0]
            out[f"{w}_in_stretch_bar_positions_first_last"] = f"{idx.min() if len(idx) else -1}-{idx.max() if len(idx) else -1}"
            # raw spread by decile of bar position
            q = pd.Series(raw.values).groupby(np.arange(len(raw)) // 12).agg(["mean", "min", "max"])
            out[f"{w}_raw_spread_by_12bar_block"] = q
    out["summary"] = pd.DataFrame(rows).T
    return out
