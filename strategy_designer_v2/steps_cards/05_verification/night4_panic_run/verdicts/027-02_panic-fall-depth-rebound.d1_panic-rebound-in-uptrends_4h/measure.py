import numpy as np
import pandas as pd
from scipy import stats


def _component_series(df, comp_id, field):
    """Return the recorded component value as a float Series (NaN where not recorded)."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        def get(v):
            if isinstance(v, str):
                try:
                    import json
                    v = json.loads(v)
                except Exception:
                    return np.nan
            if isinstance(v, dict):
                c = v.get(comp_id)
                if isinstance(c, dict):
                    x = c.get(field)
                    try:
                        return float(x)
                    except (TypeError, ValueError):
                        return np.nan
            return np.nan
        return df["debug_info.components"].apply(get).astype(float)
    return pd.Series(np.nan, index=df.index)


def measure(bars):
    H = 84
    BAND = 2.0
    MIN_CASES = 30
    COMP = "panic_buy"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            rng = high - low
            ratio = rng.rolling(180).mean() / rng.rolling(6).mean()
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            panic = (regime == "mean_reversion") | (ratio <= 0.3333 + 1e-9)
            lhv = _component_series(df, COMP, "last_history_value")
            ret540 = close / close.shift(540) - 1
            uptrend = (lhv > 0) | (ret540 > 0)
            situation = panic & uptrend
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (f > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    main_name = "mean unusual 84-bar return of long bets (one per 84-bar grid cell)"
    main_thr = "confirm: mean > 0 with t >= 2 over >= 30 cases (and supporting check passes); reject: mean < 0 with t <= -2 over >= 30 cases"
    sup_name = "mean unusual return, forecast above cases' median minus at or below"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": (f"only {agreement:.1%} of active bars are long bars of the plan's situation "
                           "(6-bar mean range >= 3x its 180-bar mean with a positive 540-bar return), below the 90% needed"),
            "reading": "Panic taken from the recorded regime (the detector's decision on mbr <= 0.3333) or the recomputed high-low range ratio; uptrend from a positive raw component value or a positive 540-bar close return.",
        }

    # ---------- 2. normal drift per coin ----------
    drift = {}
    for coin in sorted(bars):
        rets = []
        for w in sorted(bars[coin]):
            c = pd.to_numeric(bars[coin][w]["close"], errors="coerce").to_numpy()
            for p in range(0, len(c) - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    unusual = []
    fc = []
    for coin in sorted(bars):
        if not np.isfinite(drift[coin]):
            continue
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            n = len(df)
            ref = 0.0
            taken_cells = set()
            for t in range(n):
                ft = f[t]
                if ft > 0:
                    if ft - ref >= BAND:
                        ref = ft
                        cell = t // H
                        if cell not in taken_cells:
                            taken_cells.add(cell)
                            if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                                r = c[t + H] / c[t] - 1
                                unusual.append(r - drift[coin])
                                fc.append(ft)
                    else:
                        ref = min(ref, ft)
                else:
                    ref = 0.0

    unusual = np.array(unusual, dtype=float)
    fc = np.array(fc, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_up = n_lo = 0
    if n_cases > 0:
        med = float(np.median(fc))
        up = unusual[fc > med]
        lo = unusual[fc <= med]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up > 0 and n_lo > 0:
            sup_val = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"only {n_cases} cases, fewer than the plan's minimum of 30 cases"
    elif t_u is not None and mean_u > 0 and t_u >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "mean unusual 84-bar return positive with t >= 2 over at least 30 cases, and the supporting check passes"
        else:
            status = "inconclusive"
            decided = "the main measure meets the confirm rule but the supporting check fails"
    elif t_u is not None and mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "mean unusual 84-bar return negative with t <= -2 over at least 30 cases"
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 over at least 30 cases"

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_u is None else {"name": "t of the mean", "value": t_u},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": {"cases": n_cases, "cases above median": n_up, "cases at or below median": n_lo,
                   "active bars": int(n_active)},
        "decided_by": decided,
        "reading": ("A case is the first long bet (forecast rise >= 2 from its lowest positive level since the last bet, from 0 after flat) "
                    "in each 84-bar grid cell counted from each window's first row, with a full 84-bar return inside the window; "
                    "drift is each coin's mean non-overlapping 84-bar return over all its windows; panic taken from the recorded regime or the recomputed high-low range ratio."),
    }
