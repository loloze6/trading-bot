import numpy as np
import pandas as pd


def _to_dt(s):
    if pd.api.types.is_numeric_dtype(s):
        v = pd.to_numeric(s, errors="coerce")
        med = float(np.nanmedian(np.abs(v.values))) if len(v) else 0.0
        unit = "s"
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True, errors="coerce")


def measure(bars):
    H = 2
    MIN_CASES = 200
    RAW = "debug_info.components.weekend_move.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ts = _to_dt(df["timestamp"])
            ret_prices = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                ret = raw.where(raw.notna(), ret_prices)
            else:
                ret = ret_prices
            # Sunday bar (bar opening Sunday UTC): its close is read when the coming bar is Monday
            is_sunday = (ts.dt.dayofweek == 6).values
            active = (fc != 0).values
            expected_sign = -np.sign(ret.values)
            on_side = np.sign(fc.values) == expected_sign
            situ = is_sunday & on_side & np.isfinite(ret.values) & (ret.values != 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast x drift-adjusted 2-bar return over Sunday-close cases"
    threshold = "confirm: mean > 0 with t >= 2 over >= 200 cases and size check passes; reject: mean < 0 with t <= -2 over >= 200 cases"
    reading = ("The situation is a bar opening on Sunday UTC with forecast sign opposite to its 1-day return (raw value, or close-to-close if missing); "
               "cases need a 2-bar return inside the window; each coin's drift is the mean of its non-overlapping 2-bar returns on a grid from each window's first row; "
               "thirds are formed by sorting cases by |forecast| (stable order, ties by position) and splitting into three near-equal groups; "
               "the size check compares the mean of sign(forecast) x drift-adjusted return, largest third minus smallest third.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are Sunday-close bars with a forecast against "
                           "the Sunday 1-day move, so the config does not do what the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_fc = []
    case_r = []
    case_coin = []
    drift = {}
    for coin in sorted(bars):
        grid_rets = []
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            n = len(close)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            reg = df["regime"].astype(str).values
            n = len(df)
            for i in range(n):
                if reg[i] != "mean_reversion" or not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r) or not np.isfinite(drift[coin]):
                    continue
                case_fc.append(fc[i])
                case_r.append(r - drift[coin])
                case_coin.append(coin)

    case_fc = np.array(case_fc, dtype=float)
    case_r = np.array(case_r, dtype=float)
    n_cases = int(len(case_fc))

    mean_prod = None
    t_val = None
    if n_cases >= 2:
        prod = case_fc * case_r
        mean_prod = float(np.mean(prod))
        sd = float(np.std(prod, ddof=1))
        t_val = float(mean_prod / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
    elif n_cases == 1:
        mean_prod = float(case_fc[0] * case_r[0])

    sup_value = None
    sup_passed = None
    n_small = n_large = 0
    if n_cases >= 3:
        order = np.argsort(np.abs(case_fc), kind="mergesort")
        thirds = np.array_split(order, 3)
        dirret = np.sign(case_fc) * case_r
        small = dirret[thirds[0]]
        large = dirret[thirds[2]]
        n_small, n_large = int(len(small)), int(len(large))
        sup_value = float(np.mean(large) - np.mean(small))
        sup_passed = bool(sup_value > 0)

    counts = {"cases": n_cases, "smallest third cases": n_small, "largest third cases": n_large}
    stat = {"name": "t of the mean", "value": t_val} if t_val is not None else None
    supporting = {"name": "largest third minus smallest third, mean drift-adjusted 2-bar return in forecast direction",
                  "value": sup_value, "passed": sup_passed}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 200 cases."
    elif mean_prod is not None and t_val is not None and mean_prod > 0 and t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = "The mean forecast-weighted drift-adjusted 2-bar return is positive with t >= 2 over at least 200 cases and the size check passes."
    elif mean_prod is not None and t_val is not None and mean_prod < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean forecast-weighted drift-adjusted 2-bar return is negative with t <= -2 over at least 200 cases: weekend moves continue."
    elif t_val is not None and t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the size check (largest third above smallest third) fails, which the plan rules inconclusive."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2, which the plan rules inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_prod, "statistic": stat, "threshold": threshold},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
