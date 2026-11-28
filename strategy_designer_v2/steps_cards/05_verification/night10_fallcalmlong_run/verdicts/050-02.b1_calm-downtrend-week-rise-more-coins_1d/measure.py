import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.scaled_rise_7d.last_history_value"

    def _f(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        return x if np.isfinite(x) else None

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            # profile: the regime detector's decision; "unknown" is the bar on which
            # neither veto fired (trend >= -10 or swing > 0.5 -> chop), i.e. falling calm
            in_profile = df["regime"].astype(str) == "unknown"
            # the coin has risen over 7 days: raw scaled return > 0 (same sign as the 7-day return)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            ret7 = close / close.shift(7) - 1.0
            rose = raw.where(raw.notna(), ret7) > 0
            active = fc != 0
            good = active & in_profile & rose & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(good.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "distinct case days": None},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are falling-calm bars "
                           "(regime 'unknown') where the coin rose over 7 days with a long forecast"
                           if n_active > 0 else "the record has no active bars to compare with the plan's situation"),
            "reading": "the falling calm profile is read from the recorded regime ('unknown' = no veto fired), "
                       "the 7-day rise from the raw component's sign (price 7-bar return where not recorded).",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, unusual, forecast)
    for coin, wins in bars.items():
        grid_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rows.append((c1 / c0 - 1.0, fc[i], ts.iloc[i].floor("D")))
        if not grid_rows:
            continue
        rets = np.array([g[0] for g in grid_rows])
        drift = float(np.mean(rets))
        for r, f, d in grid_rows:
            if np.isfinite(f) and f > 0:
                cases.append((coin, d, r - drift, float(f)))

    n_cases = len(cases)
    case_days = len(set(c[1] for c in cases))

    mean_u = None
    t_main = None
    if n_cases > 0:
        u = np.array([c[2] for c in cases])
        mean_u = float(np.mean(u))
        dev = pd.Series(u - mean_u, index=[c[1] for c in cases])
        S = dev.groupby(level=0).sum().values
        D = len(S)
        if D > 1:
            var = np.sum(S ** 2) * D / (D - 1) / (n_cases ** 2)
            se = np.sqrt(var)
            t_main = float(mean_u / se) if se > 0 else None

    # supporting check: upper half (forecast > coin's median of case forecasts) minus lower half (<= median)
    upper, lower = [], []
    by_coin = {}
    for c in cases:
        by_coin.setdefault(c[0], []).append(c)
    for coin, cs in by_coin.items():
        med = np.median([c[3] for c in cs])
        for c in cs:
            (upper if c[3] > med else lower).append(c[2])
    diff = None
    t_diff = None
    if len(upper) > 0 and len(lower) > 0:
        diff = float(np.mean(upper) - np.mean(lower))
        if len(upper) > 1 and len(lower) > 1:
            tt = stats.ttest_ind(upper, lower, equal_var=False).statistic
            t_diff = _f(tt)
    sup_passed = None if diff is None else bool(diff > 0)

    if case_days < 30:
        status = "not observable"
        decided = f"fewer than 30 distinct case days across all coins and windows ({case_days})."
    else:
        conf = (mean_u is not None and t_main is not None and mean_u > 0 and t_main >= 2)
        rej = ((mean_u is not None and t_main is not None and mean_u < 0 and t_main <= -2)
               or (t_diff is not None and t_diff <= -2))
        if conf and sup_passed:
            status = "confirmed"
            decided = "mean unusual 3-day move > 0 with t >= 2 and upper-minus-lower difference > 0."
        elif rej:
            status = "rejected"
            if mean_u is not None and t_main is not None and mean_u < 0 and t_main <= -2:
                decided = "mean unusual 3-day move < 0 with t <= -2."
            else:
                decided = "upper-minus-lower difference has Welch t <= -2."
        else:
            status = "inconclusive"
            if conf:
                decided = "main measure meets the confirm rule but the upper-minus-lower difference is <= 0 with Welch t above -2."
            else:
                decided = "main-measure result meets neither the confirm nor the reject rule (t between -2 and 2 or sign/threshold not met)."

    return {
        "status": status,
        "situation_check": {"agreement": _f(agreement), "passed": True},
        "main_measure": {
            "name": "mean unusual 3-day move on forecast > 0 cases (non-overlapping grid)",
            "value": _f(mean_u),
            "statistic": None if t_main is None else {"name": "t of the mean, cases of one day taken together", "value": _f(t_main)},
            "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "upper-minus-lower half (by coin's median forecast) mean unusual 3-day move",
            "value": _f(diff),
            "passed": sup_passed,
            "welch_t": _f(t_diff),
            "n_upper": len(upper),
            "n_lower": len(lower),
        },
        "counts": {"distinct case days": int(case_days), "cases": int(n_cases)},
        "decided_by": decided,
        "reading": "cases are grid bars (positions 0,3,6,... of each window) with forecast > 0 and a 3-bar return inside the window, the drift is the coin's mean grid 3-bar return over all its windows, the halves split each coin's case forecasts at their median with ties at the median put in the lower half, and the 30-day minimum is treated as 'not observable'.",
    }
