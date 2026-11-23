import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    RAW = "debug_info.components.sunday_rev.last_history_value"

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = _ts(df)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # price fallback: 24-bar return, inside the window
            ret24 = np.full(len(df), np.nan)
            if len(df) > 24:
                ret24[24:] = close[24:] / close[:-24] - 1.0
            is_sun_last = ((ts.dt.dayofweek == 6) & (ts.dt.hour == 23)).values
            active = np.isfinite(fc) & (fc != 0)
            for i in np.where(active)[0]:
                n_active += 1
                move = raw[i] if np.isfinite(raw[i]) else ret24[i]
                if not is_sun_last[i] or not np.isfinite(move) or move == 0:
                    continue
                if np.sign(fc[i]) == -np.sign(move):
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the slope of 48-bar excess return on the forecast, pooled"
    threshold = "confirm if t >= +2 and mean signed unusual move > 0; reject if t <= -2; inconclusive otherwise"
    reading = ("Sunday's last bar is the bar starting Sunday 23:00 UTC (its close ends Sunday); Sunday's move is the sign "
               "of the component's raw value (24-bar price return where it is missing); a case is such a bar with a "
               "nonzero forecast and a 48-bar forward return inside its window; the normal drift is the coin's mean "
               "48-bar return on the non-overlapping grid of all its windows; the slope t is the ordinary OLS t.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing active bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are Sunday-close bars with the forecast against "
                           "Sunday's 24-hour move, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    per_coin = {}
    for coin, wins in bars.items():
        # normal drift: non-overlapping 48-bar returns over all windows
        grid = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid.extend(r[np.isfinite(r)].tolist())
        drift = float(np.mean(grid)) if grid else np.nan
        cnt = 0
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = _ts(df)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            is_sun_last = ((ts.dt.dayofweek == 6) & (ts.dt.hour == 23)).values
            for i in np.where(is_sun_last & np.isfinite(fc) & (fc != 0))[0]:
                if i + H >= len(c) or not np.isfinite(drift):
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                xs.append(float(fc[i]))
                ys.append(float(r - drift))
                cnt += 1
        per_coin[coin] = cnt

    xs = np.array(xs)
    ys = np.array(ys)
    n = len(xs)
    counts = {"cases in total": int(n)}
    for coin, cnt in per_coin.items():
        counts[f"cases {coin}"] = int(cnt)

    slope = None
    tval = None
    if n >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr > 0 else None
    signed = np.sign(xs) * ys if n > 0 else np.array([])
    mean_signed = float(np.mean(signed)) if n > 0 else None
    supp_pass = (mean_signed > 0) if mean_signed is not None else None

    main = {"name": main_name, "value": tval,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": threshold}
    supp = {"name": "mean signed unusual move over the cases, before costs",
            "value": mean_signed, "passed": supp_pass}

    low = [c for c, k in per_coin.items() if k < 30]
    if n < 300 or low or tval is None:
        status = "not observable"
        if n < 300:
            decided = f"The minimum of 300 cases in total is not reached ({n})."
        elif low:
            decided = f"The minimum of 30 cases per coin is not reached for {', '.join(low)}."
        else:
            decided = "The slope's t cannot be computed on the cases."
    elif tval >= 2 and supp_pass:
        status = "confirmed"
        decided = "The slope's t is +2 or more and the mean signed unusual move is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: moves follow Sunday's direction in proportion to the forecast."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is +2 or more but the mean signed unusual move is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is strictly between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
