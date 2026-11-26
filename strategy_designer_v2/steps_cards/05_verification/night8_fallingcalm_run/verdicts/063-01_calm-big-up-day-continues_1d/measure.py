import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.scaled_rise.last_history_value"
    PPV = "debug_info.components.scaled_rise.post_pipeline_value"
    H = 5
    CALM = "unknown"  # the regime that holds the strategy; the 'chop' veto (vol percentile > 0.5) marks non-calm bars

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            ret1 = close.pct_change()
            vol = ret1.rolling(30, min_periods=30).std()
            recomputed = ret1 / vol
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce").where(lambda s: s.notna(), recomputed)
            else:
                raw = recomputed
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str)
            active = fc != 0
            situation = (raw > 0) & (regime == CALM)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars are long bars on a calm-profile day with a positive "
                           "vol-scaled one-day return (or no active bars at all), so the config does not do what "
                           "the Fidelity's situation and long side say."),
            "reading": "Calm profile read as the regime 'unknown' (not vetoed to 'chop'); the rise as a raw scaled return above 0.",
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin drift: mean non-overlapping 5-bar return over all its windows
        all_fwd = []
        per_window = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            idx = np.arange(0, len(df), H)
            idx = idx[idx + H < len(df)]
            fwd = close[idx + H] / close[idx] - 1.0
            all_fwd.extend(list(fwd[np.isfinite(fwd)]))
            per_window.append((df, idx, fwd))
        if len(all_fwd) == 0:
            continue
        drift = float(np.mean(all_fwd))
        for df, idx, fwd in per_window:
            if len(idx) == 0:
                continue
            regime = df["regime"].astype(str).values[idx]
            if PPV in df.columns:
                f = pd.to_numeric(df[PPV], errors="coerce").values[idx]
            else:
                f = np.full(len(idx), np.nan)
            m = (regime == CALM) & np.isfinite(f) & np.isfinite(fwd)
            xs.extend(list(f[m]))
            ys.extend(list(fwd[m] - drift))

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_cases = int(len(x))
    n_pos = int(np.sum(x > 0))
    hi = x >= 10
    n_hi = int(np.sum(hi))
    sup_val = float(np.mean(y[hi])) if n_hi > 0 else None
    sup_pass = bool(sup_val is not None and sup_val > 0)

    slope, t = None, None
    if n_cases >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    counts = {"grid cases": n_cases, "grid cases with forecast above 0": n_pos,
              "grid cases with forecast at or above 10": n_hi}

    if n_pos < 100:
        status = "not observable"
        decided = f"Only {n_pos} grid cases with a forecast above 0, below the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return at forecast >= 10 is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting mean at forecast >= 10 is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of excess 5-bar return on scaled_rise post_pipeline_value, in-profile grid bars",
            "value": slope,
            "statistic": {"name": "slope t", "value": t} if t is not None else None,
            "threshold": "confirm if t >= 2 (with supporting mean > 0); reject if t <= -2",
        },
        "supporting_check": {"name": "mean excess 5-bar return on grid cases with forecast >= 10",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("In-profile bars are those with regime 'unknown' (calm, not vetoed to 'chop'), the coin's drift is its "
                    "mean 5-bar return on the 0,5,10,... grid of all its windows, the plan's 'else inconclusive' minimum "
                    "of 100 positive-forecast cases is applied as 'not observable' per the workflow, and a missing "
                    "supporting mean counts as not above 0."),
    }
