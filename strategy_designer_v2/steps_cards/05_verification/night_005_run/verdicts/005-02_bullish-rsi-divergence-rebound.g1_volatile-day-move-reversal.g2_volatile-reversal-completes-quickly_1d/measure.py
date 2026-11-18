import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    FC_MIN = 5.0
    MIN_CASES = 30
    move_col = "debug_info.components.move.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # raw one-day move: recorded value where present, else recomputed from prices (inside the window)
            ret1 = close.pct_change()
            if move_col in df.columns:
                raw = pd.to_numeric(df[move_col], errors="coerce")
                move = raw.where(raw.notna(), ret1)
            else:
                move = ret1
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            active = fc.notna() & (fc != 0)
            vol_ok = regime == "mean_reversion"          # the detector's decision on 20d vol rank >= 0.8
            expected_side = -np.sign(move)              # fade the day's move
            situ = vol_ok & move.notna() & (move != 0) & (np.sign(fc) == expected_side)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean signed excess 3-bar return on non-overlapping grid bars with |forecast| >= 5"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: t <= -2"
    sup_name = "OLS slope of signed excess 3-bar return on |forecast|, positive with t >= 1"
    reading = ("The plan's volatility rule is read from the recorded regime ('mean_reversion' = 20-day vol rank >= 0.8) "
               "and a 'large move' bar is any bar with a non-zero one-day move faded by the forecast's sign; the coin's "
               "mean 3-bar return is the mean over all non-overlapping grid bars of all its windows; the plan's "
               "'fewer than 30 qualifying cases' is treated as a minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on fade side": n_agree},
            "decided_by": ("Fewer than 90% of the active bars are bars where the regime is the high-volatility "
                           "rule and the forecast fades the day's move, as the Fidelity's situation and outcome require."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    coin_mean = {}
    cases = []  # (coin, sign, |fc|, ret)
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                f = fc[t]
                if np.isfinite(f) and abs(f) >= FC_MIN:
                    cases.append((coin, float(np.sign(f)), float(abs(f)), r))
        coin_mean[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    y, x = [], []
    for coin, s, af, r in cases:
        mu = coin_mean.get(coin, np.nan)
        if not np.isfinite(mu):
            continue
        y.append(s * r - s * mu)
        x.append(af)
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    n_cases = int(len(y))

    mean_val = float(np.mean(y)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = np.std(y, ddof=1)
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_cases)))

    slope = None
    slope_t = None
    sup_passed = None
    if n_cases >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        if lr.stderr is not None and lr.stderr > 0:
            slope_t = float(lr.slope / lr.stderr)
        sup_passed = bool(slope > 0 and slope_t is not None and slope_t >= 1.0)
    elif n_cases > 0:
        sup_passed = False

    counts = {"qualifying cases across all coins and windows": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} qualifying cases (grid bars with |forecast| >= 5), below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean_val > 0 and t_val >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The mean signed excess 3-bar return is above 0 with t >= 2 and the slope on |forecast| is positive with t >= 1."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule but the supporting slope check fails, which the plan calls inconclusive."
    elif t_val <= -2:
        status = "rejected"
        decided = "The mean signed excess 3-bar return has t <= -2: price continues in the direction of the large move."
    else:
        status = "inconclusive"
        decided = "The t of the mean signed excess 3-bar return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": sup_name,
            "value": slope_t,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
