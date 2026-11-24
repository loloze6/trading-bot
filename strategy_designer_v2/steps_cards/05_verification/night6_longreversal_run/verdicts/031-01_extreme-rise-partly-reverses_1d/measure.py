import json
import numpy as np
import pandas as pd


COMP_ID = "overreach"
HORIZON = 30
BAND = 2.0
MIN_CASES = 30
MIN_DAYS = 20
T_THR = 2.0


def _component_values(df, comp_id, field="last_history_value"):
    """Raw component value per bar; NaN where it is not recorded."""
    flat = "debug_info.components.%s.%s" % (comp_id, field)
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce").reset_index(drop=True)
    out = np.full(len(df), np.nan)
    if "debug_info.components" in df.columns:
        col = df["debug_info.components"].reset_index(drop=True)
        for i, v in enumerate(col):
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(comp_id)
                if isinstance(c, dict) and field in c:
                    try:
                        out[i] = float(c[field])
                    except (TypeError, ValueError):
                        pass
    return pd.Series(out)


def _bets(forecast):
    """Bars where the forecast rises on its own side by at least the band."""
    f = np.asarray(forecast, dtype=float)
    bets = np.zeros(len(f), dtype=bool)
    prev_side = 0
    ref = 0.0
    for i, x in enumerate(f):
        if not np.isfinite(x) or x == 0:
            prev_side = 0
            ref = 0.0
            continue
        side = 1 if x > 0 else -1
        mag = abs(x)
        if side != prev_side:
            ref = 0.0
        if mag - ref >= BAND:
            bets[i] = True
            ref = mag
        else:
            ref = min(ref, mag)
        prev_side = side
    return bets


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            z = _component_values(df, COMP_ID).values
            active = fc != 0
            situation = np.where(np.isfinite(z), z >= 1.0, False)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    threshold_txt = ("confirm: mean > 0 with t >= 2.0; reject: mean < 0 with t <= -2.0; "
                     "at least 30 cases on at least 20 distinct days")
    main_name = "mean 30-bar unusual move in the short direction (return minus coin's normal 30-bar drift)"
    reading = ("The situation is read from the recorded raw z90 (overreach last_history_value) >= 1 with a short "
               "forecast, a bar without that recorded value counting as outside the situation since 365-day volatility "
               "cannot be rebuilt from the windows' prices; a case is the first bet bar (forecast rising on the short "
               "side by >= 2 points from its lowest level since the last bet) in regime mean_reversion in each "
               "30-bar grid cell counted from each window's first row, cases without a 30-bar return inside the "
               "window are left out, the normal drift is the coin's mean 30-bar return on the same grid over all its "
               "windows, the t is day-clustered (deviations summed per UTC day, with a G/(G-1) correction), and "
               "unmet minimum counts give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are bars where z90 >= 1 with a short "
                           "forecast (agreement %.3f), so the config does not do what the plan's Fidelity says."
                           % agreement),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_ret = []
    case_coin = []
    case_day = []
    drift = {}
    for coin in sorted(bars):
        grid_rets = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            for p in range(0, n - HORIZON, HORIZON):
                c0, c1 = close[p], close[p + HORIZON]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            bets = _bets(fc)
            n = len(df)
            taken = set()
            for t in range(n):
                cell = t // HORIZON
                if cell in taken:
                    continue
                if not (bets[t] and reg[t] == "mean_reversion" and fc[t] < 0):
                    continue
                taken.add(cell)
                if t + HORIZON >= n:
                    continue
                c0, c1 = close[t], close[t + HORIZON]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                if not np.isfinite(drift[coin]) or pd.isna(ts.iloc[t]):
                    continue
                r = c1 / c0 - 1.0
                case_ret.append(-(r - drift[coin]))
                case_coin.append(coin)
                case_day.append(ts.iloc[t].floor("D"))

    x = np.asarray(case_ret, dtype=float)
    n_cases = int(len(x))
    days = pd.Series(case_day)
    n_days = int(days.nunique()) if n_cases else 0

    mean_val = float(np.mean(x)) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = x - x.mean()
        s_day = pd.Series(dev).groupby(days.values).sum().values
        g = len(s_day)
        var_m = (np.sum(s_day ** 2) / n_cases ** 2) * (g / (g - 1.0))
        if var_m > 0:
            t_val = float(x.mean() / np.sqrt(var_m))

    counts = {"cases": n_cases, "distinct days": n_days}
    stat = {"name": "t of the mean, cases of one day taken together",
            "value": t_val} if t_val is not None else None

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = ("The plan's minimum of %d cases on %d distinct days is not reached (%d cases on %d days)."
                   % (MIN_CASES, MIN_DAYS, n_cases, n_days))
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed (zero spread), so neither the confirm nor the reject rule is met."
    elif mean_val > 0 and t_val >= T_THR:
        status = "confirmed"
        decided = ("Confirm rule met: mean unusual move in the short direction %.4f > 0 with t %.2f >= 2.0 over "
                   "%d cases on %d days." % (mean_val, t_val, n_cases, n_days))
    elif mean_val < 0 and t_val <= -T_THR:
        status = "rejected"
        decided = ("Reject rule met: mean unusual move in the short direction %.4f < 0 with t %.2f <= -2.0 over "
                   "%d cases on %d days (the coins keep rising)." % (mean_val, t_val, n_cases, n_days))
    else:
        status = "inconclusive"
        decided = ("Inconclusive rule: t %.2f lies between -2.0 and 2.0 (mean %.4f) over %d cases on %d days."
                   % (t_val, mean_val, n_cases, n_days))

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_val, "statistic": stat, "threshold": threshold_txt},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
