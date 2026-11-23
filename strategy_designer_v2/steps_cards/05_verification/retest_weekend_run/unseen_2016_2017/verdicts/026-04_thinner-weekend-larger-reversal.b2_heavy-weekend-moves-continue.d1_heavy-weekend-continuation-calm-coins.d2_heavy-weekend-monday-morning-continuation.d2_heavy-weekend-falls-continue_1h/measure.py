import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 12
    RAW = "debug_info.components.weekend_fall.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0 or "forecast" not in df.columns:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")

            # Sunday 23:00 bar (its coming bar is Monday 00:00 UTC)
            is_sun23 = ((ts.dt.dayofweek == 6) & (ts.dt.hour == 23)).values

            # weekend fall: sign of the component's raw value, else the 48-bar price return
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            ret48 = close / close.shift(48) - 1.0
            fall = np.where(raw.notna().values, raw.values < 0,
                            np.where(ret48.notna().values, ret48.values < 0, False))

            # weekend volume vs the 120 bars before it
            recent = vol.rolling(48, min_periods=48).mean()
            prior = vol.shift(48).rolling(120, min_periods=120).mean()
            ratio = recent / prior
            reg_trend = (df["regime"].astype(str) == "trending").values if "regime" in df.columns else np.zeros(len(df), bool)
            heavy = np.where(ratio.notna().values & np.isfinite(ratio.values),
                             ratio.values > 1.0, reg_trend)

            situation = is_sun23 & fall & heavy
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "mean short-direction 12-bar excess return over coin drift, Sunday 23:00 signals (forecast <= -2)"
    thr = "confirm: t >= 2 with slope on forecast size > 0; reject: t <= -2; otherwise inconclusive; at least 30 cases"
    reading = ("Situation bars are those starting Sunday 23:00 UTC with a negative raw weekend_fall value (else negative 48-bar return) "
               "and a recomputed 48/120-bar volume ratio above 1 (regime 'trending' where it cannot be recomputed); "
               "the excess is -(r12 - coin drift), drift being the coin's mean 12-bar return on the 0,12,24,... grid of all its windows; "
               "cases are deduplicated to the first per coin and ISO week, those without 12 later bars in the window are dropped, "
               "and the slope is on |forecast|.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement) if agreement is not None else None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are Sunday 23:00 bars after a weekend fall "
                           "on heavier-than-weekday volume with a short forecast."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    excess_all = []
    size_all = []
    for coin, wins in bars.items():
        # coin drift: mean 12-bar return on non-overlapping grid of all windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                a, b = c[i], c[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        seen = set()
        cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            c = pd.to_numeric(df["close"], errors="coerce").values
            idx = np.where(np.isfinite(fc) & (fc <= -2))[0]
            for i in idx:
                cases.append((ts.iloc[i], i, fc[i], c, w))
        cases.sort(key=lambda x: x[0])
        for t0, i, f, c, w in cases:
            iso = t0.isocalendar()
            key = (int(iso[0]), int(iso[1]))
            if key in seen:
                continue
            seen.add(key)
            if i + H >= len(c):
                continue
            a, b = c[i], c[i + H]
            if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                continue
            r = b / a - 1.0
            excess_all.append(-(r - drift))
            size_all.append(abs(float(f)))

    x = np.array(excess_all, dtype=float)
    s = np.array(size_all, dtype=float)
    n = int(len(x))

    mean_ex = float(np.mean(x)) if n > 0 else None
    t = None
    if n >= 2:
        sd = float(np.std(x, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n))) if sd > 0 else None
    slope = None
    if n >= 3 and np.std(s) > 0:
        slope = float(stats.linregress(s, x).slope)
    slope_pass = (slope > 0) if slope is not None else None

    if n < 30:
        status = "not observable"
        decided = f"Only {n} cases over all coins and windows, below the plan's minimum of 30."
    elif t is not None and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean short-direction excess return is positive with t >= 2 and the slope on the forecast's size is above 0."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "Mean short-direction excess return has t <= -2: Monday's first 12 hours rise beyond the coin's drift."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on the forecast's size is at or below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "ordinary t of the mean", "value": t} if t is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "least-squares slope of short-direction excess return on |forecast|",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": {"cases over all coins and windows": n},
        "decided_by": decided,
        "reading": reading,
    }
