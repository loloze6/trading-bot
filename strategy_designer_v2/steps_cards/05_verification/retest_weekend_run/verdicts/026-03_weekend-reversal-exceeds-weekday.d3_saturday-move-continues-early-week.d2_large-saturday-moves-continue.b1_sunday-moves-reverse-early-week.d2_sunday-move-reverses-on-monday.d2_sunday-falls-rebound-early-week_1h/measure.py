import numpy as np
import pandas as pd


def measure(bars):
    H = 48
    RAW = "debug_info.components.sunday_fall_vol.last_history_value"
    MIN_CASES = 100

    def to_ts(s):
        if np.issubdtype(s.dtype, np.number):
            v = s.dropna()
            unit = "ms" if (len(v) and v.abs().max() > 1e11) else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    n_active = 0
    n_agree = 0
    case_rows = []  # (forecast, excess)

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # the coin's normal 48h drift: non-overlapping 48h returns on all windows
        drift_samples = []
        prepared = {}
        for w in sorted(wins.keys()):
            df = wins[w].copy().reset_index(drop=True)
            if len(df) == 0:
                continue
            df["_ts"] = to_ts(df["timestamp"])
            close = df["close"].astype(float).values
            n = len(close)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    drift_samples.append(c1 / c0 - 1.0)
            prepared[w] = df
        drift = float(np.mean(drift_samples)) if drift_samples else np.nan

        for w, df in prepared.items():
            close = df["close"].astype(float).values
            n = len(close)
            fc = df["forecast"].astype(float).values
            ts = df["_ts"]
            # Sunday-close bar: the bar starting Sunday 23:00 UTC (its close ends Sunday)
            sunday_close = ((ts.dt.dayofweek == 6) & (ts.dt.hour == 23)).values
            # Sunday's 24h move: raw component value, else recomputed from prices
            raw = df[RAW].astype(float).values if RAW in df.columns else np.full(n, np.nan)
            ret24 = np.full(n, np.nan)
            if n > 24:
                ret24[24:] = close[24:] / close[:-24] - 1.0
            move = np.where(np.isfinite(raw), raw, ret24)
            fell = np.isfinite(move) & (move < 0)

            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & sunday_close & fell & (fc > 0)).sum())

            # cases: Sunday-close bars with forecast >= 2
            for i in np.where(sunday_close & np.isfinite(fc) & (fc >= 2))[0]:
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0 and np.isfinite(drift)):
                    continue
                case_rows.append((float(fc[i]), float(c1 / c0 - 1.0 - drift)))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "mean excess 48h return after Sunday-close bars with forecast >= 2"
    threshold = "t >= 2 confirms (with correlation > 0); t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": len(case_rows), "active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Sunday 23:00 UTC bars after a "
                           "falling Sunday with a long forecast, so the config does not trade the plan's situation."),
            "reading": ("The Sunday-close bar is the bar starting Sunday 23:00 UTC; a fall is a negative raw "
                        "component value (or a negative 24h price return where it is not recorded)."),
        }

    n_cases = len(case_rows)
    mean_ex = None
    t = None
    corr = None
    if n_cases >= 1:
        f = np.array([r[0] for r in case_rows])
        x = np.array([r[1] for r in case_rows])
        mean_ex = float(np.mean(x))
        if n_cases >= 2:
            sd = float(np.std(x, ddof=1))
            t = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None
            if np.std(f) > 0 and np.std(x) > 0:
                corr = float(np.corrcoef(f, x)[0, 1])

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, fewer than the plan's minimum of 100."
        sc_passed = None if corr is None else bool(corr > 0)
    else:
        sc_passed = None if corr is None else bool(corr > 0)
        if t is not None and t >= 2 and sc_passed:
            status = "confirmed"
            decided = "The mean excess 48h return has t >= 2 and the correlation is above 0 (confirm rule)."
        elif t is not None and t <= -2:
            status = "rejected"
            decided = "The mean excess 48h return has t <= -2 (reject rule)."
        elif t is not None and t >= 2:
            status = "inconclusive"
            decided = "t >= 2 but the correlation is at or below 0, which the plan calls inconclusive."
        else:
            status = "inconclusive"
            decided = "The t of the mean excess 48h return is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t is None else {"name": "ordinary t of the mean", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "correlation of forecast with 48h excess return over the cases",
            "value": corr,
            "passed": sc_passed,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": ("The Sunday-close bar is the bar starting Sunday 23:00 UTC, the 48h return is close 48 rows "
                    "later in the same window, the drift is the coin's mean over 48-row non-overlapping stretches "
                    "from each window's first row, and the correlation is Pearson's."),
    }
