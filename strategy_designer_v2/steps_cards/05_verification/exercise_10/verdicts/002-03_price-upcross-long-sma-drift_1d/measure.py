import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_BLOCKS = 50
    MIN_POS_BLOCKS = 20

    def find_raw_col(df):
        preferred = "debug_info.components.ma_dist.last_history_value"
        if preferred in df.columns:
            return preferred
        cands = [c for c in df.columns
                 if c.startswith("debug_info.components.") and c.endswith(".last_history_value")]
        return cands[0] if cands else None

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    raw_missing = False
    for coin, wins in bars.items():
        for w, df in wins.items():
            col = find_raw_col(df)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if col is None:
                active = f.notna() & (f != 0)
                n_active += int(active.sum())
                raw_missing = True
                continue
            raw = pd.to_numeric(df[col], errors="coerce")
            ok = f.notna() & raw.notna()
            active = ok & (f != 0)
            situation = raw > 0  # close above its 200-day SMA (positive distance)
            agree = active & situation & (f > 0)  # expected side: long
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the close is above "
                           "its 200-day SMA (component raw distance > 0)"
                           + ("; the component's raw value column is missing" if raw_missing else "") + "."),
            "reading": "The situation is taken as the component's raw value (percent distance from the 200-day SMA) "
                       "being above zero, with a positive forecast as the long side.",
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, ft = close[t], close[t + H], f[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(ft)) or c0 <= 0 or c1 <= 0:
                    continue
                xs.append(ft)
                ys.append(np.log(c1 / c0))

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_blocks = int(len(x))
    n_pos = int((x > 0).sum())

    slope = None
    tstat = None
    if n_blocks >= 3 and np.ptp(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        if res.stderr is not None and res.stderr > 0 and np.isfinite(res.stderr):
            tstat = float(res.slope / res.stderr)

    share_all = float((y > 0).mean()) if n_blocks > 0 else None
    share_pos = float((y[x > 0] > 0).mean()) if n_pos > 0 else None
    if share_all is not None and share_pos is not None:
        sup_value = share_pos - share_all
        sup_passed = bool(sup_value > 0)
    else:
        sup_value = None
        sup_passed = None

    counts = {"non-overlapping blocks": n_blocks, "blocks starting with forecast > 0": n_pos}

    if n_blocks < MIN_BLOCKS:
        status = "not observable"
        decided = f"Only {n_blocks} non-overlapping 10-bar blocks exist, fewer than the 50 the plan requires."
    elif n_pos < MIN_POS_BLOCKS:
        status = "not observable"
        decided = f"Only {n_pos} blocks start with forecast > 0, fewer than the 20 the plan requires."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope t-stat cannot be computed (no variation in the forecast), so it meets neither the confirm nor the reject rule."
    elif tstat >= 2 and sup_passed:
        status = "confirmed"
        decided = "Slope t-stat >= 2 and the share of positive returns is higher in forecast > 0 blocks than in all blocks."
    elif tstat <= -2:
        status = "rejected"
        decided = "Slope t-stat <= -2: moves above the average reverse."
    else:
        status = "inconclusive"
        if tstat >= 2:
            decided = "Slope t-stat >= 2 but the share of positive returns is not higher in forecast > 0 blocks than in all blocks, so neither confirm nor reject holds."
        else:
            decided = "Slope t-stat lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "OLS slope (with intercept) of next-10-bar log return on forecast at block start",
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
            "threshold": "slope t-stat >= 2 confirms (with supporting share higher), <= -2 rejects",
        },
        "supporting_check": {
            "name": "share of positive 10-bar returns in forecast > 0 blocks minus share over all blocks",
            "value": None if sup_value is None else float(sup_value),
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The situation is the component's raw value (distance from the 200-day SMA, read from the record's "
                    "only last_history_value column when 'ma_dist' is absent) above zero with a positive forecast; blocks "
                    "start at positions 0, 10, 20, ... of each window and are kept only when the bar 10 later is in the same window."),
    }
