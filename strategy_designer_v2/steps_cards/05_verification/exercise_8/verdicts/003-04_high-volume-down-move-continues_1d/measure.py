import numpy as np
import pandas as pd


def measure(bars):
    DROP_COL = "debug_info.components.drop.last_history_value"

    # ---------- 1. Situation check ----------
    n_active_checked = 0
    n_agree = 0
    gains = []
    fcs = []

    for coin, windows in bars.items():
        for w, df in windows.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float)

            # Raw 1-day change: the component's raw value, or the close change if missing.
            chg = df[DROP_COL].astype(float) if DROP_COL in df.columns else pd.Series(np.nan, index=df.index)
            chg = chg.where(chg.notna(), close.pct_change())

            # 20-bar mean volume, current bar included, computed inside the window.
            vmean = vol.rolling(20, min_periods=20).mean()

            active = fc.notna() & (fc != 0)
            checkable = active & chg.notna() & vmean.notna() & vol.notna()
            situation = (chg < 0) & (vol >= vmean)
            agree = checkable & situation & (fc < 0)
            n_active_checked += int(checkable.sum())
            n_agree += int(agree.sum())

            # ---------- main measure inputs ----------
            ret_next = close.shift(-1) / close - 1.0
            win_mean = (close / close.shift(1) - 1.0).mean()
            ok = active & ret_next.notna()
            g = (fc[ok] / 10.0) * (ret_next[ok] - win_mean)
            gains.extend(g.tolist())
            fcs.extend(fc[ok].tolist())

    agreement = (n_agree / n_active_checked) if n_active_checked > 0 else 0.0
    passed = agreement >= 0.9

    threshold_txt = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; inconclusive otherwise or if fewer than 40 active bars"
    reading = ("Volume test uses a 20-bar rolling mean that includes the current bar, computed within each window. "
               "Bars before 20 bars of history are left out of the situation check. The position is forecast/10 as the plan says. "
               "The window mean daily return is the mean of close-to-close changes in that window. "
               "Active bars are non-zero-forecast bars with a next bar in the same window. "
               "The halves come from a rank split by forecast, most negative first, and the middle bar is dropped when the count is odd.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean demeaned per-bar gain (forecast/10 x next-bar return minus window mean)",
                             "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(len(gains))},
            "decided_by": ("Fewer than 90% of active bars are high-volume down days traded short: "
                           "the config's active bars do not match the plan's situation of a down day "
                           "with volume at or above its 20-bar mean, taken short."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    gains = np.asarray(gains, dtype=float)
    fcs = np.asarray(fcs, dtype=float)
    n = len(gains)
    mean = float(gains.mean()) if n > 0 else None
    t = None
    if n > 1:
        sd = gains.std(ddof=1)
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    # Supporting check: larger-short half vs smaller-short half
    sup_val, sup_pass = None, None
    if n >= 2:
        order = np.argsort(fcs, kind="mergesort")  # most negative first
        half = n // 2
        larger = gains[order[:half]]
        smaller = gains[order[n - half:]]
        sup_val = float(larger.mean() - smaller.mean())
        sup_pass = bool(sup_val > 0)

    if n < 40:
        status = "inconclusive"
        decided = "Fewer than 40 active bars pooled across windows, so the plan calls the result inconclusive."
    elif t is not None and mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean demeaned per-bar gain is above 0 with t >= 2, which meets the plan's confirm rule."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean demeaned per-bar gain is below 0 with t <= -2, which meets the plan's reject rule."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, so the plan calls the result inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean demeaned per-bar gain (forecast/10 x next-bar return minus window mean)",
                         "value": mean,
                         "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
                         "threshold": threshold_txt},
        "supporting_check": {"name": "larger-short half minus smaller-short half mean demeaned gain",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"active bars": int(n)},
        "decided_by": decided,
        "reading": reading,
    }
