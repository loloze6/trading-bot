import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    MIN_CASES = 50
    LHV = "debug_info.components.day_move.last_history_value"
    PROFILE_REGIME = "unknown"  # the regime the choppy calm profile keeps (vetoes send the rest to "chop")

    reading = ("The profile is read from the recorded regime ('unknown' = inside the choppy calm profile, since the "
               "detector's components are not recorded), the situation is a raw day_move value above 0 on such a bar "
               "on the long side, the coin's mean 5-bar return is taken on the non-overlapping grid of all its "
               "windows, the slope is a pooled OLS of excess return on forecast with its ordinary t, and the plan's "
               "'fewer than 50 grid cases' minimum is applied as 'not observable'.")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            reg = df["regime"].astype(str).str.strip().str.lower()
            situation = (reg == PROFILE_REGIME) & raw.notna() & (raw > 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of 5-bar excess return on forecast (grid bars, forecast > 0)",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms (with mean unusual move > 0), t <= -2 rejects"},
            "supporting_check": {"name": "mean unusual move of the cases > 0", "value": None, "passed": None},
            "counts": {"grid cases with forecast > 0": 0},
            "decided_by": "No bar has a non-zero forecast, so fewer than 50 grid cases with forecast > 0 exist.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Only {:.1%} of the bars with a non-zero forecast are up days (raw day_move > 0) inside "
                           "the choppy calm profile with a long forecast, below the 90 % the plan's Fidelity "
                           "requires.".format(agreement)),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    rows.append((fc[i], r))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for f, r in rows:
            xs.append(f)
            ys.append(r - drift)

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_cases = int(len(x))

    mean_unusual = float(np.mean(y)) if n_cases > 0 else None
    sup_passed = (mean_unusual > 0) if mean_unusual is not None else None

    slope = None
    t_slope = None
    if n_cases >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        if res.stderr is not None and np.isfinite(res.stderr) and res.stderr > 0:
            t_slope = float(res.slope / res.stderr)

    main = {
        "name": "slope of 5-bar excess return on forecast (grid bars, forecast > 0, pooled)",
        "value": slope,
        "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
        "threshold": "t >= 2 confirms (with mean unusual move > 0); t <= -2 rejects; otherwise inconclusive",
    }
    supporting = {"name": "mean unusual move of the cases > 0", "value": mean_unusual,
                  "passed": (bool(sup_passed) if sup_passed is not None else None)}
    counts = {"grid cases with forecast > 0": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = "Only {} grid cases with forecast > 0, fewer than the plan's minimum of 50.".format(n_cases)
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t cannot be computed (no spread in the forecast), so it meets neither rule."
    elif t_slope >= 2:
        if sup_passed:
            status = "confirmed"
            decided_by = "The slope's t is 2 or more and the mean unusual move of the cases is above 0."
        else:
            status = "inconclusive"
            decided_by = "A confirming slope (t >= 2) but the mean unusual move of the cases is 0 or below."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope's t is -2 or less: larger rises are followed by smaller excess returns."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
