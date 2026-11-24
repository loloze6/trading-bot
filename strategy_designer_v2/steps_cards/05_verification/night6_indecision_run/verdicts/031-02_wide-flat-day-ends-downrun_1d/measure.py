import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    RR_COL = "debug_info.components.range_ratio.last_history_value"
    FL_COL = "debug_info.components.flatness.last_history_value"
    eps = 1e-9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_undetermined = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            o = df["open"].astype(float).values
            h = df["high"].astype(float).values
            l = df["low"].astype(float).values
            c = df["close"].astype(float).values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            rng = h - l
            # range over its 20-bar mean bar range (current bar included, exclude_current 0)
            rr_calc = rng / pd.Series(rng).rolling(20, min_periods=20).mean().values
            rr_rec = (pd.to_numeric(df[RR_COL], errors="coerce").values
                      if RR_COL in df.columns else np.full(len(df), np.nan))
            rr = np.where(np.isfinite(rr_rec), rr_rec, rr_calc)
            with np.errstate(divide="ignore", invalid="ignore"):
                fl_calc = np.where(rng > 0, 1.0 - np.abs(c - o) / rng, np.nan)
            fl_rec = (pd.to_numeric(df[FL_COL], errors="coerce").values
                      if FL_COL in df.columns else np.full(len(df), np.nan))
            fl = np.where(np.isfinite(fl_rec), fl_rec, fl_calc)
            c_lag = pd.Series(c).shift(5).values
            fall = c < c_lag
            for i in range(len(df)):
                if f[i] == 0:
                    continue
                if not (np.isfinite(c_lag[i]) and np.isfinite(rr[i]) and np.isfinite(fl[i])):
                    n_undetermined += 1
                    continue
                n_active += 1
                in_sit = bool(fall[i]) and rr[i] >= 1.0 - eps and fl[i] >= 0.9 - eps
                if in_sit and f[i] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading_sit = ("Situation checked from prices within each window (close below its close 5 bars earlier, "
                   "range over the 20-bar mean range including the current bar >= 1.0, flatness 1-|close-open|/range >= 0.9, "
                   "recorded component values used where present), active bars whose 5-bar or 20-bar history lies before "
                   "the window's first recorded bar left out of the share")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual 5-day move per long case", "value": None,
                             "statistic": None, "threshold": "t >= 2 (confirm) / t <= -2 (reject), at least 30 cases"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars undetermined": int(n_undetermined)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on days after a 5-day fall "
                           "with range at least its 20-day mean and body at most 10% of the range."
                           if n_active > 0 else "No active bar could be checked against the plan's situation."),
            "reading": reading_sit + ".",
        }

    # ---------- 2. criterion ----------
    case_moves = []
    case_days = []
    for coin, wins in bars.items():
        # normal 5-day drift: non-overlapping grid returns over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            floor = 0.0
            prev = 0.0
            used_cells = set()
            for i in range(len(df)):
                fi = f[i]
                bet = False
                if fi <= 0:
                    floor = 0.0
                else:
                    if prev <= 0:
                        floor = 0.0
                    if fi - floor >= BAND - eps:
                        bet = True
                        floor = fi
                    else:
                        floor = min(floor, fi)
                prev = fi
                if not bet:
                    continue
                cell = i // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if i + H >= len(c) or not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] <= 0:
                    continue
                r = c[i + H] / c[i] - 1.0
                case_moves.append(r - drift)
                case_days.append(ts.iloc[i].normalize())

    n = len(case_moves)
    x = np.array(case_moves, dtype=float)
    days = pd.Series(case_days)
    n_days = int(days.nunique()) if n > 0 else 0
    mean = float(x.mean()) if n > 0 else None
    t = None
    if n > 1 and n_days > 1:
        dev = pd.Series(x - x.mean())
        s = dev.groupby(days.values).sum().values
        var = (s ** 2).sum() / (n ** 2) * (n_days / (n_days - 1))
        if var > 0:
            t = float(mean / np.sqrt(var))

    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 cases"
    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 30 cases."
    elif t is not None and mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 over at least 30 cases (confirm rule)."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 over at least 30 cases (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 over at least 30 cases (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean unusual 5-day move per long case",
                         "value": mean,
                         "statistic": ({"name": "t of the mean, cases of one day clustered", "value": t}
                                       if t is not None else None),
                         "threshold": threshold},
        "supporting_check": None,
        "counts": {"cases": int(n), "days": n_days},
        "decided_by": decided,
        "reading": (reading_sit + "; a case is the first long bet (forecast rise >= 2 from its lowest long level since "
                    "the last bet, from 0 after flat) in each 5-bar cell counted from each window's first row, the "
                    "drift is the coin's mean non-overlapping 5-bar return over all its windows, and the day-clustered "
                    "standard error sums deviations per UTC day with a G/(G-1) small-sample factor."),
    }
