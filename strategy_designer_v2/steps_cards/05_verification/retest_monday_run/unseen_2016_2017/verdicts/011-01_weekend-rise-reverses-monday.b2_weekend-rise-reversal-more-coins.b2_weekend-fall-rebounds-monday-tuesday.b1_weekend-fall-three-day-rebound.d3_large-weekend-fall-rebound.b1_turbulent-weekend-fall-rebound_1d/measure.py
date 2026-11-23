import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BET = 2.0
    MIN_CASES = 100
    RAW = "debug_info.components.wkend_fall.last_history_value"

    def to_ts(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            mx = np.nanmax(np.abs(v.values)) if len(v) else 0
            unit = "ns" if mx > 1e17 else ("us" if mx > 1e14 else ("ms" if mx > 1e11 else "s"))
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["_ts"] = to_ts(d["timestamp"])
            d = d.sort_values("_ts").reset_index(drop=True)
            d["_close"] = pd.to_numeric(d["close"], errors="coerce")
            d["_fc"] = pd.to_numeric(d["forecast"], errors="coerce")
            prepared[coin][w] = d

            # the coming bar (next calendar day) is a Monday: the bar starts on a Sunday
            next_is_monday = ((d["_ts"] + pd.Timedelta(days=1)).dt.dayofweek == 0).values
            # Sunday bar's own return (Saturday close to Sunday close)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            ret1 = d["_close"].pct_change()
            fall_val = raw.where(raw.notna(), ret1)
            is_fall = (fall_val < 0).values
            # vol ratio >= 1: detector component not recorded; its decision is the regime
            reg = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * len(d))
            turbulent = (reg == "mean_reversion")
            situation = next_is_monday & is_fall & turbulent

            fc = d["_fc"].values
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("The vol-ratio >= 1 condition is read from the recorded regime 'mean_reversion' because the detector's "
               "component is not recorded and its 365-day lookback cannot be rebuilt inside a window; the Sunday bar is "
               "the bar starting on a Sunday (UTC); cases are all Sunday-close bars with forecast >= 2 having a bar t+3 in "
               "the same window (Sundays are 7 bars apart, so none overlap); the coin's normal 3-day drift is the mean of "
               "non-overlapping 3-bar returns at positions 0,3,6,... of each of its windows pooled; the median split puts "
               "forecasts above the median in the upper half and those at or below it in the lower half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 3-day move of Sunday-close bets", "value": None,
                             "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"cases in total": None},
            "decided_by": ("Fewer than 90% of the active bars are long bets on Sunday bars after a weekend fall in a "
                           "turbulent regime (vol ratio >= 1), as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- normal drift per coin ----------
    drift = {}
    for coin, wins in prepared.items():
        rets = []
        for w, d in wins.items():
            c = d["_close"].values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                rets.extend(list(r[np.isfinite(r)]))
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    unusual = []
    fcs = []
    for coin, wins in prepared.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, d in wins.items():
            c = d["_close"].values
            fc = d["_fc"].values
            sunday = ((d["_ts"] + pd.Timedelta(days=1)).dt.dayofweek == 0).values
            n = len(d)
            for t in range(n - H):
                if sunday[t] and np.isfinite(fc[t]) and fc[t] >= BET:
                    r = c[t + H] / c[t] - 1.0
                    if np.isfinite(r):
                        unusual.append(r - drift[coin])
                        fcs.append(fc[t])
    unusual = np.array(unusual, dtype=float)
    fcs = np.array(fcs, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_stat = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_up = n_lo = 0
    if n_cases > 0:
        med = float(np.median(fcs))
        up = unusual[fcs > med]
        lo = unusual[fcs <= med]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up > 0 and n_lo > 0:
            sup_val = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": "mean unusual 3-day move of Sunday-close bets (forecast >= 2)",
            "value": mean_u,
            "statistic": ({"name": "ordinary t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": "positive with t >= 2 (and supporting check passes) to confirm; negative with t <= -2 to reject"}
    sup = {"name": "mean unusual move, upper minus lower half at median forecast", "value": sup_val, "passed": sup_pass}
    counts = {"cases in total": n_cases, "upper half cases": n_up, "lower half cases": n_lo}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases in total, fewer than the plan's minimum of 100."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed (zero dispersion), so it is not >= 2 nor <= -2."
    elif mean_u > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the upper-minus-lower half difference is above 0."
        else:
            status = "inconclusive"
            decided = "The mean unusual move has t >= 2 but the supporting check (upper minus lower half > 0) fails."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
