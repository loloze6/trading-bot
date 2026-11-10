import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_BLOCKS = 50
    MIN_POS_BLOCKS = 20
    PREFIX = "debug_info.components."
    SUFFIX = ".last_history_value"

    # ---------- locate the raw component column ----------
    def find_raw_col(df):
        preferred = PREFIX + "ma_dist" + SUFFIX
        if preferred in df.columns:
            return preferred, False
        cands = [c for c in df.columns if c.startswith(PREFIX) and c.endswith(SUFFIX)]
        if cands:
            return sorted(cands)[0], True
        return None, True

    # ---------- 1. situation check ----------
    n_active = 0
    n_ok = 0
    raw_col_used = None
    used_fallback = False
    missing_raw = False
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            col, fb = find_raw_col(df)
            if col is None:
                missing_raw = True
                continue
            raw_col_used = col
            used_fallback = used_fallback or fb
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[col], errors="coerce")
            mask = f.notna() & raw.notna() & (f != 0)
            n_active += int(mask.sum())
            # Situation: close above its 200-day SMA (raw distance > 0); side: long (forecast > 0)
            n_ok += int((mask & (raw > 0) & (f > 0)).sum())

    if missing_raw and raw_col_used is None:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": 0.0, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {},
            "decided_by": "The record holds no raw value of the config's component, so the situation "
                          "'close above its 200-day SMA' cannot be checked against the forecast.",
            "reading": "none",
        }

    agreement = (n_ok / n_active) if n_active > 0 else 1.0
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast have the close above its "
                          "200-day SMA with a long forecast, so the config does not trade the plan's "
                          "situation on the plan's side.",
            "reading": "Situation taken as raw component value > 0 (close above SMA200) with forecast > 0"
                       + (f"; raw column '{raw_col_used}' used since 'ma_dist' was absent." if used_fallback else "."),
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, f0 = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f0)) or c0 <= 0 or c1 <= 0:
                    continue
                xs.append(float(f0))
                ys.append(float(np.log(c1 / c0)))

    x = np.array(xs)
    y = np.array(ys)
    n_blocks = int(len(x))
    n_pos = int((x > 0).sum())

    slope = None
    tstat = None
    if n_blocks >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        if res.stderr is not None and res.stderr > 0:
            tstat = float(res.slope / res.stderr)

    share_all = float((y > 0).mean()) if n_blocks > 0 else None
    share_pos = float((y[x > 0] > 0).mean()) if n_pos > 0 else None
    sup_value = (share_pos - share_all) if (share_pos is not None and share_all is not None) else None
    sup_passed = (sup_value > 0) if sup_value is not None else None

    if n_blocks < MIN_BLOCKS or n_pos < MIN_POS_BLOCKS:
        status = "inconclusive"
        decided = (f"Inconclusive: {n_blocks} non-overlapping blocks (minimum 50) and {n_pos} starting "
                   f"with forecast > 0 (minimum 20).")
    elif tstat is None:
        status = "inconclusive"
        decided = "Inconclusive: the slope t-stat cannot be computed (no variation in the forecast)."
    elif tstat >= 2 and sup_passed:
        status = "confirmed"
        decided = ("Confirmed: slope t-stat >= 2 and the share of positive 10-bar returns is higher in "
                   "forecast > 0 blocks than in all blocks.")
    elif tstat <= -2:
        status = "rejected"
        decided = "Rejected: slope t-stat <= -2, moves above the average reverse."
    elif tstat >= 2:
        status = "inconclusive"
        decided = ("Inconclusive: slope t-stat >= 2 but the supporting share is not higher in forecast > 0 "
                   "blocks, so the confirm rule is not met and neither is the reject rule.")
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope t-stat lies between -2 and 2."

    reading = ("Blocks start at positions 0, 10, 20, ... of each window and need close[t+10] inside the window; "
               "the t-stat is the OLS slope over its standard error; the supporting check passes when the "
               "forecast > 0 share minus the all-blocks share is > 0; t >= 2 with a failed supporting check is "
               "read as inconclusive")
    if used_fallback:
        reading += f"; raw column '{raw_col_used}' was used for the situation check since 'ma_dist' was absent"
    if n_active == 0:
        reading += "; with no active bars the situation check passes vacuously"
    reading += "."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "OLS slope of next-10-bar log return on forecast at block start",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tstat} if tstat is not None else None,
            "threshold": "confirm if t >= 2 (with supporting check); reject if t <= -2; else inconclusive",
        },
        "supporting_check": {
            "name": "share of positive 10-bar returns, forecast > 0 blocks minus all blocks",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": {
            "non_overlapping_blocks": n_blocks,
            "blocks_with_forecast_gt_0": n_pos,
        },
        "decided_by": decided,
        "reading": reading,
    }
