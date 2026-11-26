import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RISE_COL = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            r = close.pct_change()
            sd = r.rolling(30, min_periods=30).std(ddof=1)
            rise_re = r / sd
            if RISE_COL in d.columns:
                rise = pd.to_numeric(d[RISE_COL], errors="coerce")
                rise = rise.where(rise.notna(), rise_re)
            else:
                rise = rise_re
            f = pd.to_numeric(d["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            ok = active & (rise >= 1.0 - 1e-9) & (f < 0)
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean unusual 5-bar move after short bets, in the short direction"
    threshold = "confirm: mean > 0 with t >= 2 and size check passing; reject: mean < 0 with t <= -2"
    reading_common = ("The situation is checked as a raw scaled rise >= 1.0 (recorded last_history_value, recomputed "
                      "from closes with a 30-return ddof-1 std including the day where missing) with a negative "
                      "forecast, the falling-agitated profile not being recomputable from the record (365-bar "
                      "percentile, warm-up not recorded); a case is the first short bet (forecast magnitude rising by "
                      ">= 2 from its lowest short level since the last bet, from 0 after flat) in each 5-bar grid cell "
                      "of a window, drift is the mean of the coin's grid 5-bar returns over all its windows, the day "
                      "t sums deviations per UTC day, and the size check splits strictly above/below the cases' median "
                      "|forecast|.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0, "distinct days": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with a scaled one-day "
                           "rise of at least 1 std, as the plan's situation requires."),
            "reading": reading_common,
        }

    # ---------- 2. criterion ----------
    cases = []  # (day, unusual, absf)
    for coin, wins in bars.items():
        # normal drift over all windows of the coin
        grid_rets = []
        prepared = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            prepared[w] = d
            c = d["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, d in prepared.items():
            c = d["close"].astype(float).values
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_short = False
            for i in range(n):
                if f[i] < 0:
                    mag = -f[i]
                    if not prev_short:
                        ref = 0.0
                    if mag - ref >= BAND - 1e-12:
                        bet[i] = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                    prev_short = True
                else:
                    ref = 0.0
                    prev_short = False
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                ret = c[t + H] / c[t] - 1.0
                unusual = -(ret - drift)
                cases.append((ts.iloc[t].normalize(), unusual, abs(f[t])))

    n_cases = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_u = None
    tval = None
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        u = np.array([x[1] for x in cases], dtype=float)
        mean_u = float(u.mean())
        dev = u - mean_u
        dser = pd.Series(dev, index=[x[0] for x in cases]).groupby(level=0).sum()
        se = float(np.sqrt(np.sum(dser.values ** 2)) / n_cases)
        if n_days >= 2 and se > 0:
            tval = float(mean_u / se)
        a = np.array([x[2] for x in cases], dtype=float)
        med = np.median(a)
        hi = u[a > med]
        lo = u[a < med]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"The plan's minimum counts are not reached ({n_cases} cases vs 30, {n_days} distinct days vs 20).")
    elif tval is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the size check passes (confirm rule)."
    elif mean_u < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 (reject rule)."
    elif mean_u > 0 and tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the size check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases grouped by day", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean unusual move above minus below the cases' median |forecast|",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_common,
    }
