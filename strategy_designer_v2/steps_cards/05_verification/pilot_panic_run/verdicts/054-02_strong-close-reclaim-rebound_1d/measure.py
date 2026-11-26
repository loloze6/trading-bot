import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    PERIOD = 30

    def get_reclaim_raw(df):
        col = "debug_info.components.reclaim.last_history_value"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        out = np.full(len(df), np.nan)
        if "debug_info.components" in df.columns:
            for i, cell in enumerate(df["debug_info.components"].to_numpy()):
                c = cell
                if isinstance(c, str):
                    try:
                        c = json.loads(c)
                    except Exception:
                        c = None
                if isinstance(c, dict):
                    r = c.get("reclaim")
                    if isinstance(r, dict):
                        v = r.get("last_history_value")
                        try:
                            out[i] = float(v)
                        except Exception:
                            pass
        return out

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            hi = df["high"].to_numpy(float)
            lo = df["low"].to_numpy(float)
            cl = df["close"].to_numpy(float)
            reg = df["regime"].astype(str).to_numpy()
            v = get_reclaim_raw(df)
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                profile_ok = reg[i] == "mean_reversion"  # no profile veto fired, pierce rule chose it
                rng = hi[i] - lo[i]
                tol = 1e-9 * abs(cl[i])
                pierce = False
                if np.isfinite(v[i]) and rng > 0:
                    low30 = cl[i] - v[i] * rng
                    pierce = (lo[i] < low30 - tol) and (cl[i] >= low30 - tol)
                elif i >= PERIOD:
                    low30 = np.nanmin(lo[i - PERIOD:i])
                    pierce = (lo[i] < low30 - tol) and (cl[i] >= low30 - tol)
                if profile_ok and pierce and fc[i] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean excess 5-bar return of cases over the coin's falling-agitated 5-bar mean"
    thr = "confirm: mean > 0 with t >= 2 (and upper half beats lower half); reject: mean < 0 with t <= -2; at least 30 cases"
    reading = ("Falling agitated bars are taken as bars whose regime is not 'chop' (the profile vetoes set chop), the pierce "
               "is rebuilt from the reclaim raw value (low30 = close - value x range, low < low30 <= close) or from prices "
               "when not recorded, a case is the first long bet (forecast rise >= 2 from its lowest level since the last bet, "
               "from 0 after a flat) in each 5-bar grid cell of a window, the day-clustered t uses deviations summed per day "
               "with a D/(D-1) correction, and the median split puts forecasts above the median in the upper half and the rest "
               "in the lower half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are falling-agitated pierce-and-reclaim days of the prior "
                           "30-day low with a long forecast, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- baseline per coin ----------
    baseline = {}
    for coin in bars:
        rets = []
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            cl = df["close"].to_numpy(float)
            reg = df["regime"].astype(str).to_numpy()
            for t in range(0, len(df) - H, H):
                if reg[t] != "chop" and np.isfinite(cl[t]) and np.isfinite(cl[t + H]) and cl[t] > 0:
                    rets.append(cl[t + H] / cl[t] - 1.0)
        baseline[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    cases = []  # (day, excess, forecast)
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            cl = df["close"].to_numpy(float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            ref = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                bet = False
                if f <= 0:
                    ref = 0.0
                else:
                    if f - ref >= BAND:
                        bet = True
                        ref = f
                    else:
                        ref = min(ref, f)
                if not bet:
                    continue
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= n:
                    continue
                if not (np.isfinite(cl[t]) and np.isfinite(cl[t + H]) and cl[t] > 0):
                    continue
                b = baseline.get(coin, np.nan)
                if not np.isfinite(b):
                    continue
                r = cl[t + H] / cl[t] - 1.0
                cases.append((ts.iloc[t].floor("D"), r - b, float(f)))

    n_cases = len(cases)
    mean_ex = None
    tval = None
    n_days = 0
    if n_cases > 0:
        ex = np.array([c[1] for c in cases])
        days = pd.Series([c[0] for c in cases])
        mean_ex = float(ex.mean())
        dev = pd.Series(ex - mean_ex).groupby(days.values).sum()
        n_days = int(len(dev))
        if n_days > 1:
            var = (dev.values ** 2).sum() * n_days / (n_days - 1) / (n_cases ** 2)
            se = np.sqrt(var)
            if se > 0:
                tval = float(mean_ex / se)

    diff = None
    sc_passed = None
    if n_cases > 0:
        fv = np.array([c[2] for c in cases])
        ex = np.array([c[1] for c in cases])
        med = np.median(fv)
        up = ex[fv > med]
        dn = ex[fv <= med]
        if len(up) > 0 and len(dn) > 0:
            diff = float(up.mean() - dn.mean())
            sc_passed = bool(diff > 0)
        else:
            sc_passed = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, below the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the mean excess return could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and tval >= 2 and sc_passed:
        status = "confirmed"
        decided = "The mean excess return is positive with t >= 2, the upper half beats the lower half, with at least 30 cases."
    elif mean_ex < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean excess return is negative with t <= -2, with at least 30 cases."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the upper half does not beat the lower half."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": tval}
                          if tval is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "upper-half minus lower-half mean excess return (median forecast split)",
            "value": diff,
            "passed": sc_passed,
        },
        "counts": {"cases": int(n_cases), "days": int(n_days)},
        "decided_by": decided,
        "reading": reading,
    }
