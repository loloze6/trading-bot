import numpy as np
import pandas as pd


def measure(bars):
    H = 2
    BAND = 2.0
    MIN_DAYS = 30
    LHV = "debug_info.components.rise_vol.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_active_checked = 0
    n_agree = 0
    n_active_unchecked_agree_partial = 0
    n_active_unchecked = 0

    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            ret1 = close.pct_change()
            sd20 = ret1.rolling(20, min_periods=20).std(ddof=1)
            sd60 = ret1.rolling(60, min_periods=60).std(ddof=1)
            vr = sd20 / sd60
            rise_px = close / close.shift(14) - 1.0
            if LHV in d.columns:
                lhv = pd.to_numeric(d[LHV], errors="coerce")
                rise_sign = np.where(lhv.notna(), np.sign(lhv), np.sign(rise_px))
            else:
                rise_sign = np.sign(rise_px)
            rise_sign = pd.Series(rise_sign, index=d.index)
            friday = d["ts"].dt.weekday == 4
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            d["fc"] = fc
            prepared[coin][w] = d

            active = fc != 0
            for i in np.where(active.values)[0]:
                n_active += 1
                side_ok = fc.iloc[i] > 0
                rise_ok = rise_sign.iloc[i] > 0
                fri_ok = bool(friday.iloc[i])
                v = vr.iloc[i]
                if pd.notna(v) and np.isfinite(v):
                    n_active_checked += 1
                    if side_ok and rise_ok and fri_ok and v > 1.0:
                        n_agree += 1
                else:
                    n_active_unchecked += 1
                    if side_ok and rise_ok and fri_ok:
                        n_active_unchecked_agree_partial += 1

    if n_active_checked > 0:
        agreement = n_agree / n_active_checked
    elif n_active_unchecked > 0:
        agreement = n_active_unchecked_agree_partial / n_active_unchecked
    else:
        agreement = None

    reading = ("Friday close = a bar whose UTC start time is a Friday (next bar Saturday); the volatility ratio is "
               "recomputed in each window as the 20-day over the 60-day std (ddof 1) of daily close returns and the "
               "agreement is taken over the active bars where it is computable (Friday, rise and side only if none is); "
               "the 14-day rise sign is read from rise_vol's raw value (positive ratio) or the 14-day price return; "
               "cases are long forecast rises of at least 2 points, once per 2-bar grid cell, with the 2-bar return "
               "inside the window, the drift is the mean non-overlapping 2-bar return over all the coin's windows, "
               "the t clusters cases by UTC day, the median split uses the forecast at the case bar, and the plan's "
               "'at least 30 days with cases' minimum gives 'not observable' when not reached.")

    main_name = "mean unusual 2-bar move (Fri close to Sun close) minus normal 2-day drift, per case"
    thr = "confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2"

    if agreement is None:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"days with cases": 0, "cases": 0},
            "decided_by": "No active forecast bars: fewer than the plan's minimum of 30 days with cases.",
            "reading": reading,
        }

    passed = agreement >= 0.90
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active forecast bars are long Friday closes with a 14-day rise and a "
                           "20/60-day volatility ratio above 1, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (day, coin, unusual, forecast)
    for coin, wins in prepared.items():
        # normal drift over all windows: non-overlapping 2-bar returns
        grid_rets = []
        for w, d in wins.items():
            c = d["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, d in wins.items():
            fc = d["fc"].values
            c = d["close"].astype(float).values
            n = len(d)
            low = 0.0
            prev_pos = False
            used_cells = set()
            for i in range(n):
                f = fc[i]
                if f > 0:
                    if not prev_pos:
                        low = 0.0
                    low = min(low, f)
                    if f - low >= BAND:
                        low = f
                        cell = i // H
                        if cell not in used_cells and i + H < n:
                            used_cells.add(cell)
                            if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                                r = c[i + H] / c[i] - 1.0
                                day = d["ts"].iloc[i].strftime("%Y-%m-%d")
                                cases.append((day, coin, r - drift, float(f)))
                    prev_pos = True
                else:
                    prev_pos = False
                    low = 0.0

    n_cases = len(cases)
    days = sorted(set(cs[0] for cs in cases))
    n_days = len(days)
    counts = {"days with cases": int(n_days), "cases": int(n_cases)}

    if n_days < MIN_DAYS:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name,
                             "value": float(np.mean([c[2] for c in cases])) if n_cases else None,
                             "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n_days} days with cases, fewer than the plan's minimum of 30.",
            "reading": reading,
        }

    x = np.array([cs[2] for cs in cases])
    f = np.array([cs[3] for cs in cases])
    dk = np.array([cs[0] for cs in cases])
    mean = float(x.mean())
    dev = x - mean
    sums = pd.Series(dev).groupby(dk).sum().values
    G = len(sums)
    var = (G / (G - 1)) * np.sum(sums ** 2) / (n_cases ** 2) if G > 1 else np.nan
    se = float(np.sqrt(var)) if np.isfinite(var) else np.nan
    t = float(mean / se) if se and np.isfinite(se) and se > 0 else None

    med = float(np.median(f))
    hi = x[f >= med]
    lo = x[f < med]
    if len(hi) > 0 and len(lo) > 0:
        diff = float(hi.mean() - lo.mean())
        check_pass = diff > 0
    else:
        diff = None
        check_pass = False

    if t is not None and mean > 0 and t >= 2 and check_pass:
        status = "confirmed"
        decided = "Mean unusual move > 0 with t >= 2 and the high-minus-low forecast difference > 0: the confirm rule."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move < 0 with t <= -2: the reject rule."
    else:
        status = "inconclusive"
        if t is not None and mean > 0 and t >= 2:
            decided = "t >= 2 but the supporting check failed: inconclusive per the plan."
        else:
            decided = "t between -2 and 2 (or undefined): neither confirm nor reject, so inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": {"name": "t of the mean, cases clustered by day", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move at/above median forecast minus below median",
                             "value": diff, "passed": bool(check_pass)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
