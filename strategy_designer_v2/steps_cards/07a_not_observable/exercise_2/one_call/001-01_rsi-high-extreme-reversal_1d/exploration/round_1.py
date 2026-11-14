import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    fc_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            f = b["forecast"]
            rsi_raw = b["debug_info.components.rsi_high.last_history_value"]
            post = b["debug_info.components.rsi_high.post_pipeline_value"]
            rsi = 50 - rsi_raw
            c = b["close"].values
            fwd = pd.Series(c).shift(-5).values / c - 1
            fwd = pd.Series(fwd, index=b.index)
            base = fwd.mean()
            grid = np.arange(len(b)) % 5 == 0
            def cnt(mask):
                return int(mask.sum())
            rows.append({
                "coin": coin, "win": w, "bars": len(b),
                "fc_nonzero": cnt(f < 0),
                "fc<=-1": cnt(f <= -1), "fc<=-5": cnt(f <= -5), "fc<=-10": cnt(f <= -10),
                "fc<=-10_grid": cnt((f <= -10) & grid & fwd.notna()),
                "fc<=-5_grid": cnt((f <= -5) & grid & fwd.notna()),
                "fc<0_grid": cnt((f < 0) & grid & fwd.notna()),
                "rsi>60": cnt(rsi > 60), "rsi>70": cnt(rsi > 70), "rsi>80": cnt(rsi > 80),
                "rsi_mean": rsi.mean(), "rsi_max": rsi.max(),
                "fc_min": f.min(), "post_min": post.min(),
                "fwd5_mean": base, "fwd5_std": fwd.std(),
            })
            # excess at various thresholds, all bars (overlapping) and grid
            for thr in [0, -1, -5, -10]:
                m = (f < thr) if thr == 0 else (f <= thr)
                for g in ["all", "grid"]:
                    mm = m & fwd.notna() & (grid if g == "grid" else True)
                    x = (fwd[mm] - base)
                    fc_rows.append({"coin": coin, "thr": thr, "sample": g, "n": len(x),
                                    "mean_excess": x.mean() if len(x) else np.nan,
                                    "std": x.std() if len(x) > 1 else np.nan,
                                    "t": stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan})
            # rsi>70 excess
            for lvl in [60, 70]:
                mm = (rsi > lvl) & fwd.notna()
                x = fwd[mm] - base
                fc_rows.append({"coin": coin, "thr": f"rsi>{lvl}", "sample": "all", "n": len(x),
                                "mean_excess": x.mean() if len(x) else np.nan, "std": x.std() if len(x)>1 else np.nan,
                                "t": stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan})
            # z-score spread: post value distribution among nonzero
            q = f[f < 0].quantile([0.1, 0.25, 0.5, 0.75, 0.9]) if (f < 0).any() else pd.Series(dtype=float)
            out["fc_quantiles_nonzero_" + coin] = q
            # runs of fc<=-10
            ext = (f <= -10).astype(int)
            runs = (ext.diff() == 1).sum() + (ext.iloc[0] == 1)
            out["episodes_fc<=-10_" + coin] = int(runs)
            ts = pd.to_datetime(b["timestamp"])
            out["span_days_" + coin + w] = float((ts.iloc[-1] - ts.iloc[0]).days)
    out["summary"] = pd.DataFrame(rows)
    out["excess"] = pd.DataFrame(fc_rows)
    return out
