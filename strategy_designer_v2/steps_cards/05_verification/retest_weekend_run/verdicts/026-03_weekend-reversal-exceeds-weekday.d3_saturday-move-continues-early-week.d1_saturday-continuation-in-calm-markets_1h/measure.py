import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    FC = "forecast"
    RAW = "debug_info.components.sat_move.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.reset_index(drop=True)
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            act = fc != 0
            if not act.any():
                continue
            close_by_ts = pd.Series(pd.to_numeric(d["close"], errors="coerce").values,
                                    index=d["timestamp"])
            close_by_ts = close_by_ts[~close_by_ts.index.duplicated()]
            raw = (pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns
                   else pd.Series(np.nan, index=d.index))
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            for i in np.where(act.values)[0]:
                n_active += 1
                ts = d.at[i, "timestamp"]
                # decision bar: the bar starting Sunday 23:00 UTC (its close is Monday 00:00)
                if not (ts.dayofweek == 6 and ts.hour == 23):
                    continue
                # volatility gate: detector's decision (its components are not recorded)
                if regime.iat[i] != "trending":
                    continue
                # Saturday's return: close at Sunday 00:00 over close at Saturday 00:00
                c1 = close_by_ts.get(ts - pd.Timedelta(hours=24), np.nan)
                c0 = close_by_ts.get(ts - pd.Timedelta(hours=48), np.nan)
                if np.isfinite(c1) and np.isfinite(c0) and c0 > 0:
                    sat = c1 / c0 - 1.0
                else:
                    sat = raw.iat[i]
                if not np.isfinite(sat) or sat == 0:
                    continue
                if np.sign(sat) == np.sign(fc.iat[i]):
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("The situation bar is the bar whose start timestamp is Sunday 23:00 UTC, the calm-volatility gate is "
               "read from the recorded regime ('trending') because the detector's 8760-bar volatility ratio is not "
               "recorded and cannot be rebuilt inside a window, Saturday's move is close(Sun 00:00)/close(Sat 00:00)-1 "
               "by timestamp (sat_move raw value sign if a bar is missing); cases are pooled over all coins and windows, "
               "the drift is each coin's mean 48-bar return on the 0,48,96,... grid of all its windows, and the "
               "supporting split puts abs(forecast) above the median in the upper half and the rest in the lower half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Sunday 23:00 bars in the calm "
                           "regime with the forecast on the side of Saturday's move, so the config does not do what "
                           "the plan's Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    f_all, r_all = [], []
    for coin, wins in bars.items():
        grid = []
        cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            n = len(close)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = close[H:] / close[:n - H] - 1.0
            g = fwd[0:n:H]
            grid.extend(list(g[np.isfinite(g)]))
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).values
            idx = np.where(fc != 0)[0]
            for i in idx:
                if np.isfinite(fwd[i]):
                    cases.append((fc[i], fwd[i]))
        if len(grid) == 0:
            continue
        drift = float(np.mean(grid))
        for f, r in cases:
            f_all.append(f)
            r_all.append(r - drift)

    f_all = np.array(f_all, dtype=float)
    r_all = np.array(r_all, dtype=float)
    n_cases = int(len(f_all))

    mean = tval = None
    if n_cases >= 2:
        x = (f_all / 10.0) * r_all
        mean = float(np.mean(x))
        sd = float(np.std(x, ddof=1))
        tval = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
    elif n_cases == 1:
        mean = float((f_all[0] / 10.0) * r_all[0])

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        med = np.median(np.abs(f_all))
        dirret = np.sign(f_all) * r_all
        up = dirret[np.abs(f_all) > med]
        lo = dirret[np.abs(f_all) <= med]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {
        "name": "mean of (forecast/10) x de-drifted 48-bar return",
        "value": mean,
        "statistic": {"name": "t of the mean", "value": tval} if tval is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 over at least 100 cases; reject: mean < 0 with t <= -2 over at least 100 cases",
    }
    support = {"name": "upper-half minus lower-half mean directional de-drifted return (split at median abs forecast)",
               "value": sup_val, "passed": sup_pass}
    counts = {"cases": n_cases}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 100."
    elif tval is not None and mean > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The main mean is positive with t >= 2 over at least 100 cases and the supporting check is positive."
        else:
            status = "inconclusive"
            decided = "A t >= 2 whose supporting check is not positive."
    elif tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The main mean is negative with t <= -2 over at least 100 cases."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
