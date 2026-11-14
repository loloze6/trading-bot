def explore(data):
    import numpy as np, pandas as pd
    out = {}
    inv = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            inv.append({"coin": c, "window": w, "bars": len(b), "years": str(sorted(pd.to_datetime(b["timestamp"]).dt.year.unique().tolist()))})
    out["inventory"] = pd.DataFrame(inv)
    rows = []; fwd_all = []; ext_all = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            f = b["forecast"].astype(float)
            raw = b["debug_info.components.rsi_high.last_history_value"].astype(float)
            rsi = 50 - raw
            cl = b["close"].astype(float).reset_index(drop=True)
            fwd = cl.shift(-5)/cl - 1
            fr = f.reset_index(drop=True)
            grid = np.arange(0, len(b), 5)
            g = fr.iloc[grid]
            gf = fwd.iloc[grid]
            ext = fr <= -10
            # runs of extreme
            runs = (ext & ~ext.shift(1, fill_value=False)).sum()
            rows.append({"coin": c, "window": w,
                         "bars_nonnull_fc": int(f.notna().sum()),
                         "bars_fc_lt0": int((f < 0).sum()),
                         "bars_fc_le_-10": int(ext.sum()),
                         "extreme_episodes": int(runs),
                         "grid_bars": len(grid),
                         "grid_extreme_with_fwd": int(((g <= -10) & gf.notna()).sum()),
                         "rsi_ge70": int((rsi >= 70).sum()), "rsi_ge60": int((rsi >= 60).sum()),
                         "rsi_mean": rsi.mean(), "rsi_max": rsi.max(),
                         "fwd5_std": fwd.std(), "fwd5_mean": fwd.mean(),
                         "fwd5_mean_ext_allbars": fwd[ext].mean(),
                         "first_bar_fc_nonzero": int(np.argmax(fr.fillna(0).values != 0)) if (fr.fillna(0)!=0).any() else -1})
            fwd_all.append(fwd); 
            out["forecast_quantiles"] = f.describe(percentiles=[.05,.1,.25,.5,.75])
            bins = pd.cut(f, [-20.01,-15,-10,-5,-1,-1e-9,1e-9,20])
            out["forecast_bins"] = bins.value_counts().sort_index()
            rb = pd.cut(rsi, [0,30,40,50,60,70,80,100])
            out["rsi_bins"] = rb.value_counts().sort_index()
            # z-score vs rsi: what rsi level gives fc<=-10
            out["rsi_when_ext"] = rsi[ext.values].describe()
            # how many extreme cases using all bars non-overlap from episode starts
    out["per_window"] = pd.DataFrame(rows).T
    # needed sample size given std
    s = pd.concat(fwd_all).std()
    out["cases_needed_for_t2_at_obs_effect"] = (2*s/0.0675)**2
    out["fwd5_std_pooled"] = s
    return out
