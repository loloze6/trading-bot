import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.sma_cross_spread.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw > 0) & (f > 0)
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
            "main_measure": {
                "name": "OLS slope of 10-bar excess return on forecast",
                "value": None,
                "statistic": None,
                "threshold": "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"non-overlapping samples": None, "samples with forecast > 0": None},
            "decided_by": (
                "Fewer than 90% of bars with a non-zero forecast are long bars with SMA50 above SMA200 "
                "(raw spread > 0), so the config does not follow the plan's situation and side."
            ),
            "reading": "Situation taken as raw SMA50-SMA200 spread > 0 with forecast > 0 (long).",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            if n <= H:
                continue
            fwd = np.full(n, np.nan)
            fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            drift_vals = fwd[np.isfinite(fwd)]
            if len(drift_vals) == 0:
                continue
            drift = float(np.mean(drift_vals))
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = fwd[i]
                fi = f[i]
                if np.isfinite(r) and np.isfinite(fi):
                    xs.append(float(fi))
                    ys.append(float(r - drift))

    x = np.array(xs)
    y = np.array(ys)
    n_total = int(len(x))
    n_pos = int((x > 0).sum())
    n_zero = int((x == 0).sum())
    counts = {"non-overlapping samples": n_total, "samples with forecast > 0": n_pos}

    # Supporting check
    if n_pos > 0 and n_zero > 0:
        share_pos = float(np.mean(y[x > 0] > 0))
        share_zero = float(np.mean(y[x == 0] > 0))
        diff = share_pos - share_zero
        supporting = {
            "name": "share of positive excess returns, forecast>0 minus forecast=0",
            "value": diff,
            "passed": bool(diff > 0),
        }
    else:
        supporting = {
            "name": "share of positive excess returns, forecast>0 minus forecast=0",
            "value": None,
            "passed": None,
        }

    slope = None
    tval = None
    if n_total >= 3 and np.var(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        if lr.stderr is not None and lr.stderr > 0:
            tval = float(lr.slope / lr.stderr)

    threshold = "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects; otherwise inconclusive"

    if n_total < 40 or n_pos < 15:
        status = "not observable"
        decided_by = (
            f"Minimum counts not reached: {n_total} non-overlapping samples (need 40) and "
            f"{n_pos} samples with forecast > 0 (need 15)."
        )
    elif slope is not None and tval is not None and slope > 0 and tval >= 2:
        status = "confirmed"
        decided_by = "Confirm rule met: the slope is positive with t >= 2."
    elif slope is not None and tval is not None and slope < 0 and tval <= -2:
        status = "rejected"
        decided_by = "Reject rule met: the slope is negative with t <= -2, moves after up-crosses reverse."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive rule met: the slope's t lies between -2 and 2 (or could not be computed)."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": "OLS slope of 10-bar excess return on forecast",
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided_by,
        "reading": (
            "The window's mean 10-bar return (holding drift) is the mean of the forward 10-bar return over all bars "
            "of that window that have one, samples are taken at positions 0, 10, 20, ... of each window with the "
            "full 10 bars inside the window, and the slope's t is the ordinary OLS t (slope / standard error)."
        ),
    }
