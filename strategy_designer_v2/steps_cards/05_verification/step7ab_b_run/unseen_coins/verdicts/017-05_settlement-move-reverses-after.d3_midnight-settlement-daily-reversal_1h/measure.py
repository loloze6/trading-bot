import numpy as np
import pandas as pd
from scipy import stats


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0
        unit = "ns" if med > 1e17 else ("us" if med > 1e14 else ("ms" if med > 1e11 else "s"))
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 24
    RAW = "debug_info.components.pre_settle_move.last_history_value"

    n_active = 0
    n_agree = 0
    case_rows = []  # (coin, forecast, fwd_return)
    coin_grid_returns = {}

    for coin in sorted(bars.keys()):
        grid_all = []
        for w in sorted(bars[coin].keys(), key=lambda x: (len(str(x)), str(x))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = _to_utc(df["timestamp"]).reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float).reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float)

            # Situation: bar whose close is 00:00 UTC (bar starts at 23:00 UTC)
            close_time = ts + pd.Timedelta(hours=1)
            situ = (close_time.dt.hour == 0) & (close_time.dt.minute == 0)

            # Raw component value (2-bar vol-scaled return); fall back to price 2-bar return
            ret2 = close / close.shift(2) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").astype(float).reset_index(drop=True)
                raw = raw.where(raw.notna() & (raw != 0), ret2)
            else:
                raw = ret2
            expected_sign = -np.sign(raw.fillna(0.0))

            active = fc != 0
            agree = active & situ & (np.sign(fc) == expected_sign) & (expected_sign != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            fwd = close.shift(-H) / close - 1.0

            # coin's mean 24-bar return: non-overlapping grid 0, 24, 48, ... per window
            grid_idx = np.arange(0, len(df), H)
            g = fwd.iloc[grid_idx].dropna()
            grid_all.extend(g.tolist())

            sel = situ & active & fwd.notna()
            for i in np.where(sel.values)[0]:
                case_rows.append((coin, float(fc.iloc[i]), float(fwd.iloc[i])))
        coin_grid_returns[coin] = grid_all

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    threshold = "slope > 0 with t >= 2 confirms (with check); slope < 0 with t <= -2 rejects"
    mm_name = "OLS slope of 24-bar excess return on forecast, settlement bars pooled"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": "Fewer than 90% of non-zero forecast bars are 00:00 UTC settlement bars with a forecast opposite to the 2-bar pre-settlement move.",
            "reading": "Settlement bar = bar starting 23:00 UTC (closing 00:00 UTC); expected side = opposite the sign of the raw 2-bar vol-scaled return.",
        }

    coin_mean = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in coin_grid_returns.items()}
    f = np.array([r[1] for r in case_rows], dtype=float)
    ex = np.array([r[2] - coin_mean[r[0]] for r in case_rows], dtype=float)
    ok = np.isfinite(f) & np.isfinite(ex)
    f, ex = f[ok], ex[ok]
    n_cases = int(len(f))

    reading = ("Cases are settlement bars (start 23:00 UTC, close 00:00 UTC) with non-zero forecast and a full 24-bar "
               "forward return in-window; coin mean 24-bar return from the non-overlapping 0,24,48,... grid of all its "
               "windows; thirds are floor(n/3) cases each by |forecast| (stable sort); slope t = slope / its OLS standard error.")

    slope = None
    tval = None
    sup_val = None
    sup_pass = None
    if n_cases >= 3 and np.std(f) > 0:
        lr = stats.linregress(f, ex)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr > 0 else (float(np.sign(lr.slope)) * np.inf)
        k = n_cases // 3
        if k > 0:
            order = np.argsort(np.abs(f), kind="mergesort")
            signed = np.sign(f) * ex
            sup_val = float(np.mean(signed[order[-k:]]) - np.mean(signed[order[:k]]))
            sup_pass = bool(sup_val > 0)

    counts = {"settlement cases with a non-zero forecast": n_cases}

    if n_cases < 500:
        status = "not observable"
        decided = f"Only {n_cases} settlement cases with a non-zero forecast, fewer than the 500 required."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope could not be estimated (no variation in the forecast)."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the top-minus-bottom third check is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the top-minus-bottom third check fails."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": mm_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "forecast-signed excess, top third minus bottom third by |forecast|",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
