import numpy as np
import pandas as pd


def measure(bars):
    move_col = "debug_info.components.drop.last_history_value"

    # ---------- 1. Situation check ----------
    n_active_checked = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if move_col in df.columns:
                move = pd.to_numeric(df[move_col], errors="coerce")
            else:
                move = df["close"].astype(float).pct_change()
            vol = pd.to_numeric(df["volume"], errors="coerce")
            vol_mean = vol.rolling(20, min_periods=20).mean()
            active = fc.notna() & (fc != 0)
            computable = move.notna() & vol_mean.notna() & vol.notna()
            mask = active & computable
            situation = (vol >= vol_mean) & (move < 0)
            agree = situation & (fc < 0)
            n_active_checked += int(mask.sum())
            n_agree += int((agree & mask).sum())

    agreement = (n_agree / n_active_checked) if n_active_checked > 0 else None
    passed = agreement is not None and agreement >= 0.9

    threshold_words = ("confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; "
                       "otherwise, or fewer than 40 active bars, inconclusive")
    main_name = "mean demeaned per-bar gain of (forecast/10) x next-bar return"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement),
                                "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_words},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active_checked)},
            "decided_by": ("Fewer than 90% of active bars are high-volume down days (1-day change < 0 "
                           "with volume at or above its 20-bar mean) held short, so the config does not "
                           "do what the plan's Fidelity describes."),
            "reading": ("The 20-bar mean volume includes the current bar and is computed within each "
                        "window, so the first 19 bars of each window are left out of the check."),
        }

    # ---------- 2. Criterion ----------
    gains = []
    fcs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            window_mean = nxt.dropna().mean()
            ok = fc.notna() & (fc != 0) & nxt.notna()
            g = (fc[ok] / 10.0) * (nxt[ok] - window_mean)
            gains.extend(g.tolist())
            fcs.extend(fc[ok].tolist())

    gains = np.asarray(gains, dtype=float)
    fcs = np.asarray(fcs, dtype=float)
    n = len(gains)

    mean = float(gains.mean()) if n > 0 else None
    if n > 1:
        sd = gains.std(ddof=1)
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None
    else:
        t = None

    # Supporting check
    sup_value = None
    sup_passed = None
    if n >= 2:
        order = np.argsort(fcs, kind="mergesort")  # most negative (larger short) first
        half = n // 2
        larger = gains[order[:half]]
        smaller = gains[order[n - half:]]
        if len(larger) > 0 and len(smaller) > 0:
            sup_value = float(larger.mean() - smaller.mean())
            sup_passed = bool(sup_value > 0)

    if n < 40 or t is None:
        status = "inconclusive"
        decided = "Fewer than 40 active bars pooled across windows (or no t-statistic), so the result is inconclusive."
    elif mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean demeaned per-bar gain is above 0 with t >= 2, so the plan confirms."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean demeaned per-bar gain is below 0 with t <= -2, so the plan rejects."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, so the result is neither confirmed nor rejected."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": None if t is None else {"name": "t of the mean", "value": t},
            "threshold": threshold_words,
        },
        "supporting_check": {
            "name": "mean gain larger-short half minus smaller-short half",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": {"active bars pooled across windows": int(n)},
        "decided_by": decided,
        "reading": ("The position is forecast/10 as the plan states, and the window's mean daily return is "
                    "the mean of all next-bar close-to-close returns in that window. The 20-bar mean volume "
                    "includes the current bar and is computed within each window. For the supporting check, "
                    "active bars are sorted by forecast; the floor(n/2) most negative bars form the larger-short "
                    "half and the floor(n/2) least negative bars form the smaller-short half, and the middle bar "
                    "is dropped when n is odd."),
    }
