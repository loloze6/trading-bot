import json
import math

import numpy as np
import pandas as pd
from scipy import stats


HORIZON = 3
BAND = 2.0
COMP_ID = "break_depth"


def _to_dict(x):
    if isinstance(x, dict):
        return x
    if isinstance(x, str):
        try:
            v = json.loads(x)
            return v if isinstance(v, dict) else None
        except Exception:
            return None
    return None


def _component_series(df, comp_id, field):
    col = "debug_info.components.%s.%s" % (comp_id, field)
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce").reset_index(drop=True)
    out = [np.nan] * len(df)
    if "debug_info.components" in df.columns:
        vals = df["debug_info.components"].tolist()
        for i, v in enumerate(vals):
            d = _to_dict(v)
            if not d:
                continue
            c = _to_dict(d.get(comp_id))
            if not c:
                continue
            try:
                val = c.get(field)
                out[i] = float(val) if val is not None else np.nan
            except Exception:
                out[i] = np.nan
    return pd.Series(out, dtype=float)


def _timestamps(df):
    ts = df["timestamp"]
    if pd.api.types.is_numeric_dtype(ts):
        mx = float(np.nanmax(ts.values)) if len(ts) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(ts, unit=unit, utc=True).reset_index(drop=True)
    return pd.to_datetime(ts, utc=True, errors="coerce").reset_index(drop=True)


def _short_bets(fc):
    """Bars where the short forecast rises in size by at least BAND from its lowest
    short level since the last bet (from 0 after flat or a change of side)."""
    bets = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    prev_short = False
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f >= 0:
            prev_short = False
            ref = 0.0
            continue
        m = -f
        if not prev_short:
            ref = 0.0
        if m - ref >= BAND:
            bets[i] = True
            ref = m
        else:
            ref = min(ref, m)
        prev_short = True
    return bets


def measure(bars):
    reading = ("The profile part of the situation is read from the recorded regime ('trending' is only reachable "
               "past the falling/agitated vetoes, whose components are not recorded), the break from break_depth's "
               "last_history_value < 0 (recomputed from the window's prior 30 closes where missing); a case is the "
               "first short bet (forecast rising in size on the short side by at least 2 points) in each 3-bar grid "
               "cell of a window, measured from that bet bar's close over 3 bars; the coin's normal drift is the mean "
               "of its non-overlapping 3-bar returns on the same grid over all its windows; the supporting slope is "
               "an OLS of the raw 3-bar return on post_pipeline_value with its ordinary t; the plan's 30 cases on 30 "
               "distinct days are treated as minimum counts (not observable if unmet).")

    active_total = 0
    active_agree = 0
    cases = []  # (coin, day, ret, ppv)
    drift_samples = {}

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        drift_samples.setdefault(coin, [])
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            ts = _timestamps(df)
            lhv = _component_series(df, COMP_ID, "last_history_value").values
            ppv = _component_series(df, COMP_ID, "post_pipeline_value").values
            n = len(df)

            # break below the prior 30-close low, recomputed where the record lacks it
            prior_min = pd.Series(close).shift(1).rolling(30, min_periods=30).min().values
            recomputed = np.where(np.isfinite(prior_min) & (prior_min > 0),
                                  (close / prior_min - 1.0) * 100.0, np.nan)
            brk = np.where(np.isfinite(lhv), lhv, recomputed)
            in_break = np.isfinite(brk) & (brk < 0)
            in_profile = np.array([r.strip().lower() == "trending" for r in regime])
            situation = in_break & in_profile

            active = np.isfinite(fc) & (fc != 0)
            active_total += int(active.sum())
            active_agree += int((active & situation & (fc < 0)).sum())

            # normal drift samples: grid 0, h, 2h, ...
            for g in range(0, n - HORIZON, HORIZON):
                c0, c1 = close[g], close[g + HORIZON]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    drift_samples[coin].append(c1 / c0 - 1.0)

            # cases: first short bet in each grid cell
            bets = _short_bets(fc)
            for g in range(0, n, HORIZON):
                cell = [i for i in range(g, min(g + HORIZON, n)) if bets[i]]
                if not cell:
                    continue
                s = cell[0]
                if s + HORIZON >= n:
                    continue
                c0, c1 = close[s], close[s + HORIZON]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                day = ts.iloc[s]
                day = str(day.date()) if pd.notna(day) else None
                cases.append((coin, day, c1 / c0 - 1.0, ppv[s]))

    agreement = (active_agree / active_total) if active_total > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean 3-bar unusual move in the short direction (return minus normal drift, sign flipped)"
    main_threshold = "confirm: mean > 0 with day-pooled t >= 2 and supporting check passed; reject: mean < 0 with t <= -2"
    sup_name = "OLS slope of 3-bar return on post_pipeline_value, t >= 1 and positive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_threshold},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None, "active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on a fresh 30-day "
                           "closing low inside the falling agitated (trending) regime, as the Fidelity requires."),
            "reading": reading,
        }

    drift = {c: (float(np.mean(v)) if len(v) else 0.0) for c, v in drift_samples.items()}

    days = [c[1] for c in cases]
    unusual = np.array([-(c[2] - drift.get(c[0], 0.0)) for c in cases], dtype=float)
    n_cases = int(len(cases))
    n_days = int(len(set(d for d in days if d is not None)))

    mean_u = float(np.mean(unusual)) if n_cases else None
    t_u = None
    if n_cases >= 2 and n_days >= 2:
        dev = unusual - mean_u
        per_day = {}
        for d, e in zip(days, dev):
            per_day[d] = per_day.get(d, 0.0) + e
        sums = np.array(list(per_day.values()))
        D = len(sums)
        var_mean = (D / (D - 1.0)) * float(np.sum(sums ** 2)) / (n_cases ** 2)
        se = math.sqrt(var_mean) if var_mean > 0 else 0.0
        if se > 0:
            t_u = float(mean_u / se)

    # supporting check
    rets = np.array([c[2] for c in cases], dtype=float)
    pp = np.array([c[3] for c in cases], dtype=float)
    ok = np.isfinite(rets) & np.isfinite(pp)
    slope = None
    slope_t = None
    sup_passed = None
    if ok.sum() >= 3 and np.std(pp[ok]) > 0:
        res = stats.linregress(pp[ok], rets[ok])
        slope = float(res.slope)
        if res.stderr and res.stderr > 0:
            slope_t = float(res.slope / res.stderr)
        sup_passed = bool(slope > 0 and slope_t is not None and slope_t >= 1)
    elif n_cases > 0:
        sup_passed = False

    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided_by = ("The plan's minimum of 30 cases on at least 30 distinct days is not reached "
                      "(%d cases on %d days)." % (n_cases, n_days))
    elif t_u is None:
        status = "inconclusive"
        decided_by = "The day-pooled t of the unusual move cannot be computed, so it lies in no confirm or reject range."
    elif mean_u > 0 and t_u >= 2:
        if sup_passed:
            status = "confirmed"
            decided_by = ("Confirm: the mean unusual move in the short direction is above 0 with t >= 2 and the "
                          "slope of the 3-bar return on the forecast is positive with t >= 1.")
        else:
            status = "inconclusive"
            decided_by = ("Inconclusive: the main measure is on the confirm side (mean > 0, t >= 2) but the "
                          "supporting check (positive slope with t >= 1) fails.")
    elif mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided_by = ("Reject: the mean unusual move in the short direction is below 0 with t <= -2, "
                      "the coin rebounds after a fresh monthly low.")
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the day-pooled t of the unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases pooled by day", "value": t_u} if t_u is not None else None),
            "threshold": main_threshold,
        },
        "supporting_check": {"name": sup_name, "value": slope_t if slope_t is not None else slope,
                             "passed": sup_passed},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
