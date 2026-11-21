import numpy as np
import pandas as pd
from scipy import stats

H = 26
COL_PP = "debug_info.components.thin_cloud.post_pipeline_value"


def _cloud_state(df):
    """Recompute the Ichimoku cloud (9/26/52/26) from the window's own bars.
    State: +1 close above the cloud, -1 below it, 0 inside, NaN where not computable."""
    hi = df["high"].astype(float)
    lo = df["low"].astype(float)
    cl = df["close"].astype(float)
    tenkan = (hi.rolling(9, min_periods=9).max() + lo.rolling(9, min_periods=9).min()) / 2.0
    kijun = (hi.rolling(26, min_periods=26).max() + lo.rolling(26, min_periods=26).min()) / 2.0
    span_a = ((tenkan + kijun) / 2.0).shift(26)
    span_b = ((hi.rolling(52, min_periods=52).max() + lo.rolling(52, min_periods=52).min()) / 2.0).shift(26)
    top = np.maximum(span_a, span_b)
    bot = np.minimum(span_a, span_b)
    state = pd.Series(np.nan, index=df.index)
    ok = top.notna() & bot.notna() & cl.notna()
    state[ok] = 0.0
    state[ok & (cl > top)] = 1.0
    state[ok & (cl < bot)] = -1.0
    return state.values


def _cross_flags(state):
    """For each bar: True = upward cross (above now, last non-inside state before was below),
    False = not a cross, None = not evaluable from the recorded bars."""
    n = len(state)
    out = [None] * n
    for i in range(n):
        s = state[i]
        if np.isnan(s):
            continue
        if s != 1.0:
            out[i] = False
            continue
        if i == 0 or np.isnan(state[i - 1]):
            continue
        if state[i - 1] == 1.0:
            out[i] = False
            continue
        last = None
        for j in range(i - 1, -1, -1):
            if np.isnan(state[j]):
                break
            if state[j] != 0.0:
                last = state[j]
                break
        if last is None:
            continue
        out[i] = bool(last == -1.0)
    return out


def _tmean(x):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return (float(np.mean(x)) if n else None), None
    sd = np.std(x, ddof=1)
    m = float(np.mean(x))
    if sd == 0:
        return m, None
    return m, float(m / (sd / np.sqrt(n)))


def measure(bars):
    # ---------- 1. situation check ----------
    n_active_eval = 0
    n_agree = 0
    n_active_total = 0
    n_trend_active = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            flags = _cross_flags(_cloud_state(df))
            reg = df["regime"].astype(str).values
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active_total += 1
                if reg[i] == "trending" and fc[i] > 0:
                    n_trend_active += 1
                if flags[i] is None:
                    continue
                n_active_eval += 1
                if flags[i] and fc[i] > 0:
                    n_agree += 1
    if n_active_eval > 0:
        agreement = n_agree / n_active_eval
        fallback = False
    elif n_active_total > 0:
        agreement = n_trend_active / n_active_total
        fallback = True
    else:
        agreement = None
        fallback = False

    reading_check = ("the situation is checked on the active bars where the cloud (spans shifted 26 bars) can be "
                     "recomputed from the window's own recorded bars, a cross being a close above the cloud whose last "
                     "non-inside state before was below it")
    if fallback:
        reading_check += ("; no active bar was evaluable, so agreement falls back to active bars in regime 'trending' "
                          "with a positive forecast")

    if agreement is None or agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active_total), "active bars evaluable": int(n_active_eval)},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are bars where the close first sits "
                           "above the Ichimoku cloud after a stay below it with a long forecast"
                           if agreement is not None else "the record has no bar with a non-zero forecast"),
            "reading": reading_check + ".",
        }

    # ---------- 2. criterion ----------
    cases = []  # (unusual return, post_pipeline value)
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            cl = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(cl) - H, H):
                if np.isfinite(cl[p]) and np.isfinite(cl[p + H]) and cl[p] > 0:
                    grid_rets.append(cl[p + H] / cl[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            cl = pd.to_numeric(df["close"], errors="coerce").values
            reg = df["regime"].astype(str).values
            pp = (pd.to_numeric(df[COL_PP], errors="coerce").values
                  if COL_PP in df.columns else np.full(len(df), np.nan))
            used_cells = set()
            for i in range(len(df)):
                if reg[i] != "trending":
                    continue
                if i + H >= len(df):
                    continue
                if not (np.isfinite(cl[i]) and np.isfinite(cl[i + H]) and cl[i] > 0):
                    continue
                cell = i // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                r = cl[i + H] / cl[i] - 1.0
                cases.append((r - drift, pp[i]))

    vals = np.array([c[0] for c in cases], dtype=float)
    n_cases = int(len(vals))
    mean_u, t_u = _tmean(vals) if n_cases else (None, None)

    ppv = np.array([c[1] for c in cases], dtype=float)
    okpp = np.isfinite(ppv)
    thin = np.array([])
    thick = np.array([])
    diff = None
    t_d = None
    if okpp.sum() > 0:
        med = float(np.median(ppv[okpp]))
        thin = vals[okpp & (ppv > med)]
        thick = vals[okpp & (ppv < med)]
        if len(thin) >= 1 and len(thick) >= 1:
            diff = float(np.mean(thin) - np.mean(thick))
        if len(thin) >= 2 and len(thick) >= 2:
            tt = stats.ttest_ind(thin, thick, equal_var=False)
            t_d = float(tt.statistic) if np.isfinite(tt.statistic) else None

    counts = {"cross cases": n_cases, "thin group cases": int(len(thin)), "thick group cases": int(len(thick))}

    if n_cases < 30:
        status = "not observable"
        decided = f"fewer than 30 cross cases ({n_cases}), the plan's minimum."
    elif len(thin) < 15 or len(thick) < 15:
        status = "not observable"
        decided = f"fewer than 15 cases per group for the check (thin {len(thin)}, thick {len(thick)})."
    elif (t_u is not None and t_u <= -2) or (t_d is not None and t_d <= -2):
        status = "rejected"
        decided = "reject rule: with at least 30 cases, the mean unusual return has t <= -2 or the thin-minus-thick difference has t <= -2."
    elif (mean_u is not None and mean_u > 0 and t_u is not None and t_u >= 2
          and diff is not None and diff > 0 and t_d is not None and t_d >= 2):
        status = "confirmed"
        decided = "confirm rule: with at least 30 cases, the mean unusual return is above 0 with t >= 2 and the thin-minus-thick difference is above 0 with t >= 2."
    else:
        status = "inconclusive"
        decided = "inconclusive rule: neither the confirm nor the reject rule holds (t between -2 and 2 on at least one measure)."

    check_passed = None
    if diff is not None and t_d is not None:
        check_passed = bool(diff > 0 and t_d >= 2)

    reading = (reading_check + "; cases are bars with regime 'trending' whose 26-bar return stays inside the window, "
               "at most one per 26-bar grid cell of each window (the first), the drift is the coin's mean "
               "non-overlapping 26-bar return over all its windows, groups are strictly above and strictly below the "
               "cases' median thin_cloud post_pipeline_value, and the plan's too-few-cases clause is reported as "
               "'not observable'.")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean unusual 26-bar return at upward cloud crosses",
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t_u} if t_u is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2; reject: t <= -2; at least 30 cases",
        },
        "supporting_check": {
            "name": "thin minus thick cloud mean unusual 26-bar return (Welch t)",
            "value": diff,
            "passed": check_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
