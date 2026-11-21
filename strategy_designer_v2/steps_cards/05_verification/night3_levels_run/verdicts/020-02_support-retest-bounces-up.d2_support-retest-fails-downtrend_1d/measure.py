import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND_BET = 2.0
    TOUCH_COL = "debug_info.components.touch_s.last_history_value"
    RET_COL = "debug_info.components.fall90.last_history_value"

    def _num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        return np.full(len(df), np.nan)

    def _ret90_from_prices(close):
        n = len(close)
        out = np.full(n, np.nan)
        if n > 90:
            out[90:] = close[90:] / close[:-90] - 1.0
        return out

    def _touch_from_prices(close, low, period=90, side=2, band=1.5, fall=5):
        # Fallback only for bars where the recorded raw value is missing:
        # positive when the close fell over `fall` bars and sits within `band` %
        # of at least one confirmed swing low of the last `period` bars.
        n = len(close)
        out = np.full(n, np.nan)
        swing = np.zeros(n, dtype=bool)
        for i in range(side, n - side):
            nb = np.r_[low[i - side:i], low[i + 1:i + side + 1]]
            if np.all(np.isfinite(nb)) and np.isfinite(low[i]) and np.all(low[i] < nb):
                swing[i] = True
        for t in range(n):
            if t < fall or t < period:
                continue
            if not (close[t] < close[t - fall]):
                out[t] = 0.0
                continue
            lo, hi = t - period, t - side
            cnt = 0.0
            for i in range(max(lo, 0), hi + 1):
                if swing[i] and low[i] > 0:
                    d = abs(close[t] - low[i]) / low[i] * 100.0
                    if d <= band:
                        cnt += 1.0 - d / band
            out[t] = cnt
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            low = pd.to_numeric(df["low"], errors="coerce").to_numpy(dtype=float)
            touch = _num(df, TOUCH_COL)
            ret = _num(df, RET_COL)
            active = np.isfinite(f) & (f != 0)
            if not active.any():
                continue
            if np.any(active & ~np.isfinite(ret)):
                rp = _ret90_from_prices(close)
                ret = np.where(np.isfinite(ret), ret, rp)
            if np.any(active & ~np.isfinite(touch)):
                tp = _touch_from_prices(close, low)
                touch = np.where(np.isfinite(touch), touch, tp)
            sit = np.isfinite(ret) & np.isfinite(touch) & (ret < 0) & (touch > 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (f < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "mean signed (short) excess 5-bar return at grid bars where a short bet starts"
    thr = "confirm: mean > 0 with t >= 2 and supporting check > 0; reject: t <= -2; fewer than 30 cases inconclusive"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": ("Fewer than 90 % of the active bars are short bars where the 90-day return is "
                           "below 0 and the swing-low touch nearness is above 0, as the plan's situation requires."
                           if n_active > 0 else "The forecast is never active, so no bar shows the plan's situation."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    # coin's mean 5-bar return over all windows (non-overlapping grid)
    coin_mean = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for t in range(0, len(close) - H, H):
                r = close[t + H] / close[t] - 1.0
                if np.isfinite(r):
                    rs.append(r)
        coin_mean[coin] = float(np.mean(rs)) if rs else np.nan

    vals, mags = [], []
    for coin, wins in bars.items():
        mu = coin_mean.get(coin, np.nan)
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for t in range(n):
                ft = f[t]
                if not np.isfinite(ft) or ft >= 0:
                    ref = 0.0
                    continue
                mag = -ft
                if mag - ref >= BAND_BET:
                    bet[t] = True
                    ref = mag
                else:
                    ref = min(ref, mag)
            for t in range(0, n - H, H):
                if not bet[t]:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                vals.append(-(r - mu))
                mags.append(abs(f[t]))

    vals = np.asarray(vals, dtype=float)
    mags = np.asarray(mags, dtype=float)
    n_cases = int(len(vals))

    mean_v = float(np.mean(vals)) if n_cases > 0 else None
    t_v = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        t_v = float(mean_v / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    n_hi = n_lo = 0
    if n_cases >= 2:
        med = float(np.median(mags))
        hi = vals[mags > med]
        lo = vals[mags <= med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    reading = ("Cases are the bars at positions 0, 5, 10, ... of each window on which a short bet starts "
               "(a fall of the forecast of at least 2 points below its least-negative level since the last bet, "
               "reset at flat), the excess is against the coin's mean 5-bar grid return over all its windows, and "
               "the median split puts cases with |forecast| above the median in the larger half and the rest in the smaller.")

    counts = {"cases": n_cases, "larger-forecast half": n_hi, "smaller-forecast half": n_lo,
              "active bars": int(n_active)}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, below the plan's minimum of 30."
    elif t_v is None:
        status = "inconclusive"
        decided = "The t of the mean signed excess fall cannot be computed (no spread), so it meets neither rule."
    elif mean_v > 0 and t_v >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean signed excess fall is above 0 with t >= 2 and the larger-forecast half falls more than the smaller half."
    elif t_v <= -2:
        status = "rejected"
        decided = "The mean signed excess fall has t <= -2: the price rises more than usual after the cases."
    elif t_v >= 2:
        status = "inconclusive"
        decided = "The main measure has t >= 2 but the supporting check is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean signed excess fall lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_v,
                         "statistic": ({"name": "t of the mean", "value": t_v} if t_v is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean signed excess fall, larger |forecast| half minus smaller half",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
