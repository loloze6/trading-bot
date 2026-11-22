import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.vol_move.last_history_value"

    # ---------- 1. Situation check: an up hour (rise x relative volume > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Where the raw value is not recorded, its sign is the sign of the hour's return
            # (the volume ratio is positive).
            raw_pos = np.where(raw.notna(), raw > 0, ret1 > 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (fc > 0) & pd.Series(raw_pos, index=df.index)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 24-bar move over the cases (bets of the forecast)"
    main_thr = "confirm: mean > 0 with t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2"
    sup_name = "mean unusual move of cases above the median forecast minus that of cases at or below it"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": int(n_active)},
            "decided_by": ("The plan's situation is an up hour (positive return x relative volume) taken long, "
                           "but fewer than 90% of the bars with a non-zero forecast are positive-forecast bars "
                           "on a positive raw value."),
            "reading": "Situation bars are bars whose recorded raw component value is above 0 (sign of the hour's return where missing), on the long side.",
        }

    # ---------- 2. Criterion ----------
    case_moves = []
    case_fc = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 24-bar returns on each window's grid, all windows together
        grid_rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for p in range(0, n - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(fc)
            # bets: a rise of the long forecast of at least the band from its lowest level since the last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    bet[i] = True
                    ref = f
                else:
                    ref = min(ref, f)
            # once per 24-bar grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                i = start + int(idx[0])
                if i + H >= n:
                    continue
                a, b = close[i], close[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                case_moves.append((b / a - 1.0) - drift)
                case_fc.append(fc[i])

    moves = np.asarray(case_moves, dtype=float)
    fcs = np.asarray(case_fc, dtype=float)
    n_cases = int(len(moves))

    mean = float(np.mean(moves)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(moves, ddof=1))
        t = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_hi = n_lo = 0
    if n_cases > 1:
        med = float(np.median(fcs))
        hi = moves[fcs > med]
        lo = moves[fcs <= med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"cases": n_cases, "cases above median forecast": n_hi, "cases at or below median forecast": n_lo}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than {MIN_CASES} cases across both coins and all windows ({n_cases})."
    elif t is not None and mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2, and the larger-forecast half beats the smaller half."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2."
    elif t is not None and mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "A confirming t with a failed supporting check is inconclusive."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first bet (long forecast rise >= 2 points from its lowest level since the last bet, "
                    "reset at 0) in each 24-bar grid cell of a window, with its 24-bar return needing to stay inside the window; "
                    "the median split puts cases with forecast above the median in the larger half and the rest in the smaller; "
                    "the plan's 'fewer than 30 cases' rule is applied as the minimum count giving 'not observable'."),
    }
