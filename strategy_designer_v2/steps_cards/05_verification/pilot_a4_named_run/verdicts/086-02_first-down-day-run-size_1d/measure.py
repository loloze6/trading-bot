import json
import numpy as np
import pandas as pd
from scipy import stats


COMP_ID = "run_gain_short"
HORIZON = 3
BAND = 2.0
MIN_CASES = 30
MIN_DAYS = 30


def _component_raw(df, comp_id):
    """Raw value (last_history_value) of a strategy component; NaN where not recorded."""
    flat = "debug_info.components.%s.last_history_value" % comp_id
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce").to_numpy(dtype=float)
    out = np.full(len(df), np.nan)
    if "debug_info.components" not in df.columns:
        return out
    for i, v in enumerate(df["debug_info.components"].to_numpy()):
        d = v
        if isinstance(d, str):
            try:
                d = json.loads(d)
            except Exception:
                d = None
        if isinstance(d, dict):
            c = d.get(comp_id)
            if isinstance(c, str):
                try:
                    c = json.loads(c)
                except Exception:
                    c = None
            if isinstance(c, dict) and c.get("last_history_value") is not None:
                try:
                    out[i] = float(c["last_history_value"])
                except Exception:
                    pass
    return out


def _run_gain_from_prices(close, window=30, max_bars=30):
    """Gain of the up run ending the day before a down close, in std of the 30 daily returns ending the day before."""
    n = len(close)
    out = np.full(n, np.nan)
    ret = np.full(n, np.nan)
    ret[1:] = close[1:] / close[:-1] - 1.0
    for t in range(2, n):
        if not (close[t] < close[t - 1]):
            out[t] = 0.0
            continue
        k = t - 1
        start = k
        while start - 1 >= 0 and close[start] > close[start - 1] and (k - start + 1) < max_bars:
            start -= 1
        if start == k:
            out[t] = 0.0
            continue
        r = ret[max(1, t - window):t]
        r = r[np.isfinite(r)]
        if len(r) < window:
            continue
        sd = np.std(r, ddof=1)
        if not np.isfinite(sd) or sd == 0:
            continue
        out[t] = (close[k] / close[start] - 1.0) / sd
    return out


def _short_bets(f):
    """Short bets: the forecast's short size rises by >= BAND from its lowest short size since the last bet."""
    bets = np.zeros(len(f), dtype=bool)
    ref = 0.0
    for i, x in enumerate(f):
        if not np.isfinite(x) or x >= 0:
            ref = 0.0
            continue
        m = -x
        if m - ref >= BAND:
            bets[i] = True
            ref = m
        else:
            ref = min(ref, m)
    return bets


def measure(bars):
    reading = ("Situation = regime 'trending' (the detector's decision, which carries the rising-agitated profile "
               "whose 365-bar volatility percentile cannot be rebuilt inside the recorded windows) on a down close "
               "with the recorded run gain > 0 (recomputed from prices where not recorded), expected side short; "
               "cases are short bets (short size up >= 2 from its lowest since the last bet), first one per 3-bar "
               "grid cell of each window; drift is the coin's mean 3-bar return on that grid over all its windows; "
               "the day-clustered t sums case deviations per UTC day; the slope t is ordinary least squares; "
               "the plan's 'fewer than 30 cases or 30 days' minimum is reported as not observable.")

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    case_rows = []

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # normal drift over all windows of the coin
        grid_rets = []
        prepared = []
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for p in range(0, n - HORIZON, HORIZON):
                a, b = close[p], close[p + HORIZON]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
            prepared.append((df, close, fc))
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan

        for df, close, fc in prepared:
            n = len(df)
            raw = _component_raw(df, COMP_ID)
            rec = _run_gain_from_prices(close)
            gain = np.where(np.isfinite(raw), raw, rec)
            regime = df["regime"].astype(str).to_numpy()
            down = np.zeros(n, dtype=bool)
            down[1:] = close[1:] < close[:-1]
            situation = (regime == "trending") & np.isfinite(gain) & (gain > 0) & down

            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # cases
            bets = _short_bets(fc)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            seen = set()
            for i in np.where(bets)[0]:
                cell = i // HORIZON
                if cell in seen:
                    continue
                seen.add(cell)
                if i + HORIZON >= n:
                    continue
                a, b = close[i], close[i + HORIZON]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0 and np.isfinite(drift)):
                    continue
                r = b / a - 1.0
                u = -(r - drift)
                case_rows.append({"day": ts.iloc[i].strftime("%Y-%m-%d"),
                                  "u": u, "absf": abs(fc[i])})

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-direction unusual move over 3 bars (vs coin's normal 3-bar drift)"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2; reject: mean < 0 with t <= -2"
    sup_name = "OLS slope of unusual move on |forecast|"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars on a first down close "
                           "after an up run inside the trending (rising agitated) regime, as the Fidelity states."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["day", "u", "absf"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_main = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["u"] - cases["u"].mean()
        s = dev.groupby(cases["day"]).sum().to_numpy()
        D = len(s)
        var = (D / (D - 1.0)) * float(np.sum(s ** 2))
        se = np.sqrt(var) / n_cases
        t_main = float(mean_u / se) if se > 0 else None

    slope = None
    t_slope = None
    if n_cases >= 3 and cases["absf"].nunique() > 1:
        lr = stats.linregress(cases["absf"].to_numpy(), cases["u"].to_numpy())
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_passed = None
    if slope is not None and t_slope is not None:
        sup_passed = bool(slope > 0 and t_slope >= 2)

    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = ("The plan's minimum of 30 cases and 30 distinct days is not reached (%d cases, %d days)."
                   % (n_cases, n_days))
    else:
        main_conf = mean_u is not None and t_main is not None and mean_u > 0 and t_main >= 2
        main_rej = mean_u is not None and t_main is not None and mean_u < 0 and t_main <= -2
        slope_rej = slope is not None and t_slope is not None and slope < 0 and t_slope <= -2
        if main_rej or slope_rej:
            status = "rejected"
            decided = ("Reject rule: " +
                       ("the mean unusual move is negative with t <= -2" if main_rej else "") +
                       (" and " if (main_rej and slope_rej) else "") +
                       ("the supporting slope is negative with t <= -2" if slope_rej else "") + ".")
        elif main_conf and sup_passed:
            status = "confirmed"
            decided = "Confirm rule: the mean unusual move is positive with t >= 2 and the slope on |forecast| is positive with t >= 2."
        else:
            status = "inconclusive"
            if main_conf:
                decided = "Inconclusive rule: the main measure is positive with t >= 2 but the supporting slope does not reach t >= 2."
            else:
                decided = "Inconclusive rule: the results lie between the confirm and reject rules."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases summed by day", "value": t_main}
                                       if t_main is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name,
                             "value": slope,
                             "passed": sup_passed,
                             "t": t_slope} if True else None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
