import numpy as np
import pandas as pd
from scipy import stats

RAW = "debug_info.components.scaled_rise.last_history_value"
H = 7
BAND = 2.0
MIN_DAYS = 30


def _raw_from_prices(close):
    # VolatilityScaledReturnComponent(period=3, vol_period=30): 3-day return over std of last 30 daily returns * sqrt(3)
    r1 = close.pct_change()
    r3 = close / close.shift(3) - 1.0
    vol = r1.rolling(30).std()
    return r3 / (vol * np.sqrt(3.0))


def _bets(fc):
    """Long-side bets: forecast rise of >= BAND from its lowest level on the long side since the last bet
    (from 0 after a flat or a change of side)."""
    out = np.zeros(len(fc), dtype=bool)
    base = 0.0
    prev_long = False
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f <= 0:
            base = 0.0
            prev_long = False
            continue
        if not prev_long:
            base = 0.0
        if f - base >= BAND:
            out[i] = True
            base = f
        else:
            base = min(base, f)
        prev_long = True
    return out


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), _raw_from_prices(close))
            else:
                raw = _raw_from_prices(close)
            active = fc.notna() & (fc != 0)
            situ = raw > 0  # scaled 3-day rise
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean 7-bar unusual move (return minus coin's normal 7-bar drift) per long bet, day-clustered t"
    thr = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    sup_name = "OLS slope of unusual move on forecast at signal bar"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are long forecasts on bars with a positive scaled "
                           "3-day rise, so the config does not trade the plan's situation on the long side."),
            "reading": "Situation taken as the raw scaled 3-day return > 0 with a positive forecast.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        drift_samples = []
        coin_cases = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            # normal drift samples: non-overlapping grid 0, 7, 14, ...
            for p in range(0, n - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    drift_samples.append(b / a - 1.0)
            bet = _bets(fc)
            seen = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                a, b = close[i], close[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                coin_cases.append((coin, ts.iloc[i].normalize(), b / a - 1.0, fc[i]))
        drift = float(np.mean(drift_samples)) if drift_samples else np.nan
        for c, d, r, f in coin_cases:
            if np.isfinite(drift):
                rows.append({"coin": c, "day": d, "unusual": r - drift, "forecast": f})

    cases = pd.DataFrame(rows, columns=["coin", "day", "unusual", "forecast"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean = float(cases["unusual"].mean()) if n_cases else None
    t = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["unusual"] - mean
        per_day = dev.groupby(cases["day"]).sum()
        G = len(per_day)
        var_mean = (per_day ** 2).sum() / n_cases ** 2 * G / (G - 1)
        if var_mean > 0:
            t = float(mean / np.sqrt(var_mean))

    slope = None
    if n_cases >= 3 and cases["forecast"].nunique() > 1:
        slope = float(stats.linregress(cases["forecast"], cases["unusual"]).slope)
    slope_ok = (slope is not None and slope > 0)

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days over all coins and windows, fewer than the plan's minimum of 30."
    elif mean is not None and t is not None and mean > 0 and t >= 2 and slope_ok:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and a positive supporting slope (confirm rule)."
    elif mean is not None and t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 (reject rule)."
    elif mean is not None and t is not None and mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "Confirming mean and t but supporting slope of 0 or below (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2: neither confirm nor reject rule met (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean, cases of one day summed", "value": t}
                                       if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": slope, "passed": slope_ok if slope is not None else None},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are long bets (forecast rise >= 2 points from its lowest long level since the last bet, "
                    "from 0 after flat), the first per 7-bar grid cell of each window, needing close[t+7] in the "
                    "window; the normal drift is the coin's mean non-overlapping 7-bar return over all its windows; "
                    "the day-clustered t uses a G/(G-1) correction; the plan's 30-case-day minimum is treated as the "
                    "minimum count giving 'not observable'."),
    }
