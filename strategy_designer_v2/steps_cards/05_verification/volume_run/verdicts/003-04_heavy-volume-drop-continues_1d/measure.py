import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    MIN_EVENTS = 30
    TOL = 1e-9
    FALL_COL = "debug_info.components.fall_size.last_history_value"
    VOL_COL = "debug_info.components.volume_weight.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            volume = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            # Recomputed values from prices (fallback where components are not recorded)
            ret1 = close.pct_change()
            vol20 = ret1.rolling(20, min_periods=20).std()
            fall_re = ret1 / vol20
            vratio_re = volume / volume.rolling(30, min_periods=30).mean()

            if FALL_COL in df.columns:
                fall = pd.to_numeric(df[FALL_COL], errors="coerce").combine_first(fall_re)
            else:
                fall = fall_re
            if VOL_COL in df.columns:
                vratio = pd.to_numeric(df[VOL_COL], errors="coerce").combine_first(vratio_re)
            else:
                vratio = vratio_re

            active = fc != 0
            situation = (fall <= -2.0 + TOL) & (vratio >= 1.5 - TOL)
            agree = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess 5-bar return after signal bars (vs holding the coin)"
    threshold = "confirm: mean < 0 with t <= -2 over >= 30 independent events; reject: mean > 0 with t >= +2 over >= 30"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with a one-day fall "
                           "of at least 2 usual moves on volume at least 1.5 times its 30-day mean"
                           if n_active > 0 else "No bar has a non-zero forecast, so the situation cannot be matched"),
            "reading": "Situation taken as fall <= -2 and volume ratio >= 1.5 on a short forecast, from the recorded "
                       "last_history_value columns, recomputed from prices where missing.",
        }

    # ---------- 2. Coin mean 5-bar return over all windows (non-overlapping grid) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a != 0:
                    rs.append(b / a - 1.0)
        coin_mean[coin] = float(np.mean(rs)) if rs else np.nan

    # ---------- 3. Events ----------
    ex_list, fc_list = [], []
    for coin, wins in bars.items():
        mu = coin_mean.get(coin, np.nan)
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            last_kept = None
            for p in range(len(c)):
                if not (np.isfinite(fc[p]) and fc[p] < 0):
                    continue
                if p + H >= len(c):
                    continue
                a, b = c[p], c[p + H]
                if not (np.isfinite(a) and np.isfinite(b) and a != 0):
                    continue
                if last_kept is not None and p - last_kept < H:
                    continue
                last_kept = p
                ex_list.append(b / a - 1.0 - mu)
                fc_list.append(fc[p])

    ex = np.array(ex_list, dtype=float)
    fcs = np.array(fc_list, dtype=float)
    n = len(ex)

    mean_ex = float(np.mean(ex)) if n > 0 else None
    t_stat = None
    if n > 1:
        sd = float(np.std(ex, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n)))

    # ---------- 4. Supporting check ----------
    diff = None
    check_passed = None
    if n >= 2:
        order = np.argsort(fcs, kind="mergesort")
        k = n // 2
        neg_half = ex[order[:k]]
        other_half = ex[order[k:]]
        if len(neg_half) > 0 and len(other_half) > 0:
            diff = float(np.mean(neg_half) - np.mean(other_half))
            check_passed = bool(diff < 0)

    # ---------- 5. Decision ----------
    if n < MIN_EVENTS:
        status = "not observable"
        decided_by = f"Only {n} independent events, fewer than the plan's minimum of 30."
    elif t_stat is not None and mean_ex < 0 and t_stat <= -2:
        if check_passed:
            status = "confirmed"
            decided_by = "Mean excess 5-bar return is negative with t <= -2 over at least 30 events, and the more negative forecast half falls more."
        else:
            status = "inconclusive"
            decided_by = "Confirming t <= -2 over at least 30 events, but the supporting check fails."
    elif t_stat is not None and mean_ex > 0 and t_stat >= 2:
        status = "rejected"
        decided_by = "Mean excess 5-bar return is positive with t >= +2 over at least 30 events."
    else:
        status = "inconclusive"
        decided_by = "t lies between -2 and +2 over at least 30 events."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t_stat} if t_stat is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess of more-negative-forecast half minus other half (< 0)",
            "value": diff,
            "passed": check_passed,
        },
        "counts": {"independent events": int(n)},
        "decided_by": decided_by,
        "reading": ("A signal is kept when at least 5 bars after the previous kept one in its window (so 5-bar "
                    "returns do not overlap) and only if close[t+5] exists in the window; the coin's mean is over "
                    "non-overlapping 5-bar returns on positions 0,5,10,... of all its windows; the median split "
                    "puts the floor(n/2) most negative forecasts (stable sort) in the more-negative half."),
    }
