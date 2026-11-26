import numpy as np
import pandas as pd
from scipy import stats

H = 7
BAND = 2.0
COMP = "debug_info.components.month_fall.last_history_value"
PROFILE_REGIME = "unknown"   # the config's only regime with a strategy: |60-bar return| <= 10 (choppy)


def _to_dt(s):
    if np.issubdtype(s.dtype, np.number):
        unit = "ms" if s.abs().max() > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _bets(f):
    """Short bets: a fall of the forecast of at least BAND from its smallest short depth since the last bet."""
    out = np.zeros(len(f), dtype=bool)
    ref = 0.0
    prev_short = False
    for i, v in enumerate(f):
        if not np.isfinite(v) or v >= 0:
            ref = 0.0
            prev_short = False
            continue
        depth = -v
        if not prev_short:
            ref = 0.0
        if depth - ref >= BAND - 1e-12:
            out[i] = True
            ref = depth
        else:
            ref = min(ref, depth)
        prev_short = True
    return out


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            if COMP in df.columns:
                raw = pd.to_numeric(df[COMP], errors="coerce").to_numpy(float)
            else:
                raw = np.full(len(df), np.nan)
            # recompute the 30-bar return from prices where the component is not recorded
            rec = np.full(len(df), np.nan)
            if len(df) > 30:
                rec[30:] = (close[30:] / close[:-30] - 1.0) * 100.0
            raw = np.where(np.isfinite(raw), raw, rec)
            regime = df["regime"].astype(str).to_numpy()
            active = np.isfinite(fc) & (fc != 0)
            sit = (regime == PROFILE_REGIME) & np.isfinite(raw) & (raw < 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars with a negative 30-bar return "
                           "inside the choppy profile (regime 'unknown'), as the Fidelity states."),
            "reading": "The choppy profile is the config's 'unknown' regime (60-bar move within +-10%), read from the regime column.",
        }

    # ---------- normal drift per coin ----------
    drift = {}
    for coin in bars:
        rets = []
        for w in bars[coin]:
            c = pd.to_numeric(bars[coin][w]["close"], errors="coerce").to_numpy(float)
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases and grid ----------
    case_moves, case_days = [], []
    xs, ys = [], []
    for coin in sorted(bars):
        d = drift[coin]
        if not np.isfinite(d):
            continue
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            ts = _to_dt(df["timestamp"])
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:-H] = c[H:] / c[:-H] - 1.0
            bet = _bets(fc)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if not np.isfinite(fwd[t]):
                    continue
                case_moves.append(-(fwd[t] - d))
                case_days.append(ts.iloc[t].strftime("%Y-%m-%d"))
            for p in range(0, n, H):
                if np.isfinite(fc[p]) and fc[p] < 0 and np.isfinite(fwd[p]):
                    xs.append(fc[p])
                    ys.append(fwd[p] - d)

    n_cases = len(case_moves)
    n_days = len(set(case_days))

    # main measure: mean with day-clustered t
    mean_mv, t_main = None, None
    if n_cases > 0:
        m = np.asarray(case_moves)
        mean_mv = float(m.mean())
        dev = pd.Series(m - m.mean()).groupby(np.asarray(case_days)).sum().to_numpy()
        G = len(dev)
        if G > 1:
            var = (G / (G - 1)) * np.sum(dev ** 2) / n_cases ** 2
            if var > 0:
                t_main = float(mean_mv / np.sqrt(var))

    # supporting check: OLS slope of excess return on forecast
    slope, t_slope = None, None
    if len(xs) >= 3 and np.std(xs) > 0:
        lr = stats.linregress(np.asarray(xs), np.asarray(ys))
        slope = float(lr.slope)
        if lr.stderr and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)
    sup_pass = None if t_slope is None else bool(slope > 0 and t_slope >= 2)

    counts = {"cases": int(n_cases), "distinct days": int(n_days), "grid bars with forecast < 0": int(len(xs))}

    if n_cases < 100 or n_days < 30:
        status = "not observable"
        decided = f"Minimum not reached: {n_cases} cases (need 100) on {n_days} distinct days (need 30)."
    elif t_main is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed."
    elif mean_mv > 0 and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and the slope is positive with t >= 2."
    elif (mean_mv < 0 and t_main <= -2) or (t_slope is not None and t_slope <= -2):
        status = "rejected"
        decided = ("Mean unusual move below 0 with t <= -2." if (mean_mv < 0 and t_main <= -2)
                   else "The slope's t is <= -2.")
    else:
        status = "inconclusive"
        decided = ("The main measure confirms but the slope check fails." if (mean_mv > 0 and t_main >= 2)
                   else "Neither the confirm nor the reject rule is met (t between -2 and 2).")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 7-bar move of short cases (short direction)",
            "value": mean_mv,
            "statistic": None if t_main is None else {"name": "day-clustered t", "value": t_main},
            "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "OLS slope of 7-bar excess return on forecast (grid bars, forecast < 0), t",
            "value": t_slope,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The choppy profile is the 'unknown' regime column; a case is the first short bet in each 7-bar "
                    "grid cell of a window, drift is the coin's mean non-overlapping 7-bar return over all windows, "
                    "the clustered t uses a G/(G-1) correction, and the slope's t is the ordinary pooled OLS t."),
    }
