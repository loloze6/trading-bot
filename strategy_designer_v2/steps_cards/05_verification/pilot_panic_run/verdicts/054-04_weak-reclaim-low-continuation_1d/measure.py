import json
import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    PERIOD = 30
    MIN_DAYS = 30

    def _comp_value(df, comp_id, field="last_history_value"):
        flat = "debug_info.components.%s.%s" % (comp_id, field)
        if flat in df.columns:
            return pd.to_numeric(df[flat], errors="coerce")
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].values:
                val = np.nan
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
                    if isinstance(c, dict):
                        x = c.get(field)
                        try:
                            val = float(x) if x is not None else np.nan
                        except Exception:
                            val = np.nan
                out.append(val)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    n_active = 0
    n_agree = 0
    cases = []  # (day, coin, unusual_short, nearness)

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # normal 5-day drift of the coin over all windows (non-overlapping grid)
        grid_rets = []
        prepared = {}
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            prepared[w] = df
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            for i in range(0, n - H, H):
                if np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    grid_rets.append(close[i + H] / close[i] - 1.0)
        drift = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

        for w, df in prepared.items():
            n = len(df)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            high = pd.to_numeric(df["high"], errors="coerce").values
            low = pd.to_numeric(df["low"], errors="coerce").values
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)
            near = _comp_value(df, "nearness").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            days = ts.dt.floor("D").astype(str).values

            # prior 30-day low (bar t excluded), only where 30 prior bars exist in the window
            low30 = pd.Series(low).shift(1).rolling(PERIOD, min_periods=PERIOD).min().values

            # ---- situation check ----
            for t in range(n):
                if fc[t] == 0:
                    continue
                n_active += 1
                in_profile_and_rule = regime[t] == "mean_reversion"
                nv = near[t]
                near_ok = np.isfinite(nv) and nv > 0 and nv <= 1.0 + 1e-9
                if np.isfinite(low30[t]):
                    price_ok = (low[t] < low30[t]) and (close[t] > low30[t])
                else:
                    price_ok = near_ok
                if in_profile_and_rule and near_ok and price_ok and fc[t] < 0:
                    n_agree += 1

            # ---- cases: short bets (rise of the short forecast by >= band) ----
            is_bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_side = 0
            for t in range(n):
                f = fc[t]
                side = -1 if f < 0 else (1 if f > 0 else 0)
                if side != -1:
                    ref = 0.0
                    prev_side = side
                    continue
                m = -f
                if prev_side != -1:
                    ref = 0.0
                ref = min(ref, m)
                if m - ref >= BAND:
                    is_bet[t] = True
                    ref = m
                prev_side = -1

            for start in range(0, n, H):
                idx = [t for t in range(start, min(start + H, n)) if is_bet[t]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n or not np.isfinite(drift):
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                r = close[t + H] / close[t] - 1.0
                u = -(r - drift)
                cases.append((days[t], coin, float(u), float(near[t]) if np.isfinite(near[t]) else np.nan))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else (agreement >= 0.9)

    main_name = "mean unusual 5-day move of the short cases, short direction"
    threshold = "confirm: mean > 0 with t >= 2 and positive nearness slope; reject: mean < 0 with t <= -2; at least 30 distinct case days"
    reading = ("Profile taken from the recorded regime 'mean_reversion' (the detector's 365-bar volatility percentile cannot be "
               "rebuilt from the window bars), pierce-and-reclaim recomputed from prices where 30 prior bars exist in the window "
               "and otherwise from a raw nearness in (0,1]; a case is the first short bet in each 5-bar grid cell of its window "
               "with a full 5-bar return inside the window; the minimum of 30 cases on distinct days is treated as a minimum count "
               "giving 'not observable'; the day-clustered t uses a small-sample factor D/(D-1).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars on a pierce-and-reclaim of the prior 30-day low inside the falling agitated profile, so the config does not do what the Fidelity states.",
            "reading": reading,
        }

    n_cases = len(cases)
    case_days = sorted(set(c[0] for c in cases))
    n_days = len(case_days)

    mean_u = None
    t_stat = None
    if n_cases > 0:
        u = np.array([c[2] for c in cases])
        mean_u = float(np.mean(u))
        dev = pd.Series(u - mean_u).groupby(pd.Series([c[0] for c in cases])).sum().values
        D = len(dev)
        if D > 1:
            var_mean = np.sum(dev ** 2) / (n_cases ** 2) * D / (D - 1)
            se = np.sqrt(var_mean)
            t_stat = float(mean_u / se) if se > 0 else None

    slope = None
    slope_ok = None
    if n_cases > 0:
        x = np.array([c[3] for c in cases])
        y = np.array([c[2] for c in cases])
        ok = np.isfinite(x) & np.isfinite(y)
        if ok.sum() >= 3 and np.unique(x[ok]).size >= 2:
            lr = stats.linregress(x[ok], y[ok])
            slope = float(lr.slope)
            slope_ok = bool(slope > 0)
        else:
            slope_ok = False if ok.sum() > 0 else None

    counts = {"cases": int(n_cases), "distinct case days": int(n_days),
              "active bars": int(n_active)}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = "Fewer than 30 cases counted on distinct days (%d), so the data could not show the idea." % n_days
    elif mean_u is not None and t_stat is not None and mean_u > 0 and t_stat >= 2 and slope_ok:
        status = "confirmed"
        decided = "The mean unusual move in the short direction is above 0 with t >= 2 and the nearness slope is positive."
    elif mean_u is not None and t_stat is not None and mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move in the short direction is below 0 with t <= -2: the coin rises more than its drift after these days."
    else:
        status = "inconclusive"
        if mean_u is not None and t_stat is not None and mean_u > 0 and t_stat >= 2:
            decided = "The mean unusual move meets the confirm rule but the supporting nearness slope is not positive."
        else:
            decided = "The t of the mean unusual move lies between -2 and 2 (or cannot be computed), meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": bool(passed)},
        "main_measure": {"name": main_name,
                         "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_stat}
                                       if t_stat is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "slope of short-direction unusual move on raw nearness",
                             "value": slope, "passed": slope_ok},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
