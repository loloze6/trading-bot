import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.sma_cross_spread.last_history_value"

    in_rets, out_rets = [], []
    n_active = 0
    n_agree = 0
    n_stretches = 0

    for coin in bars:
        for window in bars[coin]:
            df = bars[coin][window].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)

            # --- situation check: active bars should be bars with SMA50 > SMA200, forecast long
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

            # --- distinct up-cross stretches: contiguous runs of raw spread > 0 inside this window
            pos = (raw > 0).fillna(False).astype(int).values
            if len(pos) > 0:
                starts = np.sum((pos[1:] == 1) & (pos[:-1] == 0)) + (1 if pos[0] == 1 else 0)
                n_stretches += int(starts)

            # --- next-bar returns inside the window only
            nxt = close.shift(-1) / close - 1.0
            valid = fc.notna() & nxt.notna() & np.isfinite(nxt)
            in_mask = valid & (fc > 0)
            out_mask = valid & (fc == 0)
            in_rets.extend(nxt[in_mask].astype(float).tolist())
            out_rets.extend(nxt[out_mask].astype(float).tolist())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    counts = {
        "in-stretch bars": int(len(in_rets)),
        "out-of-stretch bars": int(len(out_rets)),
        "distinct up-cross stretches": int(n_stretches),
    }

    reading = ("In-stretch bars are forecast > 0 and out-of-stretch bars forecast = 0 with next-bar returns taken inside each window; "
               "the situation is a positive raw SMA spread with a long forecast; a distinct up-cross stretch is a contiguous run of "
               "positive raw spread within one window; the supporting check passes when its difference is positive.")

    threshold = "confirm if difference > 0 with Welch t >= 2; reject if difference < 0 with t <= -2; else inconclusive; needs >= 100 in, >= 100 out, >= 3 stretches"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean next-bar return in-stretch minus out-of-stretch",
                             "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": ("Fewer than 90% of active bars are long bars with the 50-day SMA above the 200-day SMA, "
                           "so the config's forecast does not follow the plan's cross-to-cross long situation."),
            "reading": reading,
        }

    a = np.asarray(in_rets, dtype=float)
    b = np.asarray(out_rets, dtype=float)

    diff = None
    t_val = None
    if len(a) >= 2 and len(b) >= 2:
        diff = float(a.mean() - b.mean())
        t_res = stats.ttest_ind(a, b, equal_var=False)
        t_val = float(t_res.statistic) if np.isfinite(t_res.statistic) else None
    elif len(a) >= 1 and len(b) >= 1:
        diff = float(a.mean() - b.mean())

    sup_val = None
    sup_pass = None
    if len(a) > 0 and len(b) > 0:
        sup_val = float((a > 0).mean() - (b > 0).mean())
        sup_pass = bool(sup_val > 0)

    enough = len(a) >= 100 and len(b) >= 100 and n_stretches >= 3

    if not enough:
        status = "inconclusive"
        decided = ("Inconclusive: the test needs at least 100 in-stretch bars, 100 out-of-stretch bars and 3 distinct "
                   "up-cross stretches, and the record has fewer.")
    elif t_val is None or diff is None:
        status = "inconclusive"
        decided = "Inconclusive: the Welch t-statistic could not be computed."
    elif diff > 0 and t_val >= 2:
        status = "confirmed"
        decided = "Confirmed: the in-stretch minus out-of-stretch mean next-bar return is positive with Welch t >= 2."
    elif diff < 0 and t_val <= -2:
        status = "rejected"
        decided = "Rejected: the difference is negative with Welch t <= -2, so moves after up crosses reverse."
    else:
        status = "inconclusive"
        decided = "Inconclusive: |t| < 2 for the in-stretch minus out-of-stretch mean next-bar return."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean next-bar return in-stretch minus out-of-stretch",
            "value": diff,
            "statistic": ({"name": "Welch t", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "share of up next-bars in-stretch minus out-of-stretch",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
