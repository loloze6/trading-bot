import numpy as np
import pandas as pd
from scipy import stats

H = 10
FC = "forecast"
RAW = "debug_info.components.mom28.last_history_value"
MIN_POS = 100


def _raw_mom(df):
    close = df["close"].astype(float).reset_index(drop=True)
    recomputed = close / close.shift(28) - 1.0
    if RAW in df.columns:
        raw = pd.to_numeric(df[RAW], errors="coerce").reset_index(drop=True)
        raw = raw.where(raw.notna(), recomputed)
    else:
        raw = recomputed
    return raw


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0 or FC not in df.columns:
                continue
            fc = pd.to_numeric(df[FC], errors="coerce").reset_index(drop=True)
            raw = _raw_mom(df)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (fc > 0) & raw.notna() & (raw > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of 10-day return minus normal drift on forecast, pooled non-overlapping grid cases"
    main_thr = "confirm if slope t >= 2 with supporting check passing; reject if t <= -2; otherwise inconclusive"
    sup_name = "mean 10-day return minus normal drift among grid cases with forecast > 0, above 0"
    reading_base = ("Situation = raw 28-day return > 0 with a long (positive) forecast, raw value recomputed from closes "
                    "where missing; grid = rows 0,10,20,... of each window with close[t+10] in the same window; normal "
                    "drift = each coin's mean grid 10-day return over all its windows; slope t from pooled OLS with "
                    "intercept; the plan's 'fewer than 100 grid cases with forecast > 0' minimum is reported as "
                    "'not observable' per the workflow rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a nonzero forecast are bars where the 28-day return is a rise "
                           "with a long forecast (agreement %.3f), so the config does not do what the Fidelity says."
                           % agreement),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).to_numpy()
            fc = (pd.to_numeric(df[FC], errors="coerce").to_numpy()
                  if FC in df.columns else np.full(len(df), np.nan))
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[t]))
    g = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(g) > 0:
        drift = g.groupby("coin")["ret"].mean()
        g["ex"] = g["ret"] - g["coin"].map(drift)
    else:
        g["ex"] = []
    gv = g.dropna(subset=["ex", "fc"])
    n_cases = int(len(gv))
    pos = gv[gv["fc"] > 0]
    n_pos = int(len(pos))

    slope = None
    tval = None
    if n_cases >= 3 and gv["fc"].nunique() > 1:
        lr = stats.linregress(gv["fc"].to_numpy(float), gv["ex"].to_numpy(float))
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_val = float(pos["ex"].mean()) if n_pos > 0 else None
    sup_pass = (bool(sup_val > 0) if sup_val is not None else None)

    counts = {"grid cases": n_cases, "grid cases with forecast > 0": n_pos}

    if n_pos < MIN_POS:
        status = "not observable"
        decided = "Fewer than 100 grid cases with forecast > 0 (%d), the plan's minimum count, so the data cannot show the idea." % n_pos
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more (%.2f) and the supporting check passes." % tval
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more (%.2f) but the supporting check fails, which the plan calls inconclusive." % tval
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less (%.2f)." % tval
    else:
        status = "inconclusive"
        decided = "The slope's t (%.2f) is between -2 and 2, which the plan calls inconclusive." % tval

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
