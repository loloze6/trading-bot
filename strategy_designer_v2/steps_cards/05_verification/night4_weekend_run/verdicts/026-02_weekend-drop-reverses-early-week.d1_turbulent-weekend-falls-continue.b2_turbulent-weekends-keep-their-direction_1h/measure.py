import numpy as np
import pandas as pd


def measure(bars):
    H = 48
    BAND = 2.0
    RAW = "debug_info.components.wkend.last_history_value"

    n_active = 0
    n_agree = 0
    case_rows = []  # (unusual move, |forecast|)

    for coin, windows in bars.items():
        # coin's normal 48-bar drift: non-overlapping grid 0, H, 2H, ... per window, all windows together
        grid_rets = []
        prepared = {}
        for w, df in windows.items():
            d = df.reset_index(drop=True).copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            prepared[w] = d
            c = d["close"].to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        drift = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

        for w, d in prepared.items():
            ts = d["ts"]
            close = d["close"].to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            raw = (pd.to_numeric(d[RAW], errors="coerce").to_numpy(dtype=float)
                   if RAW in d.columns else np.full(len(d), np.nan))
            nxt = ts + pd.Timedelta(hours=1)
            is_sit = ((nxt.dt.weekday == 0) & (nxt.dt.hour == 0)).to_numpy()

            # weekend return from prices, as a fallback for the side when the raw value is missing
            close_by_ts = pd.Series(close, index=ts)
            close_by_ts = close_by_ts[~close_by_ts.index.duplicated()]

            for i in range(len(d)):
                if fc[i] == 0:
                    continue
                n_active += 1
                if not is_sit[i]:
                    continue
                side_val = raw[i]
                if not np.isfinite(side_val):
                    t0 = ts.iloc[i] - pd.Timedelta(hours=H)
                    if t0 in close_by_ts.index and close_by_ts[t0] != 0:
                        side_val = close[i] / close_by_ts[t0] - 1.0
                    else:
                        side_val = np.nan
                if np.isfinite(side_val) and side_val != 0 and np.sign(side_val) == np.sign(fc[i]):
                    n_agree += 1

            # cases: bets (|forecast| >= band, risen from 0) on the Monday 00:00 bar
            for i in np.where(is_sit & (np.abs(fc) >= BAND))[0]:
                if i + H >= len(d):
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H])) or close[i] == 0:
                    continue
                if not np.isfinite(drift):
                    continue
                r = close[i + H] / close[i] - 1.0
                case_rows.append(((r - drift) * np.sign(fc[i]), abs(fc[i])))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    reading = ("Cases are the Monday 00:00 bars (stamped Sunday 23:00) with |forecast| >= the 2-point band, "
               "i.e. the workflow's bets; returns are positional close[t+48]/close[t]-1 inside the window; the "
               "normal drift is the coin's mean 48-bar return on the 0,48,96,... grid of all its windows; cases at "
               "exactly the median |forecast| are left out of both halves; the plan's 'fewer than 100 cases' "
               "minimum is treated as 'not observable'.")

    main_name = "mean drift-adjusted 48-bar move signed by forecast (Monday bets)"
    thr = "confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": int(len(case_rows))},
            "decided_by": ("Fewer than 90% of active bars are Monday 00:00 bars whose forecast sign matches "
                           "the weekend return's sign."),
            "reading": reading,
        }

    n = len(case_rows)
    um = np.array([c[0] for c in case_rows], dtype=float)
    af = np.array([c[1] for c in case_rows], dtype=float)

    mean = float(np.mean(um)) if n > 0 else None
    if n > 1 and np.std(um, ddof=1) > 0:
        t = float(np.mean(um) / (np.std(um, ddof=1) / np.sqrt(n)))
    else:
        t = None

    diff = None
    check_pass = None
    if n > 0:
        med = float(np.median(af))
        above = um[af > med]
        below = um[af < med]
        if len(above) > 0 and len(below) > 0:
            diff = float(np.mean(above) - np.mean(below))
            check_pass = bool(diff > 0)

    counts = {"cases": int(n)}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases across all coins and windows, fewer than the plan's minimum of 100."
    elif t is None or mean is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither rule is met."
    elif mean > 0 and t >= 2 and check_pass is True:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the above-minus-below-median difference is > 0."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 (the weekend move reversed)."
    elif mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean unusual move above minus below median |forecast|",
            "value": diff,
            "passed": check_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
