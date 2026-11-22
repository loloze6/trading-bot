import numpy as np
import pandas as pd
from scipy import stats

H = 5
BAND = 2.0
MIN_CASES = 50
FD = "debug_info.components.fall_depth.last_history_value"


def _bounce_variants(close):
    r = close.pct_change()
    out = []
    for ddof in (0, 1):
        s_inc = r.rolling(20, min_periods=20).std(ddof=ddof)
        s_exc = r.shift(1).rolling(20, min_periods=20).std(ddof=ddof)
        out.append(r / s_inc.replace(0, np.nan))
        out.append(r / s_exc.replace(0, np.nan))
    return pd.concat(out, axis=1)


def _short_bets(fc):
    bets = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    for i, f in enumerate(fc):
        m = -f if (np.isfinite(f) and f < 0) else 0.0
        if m == 0.0:
            ref = 0.0
            continue
        if m - ref >= BAND:
            bets[i] = True
            ref = m
        else:
            ref = min(ref, m)
    return bets


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    n_unknown = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            ret90_rec = df[FD].astype(float) if FD in df.columns else pd.Series(np.nan, index=df.index)
            ret90_px = close / close.shift(90) - 1.0
            ret90 = ret90_rec.where(ret90_rec.notna(), ret90_px)
            bv = _bounce_variants(close)
            bmax = bv.max(axis=1, skipna=True)
            ball_nan = bv.isna().all(axis=1)
            for i in np.where(fc.values != 0)[0]:
                if not np.isfinite(ret90.iloc[i]) or ball_nan.iloc[i]:
                    n_unknown += 1
                    continue
                n_active += 1
                if ret90.iloc[i] < 0 and bmax.iloc[i] >= 2.0 - 1e-9 and fc.iloc[i] < 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Bets are the forecast.md short-side rises of at least 2 points, the first one in each 5-bar grid cell "
               "(positions 0,5,10,... of each window) on a mean_reversion bar is the case, the coin's mean 5-day return "
               "is over its non-overlapping grid samples of all windows, the slope t is the OLS slope's t of excess "
               "return on fall_depth, the plan's 'fewer than 50 cases' is treated as the minimum count (not observable), "
               "and in the situation check the bounce (1-day return over the 20-day std of daily returns, counted if any "
               "of the ddof 0/1, current-bar-in/out variants is at least 2) and the 90-day return (recorded fall_depth, "
               "else from prices) leave out of the share the active bars where they cannot be computed inside the window.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active, "active bars not computable": n_unknown},
            "decided_by": ("Fewer than 90% of the active bars are bars where the 90-day return is below 0 and the "
                           "vol-scaled 1-day return is at least 2 with a short forecast, so the config does not do "
                           "what the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- criterion ----------
    xs, ys = [], []
    for coin in sorted(bars):
        grid = []
        cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = df["close"].astype(float).values
            for p in range(0, n - H, H):
                if close[p] > 0 and np.isfinite(close[p]) and np.isfinite(close[p + H]):
                    grid.append(close[p + H] / close[p] - 1.0)
            fc = df["forecast"].astype(float).values
            bets = _short_bets(fc)
            reg = df["regime"].astype(str).values
            fd = df[FD].astype(float).values if FD in df.columns else np.full(n, np.nan)
            seen = set()
            for i in range(n):
                if not bets[i] or reg[i] != "mean_reversion":
                    continue
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and close[i] > 0 and np.isfinite(close[i + H]) and np.isfinite(fd[i])):
                    continue
                cases.append((fd[i], close[i + H] / close[i] - 1.0))
        if not grid:
            continue
        mu = float(np.mean(grid))
        for x, r in cases:
            xs.append(float(x))
            ys.append(float(r - mu))

    n_cases = len(xs)
    slope = None
    t_slope = None
    if n_cases >= 3:
        x = np.array(xs)
        y = np.array(ys)
        if np.std(x) > 0:
            res = stats.linregress(x, y)
            slope = float(res.slope)
            t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None
    sup = float(np.mean(-np.array(ys))) if n_cases > 0 else None
    sup_pass = (sup > 0) if sup is not None else None

    main = {"name": "OLS slope of excess 5-day return on 90-day return (fall_depth)",
            "value": slope,
            "statistic": {"name": "slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": "confirm: slope > 0 with t >= 2 (and supporting check); reject: slope < 0 with t <= -2; at least 50 cases"}
    supporting = {"name": "mean excess 5-day return in the short direction", "value": sup, "passed": sup_pass}
    counts = {"cases": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases, fewer than the plan's minimum of 50."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t_slope >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the short-direction case mean is above 0, over at least 50 cases."
        else:
            status = "inconclusive"
            decided = "The slope t is >= 2 but the short-direction case mean is not above 0, which the plan calls inconclusive."
    elif slope < 0 and t_slope <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 over at least 50 cases."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
