def explore(data):
    import numpy as np, pandas as pd
    out = {}
    out["coins_windows"] = pd.DataFrame([(c, w, len(data["bars"][c][w])) for c in data["bars"] for w in data["bars"][c]], columns=["coin","window","bars"])
    rows = []; dist = []; fwd_rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            f = b["forecast"]; rsi = b["debug_info.components.rsi_high.last_history_value"]
            raw = b["debug_info.components.rsi_high.post_pipeline_value"]
            fwd = b["close"].shift(-5)/b["close"]-1
            grid = b.index % 5 == 0
            r = {"coin": c, "window": w, "bars": len(b),
                 "fc_nonzero": int((f < 0).sum()), "fc<=-5": int((f <= -5).sum()),
                 "fc<=-10": int((f <= -10).sum()), "fc<=-15": int((f <= -15).sum()), "fc<=-20": int((f <= -20).sum()),
                 "grid_fc<=-10_fwd": int(((f <= -10) & grid & fwd.notna()).sum()),
                 "rsi_raw_min": float(rsi.min()), "rsi_raw_max": float(rsi.max()),
                 "rsi_raw_mean": float(rsi.mean()),
                 "forecast_min": float(f.min()), "fc_mean_when_short": float(f[f<0].mean()) if (f<0).any() else np.nan}
            # episodes of forecast<=-10
            m = (f <= -10).astype(int)
            r["episodes_fc<=-10"] = int(((m.diff() == 1) | ((m.index == 0) & (m == 1))).sum())
            rows.append(r)
            dist.append(pd.cut(f, [-20.01, -15, -10, -5, -1, -1e-9, 0.01, 21]).value_counts().sort_index().rename(c+"_"+w))
            base = fwd.mean()
            for thr in [0, -1, -5, -10]:
                sel = (f <= thr) & (f < 0) & fwd.notna()
                selg = sel & grid
                ex = fwd[sel] - base
                exg = fwd[selg] - base
                fwd_rows.append({"thr": thr, "n_all": int(sel.sum()), "mean_ex_all": ex.mean(), "sd_ex_all": ex.std(),
                                 "n_grid": int(selg.sum()), "mean_ex_grid": exg.mean(),
                                 "t_grid": exg.mean()/(exg.std()/np.sqrt(len(exg))) if len(exg) > 1 else np.nan})
            fwd_rows.append({"thr": "all_bars", "n_all": int(fwd.notna().sum()), "mean_ex_all": 0, "sd_ex_all": fwd.std(),
                             "n_grid": int((grid & fwd.notna()).sum()), "mean_ex_grid": np.nan, "t_grid": np.nan})
            out["rsi_share_above"] = pd.Series({k: float((rsi > k).mean()) for k in [50, 60, 65, 70, 75, 80]})
            out["post_vs_forecast_corr"] = float(np.corrcoef(raw.fillna(0), f.fillna(0))[0,1])
    out["summary"] = pd.DataFrame(rows)
    out["forecast_bins"] = pd.concat(dist, axis=1)
    out["fwd_excess"] = pd.DataFrame(fwd_rows)
    return out
