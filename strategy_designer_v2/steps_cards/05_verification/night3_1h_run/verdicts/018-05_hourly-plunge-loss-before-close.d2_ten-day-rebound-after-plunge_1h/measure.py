import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 240
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.drop_after_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(float)
            n = len(df)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(float)
            else:
                raw = np.full(n, np.nan)
            ret24 = np.full(n, np.nan)
            ret720 = np.full(n, np.nan)
            if n > 24:
                ret24[24:] = close[24:] / close[:-24] - 1.0
            if n > 720:
                ret720[720:] = close[720:] / close[:-720] - 1.0
            # situation: a fall over the last 24 bars after a positive 720-bar return
            raw_ok = np.isfinite(raw)
            price_ok = np.isfinite(ret24) & np.isfinite(ret720)
            sit_raw = raw_ok & (np.nan_to_num(raw) > 0)
            sit_price = price_ok & (np.nan_to_num(ret24) < 0) & (np.nan_to_num(ret720) > 0)
            situation = np.where(
                raw_ok & price_ok, sit_raw & sit_price,
                np.where(raw_ok, sit_raw, np.where(price_ok, sit_price, False)),
            )
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "t of the mean unusual 240-bar move after a long bet, pooled over coins"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and slope check passes; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("Situation = raw component > 0 and, where the window's prices allow, a negative 24-bar and positive 720-bar return; "
               "a bet is a rise of the positive forecast of >= 2 points from its lowest positive level since the last bet (from 0 at a window start or after a flat), "
               "the first bet of each 240-bar grid cell (counted from each window's first row) is the case; drift is the coin's mean non-overlapping 240-bar return over all its windows; "
               "the slope is an OLS of the unusual move on the signal bar's forecast; fewer than 30 cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "active_bars": int(n_active)},
            "decided_by": (f"Only {agreement:.3f} of the active bars are long bars of the plan's situation "
                           "(a 24-bar fall after a positive 720-bar return), below the 90 % required."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    unusual_all = []
    fc_all = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 240-bar returns over all windows
        drift_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            for p in range(0, len(close) - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    drift_rets.append(r)
        if len(drift_rets) == 0:
            continue
        drift = float(np.mean(drift_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(float)
            n = len(fc)
            base = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    base = 0.0
                    continue
                base = min(base, f)
                if f - base >= BAND:
                    base = f
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n:
                        r = close[t + H] / close[t] - 1.0
                        if np.isfinite(r):
                            unusual_all.append(r - drift)
                            fc_all.append(f)

    u = np.asarray(unusual_all, float)
    x = np.asarray(fc_all, float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_u = None
    if n_cases >= 2:
        sd = float(np.std(u, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    slope = None
    slope_t = None
    slope_pass = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, u)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
        slope_pass = bool(slope > 0 and slope_t is not None and slope_t >= 1.0)
    elif n_cases > 0:
        slope_pass = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, below the plan's minimum of 30."
    elif t_u is not None and mean_u > 0 and t_u >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 over at least 30 cases and the slope check passes."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the slope check fails."
    elif t_u is not None and mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_u is None else {"name": "t of the mean", "value": t_u},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "t of the OLS slope of unusual move on signal forecast (positive, t >= 1)",
            "value": slope_t,
            "passed": slope_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
