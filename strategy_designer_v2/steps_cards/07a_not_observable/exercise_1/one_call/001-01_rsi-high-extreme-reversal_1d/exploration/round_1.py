def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    out["coins_windows"] = pd.DataFrame([{"coin": c, "windows": len(data["bars"][c]),
        "bars": sum(len(d) for d in data["bars"][c].values())} for c in coins])
    rows = []; fdist = []; rsi_rows = []; vary = []
    for c in coins:
        for w, b in data["bars"][c].items():
            f = b["forecast"].astype(float)
            rsi = b["debug_info.components.rsi_high.last_history_value"].astype(float)
            post = b["debug_info.components.rsi_high.post_pipeline_value"].astype(float)
            fwd = b["close"].shift(-5) / b["close"] - 1
            grid = np.arange(len(b)) % 5 == 0
            rows.append({"coin": c, "win": w, "bars": len(b),
                "f_nonzero": int((f < 0).sum()), "f_le_-5": int((f <= -5).sum()),
                "f_le_-10": int((f <= -10).sum()), "f_le_-10_grid": int(((f <= -10) & grid & fwd.notna()).sum()),
                "f_le_-10_runs": int(((f <= -10) & ~(f.shift(1) <= -10)).sum()),
                "f_min": f.min(), "f_mean_when_neg": f[f < 0].mean()})
            fdist.append(pd.cut(f, [-20.01, -15, -10, -5, -2, -0.5, -1e-9, 1e-9, 20]).value_counts().sort_index().rename(f"{c}_{w}"))
            rsi_rows.append({"coin": c, "win": w, "raw_min": rsi.min(), "raw_q50": rsi.median(), "raw_max": rsi.max(),
                "raw_neg_share": (rsi < 0).mean(), "raw_le_-20(RSI>=70)": int((rsi <= -20).sum()),
                "raw_le_-15(RSI>=65)": int((rsi <= -15).sum()), "post_min": post.min(),
                "bars_nan_raw": int(rsi.isna().sum())})
            m = fwd.mean()
            for th in [-0.5, -2, -5, -10]:
                sel = fwd[(f <= th) & grid]
                ex = sel - m
                vary.append({"coin": c, "win": w, "thr": th, "n_grid": int(sel.notna().sum()),
                    "excess_mean": ex.mean(), "excess_sd": ex.std(), "fwd5_sd_all": fwd.std(),
                    "t": ex.mean() / (ex.std() / np.sqrt(sel.notna().sum())) if sel.notna().sum() > 1 else np.nan,
                    "n_needed_for_t2": (2 * ex.std() / abs(ex.mean()))**2 if sel.notna().sum() > 1 and ex.mean() != 0 else np.nan})
    out["counts"] = pd.DataFrame(rows)
    out["forecast_dist"] = pd.concat(fdist, axis=1)
    out["raw_rsi_signal"] = pd.DataFrame(rsi_rows)
    out["variation_by_threshold"] = pd.DataFrame(vary)
    return out
