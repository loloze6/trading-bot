import numpy as np
import pandas as pd
from scipy import stats


def _component_series(df, comp_id, field="last_history_value"):
    """Extract a recorded component value, whether flattened or stored as dicts."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce").reset_index(drop=True)
    if "debug_info.components" in df.columns:
        vals = []
        for d in df["debug_info.components"].tolist():
            v = np.nan
            if isinstance(d, dict):
                c = d.get(comp_id)
                if isinstance(c, dict):
                    x = c.get(field)
                    try:
                        v = float(x) if x is not None else np.nan
                    except (TypeError, ValueError):
                        v = np.nan
            vals.append(v)
        return pd.Series(vals, dtype=float)
    return pd.Series(np.nan, index=range(len(df)), dtype=float)


def _bets(forecast, band=2.0):
    """Bars where the forecast rises on its side by at least the band from its lowest level since the last bet."""
    out = []
    base = 0.0
    prev_side = 0
    for i, f in enumerate(forecast):
        if not np.isfinite(f) or f == 0:
            base = 0.0
            prev_side = 0
            continue
        side = 1 if f > 0 else -1
        if side != prev_side:
            base = 0.0
        a = abs(f)
        if a - base >= band - 1e-9:
            out.append(i)
            base = a
        else:
            base = min(base, a)
        prev_side = side
    return out


def measure(bars):
    H = 18
    tol = 0.05  # small tolerance for recomputation differences

    # ---------------- situation check ----------------
    n_active = 0
    n_agree = 0
    n_unknown = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            r6 = close / close.shift(6) - 1.0
            denom = r6.abs().rolling(180, min_periods=30).mean()
            fall24 = r6 / denom.replace(0, np.nan)

            br = (high - low) / close
            rng_re = br.rolling(180, min_periods=30).mean() / br.rolling(6, min_periods=6).mean().replace(0, np.nan)
            rng_rec = _component_series(df, "range_excess", "last_history_value")
            rng = rng_rec.where(rng_rec.notna(), rng_re)

            active = fc != 0
            for i in np.where(active.values)[0]:
                fv, rv = fall24.iloc[i], rng.iloc[i]
                if not (np.isfinite(fv) and np.isfinite(rv)):
                    n_unknown += 1
                    continue
                n_active += 1
                in_sit = (fv <= -2.0 * (1 - tol)) and (rv <= (1.0 / 3.0) * (1 + tol))
                if in_sit and fc.iloc[i] > 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    reading = ("Situation recomputed from prices (6-bar return over the mean absolute 6-bar return of the last 180 bars, "
               "bar range as (high-low)/close, recorded range_excess raw value used where present, partial windows from 30 bars, 5% tolerance, "
               "active bars whose situation cannot be computed left out); cases are the first bet in each 18-bar cell of each window's grid from its first row "
               "with the 18-bar return inside the window, the coin mean is over the non-overlapping 18-bar grid of all its windows, excess is not sign-flipped "
               "(all bets are long by plan), and the median split uses cases strictly above versus strictly below the median forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active), "active bars not computable": int(n_unknown)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of the plan's panic situation "
                           "(6-bar return <= -2 usual moves and 180/6 range ratio <= 1/3)."),
            "reading": reading,
        }

    # ---------------- criterion ----------------
    excess = []
    case_fc = []
    for coin in sorted(bars):
        # coin mean 18-bar return over all windows (non-overlapping grid)
        grid_rets = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(df) - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))

        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            seen_cells = set()
            for t in _bets(fc):
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= len(df):
                    continue
                a, b = close[t], close[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                excess.append(b / a - 1.0 - mu)
                case_fc.append(fc[t])

    excess = np.array(excess, dtype=float)
    case_fc = np.array(case_fc, dtype=float)
    n = int(len(excess))

    mean_ex = float(np.mean(excess)) if n > 0 else None
    t_stat = None
    if n >= 2:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n)))

    # supporting check
    sup_val = None
    sup_pass = None
    if n > 0:
        med = float(np.median(case_fc))
        hi = excess[case_fc > med]
        lo = excess[case_fc < med]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {
        "name": "mean excess 18-bar return of bets over the coin's mean 18-bar return",
        "value": mean_ex,
        "statistic": {"name": "t of the mean", "value": t_stat} if t_stat is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2",
    }
    support = {"name": "mean excess above median forecast minus below median", "value": sup_val, "passed": sup_pass}
    counts = {"independent cases": n}

    if n < 30:
        status = "not observable"
        decided = "Fewer than 30 independent cases across all coins and windows."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean excess return cannot be computed (zero dispersion), so it is not between the confirm or reject thresholds."
    elif mean_ex > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean excess 18-bar return is positive with t >= 2 and the above-minus-below-median difference is positive."
    elif mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean excess 18-bar return is negative with t <= -2."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
