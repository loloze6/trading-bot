import numpy as np
import pandas as pd


def measure(bars):
    H = 48
    FC = "forecast"
    WM = "debug_info.components.weekend_move.last_history_value"
    TR = "debug_info.components.trend30d.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_checked = 0
    n_agree = 0
    n_unverifiable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close = df["close"].astype(float).to_numpy()
            vol = df["volume"].astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).to_numpy()

            # The bar whose next bar starts Monday 00:00 UTC is the Sunday 23:00 bar.
            is_time = ((ts.dt.dayofweek == 6) & (ts.dt.hour == 23)).to_numpy()

            # Volume ratio: mean of the last 48 bars against the mean of the 120 bars before them.
            short_mean = vol.rolling(48, min_periods=48).mean()
            prior_mean = vol.shift(48).rolling(120, min_periods=120).mean()
            vr = (short_mean / prior_mean).to_numpy()

            # Weekend 48-bar return: recorded raw component sign if present, else from prices.
            ret48 = np.full(len(df), np.nan)
            if len(df) > H:
                ret48[H:] = close[H:] / close[:-H] - 1.0
            wm = pd.to_numeric(df[WM], errors="coerce").to_numpy() if WM in df.columns else np.full(len(df), np.nan)
            wk = np.where(np.isfinite(wm), wm, ret48)
            tr = pd.to_numeric(df[TR], errors="coerce").to_numpy() if TR in df.columns else np.full(len(df), np.nan)

            active = fc != 0
            for i in np.where(active)[0]:
                n_active += 1
                if not (np.isfinite(vr[i]) and np.isfinite(wk[i]) and np.isfinite(tr[i])):
                    n_unverifiable += 1
                    continue
                n_checked += 1
                s_wk = np.sign(wk[i])
                sit = bool(is_time[i]) and vr[i] >= 1.0 and s_wk != 0 and np.sign(tr[i]) == s_wk
                if sit and np.sign(fc[i]) == s_wk:
                    n_agree += 1

    agreement = float(n_agree / n_checked) if n_checked > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading_base = ("Situation bar = bar starting Sunday 23:00 UTC with volume ratio (mean of last 48 bars over the mean of "
                    "the 120 before) >= 1 and weekend-return sign equal to the recorded trend30d sign, expected side = "
                    "weekend move sign; active bars whose values cannot be computed are left out of the agreement; "
                    "the 'fewer than 100 cases' rule is applied as 'not observable'; top/bottom half pool all cases "
                    "ranked by |forecast| (middle case dropped if odd).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean signed unusual 48-bar move per case", "value": None,
                             "statistic": None, "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars checked": int(n_checked),
                       "active bars unverifiable": int(n_unverifiable)},
            "decided_by": ("Fewer than 90% of the forecast bars are Sunday 23:00 heavy-volume weekends with the trend aligned "
                           "and the forecast on the weekend move's side." if agreement is not None
                           else "No active bar could be checked against the plan's situation."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    case_vals = []
    case_absf = []
    for coin, wins in bars.items():
        # normal 48-bar drift: non-overlapping grid of every window of the coin
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).to_numpy()
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.extend(r[np.isfinite(r)].tolist())
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).to_numpy()
            for i in np.where(fc != 0)[0]:
                if i + H >= len(c):
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                case_vals.append(np.sign(fc[i]) * (r - drift))
                case_absf.append(abs(fc[i]))

    vals = np.array(case_vals, dtype=float)
    absf = np.array(case_absf, dtype=float)
    n = len(vals)

    mean = float(np.mean(vals)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(vals, ddof=1))
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    sup_val, sup_pass, top_mean, bot_mean = None, None, None, None
    if n >= 2:
        order = np.argsort(-absf, kind="mergesort")
        half = n // 2
        top = vals[order[:half]]
        bot = vals[order[n - half:]]
        top_mean, bot_mean = float(np.mean(top)), float(np.mean(bot))
        sup_val = top_mean - bot_mean
        sup_pass = bool(sup_val > 0)

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases over all coins and windows, fewer than the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean cannot be computed (zero dispersion), so neither rule is met."
    elif mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean signed unusual move is positive with t >= 2 and the top half of |forecast| beats the bottom half."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean signed unusual move is negative with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (top half above bottom half) fails."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean signed unusual 48-bar move per case",
                         "value": mean,
                         "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
                         "threshold": "mean > 0 with t >= 2 (and check passes) to confirm; mean < 0 with t <= -2 to reject"},
        "supporting_check": {"name": "top-half minus bottom-half |forecast| mean unusual move",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"cases": int(n)},
        "decided_by": decided,
        "reading": reading_base,
    }
