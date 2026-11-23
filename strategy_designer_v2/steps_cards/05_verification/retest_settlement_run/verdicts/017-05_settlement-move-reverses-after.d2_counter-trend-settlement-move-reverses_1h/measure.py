import numpy as np
import pandas as pd
from scipy import stats


def _ts(series):
    s = series
    if pd.api.types.is_numeric_dtype(s):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 8
    UP = "debug_info.components.trend_up.last_history_value"
    DN = "debug_info.components.trend_down.last_history_value"

    n_active = 0
    n_agree = 0
    case_vals = []
    case_absf = []

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        frames = {}
        grid_rets = []
        for w in sorted(wins.keys(), key=lambda x: (len(str(x)), str(x))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            # normal-drift grid: positions 0, H, 2H, ... of each window
            pos = np.arange(0, len(df), H)
            c = close.values
            for p in pos:
                if p + H < len(c) and np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
            frames[w] = df
        drift = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

        for w, df in frames.items():
            close = df["close"].astype(float)
            ts = _ts(df["timestamp"])
            close_time = ts + pd.Timedelta(hours=1)
            settle = close_time.dt.hour.isin([0, 8, 16]) & (close_time.dt.minute == 0)
            settle = settle.values

            pre = (close / close.shift(2) - 1.0).values
            trend_px = (close / close.shift(24) - 1.0)
            trend = pd.Series(np.nan, index=df.index)
            if UP in df.columns:
                trend = trend.fillna(pd.to_numeric(df[UP], errors="coerce"))
            if DN in df.columns:
                trend = trend.fillna(pd.to_numeric(df[DN], errors="coerce"))
            trend = trend.fillna(trend_px).values

            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values

            # situation check
            long_sit = settle & (pre < 0) & (trend > 0)
            short_sit = settle & (pre > 0) & (trend < 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & ((long_sit & (fc > 0)) | (short_sit & (fc < 0)))).sum())

            # cases
            regime = df["regime"].astype(str).values
            fwd = (close.shift(-H) / close - 1.0).values
            is_case = settle & np.isin(regime, ["trending", "mean_reversion"]) & (np.abs(fc) >= 2)
            for i in np.where(is_case)[0]:
                r = fwd[i]
                if not np.isfinite(r) or not np.isfinite(drift):
                    continue
                case_vals.append((r - drift) * np.sign(fc[i]))
                case_absf.append(abs(fc[i]))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    main_name = "mean signed excess 8-bar return after settlement cases"
    thr = "confirm if t >= 2 (with positive slope); reject if t <= -2"
    reading = ("Settlement bars are those whose close (timestamp + 1h) falls at 00:00, 08:00 or 16:00 UTC; "
               "returns, the 2-bar pre-move and the 24-bar trend are taken by row position inside each window "
               "(trend from the recorded raw component where present, else from prices); cases without a full "
               "8-bar return inside their window are dropped; the 100-case minimum is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of bars with a nonzero forecast are settlement bars where the 2-bar "
                           "pre-move opposes the 24-bar trend with the forecast on the trend's side (long after a "
                           "pre-dip in an uptrend, short after a pre-rally in a downtrend)."),
            "reading": reading,
        }

    v = np.asarray(case_vals, dtype=float)
    a = np.asarray(case_absf, dtype=float)
    n = int(len(v))
    mean = float(np.mean(v)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(v, ddof=1))
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None
    slope = None
    if n > 2 and np.std(a) > 0:
        slope = float(stats.linregress(a, v).slope)

    slope_pass = None if slope is None else bool(slope > 0)

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 100 cases in total."
    elif t is not None and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean signed excess return has t >= 2 and the slope on |forecast| is positive."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "The mean signed excess return has t <= -2."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on |forecast| is 0 or below."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "slope of signed excess return on |forecast|", "value": slope,
                             "passed": slope_pass},
        "counts": {"cases": n},
        "decided_by": decided,
        "reading": reading,
    }
