import numpy as np
import pandas as pd
from scipy import stats


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype("float64")
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _bets(fc, band=2.0):
    """Flag bars where the forecast rises on its side by at least the band
    from its lowest level on that side since its last bet (from 0 after flat or a side change)."""
    n = len(fc)
    is_bet = np.zeros(n, dtype=bool)
    side = 0
    base = 0.0
    for i in range(n):
        f = fc[i]
        if not np.isfinite(f) or f == 0:
            side = 0
            base = 0.0
            continue
        s = 1 if f > 0 else -1
        mag = abs(f)
        if s != side:
            side = s
            base = 0.0
        if mag - base >= band:
            is_bet[i] = True
            base = mag
        else:
            base = min(base, mag)
    return is_bet


def measure(bars):
    H = 48
    raw_col = "debug_info.components.weekend_gain.last_history_value"

    n_active = 0
    n_agree = 0
    drift_samples = {}
    case_rows = []  # (coin, ret, |forecast|)

    for coin in sorted(bars.keys()):
        drift_samples[coin] = []
        for w in sorted(bars[coin].keys(), key=lambda x: (len(str(x)), str(x))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            ts = _to_utc(df["timestamp"]).reset_index(drop=True)
            nxt = ts + pd.Timedelta(hours=1)
            is_mon0 = ((nxt.dt.weekday == 0) & (nxt.dt.hour == 0) & (nxt.dt.minute == 0)).values

            # raw 48-bar return: recorded value, else recomputed from prices inside the window
            recomputed = pd.Series(close).pct_change(H).values
            if raw_col in df.columns:
                raw = pd.to_numeric(df[raw_col], errors="coerce").values.astype(float)
                raw = np.where(np.isfinite(raw), raw, recomputed)
            else:
                raw = recomputed

            # situation check
            active = fc != 0
            situation_short = is_mon0 & np.isfinite(raw) & (raw > 0)
            n_active += int(active.sum())
            n_agree += int((active & situation_short & (fc < 0)).sum())

            # forward 48-bar returns inside the window
            fwd = np.full(len(close), np.nan)
            if len(close) > H:
                fwd[:-H] = close[H:] / close[:-H] - 1.0

            # normal drift grid: positions 0, 48, 96, ...
            grid = np.arange(0, len(close), H)
            g = fwd[grid]
            drift_samples[coin].extend([x for x in g if np.isfinite(x)])

            # cases: Monday-00:00 bar, negative forecast, makes a bet
            bet = _bets(fc)
            idx = np.where(is_mon0 & (fc < 0) & bet & np.isfinite(fwd))[0]
            for i in idx:
                case_rows.append((coin, fwd[i], abs(fc[i])))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean signed unusual 48-bar move after a weekend-gain short (short direction, net of coin drift)"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: t <= -2; at least 100 cases"
    reading = ("A case is a bar stamped Sunday 23:00 UTC (closing at Monday 00:00) with a negative forecast that is a bet "
               "under the 2-point band rule, its 48-bar return taken by row inside its window and the coin's drift from "
               "the 0,48,96,... grid of all its windows; the plan's fewer-than-100-cases rule is reported as 'not observable' "
               "per the workflow's minimum-count rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "active_bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of the {n_active} active bars are Monday-00:00 bars after a positive "
                           "48-bar weekend return with a short forecast, below the 90% the plan's situation requires."),
            "reading": reading,
        }

    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in drift_samples.items()}
    vals, sizes = [], []
    for coin, r, a in case_rows:
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        vals.append(-(r - d))
        sizes.append(a)
    vals = np.array(vals, dtype=float)
    sizes = np.array(sizes, dtype=float)
    n = int(len(vals))

    mean_v = float(np.mean(vals)) if n > 0 else None
    t_v = None
    if n > 1:
        sd = float(np.std(vals, ddof=1))
        t_v = float(mean_v / (sd / np.sqrt(n))) if sd > 0 else None
    slope = None
    if n > 1 and np.ptp(sizes) > 0:
        slope = float(stats.linregress(sizes, vals).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    sc = {"agreement": None if agreement is None else float(agreement), "passed": passed}
    mm = {"name": main_name, "value": mean_v,
          "statistic": None if t_v is None else {"name": "t of the mean", "value": t_v},
          "threshold": threshold}
    sup = {"name": "OLS slope of signed unusual move on |forecast|", "value": slope, "passed": slope_pass}
    counts = {"cases": n}

    if n < 100:
        return {"status": "not observable", "situation_check": sc, "main_measure": mm,
                "supporting_check": sup, "counts": counts,
                "decided_by": f"Only {n} cases, fewer than the 100 the plan requires.",
                "reading": reading}

    if t_v is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so neither rule is met."
    elif t_v >= 2 and mean_v > 0 and slope_pass:
        status = "confirmed"
        decided = "The mean signed unusual move is positive with t >= 2 and the slope on |forecast| is above 0."
    elif t_v <= -2:
        status = "rejected"
        decided = "The mean signed unusual move has t <= -2: weekend gains are followed by rises beyond the coin's drift."
    elif t_v >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on |forecast| is at or below 0 (or undefined), so the result is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2."

    return {"status": status, "situation_check": sc, "main_measure": mm,
            "supporting_check": sup, "counts": counts,
            "decided_by": decided, "reading": reading}
