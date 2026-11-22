import numpy as np
import pandas as pd


def measure(bars):
    H = 6
    BAND = 2.0
    RAW = "debug_info.components.vol_surge_up.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ret1 = np.full(len(df), np.nan)
            if len(df) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # situation: a rising hour weighted by its volume ratio (raw product > 0);
            # where the raw value is not recorded, the hour's own rise from the prices
            situ = np.where(~np.isnan(raw), raw > 0, ret1 > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 6-bar move after a long bet (BTC and ETH pooled)"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on a "
                           "volume-weighted rising hour, as the plan's Fidelity requires"
                           if n_active > 0 else "The forecast is never non-zero, so no bar takes the plan's long side"),
            "reading": "Situation taken as a positive raw volume-weighted scaled return (a rising hour) with a positive forecast.",
        }

    # ---------- 2. criterion ----------
    unusual_all = []
    fc_all = []
    for coin, wins in bars.items():
        # coin's normal 6-bar drift: mean of non-overlapping grid returns over all windows
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            # long bets: rise of the forecast of >= band from its lowest level since the last bet
            low = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    low = f
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n:
                        r = close[t + H] / close[t] - 1.0
                        if np.isfinite(r):
                            coin_cases.append((r, f))
                else:
                    low = min(low, f)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for r, f in coin_cases:
            unusual_all.append(r - drift)
            fc_all.append(f)

    u = np.array(unusual_all, dtype=float)
    fcs = np.array(fc_all, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t_stat = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_top = n_bot = 0
    if n_cases > 1:
        med = float(np.median(fcs))
        top = u[fcs > med]
        bot = u[fcs <= med]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top > 0 and n_bot > 0:
            sup_val = float(np.mean(top) - np.mean(bot))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    reading = ("A case is the first long bet (forecast rise of >= 2 points from its lowest level since the last bet, "
               "from 0 after a flat) in each 6-bar grid cell counted from each window's first row, the drift is the "
               "coin's mean non-overlapping 6-bar return over all its windows, the supporting split puts cases above "
               "the median entry forecast in the top half and those at or below it in the bottom half, and fewer "
               "than 30 cases is read as the plan's minimum count, so not observable.")

    counts = {"cases in total": n_cases, "top half cases": n_top, "bottom half cases": n_bot}

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases in total ({n_cases}), the plan's minimum count."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither rule is met."
    elif mean_u > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is above 0 with t >= 2 and the top-minus-bottom half difference is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check (top half minus bottom half above 0) fails."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan reads as inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": {"name": "ordinary t of the mean", "value": t_stat} if t_stat is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean unusual move, top half minus bottom half by entry forecast",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
