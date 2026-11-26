import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    BAND = 2.0
    RISE_COL = "debug_info.components.rise.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            r1 = close.pct_change(1)
            vol = r1.rolling(30, min_periods=30).std()
            rise_re = r1 / vol
            if RISE_COL in df.columns:
                rise = pd.to_numeric(df[RISE_COL], errors="coerce")
                rise = rise.where(rise.notna(), rise_re)
            else:
                rise = rise_re
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str)
            active = fc != 0
            # profile passed (vetoes give "chop") and the rule passed: regime mean_reversion
            in_profile = regime == "mean_reversion"
            situation = in_profile & (rise > 0) & (rise <= 1.0)
            agree = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean unusual 2-bar move of short cases (short direction)"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2 and check > 0; reject: t <= -2 or upper-minus-lower Welch t <= -2"
    sup_name = "mean unusual move, upper minus lower half of |forecast|"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars with a one-day scaled rise in (0, 1] inside the falling-agitated profile (regime mean_reversion).",
            "reading": "The profile is read from the recorded regime (mean_reversion means neither profile veto fired), since its 365-bar component cannot be recomputed inside a window; the rise is the recorded raw value, recomputed from closes where missing.",
        }

    # ---------- 2. Drift per coin (non-overlapping 2-bar grid, all windows) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df.sort_values("timestamp")["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Cases ----------
    cases = []  # (day, unusual move, |forecast|)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_side = 0
            for i in range(n):
                f = fc[i]
                side = -1 if f < 0 else (1 if f > 0 else 0)
                if side != prev_side:
                    ref = 0.0
                if side == -1:
                    s = -f
                    if s - ref >= BAND:
                        bet[i] = True
                        ref = s
                    else:
                        ref = min(ref, s)
                elif side == 0:
                    ref = 0.0
                else:
                    s = f
                    if s - ref >= BAND:
                        ref = s
                    else:
                        ref = min(ref, s)
                prev_side = side
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if bet[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n or not (c[t] > 0 and np.isfinite(c[t + H])):
                    continue
                ret = c[t + H] / c[t] - 1.0
                unusual = -(ret - drift[coin])
                cases.append((ts.iloc[t].normalize(), unusual, abs(fc[t])))

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)

    mean_u = None
    t_main = None
    diff = None
    welch_t = None
    if n_cases > 0:
        cdf = pd.DataFrame(cases, columns=["day", "u", "af"])
        mean_u = float(cdf["u"].mean())
        if n_days > 1:
            dev = cdf["u"] - mean_u
            S = dev.groupby(cdf["day"]).sum().values
            var_m = (n_days / (n_days - 1.0)) * np.sum(S ** 2) / (n_cases ** 2)
            se = np.sqrt(var_m)
            t_main = float(mean_u / se) if se > 0 else None
        med = cdf["af"].median()
        up = cdf.loc[cdf["af"] > med, "u"]
        lo = cdf.loc[cdf["af"] <= med, "u"]
        if len(up) > 0 and len(lo) > 0:
            diff = float(up.mean() - lo.mean())
            if len(up) > 1 and len(lo) > 1:
                wt = stats.ttest_ind(up.values, lo.values, equal_var=False).statistic
                welch_t = float(wt) if np.isfinite(wt) else None

    counts = {"distinct days with cases": int(n_days), "cases": int(n_cases)}
    reading = ("A case is the first short bet (forecast rising >= 2 points on the short side from its lowest level since "
               "the last bet, reset at flat or side change) in each 2-bar grid cell of a window, measured from its own bar's close; "
               "the profile is read from the recorded regime; halves split as |forecast| > median vs <= median; "
               "the plan's 'fewer than 30 distinct days' minimum is treated as not observable.")

    sup_passed = None if diff is None else bool(diff > 0)
    result = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": None if t_main is None else {"name": "t of the mean, cases of one day taken together", "value": t_main},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_passed},
        "counts": counts,
        "reading": reading,
    }

    if n_days < 30:
        result["status"] = "not observable"
        result["decided_by"] = "Fewer than 30 distinct days with cases, the plan's minimum."
        return result

    if (t_main is not None and t_main <= -2) or (welch_t is not None and welch_t <= -2):
        result["status"] = "rejected"
        if t_main is not None and t_main <= -2:
            result["decided_by"] = "Reject: the mean unusual move has t <= -2, so rises continue."
        else:
            result["decided_by"] = "Reject: the upper-minus-lower difference has Welch t <= -2 (Welch t = %.3f), so the give-back shrinks with the rise." % welch_t
        return result

    if mean_u is not None and mean_u > 0 and t_main is not None and t_main >= 2 and diff is not None and diff > 0:
        result["status"] = "confirmed"
        result["decided_by"] = "Confirm: the mean unusual move is above 0 with t >= 2 and the upper-minus-lower check is above 0."
        return result

    result["status"] = "inconclusive"
    if mean_u is not None and mean_u > 0 and t_main is not None and t_main >= 2:
        result["decided_by"] = "Inconclusive: a positive main measure with t >= 2 but a non-positive supporting check."
    else:
        result["decided_by"] = "Inconclusive: the main measure's t is between -2 and 2 and no reject rule is met."
    return result
