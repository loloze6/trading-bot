import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.range_pos.last_history_value"
    STRAT_REGIME = "unknown"  # the only regime with a strategy: the code's "rising" profile (no chop veto)

    def range_pos_from_prices(close):
        hi = close.rolling(20, min_periods=20).max()
        lo = close.rolling(20, min_periods=20).min()
        width = hi - lo
        pos = 2.0 * (close - lo) / width - 1.0
        return pos.where(width > 0, 0.0)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d[FC], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            raw = raw.fillna(range_pos_from_prices(close))
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            in_profile = regime == STRAT_REGIME
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & in_profile & raw.notna() & (np.sign(fc) == np.sign(raw)) & (raw != 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "t of the slope of the 5-bar forward return minus normal drift on the forecast"
    threshold = "confirm: slope positive with t >= 2; reject: slope negative with t <= -2; otherwise inconclusive; at least 100 non-overlapping in-profile cases"
    reading = ("The rising profile is taken as the bars whose regime is 'unknown' (the only regime with a strategy, the "
               "chop veto not applied), the expected side is the sign of the range position (raw value, or recomputed "
               "from 20 closes when not recorded); the slope's t is the ordinary least-squares t of the pooled "
               "regression with intercept, the drift is each coin's mean 5-bar return on the non-overlapping grid of "
               "all its windows, and the plan's minimum of 100 cases is treated as the minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping in-profile cases": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the active bars are rising-profile bars whose forecast sign matches the "
                           "close's side of the middle of its 20-day range (agreement %s)." %
                           ("n/a" if agreement is None else "%.3f" % agreement)),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d[FC], errors="coerce").values
            close = pd.to_numeric(d["close"], errors="coerce").values
            n = len(d)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                f = fc[t]
                if np.isfinite(f) and f != 0:
                    cases.append((f, r))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for f, r in cases:
            xs.append(float(f))
            ys.append(r - drift)

    n_cases = len(xs)
    counts = {"non-overlapping in-profile cases": int(n_cases)}

    slope = None
    tval = None
    if n_cases >= 3 and np.std(xs) > 0:
        res = stats.linregress(np.array(xs), np.array(ys))
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    if n_cases < 100:
        status = "not observable"
        decided_by = "Fewer than 100 non-overlapping in-profile cases (%d), so the data cannot show the idea." % n_cases
    elif tval is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed (no variation of the forecast), which meets neither the confirm nor the reject rule."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided_by = "The slope is positive with t of 2 or more (t = %.2f, %d cases)." % (tval, n_cases)
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided_by = "The slope is negative with t of -2 or less (t = %.2f, %d cases): closes high in the range are followed by below-drift moves." % (tval, n_cases)
    else:
        status = "inconclusive"
        decided_by = "A t between -2 and 2 is inconclusive (t = %.2f, %d cases)." % (tval, n_cases)

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": tval,
            "statistic": None if tval is None else {"name": "OLS t of the slope", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
