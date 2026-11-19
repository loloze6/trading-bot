import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    RAW = "debug_info.components.grind_fall.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: the coin fell over the past 72 bars. The expected side is short.
    # The raw component value is signed by the 72-bar net return, so raw < 0 means a net fall.
    # Where the raw value is missing, use the in-window 72-bar return from the prices.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            raw = (df[RAW].astype(float).values if RAW in df.columns
                   else np.full(len(df), np.nan))
            past_ret = np.full(len(df), np.nan)
            if len(df) > H:
                past_ret[H:] = close[H:] / close[:-H] - 1.0
            fell = np.where(~np.isnan(raw), raw < 0,
                            np.where(~np.isnan(past_ret), past_ret < 0, False))
            active = (~np.isnan(fc)) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & fell & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean case gain (forecast/10 x excess 72-bar forward return), non-overlapping grid, forecast < 0"
    main_thr = "confirm: mean > 0 with t >= 2 (and supporting difference < 0); reject: mean < 0 with t <= -2"
    sup_name = "excess 72-bar return, forecast below median minus above median (Welch t)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars after a "
                           "72-bar net fall, so the config does not do what the plan's Fidelity says."
                           if n_active > 0 else "No active bars to check against the plan's situation."),
            "reading": "The situation is taken as the sign of the raw component (the 72-bar net return sign), "
                       "with the in-window price return used where the raw value is missing.",
        }

    # ---------- 2. Criterion ----------
    # Non-overlapping grid per window: positions 0, 72, 144, ..., with the forward return inside the window.
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n:
                    fwd = close[i + H] / close[i] - 1.0
                    rows.append((coin, w, fc[i], fwd))
    grid = pd.DataFrame(rows, columns=["coin", "window", "forecast", "fwd"])
    grid = grid.dropna(subset=["fwd"])

    # The coin's mean 72-bar return over all its windows (all grid bars).
    coin_mean = grid.groupby("coin")["fwd"].mean()
    grid["excess"] = grid["fwd"] - grid["coin"].map(coin_mean)

    sample = grid[(grid["forecast"].notna()) & (grid["forecast"] < 0)].copy()
    n_case = int(len(sample))
    sample["gain"] = sample["forecast"] / 10.0 * sample["excess"]

    mean_gain = float(sample["gain"].mean()) if n_case > 0 else None
    t_main = None
    if n_case > 1:
        sd = sample["gain"].std(ddof=1)
        if sd > 0:
            t_main = float(mean_gain / (sd / np.sqrt(n_case)))

    # Supporting check: below-median (larger grind) minus above-median excess return.
    diff, t_sup, n_lo, n_hi = None, None, 0, 0
    if n_case > 0:
        med = sample["forecast"].median()
        lo = sample.loc[sample["forecast"] < med, "excess"]
        hi = sample.loc[sample["forecast"] > med, "excess"]
        n_lo, n_hi = int(len(lo)), int(len(hi))
        if n_lo > 0 and n_hi > 0:
            diff = float(lo.mean() - hi.mean())
        if n_lo > 1 and n_hi > 1:
            tt = stats.ttest_ind(lo.values, hi.values, equal_var=False)
            t_sup = float(tt.statistic) if np.isfinite(tt.statistic) else None
    sup_passed = None if diff is None else bool(diff < 0)

    counts = {
        "grid bars with a negative forecast": n_case,
        "grid bars below median forecast": n_lo,
        "grid bars above median forecast": n_hi,
    }

    if n_case < 300:
        status = "not observable"
        decided = f"Only {n_case} grid bars have a negative forecast, below the plan's minimum of 300."
    elif t_main is None:
        status = "inconclusive"
        decided = "The main t cannot be computed (zero dispersion), so neither rule is met."
    elif mean_gain > 0 and t_main >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The mean gain is above 0 with t >= 2 and the supporting difference is below 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The main t is >= 2 but the supporting difference is 0 or above (inconclusive rule)."
    elif mean_gain < 0 and t_main <= -2:
        status = "rejected"
        decided = "The mean gain is below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The main t is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_gain,
            "statistic": None if t_main is None else {"name": "t of the mean", "value": t_main},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name,
            "value": diff,
            "passed": sup_passed,
            "welch_t": t_sup,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid bars are at positions 0, 72, 144, ... of each window and need an in-window forward return; "
                    "each coin's mean 72-bar return is taken over all its grid bars in all windows; bars equal to the "
                    "median forecast are left out of both groups of the supporting check; the plan's 'fewer than 300 "
                    "grid bars' minimum is treated as 'not observable'."),
    }
