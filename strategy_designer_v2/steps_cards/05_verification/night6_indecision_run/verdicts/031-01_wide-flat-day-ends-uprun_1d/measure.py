import json
import ast
import numpy as np
import pandas as pd

H = 5
BAND = 2.0
MIN_CASES = 30
EPS = 1e-9


def _parse_comp(cell):
    # The components column may hold a dict, a JSON string, or a Python repr string.
    if isinstance(cell, dict):
        return cell
    if isinstance(cell, str) and cell.strip():
        try:
            return json.loads(cell)
        except Exception:
            try:
                v = ast.literal_eval(cell)
                return v if isinstance(v, dict) else None
            except Exception:
                return None
    return None


def _component_series(df, cid):
    # Raw value of a strategy component, NaN where it is not recorded.
    flat = "debug_info.components.%s.last_history_value" % cid
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce").reset_index(drop=True)
    out = np.full(len(df), np.nan)
    if "debug_info.components" in df.columns:
        for i, cell in enumerate(df["debug_info.components"].values):
            d = _parse_comp(cell)
            if not d or cid not in d:
                continue
            c = d[cid]
            v = c.get("last_history_value") if isinstance(c, dict) else None
            try:
                out[i] = float(v)
            except (TypeError, ValueError):
                pass
    return pd.Series(out)


def _cluster_t(vals, days):
    # t of the mean, with the cases of one day taken together.
    vals = np.asarray(vals, float)
    n = len(vals)
    if n < 2:
        return None, 0
    m = vals.mean()
    dev = pd.Series(vals - m).groupby(np.asarray(days)).sum().values
    g = len(dev)
    if g < 2:
        return None, g
    var = (g / (g - 1.0)) * np.sum(dev ** 2) / n ** 2
    if var <= 0:
        return None, g
    return float(m / np.sqrt(var)), g


def measure(bars):
    act_total = 0
    act_agree = 0
    act_undetermined = 0
    case_rows = []

    for coin in sorted(bars.keys()):
        wins = bars[coin]

        # The coin's normal 5-day drift: non-overlapping grid returns over all its windows.
        grid_rets = []
        for w in sorted(wins.keys()):
            df = wins[w].reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w in sorted(wins.keys()):
            df = wins[w].reset_index(drop=True)
            if len(df) == 0:
                continue
            o = pd.to_numeric(df["open"], errors="coerce")
            hi = pd.to_numeric(df["high"], errors="coerce")
            lo = pd.to_numeric(df["low"], errors="coerce")
            c = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.strftime("%Y-%m-%d").values

            rng = hi - lo
            # Recomputed from prices; the recorded raw values take precedence where present.
            rr_calc = rng / rng.rolling(20, min_periods=20).mean()
            fl_calc = 1.0 - (c - o).abs() / rng.replace(0, np.nan)
            rr_rec = _component_series(df, "range_ratio")
            fl_rec = _component_series(df, "flatness")
            rr = rr_rec.where(rr_rec.notna(), rr_calc)
            fl = fl_rec.where(fl_rec.notna(), fl_calc)
            pe5 = c / c.shift(5) - 1.0

            # Situation check: an up 5-day run, a wide day and a flat day, on the short side.
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                a, b, f = pe5.iloc[i], rr.iloc[i], fl.iloc[i]
                if not (np.isfinite(a) and np.isfinite(b) and np.isfinite(f)):
                    act_undetermined += 1
                    continue
                act_total += 1
                situ = (a > 0) and (b >= 1.5 - EPS) and (f >= 0.9 - EPS)
                if situ and fc[i] < 0:
                    act_agree += 1

            # Short bets: a rise of |forecast| on the short side of at least the band,
            # from its lowest level since the last bet (from 0 after flat or long).
            ref = 0.0
            bet = np.zeros(len(df), bool)
            for i in range(len(df)):
                if fc[i] < 0:
                    m = -fc[i]
                    if m - ref >= BAND - EPS:
                        bet[i] = True
                        ref = m
                    else:
                        ref = min(ref, m)
                else:
                    ref = 0.0

            # One case per 5-bar grid cell: the first bet in the cell.
            cv = c.values
            seen = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= len(df):
                    continue
                if not (np.isfinite(cv[i]) and np.isfinite(cv[i + H])) or cv[i] == 0:
                    continue
                if not np.isfinite(drift):
                    continue
                ret = cv[i + H] / cv[i] - 1.0
                case_rows.append({
                    "unusual": -(ret - drift),
                    "absf": abs(fc[i]),
                    "day": days[i],
                })

    agreement = (act_agree / act_total) if act_total > 0 else None
    passed = agreement is not None and agreement >= 0.9
    threshold_txt = ("confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check passes; "
                     "reject: mean < 0 with t <= -2 over >= 30 cases")
    reading_base = ("Active bars whose 5-day return or range ratio cannot be computed inside the record "
                    "are left out of the agreement share; a case is the first short bet in each 5-bar cell "
                    "of its window, cases with no full 5-bar return in the window are dropped, the t clusters "
                    "cases by UTC day, and the supporting check compares cases strictly above with cases "
                    "strictly below the median |forecast| (ties left out).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(act_total),
                       "active bars not determinable": int(act_undetermined)},
            "decided_by": ("Fewer than 90% of active bars are short bars on a day after a 5-day rise with a "
                           "range at least 1.5x its 20-day mean and flatness at least 0.9"
                           if agreement is not None else
                           "No active bar on which the plan's situation could be checked"),
            "reading": reading_base,
        }

    cases = pd.DataFrame(case_rows, columns=["unusual", "absf", "day"])
    n = int(len(cases))
    mean = float(cases["unusual"].mean()) if n > 0 else None
    t, ndays = _cluster_t(cases["unusual"].values, cases["day"].values) if n > 0 else (None, 0)

    sup_val, sup_pass = None, None
    if n > 0:
        med = cases["absf"].median()
        above = cases.loc[cases["absf"] > med, "unusual"]
        below = cases.loc[cases["absf"] < med, "unusual"]
        if len(above) > 0 and len(below) > 0:
            sup_val = float(above.mean() - below.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n < MIN_CASES:
        status = "not observable"
        decided = "Fewer than 30 cases (%d), the plan's minimum count, so the data cannot show the idea." % n
    elif t is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("Mean unusual move in the short direction above 0 with t >= 2 over at least 30 cases, "
                       "and the supporting check passes.")
        else:
            status = "inconclusive"
            decided = "A confirming t whose supporting check fails is inconclusive."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move in the short direction below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean 5-day unusual move in the short direction",
            "value": mean,
            "statistic": {"name": "t of the mean, same-day cases taken together",
                          "value": t} if t is not None else None,
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "mean unusual move above minus below the median |forecast|",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n, "days": int(ndays), "active bars": int(act_total)},
        "decided_by": decided,
        "reading": reading_base,
    }
