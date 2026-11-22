import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 6
    BAND = 2.0
    VOL_LOW, VOL_HIGH = 0.667, 1.5
    FALL_COL = "debug_info.components.fall.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            vol = pd.to_numeric(df["volume"], errors="coerce")
            prior_mean = vol.rolling(720, min_periods=720).mean().shift(1)
            vratio = vol / prior_mean
            vol_ok_calc = (vratio >= VOL_LOW) & (vratio <= VOL_HIGH)
            vol_ok_regime = df["regime"].astype(str) == "mean_reversion"
            vol_ok = np.where(prior_mean.notna(), vol_ok_calc, vol_ok_regime)
            if FALL_COL in df.columns:
                fall = pd.to_numeric(df[FALL_COL], errors="coerce")
            else:
                fall = pd.Series(np.nan, index=df.index)
            # recompute the raw value where not recorded: 1-bar return / mean abs 1-bar return (720)
            close = pd.to_numeric(df["close"], errors="coerce")
            r1 = close.pct_change()
            fall_calc = r1 / r1.abs().rolling(720, min_periods=720).mean()
            fall = fall.where(fall.notna(), fall_calc)
            is_fall = (fall < 0).fillna(False).values
            active = (fc != 0).values
            sit = is_fall & np.asarray(vol_ok, dtype=bool) & (fc > 0).values
            n_active += int(active.sum())
            n_agree += int((active & sit).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 6-bar move after forecast rises >= 2 (long)"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    reading = ("Volume ratio recomputed from the window's volume over the prior 720 bars (the recorded regime used where "
               "fewer than 720 prior bars exist in the window), the fall is the raw component < 0; cases are bets "
               "(forecast rise >= 2 from its lowest long level since the last bet, from 0 after flat), the first per "
               "6-bar grid cell of each window, both coins pooled, drift per coin from grid 6-bar returns over all its "
               "windows; the plan's 'fewer than 30 cases' minimum is applied as not observable; a supporting check "
               "with an empty half counts as failed.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases over both coins": None},
            "decided_by": (f"Only {agreement:.1%} of active bars are quiet-volume falling hours with a long forecast, "
                           "below the 90% needed for the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    unusual = []
    case_fc = []
    for coin, wins in bars.items():
        # normal drift: grid 6-bar returns over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for k in range(0, len(c) - H, H):
                if np.isfinite(c[k]) and np.isfinite(c[k + H]) and c[k] != 0:
                    grid_rets.append(c[k + H] / c[k] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            trough = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    trough = 0.0
                    continue
                if f - trough >= BAND:
                    trough = f
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0:
                        unusual.append(c[t + H] / c[t] - 1.0 - drift)
                        case_fc.append(f)
                else:
                    trough = min(trough, f)

    unusual = np.array(unusual, dtype=float)
    case_fc = np.array(case_fc, dtype=float)
    n_cases = int(len(unusual))
    counts = {"cases over both coins": n_cases}

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_val = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    sup_val, sup_pass = None, None
    if n_cases > 0:
        med = float(np.median(case_fc))
        hi = unusual[case_fc >= med]
        lo = unusual[case_fc < med]
        counts["cases at or above median"] = int(len(hi))
        counts["cases below median"] = int(len(lo))
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": threshold}
    supporting = {"name": "mean unusual move, cases at/above median forecast minus below",
                  "value": sup_val, "passed": sup_pass}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases over both coins, fewer than the plan's minimum of 30."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "The mean unusual move reaches a confirm-level t but the supporting check fails."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
