import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.below_low.last_history_value"

    def _f(x):
        try:
            x = float(x)
        except Exception:
            return None
        return None if not np.isfinite(x) else x

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(d["close"], errors="coerce").values
            low = pd.to_numeric(d["low"], errors="coerce")
            prior_low = low.shift(1).rolling(20, min_periods=20).min().values
            recomputed = (close - prior_low) / prior_low * 100.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
            else:
                raw = np.full(len(d), np.nan)
            val = np.where(np.isfinite(raw), raw, recomputed)
            active = fc != 0
            n_active += int(active.sum())
            situ = np.isfinite(val) & (val < 0)
            n_agree += int((active & situ & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean excess 5-bar fall of short bets (return minus coin's mean 5-bar return, short direction)"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 30 cases on at least 30 distinct days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are short bars whose close is below the prior 20-day low, so the config does not trade the plan's situation on its side.",
            "reading": "none",
        }

    # ---------- 2. drift per coin: mean non-overlapping 5-bar return over all windows ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases: short bets, first bet per 5-bar grid cell ----------
    excess, absfc, days = [], [], []
    for coin, wins in bars.items():
        dr = drift.get(coin, np.nan)
        if not np.isfinite(dr):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(d["close"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            on_short = False
            for i in range(n):
                f = fc[i]
                if f < 0:
                    mag = -f
                    if not on_short:
                        ref = 0.0
                        on_short = True
                    if mag - ref >= BAND:
                        bet[i] = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                else:
                    on_short = False
                    ref = 0.0
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                excess.append(-(r - dr))
                absfc.append(abs(fc[t]))
                days.append(ts.iloc[t].strftime("%Y-%m-%d"))

    excess = np.array(excess, dtype=float)
    absfc = np.array(absfc, dtype=float)
    n_cases = int(len(excess))
    n_days = int(len(set(days)))

    mean_ex = float(excess.mean()) if n_cases else None
    tstat = None
    if n_cases >= 2 and n_days >= 2:
        dev = excess - excess.mean()
        s = pd.Series(dev).groupby(pd.Series(days)).sum().values
        G = len(s)
        var = (G / (G - 1)) * np.sum(s ** 2) / (n_cases ** 2)
        if var > 0:
            tstat = float(excess.mean() / np.sqrt(var))

    sup_val, sup_pass = None, None
    if n_cases >= 2:
        med = np.median(absfc)
        hi = excess[absfc > med]
        lo = excess[absfc < med]
        if len(hi) and len(lo):
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"cases": n_cases, "distinct days": n_days}
    main = {
        "name": main_name,
        "value": mean_ex,
        "statistic": None if tstat is None else {"name": "t of the mean, cases on the same day pooled", "value": tstat},
        "threshold": threshold,
    }
    supporting = {
        "name": "mean excess fall of cases with |forecast| above median minus below median",
        "value": sup_val,
        "passed": sup_pass,
    }

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases on 30 distinct days is not reached ({n_cases} cases on {n_days} days)."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t could not be computed (no dispersion), so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean excess fall is above 0 with t >= 2 and the high-|forecast| cases fall more than the low ones."
        else:
            status = "inconclusive"
            decided = "The mean excess fall is above 0 with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif mean_ex < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean excess fall is below 0 with t <= -2: breakdowns are followed by rises beyond the drift."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    reading = ("A case is a short bet (a rise of the forecast's size of at least 2 points from its lowest level since the last bet, "
               "from 0 after a flat), the first in each non-overlapping 5-bar grid cell from each window's first row, returned from "
               "its own close over 5 bars inside the window; the drift is the coin's mean return on the 5-bar grid of all its windows; "
               "the same-day t sums deviations per UTC day with a G/(G-1) correction; cases exactly at the median |forecast| are left "
               "out of the supporting check; the situation uses the recorded raw value, recomputed from prices where missing.")

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
