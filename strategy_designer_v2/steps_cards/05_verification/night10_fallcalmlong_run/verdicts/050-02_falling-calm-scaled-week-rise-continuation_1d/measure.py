import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.scaled_week_rise.last_history_value"
    PROFILE_REGIME = "unknown"  # the regime left when neither 'chop' veto fires = the falling calm profile

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret7_px = close / close.shift(7) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            rose = raw.where(raw.notna(), ret7_px) > 0
            in_profile = df["regime"].astype(str) == PROFILE_REGIME
            active = fc != 0
            agree = active & in_profile & rose.fillna(False) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active == 0:
        agreement = None
        sit_passed = False
    else:
        agreement = n_agree / n_active
        sit_passed = agreement >= 0.9

    main_name = "mean unusual 3-bar move of the cases, taken long"
    main_thr = "t >= 2 confirms (with positive size difference), t <= -2 rejects, otherwise inconclusive"
    sup_name = "mean unusual move of cases with forecast >= median minus those below (Welch t)"

    if agreement is not None and not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars of a 7-day rise inside the falling calm profile (regime 'unknown').",
            "reading": "The profile is read from the recorded regime (the detector's components are not recorded) and the 7-day rise from the component's raw value, or the 7-bar price return where it is missing.",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, forecast, ret)
    for coin, wins in bars.items():
        # normal drift: mean 3-bar return on the grid of all the coin's windows
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            for k in range(0, n - H, H):
                r = close[k + H] / close[k] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            # bets: long-side rise of at least BAND from the lowest level since the last bet
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev = 0.0
            for i in range(n):
                f = fc[i]
                if f > 0:
                    if prev <= 0:
                        ref = 0.0
                    ref = min(ref, f)
                    if f - ref >= BAND:
                        bet[i] = True
                        ref = f
                else:
                    ref = 0.0
                prev = f
            # once per grid cell: first bet bar in each cell
            for k in range(0, n, H):
                idx = [i for i in range(k, min(k + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r) or pd.isna(ts.iloc[i]):
                    continue
                coin_cases.append((coin, ts.iloc[i].date().isoformat(), fc[i], r))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for c, d, f, r in coin_cases:
            cases.append((c, d, f, r - drift))

    n_cases = len(cases)
    days = sorted(set(c[1] for c in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    reading = ("The falling calm profile is the recorded regime 'unknown'; a case is the first bar in each 3-bar grid cell "
               "(from each window's first row) where the forecast rose by at least 2 points from its lowest level since its last bet "
               "(from 0 after a flat), the drift is the mean 3-bar return on that grid over all the coin's windows, and the "
               "day-clustered standard error uses the per-day summed deviations with a D/(D-1) correction.")

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(sit_passed)},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 30 cases and fewer than 30 distinct days (no case at all).",
            "reading": reading,
        }

    u = np.array([c[3] for c in cases], dtype=float)
    f = np.array([c[2] for c in cases], dtype=float)
    dlab = np.array([c[1] for c in cases])
    mean_u = float(u.mean())
    dev = u - mean_u
    sums = pd.Series(dev).groupby(dlab).sum().values
    t_main = None
    if n_days >= 2:
        var = (sums ** 2).sum() / (n_cases ** 2) * (n_days / (n_days - 1))
        se = np.sqrt(var)
        if se > 0:
            t_main = float(mean_u / se)

    med = float(np.median(f))
    hi = u[f >= med]
    lo = u[f < med]
    if len(hi) >= 1 and len(lo) >= 1:
        diff = float(hi.mean() - lo.mean())
        sup_passed = bool(diff > 0)
        if len(hi) >= 2 and len(lo) >= 2:
            wt = stats.ttest_ind(hi, lo, equal_var=False).statistic
            welch_t = float(wt) if np.isfinite(wt) else None
        else:
            welch_t = None
    else:
        diff = None
        sup_passed = None
        welch_t = None

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        missing = []
        if n_cases < 30:
            missing.append(f"fewer than 30 cases ({n_cases})")
        if n_days < 30:
            missing.append(f"fewer than 30 distinct days ({n_days})")
        decided = "Minimum count not reached: " + " and ".join(missing) + "."
    elif t_main is None:
        status = "inconclusive"
        decided = "The t of the unusual move could not be computed, so it is not >= 2 nor <= -2."
    elif t_main >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "The unusual move has t >= 2 and the size difference is positive."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "The unusual move has t >= 2 but the size difference is not positive."
    elif t_main <= -2:
        status = "rejected"
        decided = "The unusual move has t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the unusual move is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(sit_passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_main is None else {"name": "t of the mean, cases of one day taken together", "value": t_main},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name + ("" if welch_t is None else f" [Welch t = {welch_t:.3f}]"),
            "value": diff,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
