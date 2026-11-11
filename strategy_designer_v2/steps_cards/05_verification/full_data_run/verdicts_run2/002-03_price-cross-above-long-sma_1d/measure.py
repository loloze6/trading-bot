import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.above_ma.last_history_value"

    # ---------- 1. Situation check: close above its 200-day SMA, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    main_name = "mean excess forward 10-bar return on positioned non-overlapping blocks (vs coin's window mean over all bars)"
    threshold = "confirm: mean > 0 with t >= 2 and hit-rate difference > 0; reject: mean < 0 with t <= -2; inconclusive otherwise or if < 100 positioned blocks pooled or < 10 per coin"

    if agreement is None:
        return {
            "status": "inconclusive",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"positioned blocks pooled": 0},
            "decided_by": "There are no bars with a non-zero forecast, so no positioned blocks exist and the minimum counts are not met.",
            "reading": "With no active bars the situation check cannot be computed and the result is treated as inconclusive.",
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars where the close is above its 200-day SMA (raw distance > 0), so the config does not trade the plan's situation.",
            "reading": "The situation is taken as the raw MovingAverageDistance value being strictly positive, with a positive forecast as the long side.",
        }

    # ---------- 2. Criterion ----------
    excess_pos = []
    fwd_pos = []
    fc_pos = []
    all_block_up = []
    per_coin = {}

    for coin, wins in bars.items():
        per_coin.setdefault(coin, 0)
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            fwd = close.shift(-H) / close - 1.0
            fwd = fwd.replace([np.inf, -np.inf], np.nan)
            mean_all = fwd.dropna().mean() if fwd.notna().any() else np.nan
            grid = np.arange(0, len(d), H)
            for i in grid:
                r = fwd.iloc[i]
                if not np.isfinite(r):
                    continue
                all_block_up.append(1.0 if r > 0 else 0.0)
                f = fc.iloc[i]
                if pd.notna(f) and f > 0 and np.isfinite(mean_all):
                    excess_pos.append(r - mean_all)
                    fwd_pos.append(r)
                    fc_pos.append(float(f))
                    per_coin[coin] += 1

    n_pos = len(excess_pos)
    mean_ex = float(np.mean(excess_pos)) if n_pos > 0 else None
    t_val = None
    if n_pos >= 2:
        sd = float(np.std(excess_pos, ddof=1))
        if sd > 0:
            t_val = float(mean_ex / (sd / np.sqrt(n_pos)))

    hit_diff = None
    if n_pos > 0 and len(all_block_up) > 0:
        hit_pos = float(np.mean([1.0 if r > 0 else 0.0 for r in fwd_pos]))
        hit_all = float(np.mean(all_block_up))
        hit_diff = hit_pos - hit_all

    slope = None
    if n_pos >= 3 and np.std(fc_pos) > 0:
        slope = float(stats.linregress(np.array(fc_pos), np.array(fwd_pos)).slope)

    min_coin = int(min(per_coin.values())) if per_coin else 0
    counts = {"positioned blocks pooled": int(n_pos)}
    for c, n in per_coin.items():
        counts["positioned blocks " + str(c)] = int(n)

    supp = {
        "name": "hit-rate difference (positioned blocks minus all blocks); slope of forward return on forecast reported",
        "value": hit_diff,
        "passed": (None if hit_diff is None else bool(hit_diff > 0)),
        "slope_forward_return_on_forecast": slope,
    }

    if n_pos < 100 or min_coin < 10:
        status = "inconclusive"
        decided = "Fewer than 100 positioned non-overlapping 10-bar blocks pooled, or fewer than 10 for at least one coin, so the result is inconclusive."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed, so the result is inconclusive."
    elif mean_ex > 0 and t_val >= 2 and hit_diff is not None and hit_diff > 0:
        status = "confirmed"
        decided = "The mean excess forward return is above 0 with t >= 2 and the hit-rate difference is above 0."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean excess forward return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, or t >= 2 without a positive hit-rate difference, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": (None if t_val is None else {"name": "one-sample t of the mean excess", "value": t_val}),
            "threshold": threshold,
        },
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": "Blocks are the bars at positions 0, 10, 20, ... of each window with forecast > 0; the coin's mean is taken over every bar of the window with a valid forward return; the hit rate across all blocks uses the same grid; the slope is reported but only the hit-rate difference enters the confirm rule, as the plan writes; the per-coin minimum applies to every coin present in the record.",
    }
