import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10

    def find_col(df, suffix):
        cols = [c for c in df.columns if c.startswith("debug_info.components.") and c.endswith(suffix)]
        return cols[0] if cols else None

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            raw_col = find_col(df, ".last_history_value")
            if raw_col is None:
                continue
            d = df[["forecast", raw_col]].dropna()
            active = d["forecast"] != 0
            n_active += int(active.sum())
            # situation: close below its 200-day SMA (raw distance < 0), expected side short
            agree = active & (d[raw_col] < 0) & (d["forecast"] < 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of excess forward 10-bar log return on forecast, short-bar non-overlapping blocks"
    threshold = "slope t >= +2 confirms (with mean excess < 0 and higher decline share); t <= -2 rejects; else inconclusive; < 15 short blocks inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars are short bars with the close below its 200-day SMA, so the config does not trade the plan's situation on its side.",
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    all_fwd = []          # forward 10-bar log returns on all tested bars
    grid_fc = []          # forecast on grid bars
    grid_fwd = []         # forward log return on grid bars
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = np.log(close[H:] / close[: n - H])
            ok = np.isfinite(fwd)
            all_fwd.extend(fwd[ok].tolist())
            for i in range(0, n, H):
                if np.isfinite(fwd[i]) and np.isfinite(fc[i]):
                    grid_fc.append(fc[i])
                    grid_fwd.append(fwd[i])

    all_fwd = np.array(all_fwd)
    grid_fc = np.array(grid_fc)
    grid_fwd = np.array(grid_fwd)
    baseline = float(np.mean(all_fwd)) if len(all_fwd) else np.nan

    short = grid_fc < 0
    n_short_blocks = int(short.sum())
    n_all_blocks = int(len(grid_fwd))

    x = grid_fc[short]
    y = grid_fwd[short] - baseline
    slope = None
    t_stat = None
    if n_short_blocks >= 3 and np.ptp(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_stat = float(res.slope / res.stderr) if res.stderr > 0 else None
    mean_excess = float(np.mean(y)) if n_short_blocks > 0 else None

    share_short = float(np.mean(grid_fwd[short] < 0)) if n_short_blocks > 0 else None
    share_all = float(np.mean(grid_fwd < 0)) if n_all_blocks > 0 else None
    diff = (share_short - share_all) if (share_short is not None and share_all is not None) else None
    sup_passed = (diff > 0) if diff is not None else None

    if n_short_blocks < 15:
        status = "inconclusive"
        decided = "Fewer than 15 non-overlapping 10-bar blocks with forecast < 0 across the windows, so the run is inconclusive whatever the t-statistic."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The slope t-statistic cannot be computed, so no confirm or reject rule is met."
    elif t_stat <= -2:
        status = "rejected"
        decided = "Slope t-statistic <= -2: price rebounds after the close goes below the average, more strongly the deeper it is below."
    elif t_stat >= 2 and mean_excess is not None and mean_excess < 0 and sup_passed:
        status = "confirmed"
        decided = "Slope t-statistic >= +2, mean excess forward return on short bars below 0, and the share of declines on short-bar blocks higher than on all blocks."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "Slope t-statistic >= +2 but the mean excess return or the decline-share condition fails, so neither the confirm nor the reject rule is met."
    else:
        status = "inconclusive"
        decided = "The slope t-statistic lies between -2 and +2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_stat} if t_stat is not None else None,
            "threshold": threshold,
            "mean_excess_forward_return_short_blocks": mean_excess,
        },
        "supporting_check": {
            "name": "share of negative 10-bar returns: short blocks minus all blocks",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping 10-bar blocks with forecast < 0": n_short_blocks,
            "all non-overlapping 10-bar blocks": n_all_blocks,
        },
        "decided_by": decided,
        "reading": "The baseline is the mean forward 10-bar log return over every bar with a full in-window forward return, the regression and the shares use the per-window grid at positions 0, 10, 20, ..., the slope t is the OLS slope over its standard error, the mean excess in the confirm rule is taken on the short grid blocks, and a t >= +2 that fails the other confirm conditions is treated as inconclusive.",
    }
