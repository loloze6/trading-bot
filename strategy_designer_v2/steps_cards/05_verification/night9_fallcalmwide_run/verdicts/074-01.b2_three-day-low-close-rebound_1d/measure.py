import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    MIN_CASES = 30
    MIN_DAYS = 30

    def to_day(ts):
        s = pd.Series(ts)
        if np.issubdtype(s.dtype, np.number):
            v = float(s.dropna().iloc[0]) if s.notna().any() else 0.0
            unit = "ms" if v > 1e11 else "s"
            d = pd.to_datetime(s, unit=unit, utc=True)
        else:
            d = pd.to_datetime(s, utc=True)
        return d.dt.strftime("%Y-%m-%d").values

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    # ---------- criterion data ----------
    case_rows = []  # (coin, day, unusual, entry_forecast)
    drift = {}

    for coin, wins in bars.items():
        # normal 3-day drift: mean of non-overlapping 3-bar returns over all windows
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            o = df["close"].astype(float)
            hi = df["high"].astype(float)
            lo = df["low"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            regime = df["regime"].astype(str).values

            rng = hi - lo
            loc = ((hi - o) / rng.where(rng > 0)).values
            ret = o.pct_change()
            sd = ret.rolling(30, min_periods=30).std()
            width = ((rng / o) / sd.where(sd > 0)).values

            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                if fc[i] <= 0:
                    continue
                if not (regime[i] == "mean_reversion"):
                    continue
                if not (np.isfinite(loc[i]) and loc[i] >= 0.75 - 1e-9):
                    continue
                if np.isfinite(width[i]):
                    if width[i] < 2.0 - 1e-9:
                        continue
                n_agree += 1

            # bets: forecast rise >= band on its (long) side from its lowest level since last bet
            days = to_day(df["timestamp"])
            c = o.values
            base = 0.0
            bet = np.zeros(len(df), dtype=bool)
            for i in range(len(df)):
                f = fc[i]
                if f > 0:
                    if f - base >= BAND - 1e-12:
                        bet[i] = True
                        base = f
                    else:
                        base = min(base, f)
                else:
                    base = 0.0
            for start in range(0, len(df), H):
                idx = [j for j in range(start, min(start + H, len(df))) if bet[j]]
                if not idx:
                    continue
                j = idx[0]
                if j + H >= len(df):
                    continue
                if not (c[j] > 0 and np.isfinite(c[j + H])) or not np.isfinite(drift[coin]):
                    continue
                r = c[j + H] / c[j] - 1.0
                case_rows.append((coin, days[j], r - drift[coin], float(fc[j])))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean unusual 3-day move per long case (return minus coin's normal 3-day drift)"
    thr = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    reading = ("Situation bars are regime 'mean_reversion' (the detector's record, which carries the rising-calm "
               "vetoes that cannot be recomputed from 120-bar windows with a 365-bar lookback) with close location "
               "from the high >= 0.75 from prices and width >= 2 (range/close over the ddof-1 std of the last 30 "
               "in-window daily returns, where 30 returns exist) and a long forecast; a case is the first bet bar of "
               "each 3-bar grid cell counted from each window's first row; the t clusters cases by UTC day; the "
               "plan's 'fewer than 30 cases or days' is treated as a minimum count, hence 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "situation bars on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are long bars of the plan's situation (wide range >= 2 "
                           "usual moves, close in the bottom quarter, rising calm regime): the config's forecast does "
                           "not follow the Fidelity."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "u", "f"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["u"] - mean_u
        g = dev.groupby(cases["day"]).sum().values
        G = len(g)
        var = (G / (G - 1.0)) * np.sum(g ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_u / se) if se > 0 else None

    slope = None
    if n_cases >= 3 and cases["f"].nunique() >= 2:
        lr = stats.linregress(cases["f"].values, cases["u"].values)
        slope = float(lr.slope)
    slope_pass = None if slope is None else bool(slope > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, cases summed per day", "value": t_val},
            "threshold": thr}
    sup = {"name": "OLS slope of unusual move on entry forecast", "value": slope, "passed": slope_pass}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"The plan's minimum of 30 cases and 30 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed, so neither confirm nor reject applies."
    elif mean_u > 0 and t_val >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the slope on the entry forecast is above 0."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on the entry forecast is at or below 0 (or not computable): inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
