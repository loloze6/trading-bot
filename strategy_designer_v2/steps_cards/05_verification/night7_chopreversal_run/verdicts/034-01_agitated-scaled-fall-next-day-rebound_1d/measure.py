import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fall_usual_moves.last_history_value"
    HORIZON = 1
    MIN_CASES = 150
    MIN_DAYS = 100

    # ---------- coin mean daily return over all windows (within-window returns only) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check + collection of cases ----------
    n_active = 0
    n_agree = 0
    rows = []  # (forecast, excess next-day return, day)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            regime = df["regime"].astype(str).str.lower().to_numpy() if "regime" in df.columns \
                else np.array(["unknown"] * len(df))
            # agitated profile: the detector did not veto to 'chop' (the strategy's regime ran)
            agitated = regime != "chop"
            fell = np.isfinite(raw) & (raw < 0)
            situation = agitated & fell

            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            days = ts.dt.floor("D").to_numpy()
            mu = coin_mean.get(coin, np.nan)
            # horizon 1 bar: grid is every bar of the window
            for i in range(0, len(df) - HORIZON, HORIZON):
                if not (np.isfinite(fc[i]) and fc[i] > 0):
                    continue
                r = close[i + HORIZON] / close[i] - 1.0
                if not np.isfinite(r) or not np.isfinite(mu) or pd.isna(days[i]):
                    continue
                rows.append((fc[i], r - mu, days[i]))

    if n_active == 0:
        agreement = None
        sit_passed = False
    else:
        agreement = n_agree / n_active
        sit_passed = agreement >= 0.9

    main_name = "slope of next-day excess return on forecast (forecast > 0, pooled)"
    main_thr = "confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2"
    sup_name = "top third minus bottom third mean next-day excess return (Welch t >= 1)"
    reading = ("Agitated bars are those whose regime is not the detector's 'chop' veto and a fall is a recorded raw "
               "component value below 0; cases are forecast > 0 bars with a next-day return inside the window; the "
               "slope is OLS with intercept, its t clustered by UTC day (CR1, G/(G-1)); thirds are the floor(n/3) "
               "lowest and highest forecasts after a stable sort.")

    if agreement is not None and not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases with forecast > 0": len(rows),
                       "distinct days": len(set(r[2] for r in rows))},
            "decided_by": ("Fewer than 90 % of the active bars are long bars after a one-day fall in the agitated "
                           "profile, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    n = len(rows)
    n_days = len(set(r[2] for r in rows))
    counts = {"cases with forecast > 0": n, "distinct days": n_days}

    if agreement is None or n < MIN_CASES or n_days < MIN_DAYS:
        if agreement is None:
            why = "There are no active bars, so no case with forecast > 0 was observed."
        elif n < MIN_CASES:
            why = f"Fewer than {MIN_CASES} cases with forecast > 0 ({n})."
        else:
            why = f"Cases fall on fewer than {MIN_DAYS} distinct days ({n_days})."
        return {
            "status": "not observable",
            "situation_check": {"agreement": None if agreement is None else float(agreement),
                                "passed": bool(sit_passed)},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": why,
            "reading": reading,
        }

    x = np.array([r[0] for r in rows], dtype=float)
    y = np.array([r[1] for r in rows], dtype=float)
    d = np.array([r[2] for r in rows])

    # ---------- main measure: slope with day-clustered t ----------
    xc = x - x.mean()
    sxx = float(np.sum(xc ** 2))
    if sxx > 0:
        slope = float(np.sum(xc * (y - y.mean())) / sxx)
        intercept = float(y.mean() - slope * x.mean())
        e = y - intercept - slope * x
        score = pd.Series(xc * e).groupby(pd.Series(d)).sum().to_numpy()
        G = len(score)
        var = float(np.sum(score ** 2)) / sxx ** 2
        if G > 1:
            var *= G / (G - 1)
        se = np.sqrt(var)
        t_slope = float(slope / se) if se > 0 else float("nan")
    else:
        slope = float("nan")
        t_slope = float("nan")

    # ---------- supporting check: top third vs bottom third ----------
    order = np.argsort(x, kind="mergesort")
    k = n // 3
    bottom = y[order[:k]]
    top = y[order[n - k:]]
    if k >= 2:
        diff = float(np.mean(top) - np.mean(bottom))
        wt = stats.ttest_ind(top, bottom, equal_var=False)
        welch_t = float(wt.statistic)
        sup_passed = bool(np.isfinite(welch_t) and welch_t >= 1.0)
    else:
        diff = None
        welch_t = float("nan")
        sup_passed = False

    # ---------- decision ----------
    if np.isfinite(t_slope) and slope > 0 and t_slope >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the supporting check passes (Welch t >= 1)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif np.isfinite(t_slope) and slope < 0 and t_slope <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": bool(sit_passed)},
        "main_measure": {
            "name": main_name,
            "value": None if not np.isfinite(slope) else slope,
            "statistic": {"name": "t of slope, cases of one day taken together",
                          "value": None if not np.isfinite(t_slope) else t_slope},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name,
            "value": diff,
            "passed": sup_passed,
            "welch_t": None if not np.isfinite(welch_t) else welch_t,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
