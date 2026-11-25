import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.scaled_fall.last_history_value"

    def wkey(w):
        try:
            return int(str(w).lstrip("w"))
        except Exception:
            return 10 ** 9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin], key=wkey):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            raw = (pd.to_numeric(df[RAW], errors="coerce").to_numpy(float)
                   if RAW in df.columns else np.full(len(df), np.nan))
            ret7 = np.full(len(df), np.nan)
            if len(df) > 7:
                ret7[7:] = close[7:] / close[:-7] - 1.0
            for i in range(len(df)):
                if not np.isfinite(f[i]) or f[i] == 0:
                    continue
                n_active += 1
                val = raw[i] if np.isfinite(raw[i]) else ret7[i]
                if np.isfinite(val) and val < 0 and f[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 5-bar move in the short direction, before costs"
    main_thr = "confirm: mean > 0 with t >= 2 (and slope > 0); reject: mean < 0 with t <= -2"
    sup_name = "OLS slope of short-direction unusual 5-bar return on abs(forecast), grid bars with forecast < 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars after a 7-bar fall "
                           "(negative raw scaled return), so the config does not trade the plan's situation."),
            "reading": "none",
        }

    # ---------- 2. drift per coin (non-overlapping 5-bar grid, all windows) ----------
    drift = {}
    for coin in bars:
        rets = []
        for w in bars[coin]:
            close = pd.to_numeric(bars[coin][w]["close"], errors="coerce").to_numpy(float)
            for p in range(0, len(close) - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases and supporting-check samples ----------
    case_vals, case_days = [], []
    sx, sy = [], []
    for coin in sorted(bars):
        d = drift[coin]
        for w in sorted(bars[coin], key=wkey):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

            # bets on the short side
            bets = np.zeros(n, dtype=bool)
            base = 0.0
            prev_short = False
            for i in range(n):
                if f[i] < 0:
                    mag = -f[i]
                    if not prev_short:
                        base = 0.0
                    if mag - base >= BAND:
                        bets[i] = True
                        base = mag
                    else:
                        base = min(base, mag)
                    prev_short = True
                else:
                    prev_short = False
                    base = 0.0

            # one case per grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bets[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n or not np.isfinite(d):
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r) or pd.isna(ts.iloc[i]):
                    continue
                case_vals.append(-(r - d))
                case_days.append(ts.iloc[i].strftime("%Y-%m-%d"))

            # supporting: grid bars with forecast < 0
            for p in range(0, n - H, H):
                if f[p] < 0 and np.isfinite(d):
                    r = close[p + H] / close[p] - 1.0
                    if np.isfinite(r):
                        sx.append(abs(f[p]))
                        sy.append(-(r - d))

    n_cases = len(case_vals)
    n_days = len(set(case_days))

    mean_u = float(np.mean(case_vals)) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        x = np.asarray(case_vals, float)
        dev = pd.Series(x - x.mean()).groupby(pd.Series(case_days)).sum().to_numpy()
        D = len(dev)
        var = (dev ** 2).sum() * D / (D - 1) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(x.mean() / se) if se > 0 else None

    slope = None
    if len(sx) >= 3 and np.ptp(sx) > 0:
        slope = float(stats.linregress(sx, sy).slope)
    sup_pass = None if slope is None else bool(slope > 0)

    counts = {"cases": int(n_cases), "distinct days": int(n_days), "supporting grid bars": int(len(sx))}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases and {n_days} distinct days, "
                   "the plan needs at least 30 of each.")
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed (zero spread), so neither rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean short-direction unusual move above 0 with t >= 2 and supporting slope above 0: confirm rule."
        else:
            status = "inconclusive"
            decided = "Confirming t but the supporting slope is at or below 0 (or not computable): inconclusive rule."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean short-direction unusual move below 0 with t <= -2: reject rule (the falls partly reverse)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2: inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day summed together",
                                                     "value": t_val},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": slope, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first short bet (rise of abs(forecast) of at least 2 points from its lowest short "
                    "level since the last bet) in each 5-bar grid cell of a window, measured from that bar's close "
                    "over 5 bars, with drift the coin's mean non-overlapping 5-bar grid return over all windows; the "
                    "situation is a negative raw scaled 7-bar return (price 7-bar return where the raw value is "
                    "missing) on a short forecast, the calm profile being the code's regime gate."),
    }
