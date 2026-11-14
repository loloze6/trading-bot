import numpy as np
import pandas as pd


def measure(bars):
    def col(df, name):
        return df[name] if name in df.columns else None

    chk_total = 0
    chk_agree = 0
    products = []
    fc_list = []

    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            volume = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            # Raw 1-day change: from the recorded component, falling back to the close.
            raw = col(df, "debug_info.components.drop.last_history_value")
            if raw is not None:
                move = pd.to_numeric(raw, errors="coerce")
                move = move.where(move.notna(), close.pct_change())
            else:
                move = close.pct_change()

            # 20-bar mean volume, current bar included, inside this window only.
            vmean = volume.rolling(20, min_periods=20).mean()

            # Situation check: a down day on volume at or above its 20-bar mean, short side.
            active = fc.notna() & (fc != 0)
            valid = active & move.notna() & vmean.notna() & volume.notna()
            situation = (move < 0) & (volume >= vmean)
            chk_total += int(valid.sum())
            chk_agree += int((valid & situation & (fc < 0)).sum())

            # Main measure: position times demeaned next-bar return.
            nxt = close.shift(-1) / close - 1.0
            mean_ret = nxt.dropna().mean() if nxt.notna().any() else np.nan
            sel = active & nxt.notna()
            if sel.any() and np.isfinite(mean_ret):
                prod = (fc[sel] / 10.0) * (nxt[sel] - mean_ret)
                products.extend(prod.tolist())
                fc_list.extend(fc[sel].tolist())

    agreement = (chk_agree / chk_total) if chk_total > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean demeaned per-bar gain (forecast/10 x next-bar return minus window mean daily return)"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; at least 40 active bars"
    reading = ("The 20-bar mean volume includes the current bar and is computed inside each window, so active bars in the "
               "first 19 rows of a window are left out of the situation check; the window's mean daily return is the "
               "mean of all its next-bar close-to-close returns; for the supporting check, active bars are sorted by "
               "forecast, and with an odd count the middle bar is dropped.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars pooled across windows": int(len(products))},
            "decided_by": ("Fewer than 90% of the active bars are high-volume down days (1-day change below 0 with "
                           "volume at or above its 20-bar mean) with a short forecast, so the config does not "
                           "do what the plan's situation says."),
            "reading": reading,
        }

    p = np.asarray(products, dtype=float)
    n = len(p)
    mean = float(p.mean()) if n > 0 else None
    t = None
    if n > 1:
        sd = p.std(ddof=1)
        if sd > 0:
            t = float(mean / (sd / np.sqrt(n)))

    # Supporting check: the larger-short half against the smaller-short half.
    sup_val = None
    sup_pass = None
    if n >= 2:
        f = np.asarray(fc_list, dtype=float)
        order = np.argsort(f, kind="mergesort")  # most negative (largest short) first
        half = n // 2
        larger = p[order[:half]]
        smaller = p[order[n - half:]]
        if len(larger) > 0 and len(smaller) > 0:
            sup_val = float(larger.mean() - smaller.mean())
            sup_pass = bool(sup_val > 0)
    supporting = {"name": "larger-short half minus smaller-short half mean demeaned gain",
                  "value": sup_val, "passed": sup_pass}

    counts = {"active bars pooled across windows": int(n)}

    if n < 40:
        status = "not observable"
        decided = "Fewer than 40 active bars pooled across windows, below the plan's minimum count."
    elif mean is not None and t is not None and mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean demeaned per-bar gain is above 0 with t >= 2 (confirm rule)."
    elif mean is not None and t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean demeaned per-bar gain is below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2 with at least 40 active bars, so it neither confirms nor rejects."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
