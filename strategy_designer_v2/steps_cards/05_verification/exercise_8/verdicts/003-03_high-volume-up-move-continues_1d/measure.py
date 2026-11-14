import numpy as np
import pandas as pd


def measure(bars):
    MOVE_COL = "debug_info.components.move.last_history_value"

    # ---------- gather per-window data (no cross-window returns) ----------
    all_next_returns = []
    active_rows = []          # (forecast, next_return) for active bars with a valid next return
    sit_total = 0             # active bars where the situation can be determined
    sit_agree = 0             # of those, bars in the situation on the long side

    for coin, windows in bars.items():
        for wname, df in windows.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            volume = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            # one-bar rise: raw component value, falling back on the close-to-close change
            if MOVE_COL in df.columns:
                move = pd.to_numeric(df[MOVE_COL], errors="coerce")
                move = move.where(move.notna(), close.pct_change())
            else:
                move = close.pct_change()

            # volume regime: volume at or above its 20-bar mean (mean includes the current bar)
            vol_mean = volume.rolling(20, min_periods=20).mean()
            vol_on = volume >= vol_mean * (1 - 1e-12)
            vol_known = vol_mean.notna() & volume.notna()

            nxt = close.shift(-1) / close - 1.0   # inside this window only

            # situation check
            active = fc.notna() & (fc != 0)
            known = active & vol_known & move.notna()
            in_sit = known & vol_on & (move > 0) & (fc > 0)
            sit_total += int(known.sum())
            sit_agree += int(in_sit.sum())

            # returns for the criterion (horizon 1: every bar is its own non-overlapping return)
            all_next_returns.extend(nxt.dropna().tolist())
            m = active & nxt.notna()
            for f, r in zip(fc[m].tolist(), nxt[m].tolist()):
                active_rows.append((float(f), float(r)))

    agreement = (sit_agree / sit_total) if sit_total > 0 else None
    passed = agreement is not None and agreement >= 0.90

    threshold_txt = ("confirm if forecast-weighted mean excess next-bar return > 0 with t >= 2; "
                     "reject if < 0 with t <= -2; otherwise, or with fewer than 60 active bars, inconclusive")
    main_name = "forecast-weighted mean next-bar return on active bars minus mean next-bar return over all bars"

    reading = ("Volume regime taken as volume >= its 20-bar rolling mean computed within each window including the current bar "
               "(active bars without 20 bars of window history are left out of the agreement share); the drift is the mean "
               "next-bar return over all bars of all windows pooled; the t-statistic of the weighted mean uses the weighted "
               "standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w); the top and bottom fifths are the floor(n/5) active "
               "bars with the highest and lowest forecasts.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(len(active_rows))},
            "decided_by": ("Fewer than 90% of active bars are long positions on up bars with volume at or above its "
                           "20-bar mean, so the config does not trade the plan's situation and side."),
            "reading": reading,
        }

    drift = float(np.mean(all_next_returns)) if all_next_returns else np.nan
    n = len(active_rows)
    w = np.array([a[0] for a in active_rows], dtype=float)
    r = np.array([a[1] for a in active_rows], dtype=float)
    x = r - drift

    value = None
    tstat = None
    if n >= 2 and np.sum(w) != 0:
        wsum = np.sum(w)
        m = float(np.sum(w * x) / wsum)
        se = np.sqrt(n / (n - 1) * np.sum(w ** 2 * (x - m) ** 2)) / abs(wsum)
        value = m
        tstat = float(m / se) if se > 0 else None
    elif n == 1 and np.sum(w) != 0:
        value = float(np.sum(w * x) / np.sum(w))

    # supporting check: top fifth vs bottom fifth by forecast
    sup_val = None
    sup_pass = None
    k = n // 5
    top_mean = bot_mean = None
    if k >= 1:
        order = np.argsort(w, kind="mergesort")
        bot_mean = float(np.mean(x[order[:k]]))
        top_mean = float(np.mean(x[order[-k:]]))
        sup_val = top_mean - bot_mean
        sup_pass = bool(top_mean > 0 and top_mean > bot_mean)

    # decision
    if n < 60:
        status = "inconclusive"
        decided_by = "Fewer than 60 active bars across the 6 windows, which the plan calls inconclusive."
    elif value is None or tstat is None:
        status = "inconclusive"
        decided_by = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif value > 0 and tstat >= 2:
        status = "confirmed"
        decided_by = "The forecast-weighted mean excess next-bar return is above 0 with a t-statistic of 2 or more."
    elif value < 0 and tstat <= -2:
        status = "rejected"
        decided_by = "The forecast-weighted mean excess next-bar return is below 0 with a t-statistic of -2 or less."
    else:
        status = "inconclusive"
        decided_by = "The t-statistic lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": None if value is None else float(value),
            "statistic": None if tstat is None else {"name": "t of the forecast-weighted mean", "value": float(tstat)},
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "top-fifth minus bottom-fifth mean next-bar excess return (top must be > 0 and > bottom)",
            "value": None if sup_val is None else float(sup_val),
            "passed": sup_pass,
        },
        "counts": {"active bars": int(n), "bars per fifth": int(k)},
        "decided_by": decided_by,
        "reading": reading,
    }
