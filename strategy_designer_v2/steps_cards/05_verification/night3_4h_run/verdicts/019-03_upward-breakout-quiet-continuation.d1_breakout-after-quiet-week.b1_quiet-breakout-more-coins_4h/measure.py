import numpy as np
import pandas as pd

RAW_COL = "debug_info.components.nr_break_quiet.last_history_value"
H = 18
BAND = 2.0
PERIOD = 12
MIN_CASES = 100


def _bets(fc):
    """Bet bars: a rise of the long forecast of at least BAND above its lowest
    level on the long side since the last bet (from 0 after a flat)."""
    out = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f <= 0:
            ref = 0.0
            continue
        if f - ref >= BAND:
            out[i] = True
            ref = f
        else:
            ref = min(ref, f)
    return out


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = df["close"].to_numpy(dtype=float)
            high = df["high"].to_numpy(dtype=float)
            prior_high = pd.Series(high).shift(1).rolling(PERIOD, min_periods=PERIOD).max().to_numpy()
            price_break = close > prior_high  # NaN prior high -> False
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            situ = np.where(np.isfinite(raw), raw > 0, price_break)
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "forecast-weighted mean unusual 18-bar move of cases"
    threshold = "confirm: positive with t >= 2 (and top-minus-bottom third > 0); reject: negative with t <= -2"
    supp_name = "mean unusual move of top third by forecast minus bottom third"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a close above "
                           "the prior 12-bar high (raw component value > 0), the plan's situation and side."),
            "reading": "The situation is read as a raw component value above 0 (or, where it is not recorded, a close above the prior 12-bar high) with a positive forecast.",
        }

    # ---------- 2. criterion ----------
    case_u = []
    case_f = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 18-bar returns over all windows of the coin
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].to_numpy(dtype=float)
            n = len(close)
            for s in range(0, n - H, H):
                r = close[s + H] / close[s] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            bet = _bets(fc)
            taken = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in taken:
                    continue
                taken.add(cell)
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r) and np.isfinite(fc[i]) and fc[i] > 0:
                    coin_cases.append((r, fc[i]))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for r, f in coin_cases:
            case_u.append(r - drift)
            case_f.append(f)

    u = np.asarray(case_u, dtype=float)
    f = np.asarray(case_f, dtype=float)
    n_cases = int(len(u))

    reading = ("A case is the first bet bar (a forecast rise of >= 2 points above its lowest long level since the "
               "last bet, from 0 after a flat) in each 18-bar grid cell of a window, with its full 18-bar return inside "
               "the window; the t of the forecast-weighted mean uses its weighted standard error "
               "sqrt(n/(n-1) * sum(w^2 (x - mean)^2)) / sum(w); thirds are floor(n/3) cases by forecast, unweighted means; "
               "the plan's 'at least 100 cases' minimum gives 'not observable' when not reached.")

    if n_cases < MIN_CASES:
        wm = float(np.sum(u * f) / np.sum(f)) if n_cases > 0 and np.sum(f) > 0 else None
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": wm, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": n_cases},
            "decided_by": f"Only {n_cases} cases, below the plan's minimum of 100 cases in total.",
            "reading": reading,
        }

    W = np.sum(f)
    wm = float(np.sum(u * f) / W)
    se = np.sqrt(n_cases / (n_cases - 1.0) * np.sum(f ** 2 * (u - wm) ** 2)) / W
    t = float(wm / se) if se > 0 else 0.0

    order = np.argsort(f, kind="mergesort")
    k = n_cases // 3
    bottom = u[order[:k]]
    top = u[order[-k:]]
    diff = float(np.mean(top) - np.mean(bottom)) if k > 0 else None
    supp_pass = bool(diff is not None and diff > 0)

    if wm > 0 and t >= 2 and supp_pass:
        status = "confirmed"
        decided = "The forecast-weighted mean unusual move is positive with t >= 2 and the top-minus-bottom-third difference is above 0."
    elif wm > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top-minus-bottom-third difference is at or below 0, which the plan calls inconclusive."
    elif wm < 0 and t <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": wm,
                         "statistic": {"name": "t of the weighted mean", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": supp_name, "value": diff, "passed": supp_pass},
        "counts": {"cases": n_cases, "cases per third": int(k)},
        "decided_by": decided,
        "reading": reading,
    }
