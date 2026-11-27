import numpy as np
import pandas as pd
from scipy import stats


def _component_raw(df, comp_id):
    col = "debug_info.components.%s.last_history_value" % comp_id
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for v in df["debug_info.components"]:
            val = np.nan
            if isinstance(v, dict):
                c = v.get(comp_id)
                if isinstance(c, dict):
                    x = c.get("last_history_value")
                    try:
                        val = float(x) if x is not None else np.nan
                    except (TypeError, ValueError):
                        val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def _short_cases(f):
    # a bet on the short side: the short forecast's size rises by >= 2 points
    # from its lowest size on that side since the last bet (from 0 after flat / long)
    cases = np.zeros(len(f), dtype=bool)
    ref = 0.0
    prev_short = False
    for i, x in enumerate(f):
        if not np.isfinite(x) or x >= 0:
            ref = 0.0
            prev_short = False
            continue
        m = -x
        if not prev_short:
            ref = 0.0
        if m - ref >= 2.0:
            cases[i] = True
            ref = m
        else:
            ref = min(ref, m)
        prev_short = True
    return cases


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            regime = df["regime"].astype(str).values
            run_loss = _component_raw(df, "run_loss").values
            n = len(df)
            for t in range(n):
                if fc[t] == 0:
                    continue
                n_active += 1
                if t >= 3:
                    up = close[t] > close[t - 1]
                    d1 = close[t - 1] < close[t - 2]
                    d2 = close[t - 2] < close[t - 3]
                    run_ok = bool(up and d1 and d2)
                else:
                    # not enough in-window history: the run's recorded loss stands for it
                    run_ok = bool(np.isfinite(run_loss[t]) and run_loss[t] > 0)
                profile_ok = regime[t] == "mean_reversion"
                side_ok = fc[t] < 0
                if run_ok and profile_ok and side_ok:
                    n_agree += 1

    reading_base = ("Situation recomputed from closes (an up close after at least two lower closes, "
                    "the run_loss raw value standing in on the first three bars of a window) and the falling calm "
                    "profile read from regime == mean_reversion since the profile components are not recorded and "
                    "need more history than a window; cases are short-side forecast rises of at least 2 points per the "
                    "holding-period bet definition; t clusters cases by UTC day with a D/(D-1) factor; deeper half is "
                    "|forecast| strictly above the median, shallower at or below; fewer than 30 case days is reported "
                    "as not observable per the workflow.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean short-side unusual next-day move on cases", "value": None,
                             "statistic": None, "threshold": "positive with t >= 2 (confirm), negative with t <= -2 (reject)"},
            "supporting_check": None,
            "counts": {"distinct case days": 0, "cases": 0, "active bars": 0},
            "decided_by": "No bar of the record holds a position, so the minimum of 30 distinct case days is not reached.",
            "reading": reading_base,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the active bars are up closes after at least two down closes inside the "
                           "falling calm profile with a short forecast, so the book does not do what the Fidelity says."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    # coin drift: mean daily return over all its windows
    drift = {}
    for coin in bars:
        rs = []
        for w in bars[coin]:
            c = pd.to_numeric(bars[coin][w]["close"], errors="coerce").values
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rs.append(r[np.isfinite(r)])
        rs = np.concatenate(rs) if rs else np.array([])
        drift[coin] = float(np.mean(rs)) if len(rs) else np.nan

    vals, absf, days = [], [], []
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            cases = _short_cases(fc)
            for t in np.where(cases)[0]:
                if t + 1 >= len(df):
                    continue
                r = close[t + 1] / close[t] - 1.0
                if not np.isfinite(r) or not np.isfinite(drift[coin]):
                    continue
                vals.append(-(r - drift[coin]))
                absf.append(abs(fc[t]))
                days.append(ts.iloc[t].strftime("%Y-%m-%d"))

    vals = np.array(vals, dtype=float)
    absf = np.array(absf, dtype=float)
    days = np.array(days)
    n_cases = len(vals)
    n_days = int(len(np.unique(days))) if n_cases else 0

    mean = float(np.mean(vals)) if n_cases else None
    t_main = None
    if n_cases and n_days >= 2:
        dev = vals - mean
        s = pd.Series(dev).groupby(days).sum().values
        var = (n_days / (n_days - 1.0)) * np.sum(s ** 2) / (n_cases ** 2)
        if var > 0:
            t_main = float(mean / np.sqrt(var))

    diff = None
    t_welch = None
    n_deep = n_shallow = 0
    if n_cases:
        med = float(np.median(absf))
        deep = vals[absf > med]
        shal = vals[absf <= med]
        n_deep, n_shallow = len(deep), len(shal)
        if n_deep and n_shallow:
            diff = float(np.mean(deep) - np.mean(shal))
            if n_deep >= 2 and n_shallow >= 2:
                tw = stats.ttest_ind(deep, shal, equal_var=False).statistic
                if np.isfinite(tw):
                    t_welch = float(tw)

    sup_passed = None if diff is None else bool(diff > 0)
    counts = {"distinct case days": n_days, "cases": int(n_cases),
              "deeper half cases": int(n_deep), "shallower half cases": int(n_shallow)}
    main = {"name": "mean short-side unusual next-day move on cases",
            "value": mean,
            "statistic": None if t_main is None else {"name": "t of the mean, cases clustered by day", "value": t_main},
            "threshold": "positive with t >= 2 (confirm), negative with t <= -2 (reject)"}
    support = {"name": "deeper-minus-shallower mean unusual move (split at median |forecast|)",
               "value": diff, "passed": sup_passed,
               "welch_t": t_welch}
    situation = {"agreement": float(agreement), "passed": True}

    if n_days < 30:
        return {"status": "not observable", "situation_check": situation, "main_measure": main,
                "supporting_check": support, "counts": counts,
                "decided_by": "Fewer than the 30 distinct case days the plan requires (%d)." % n_days,
                "reading": reading_base}

    status = "inconclusive"
    decided = ("The main measure's t is between -2 and 2, or the main confirm comes with a deeper-minus-shallower "
               "difference at or below 0 with Welch t above -2.")
    if t_main is not None and mean < 0 and t_main <= -2:
        status = "rejected"
        decided = "The main measure is negative with t <= -2: break days are followed by rises beyond drift."
    elif diff is not None and diff < 0 and t_welch is not None and t_welch <= -2:
        status = "rejected"
        decided = "The deeper-minus-shallower difference is negative with Welch t <= -2: deeper runs give back less."
    elif t_main is not None and mean > 0 and t_main >= 2 and diff is not None and diff > 0:
        status = "confirmed"
        decided = "The main measure is positive with t >= 2 and the deeper-minus-shallower difference is above 0."

    return {"status": status, "situation_check": situation, "main_measure": main,
            "supporting_check": support, "counts": counts, "decided_by": decided,
            "reading": reading_base}
