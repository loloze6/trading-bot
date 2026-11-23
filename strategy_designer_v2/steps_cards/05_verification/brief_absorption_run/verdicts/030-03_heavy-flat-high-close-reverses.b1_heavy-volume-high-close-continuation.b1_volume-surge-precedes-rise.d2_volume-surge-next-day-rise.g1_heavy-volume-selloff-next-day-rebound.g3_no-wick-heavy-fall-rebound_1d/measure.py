import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    MIN_CASES = 200

    # ---------- 1. Situation check: down day with volume >= prior 20-day mean, long side ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0

    # ---------- 2. Data for the criterion ----------
    case_fc = []
    case_excess = []

    for coin in sorted(bars.keys()):
        windows = bars[coin]
        # the coin's mean daily return over all its windows together (never across two windows)
        all_rets = []
        prepared = {}
        for w in sorted(windows.keys(), key=lambda s: (len(str(s)), str(s))):
            df = windows[w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            vr = vol / vol.rolling(20, min_periods=20).mean().shift(1)
            nxt = close.shift(-1) / close - 1.0
            all_rets.append(nxt.dropna().values)
            prepared[w] = (fc, ret1, vr, nxt)

            # situation check on active bars
            active = fc.notna() & (fc != 0)
            computable = ret1.notna() & vr.notna()
            situ = (ret1 < 0) & (vr >= 1.0)
            n_active_uncomputable += int((active & ~computable).sum())
            act_c = active & computable
            n_active += int(act_c.sum())
            n_agree += int((act_c & situ & (fc > 0)).sum())

        if len(all_rets) == 0:
            continue
        allr = np.concatenate(all_rets) if len(all_rets) else np.array([])
        if allr.size == 0:
            continue
        coin_mean = float(np.mean(allr))

        for w, (fc, ret1, vr, nxt) in prepared.items():
            m = fc.notna() & (fc > 0) & nxt.notna()
            if m.any():
                case_fc.extend(fc[m].astype(float).tolist())
                case_excess.extend((nxt[m] - coin_mean).astype(float).tolist())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    reading = ("Bars without 20 prior bars inside their window (vr not recomputable from prices) are left out of the "
               "agreement share; the coin's mean daily return is the mean of all its 1-bar returns inside its windows; "
               "cases equal to the median forecast belong to neither half; the plan's 'fewer than 200 cases' minimum "
               "is reported as not observable, as the workflow requires.")

    main_name = "mean of forecast x (next-day return - coin mean daily return) on forecast > 0 bars"
    threshold = "t >= 2 (with supporting check > 0) confirms; t <= -2 rejects; otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active),
                       "active bars not checkable": int(n_active_uncomputable)},
            "decided_by": ("Fewer than 90% of active bars are down days with volume at or above the prior 20-day "
                           "mean with a long forecast, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    fcs = np.asarray(case_fc, dtype=float)
    exc = np.asarray(case_excess, dtype=float)
    n = int(fcs.size)
    counts = {"cases with forecast > 0": n}

    vals = fcs * exc
    mean_v = float(np.mean(vals)) if n > 0 else None
    t_v = None
    if n > 1:
        sd = float(np.std(vals, ddof=1))
        t_v = float(mean_v / (sd / np.sqrt(n))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    if n > 0:
        med = float(np.median(fcs))
        hi = exc[fcs > med]
        lo = exc[fcs < med]
        counts["cases above median forecast"] = int(hi.size)
        counts["cases below median forecast"] = int(lo.size)
        if hi.size > 0 and lo.size > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": mean_v,
            "statistic": ({"name": "t of the mean", "value": t_v} if t_v is not None else None),
            "threshold": threshold}
    sup = {"name": "mean excess next-day return above minus below median forecast",
           "value": sup_val, "passed": sup_pass}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases with forecast > 0, fewer than the plan's minimum of 200."
    elif t_v is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed (zero dispersion), so neither rule is met."
    elif t_v >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The main measure's t is >= 2 and the supporting check is > 0 (confirm rule)."
    elif t_v <= -2:
        status = "rejected"
        decided = "The main measure's t is <= -2 (reject rule)."
    elif t_v >= 2:
        status = "inconclusive"
        decided = "The main measure's t is >= 2 but the supporting check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
