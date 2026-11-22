import numpy as np
import pandas as pd


def measure(bars):
    H = 48
    BAND = 2.0
    LHV = "debug_info.components.weekend_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close_time = ts + pd.Timedelta(hours=1)  # 1h bars: close = start + 1h
            d["_monday_close"] = ((close_time.dt.dayofweek == 0) &
                                  (close_time.dt.hour == 0) &
                                  (close_time.dt.minute == 0)).values
            c = d["close"].astype(float).values
            # weekend 48-bar return: recorded raw value, else from prices inside the window
            price_ret = np.full(len(d), np.nan)
            if len(d) > H:
                price_ret[H:] = c[H:] / c[:-H] - 1.0
            if LHV in d.columns:
                raw = pd.to_numeric(d[LHV], errors="coerce").values
                wret = np.where(np.isnan(raw), price_ret, raw)
            else:
                wret = price_ret
            d["_wret"] = wret
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            d["_f"] = f
            prepared[coin][w] = d

            active = f != 0
            n_active += int(active.sum())
            situ = d["_monday_close"].values & (wret < 0) & (f < 0)
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The Monday signal bar is the bar whose close (start + 1h) is Monday 00:00 UTC; the volatility-rank "
               "condition is not rechecked because a 4380-bar rank cannot be rebuilt inside the recorded windows; a "
               "case is a Monday signal bar with forecast <= -2 (a short bet of at least the 2-point band), one per "
               "48-bar grid cell of its window, with the coin's drift the mean of its non-overlapping 48-bar returns "
               "over all windows; the supporting check splits cases at the median absolute forecast pooled over all "
               "coins.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean short-direction 48-bar move beyond drift", "value": None,
                             "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject, over >= 100 cases"},
            "supporting_check": None,
            "counts": {"cases": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars closing at Monday 00:00 "
                           "UTC after a weekend fall, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    moves = []
    sizes = []
    for coin, wins in prepared.items():
        # normal drift: mean of non-overlapping 48-bar returns over all windows
        grid_rets = []
        for w, d in wins.items():
            c = d["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.extend(r[np.isfinite(r)].tolist())
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, d in wins.items():
            c = d["close"].astype(float).values
            f = d["_f"].values
            sig = np.where(d["_monday_close"].values & (f <= -BAND))[0]
            used_cells = set()
            for t in sig:
                if t + H >= len(c):
                    continue
                cell = t // H
                if cell in used_cells:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                used_cells.add(cell)
                moves.append(-(r - drift))
                sizes.append(abs(f[t]))

    moves = np.array(moves, dtype=float)
    sizes = np.array(sizes, dtype=float)
    n = int(len(moves))

    mean_move = float(np.mean(moves)) if n > 0 else None
    if n > 1 and np.std(moves, ddof=1) > 0:
        t_stat = float(np.mean(moves) / (np.std(moves, ddof=1) / np.sqrt(n)))
    else:
        t_stat = None

    sup_val = None
    sup_pass = None
    n_hi = n_lo = 0
    if n > 0:
        med = float(np.median(sizes))
        hi = moves[sizes >= med]
        lo = moves[sizes < med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": "mean short-direction 48-bar move beyond the coin's drift",
            "value": mean_move,
            "statistic": {"name": "t of the mean", "value": t_stat} if t_stat is not None else None,
            "threshold": "t >= 2 to confirm, t <= -2 to reject, over at least 100 cases"}
    sup = {"name": "mean move of cases at/above median forecast size minus below median",
           "value": sup_val, "passed": sup_pass}
    counts = {"cases": n, "cases at or above median size": n_hi, "cases below median size": n_lo}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 100."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (no dispersion), so neither confirm nor reject is met."
    elif t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: t >= 2 over at least 100 cases and larger falls are followed by larger moves."
    elif t_stat <= -2:
        status = "rejected"
        decided = "Reject: t <= -2 over at least 100 cases, weekend falls are followed by rises beyond drift."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "Inconclusive: t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
