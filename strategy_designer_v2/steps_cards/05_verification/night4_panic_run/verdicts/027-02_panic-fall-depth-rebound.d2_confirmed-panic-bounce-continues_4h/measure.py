import numpy as np
import pandas as pd
from scipy import stats

H = 84
BAND = 2.0
BOUNCE_COL = "debug_info.components.bounce.last_history_value"


def _panic_value(df):
    """Recompute the ScaledFallRangeMultiple (6-bar stretch, lag 6, 180-bar base) from prices, inside one window."""
    close = df["close"].astype(float)
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    ret6 = close / close.shift(6) - 1.0
    usual_move = ret6.abs().rolling(180, min_periods=180).mean()
    rng6 = (high.rolling(6, min_periods=6).max() - low.rolling(6, min_periods=6).min()) / close
    usual_rng = rng6.rolling(180, min_periods=180).mean()
    fall = (-ret6).clip(lower=0.0)
    fall_scaled = fall / usual_move.replace(0, np.nan)
    rng_mult = rng6 / usual_rng.replace(0, np.nan)
    prod = fall_scaled * rng_mult
    return prod.shift(6)  # the stretch that ended 6 bars (24h) ago


def _bets(f):
    """Bets per forecast.md point 7: a rise of the forecast on its own side of >= band from its lowest level on that side."""
    out = np.zeros(len(f), dtype=bool)
    side, ref = 0, 0.0
    for i, v in enumerate(f):
        if not np.isfinite(v) or v == 0:
            side, ref = 0, 0.0
            continue
        s = 1 if v > 0 else -1
        if s != side:
            side, ref = s, 0.0
        m = abs(v)
        if m - ref >= BAND:
            out[i] = True
            ref = m
        else:
            ref = min(ref, m)
    return out


def measure(bars):
    # ---------- 1. situation check ----------
    n_active, n_agree = 0, 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if df.empty:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if not active.any():
                continue
            panic = _panic_value(df)
            regime_mr = df["regime"].astype(str) == "mean_reversion"
            situ = np.where(panic.notna(), panic >= 3.0, regime_mr)
            close = df["close"].astype(float)
            ret6 = close / close.shift(6) - 1.0
            if BOUNCE_COL in df.columns:
                bounce = pd.to_numeric(df[BOUNCE_COL], errors="coerce").fillna(ret6)
            else:
                bounce = ret6
            side_ok = np.sign(f) == np.sign(bounce)
            a = active.values
            n_active += int(a.sum())
            n_agree += int((a & situ & side_ok.values).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "OLS slope of 84-bar forward return minus normal drift on the forecast at the case bar"
    threshold = "confirm: slope > 0 with t >= 2 over >= 30 independent cases; reject: slope < 0 with t <= -2 over >= 30 cases"
    reading = ("The expected side is the sign of the 24h bounce (the Fidelity's graded comparison: larger bounce, higher "
               "return), the panic value is rebuilt from prices as (fall / mean |6-bar return| over 180 bars) x "
               "(6-bar range / its 180-bar mean) for the stretch ending 6 bars back, using the recorded regime where "
               "the window's history is too short; a case is the first bet of each 84-bar grid cell of a window, "
               "pooled over all coins, with the normal drift being the coin's mean non-overlapping 84-bar return "
               "over all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent cases": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are bars where the 24h-back stretch is a panic "
                           "(scaled fall x range multiple >= 3) with the forecast on the bounce's side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin in sorted(bars):
        # normal drift: mean of non-overlapping 84-bar returns over all windows
        grid_rets = []
        for w in sorted(bars[coin]):
            c = bars[coin][w]["close"].astype(float).reset_index(drop=True).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if df.empty:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            c = df["close"].astype(float).values
            reg = df["regime"].astype(str).values
            bet = _bets(f)
            seen = set()
            for i in np.where(bet)[0]:
                if reg[i] != "mean_reversion":
                    continue
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= len(c) or not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] == 0:
                    continue
                xs.append(f[i])
                ys.append(c[i + H] / c[i] - 1.0 - drift)

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n = int(len(x))

    slope, tval = None, None
    if n >= 3 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr > 0 else None

    pos = y[x > 0]
    sup_val = float(np.mean(pos)) if len(pos) > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    counts = {"independent cases": n, "cases with positive forecast": int(len(pos))}
    main = {"name": main_name, "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": threshold}
    support = {"name": "mean excess 84-bar return of positive-forecast cases above 0",
               "value": sup_val, "passed": sup_pass}

    if n < 30 or slope is None or tval is None:
        status = "not observable"
        decided = f"The plan's minimum of 30 independent cases is not reached ({n} cases)."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 over at least 30 cases and the positive-forecast cases' mean excess return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope confirms (positive, t >= 2) but the supporting check fails, which the plan calls inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 over at least 30 independent cases."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (or its sign disagrees with its t threshold), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
