import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    PERIOD = 20
    FAIL_WINDOW = 3
    RAW = "debug_info.components.failed_break.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            high = df["high"].astype(float)
            low = df["low"].astype(float)
            fc = df["forecast"].astype(float)
            raw = df[RAW].astype(float) if RAW in df.columns else pd.Series(np.nan, index=df.index)

            # price-based failed breakout: a bar of the last few closed above the prior 20-bar high,
            # and the current close is below the low of the most recent such bar
            prior_high = high.shift(1).rolling(PERIOD, min_periods=PERIOD).max()
            is_break = (close > prior_high).fillna(False).values
            cl = close.values
            lo = low.values
            price_fail = np.zeros(len(df), dtype=bool)
            for t in range(len(df)):
                for k in range(0, FAIL_WINDOW + 1):  # most recent breakout bar among t-3..t
                    j = t - k
                    if j < 0:
                        break
                    if is_break[j]:
                        price_fail[t] = cl[t] < lo[j]
                        break
            raw_fail = (raw > 0).fillna(False).values
            situation = raw_fail | price_fail

            active = (fc != 0) & fc.notna()
            a = active.values
            n_active += int(a.sum())
            n_agree += int((a & situation & (fc.values < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    situation_check = {"agreement": agreement, "passed": bool(passed)}

    main_name = "mean short-side unusual 5-bar move after a short bet"
    threshold = "t >= 2 over at least 30 cases (confirm, with Spearman > 0); t <= -2 over at least 30 cases (reject)"
    reading = ("A short bet is a fall of the forecast of at least 2 points below its least negative level on the short "
               "side since the last bet (reset to 0 after a flat or a long), taking the first such bar in each 5-bar "
               "grid cell counted from each window's first row; the drift is the mean of each coin's non-overlapping "
               "5-bar returns at grid positions 0, 5, 10, ... of all its windows; the situation holds where the raw "
               "component value is positive or a close lies below the low of the most recent of the last bars that "
               "closed above the prior 20-bar high.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the active bars are bars of a failed breakout (close below the breakout "
                           "bar's low) with a short forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    unusual = []
    absf = []
    for coin, wins in bars.items():
        # normal drift: non-overlapping 5-bar returns over all windows
        drift_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    drift_rets.append(c[p + H] / c[p] - 1)
        if len(drift_rets) == 0:
            continue
        drift = float(np.mean(drift_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            ref = 0.0
            bet = np.zeros(len(f), dtype=bool)
            for t in range(len(f)):
                ft = f[t]
                if not np.isfinite(ft):
                    continue
                if ft >= 0:
                    ref = 0.0
                    continue
                if ft <= ref - BAND:
                    bet[t] = True
                    ref = ft
                else:
                    ref = max(ref, ft)
            for start in range(0, len(f), H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= len(c):
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1
                unusual.append(-(r - drift))
                absf.append(abs(f[t]))

    n = len(unusual)
    counts = {"cases": int(n)}
    mean_u = float(np.mean(unusual)) if n > 0 else None
    t_stat = None
    if n >= 2:
        sd = float(np.std(unusual, ddof=1))
        t_stat = float(mean_u / (sd / np.sqrt(n))) if sd > 0 else None
    rho = None
    if n >= 3:
        r_, _ = stats.spearmanr(absf, unusual)
        rho = float(r_) if np.isfinite(r_) else None
    sup_pass = None if rho is None else bool(rho > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": threshold}
    supporting = {"name": "Spearman of |forecast| vs short-side unusual move", "value": rho, "passed": sup_pass}

    if n < 30:
        status = "not observable"
        decided = f"Only {n} cases across all coins and windows, below the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean short-side unusual move has t >= 2 over at least 30 cases and the Spearman correlation is above 0."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The mean short-side unusual move has t <= -2 over at least 30 cases: the coin rises more than its drift after the failure."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 over at least 30 cases but the supporting correlation is at or below 0."
    else:
        status = "inconclusive"
        decided = "The t of the mean short-side unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
