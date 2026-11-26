import numpy as np
import pandas as pd

H = 20
BAND = 2.0
RAW_COL = "debug_info.components.break.last_history_value"


def _bets(fc):
    """Bars where the forecast rises on its side by at least BAND from its lowest level since the last bet."""
    out = []
    side, ref = 0, 0.0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f == 0:
            side, ref = 0, 0.0
            continue
        s = 1 if f > 0 else -1
        a = abs(f)
        if s != side:
            side, ref = s, 0.0
        if a - ref >= BAND:
            out.append((i, s))
            ref = a
        else:
            ref = min(ref, a)
    return out


def measure(bars):
    # ---------- situation check ----------
    n_active, n_agree = 0, 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            high = pd.to_numeric(df["high"], errors="coerce")
            prior_high = high.shift(1).rolling(60, min_periods=60).max().values
            raw = (pd.to_numeric(df[RAW_COL], errors="coerce").values
                   if RAW_COL in df.columns else np.full(len(df), np.nan))
            regime = df["regime"].astype(str).values
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                if np.isfinite(raw[i]):
                    above = raw[i] > 0
                elif np.isfinite(prior_high[i]):
                    above = close[i] > prior_high[i]
                else:
                    above = False
                if regime[i] == "chop" and above and fc[i] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 20-bar move of cases (return minus coin's normal 20-bar drift, signal direction)"
    thr = "confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    sup_name = "mean unusual move of cases with forecast above median minus below median"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars in regime 'chop' with the close above the prior 60-day high, as the Fidelity's situation requires.",
            "reading": "The chop condition is read from the recorded regime (the detector's decision); the above-high condition from the raw break distance > 0, recomputed from prices where it is not recorded.",
        }

    # ---------- cases ----------
    cases = []
    for coin in sorted(bars):
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1)
            seen = set()
            for i, s in _bets(fc):
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                coin_cases.append((ts.iloc[i].floor("D"), s, close[i + H] / close[i] - 1, fc[i]))
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan
        for d, s, r, f in coin_cases:
            if np.isfinite(drift):
                cases.append((d, s * (r - drift), f))

    N = len(cases)
    days = sorted(set(c[0] for c in cases))
    D = len(days)
    mean_u, t = None, None
    if N > 0:
        u = np.array([c[1] for c in cases])
        mean_u = float(u.mean())
        if D > 1:
            dev = pd.Series(u - mean_u, index=[c[0] for c in cases]).groupby(level=0).sum().values
            se = np.sqrt(np.sum(dev ** 2) * D / (D - 1)) / N
            t = float(mean_u / se) if se > 0 else None

    sup_val, sup_pass = None, None
    if N > 0:
        f = np.array([c[2] for c in cases])
        u = np.array([c[1] for c in cases])
        med = np.median(f)
        hi, lo = u[f > med], u[f < med]
        if len(hi) and len(lo):
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    if N < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases ({N}): the plan's minimum count is not reached."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither confirm nor reject is met."
    elif mean_u > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: mean unusual move positive with t >= 2 over at least 30 cases, and the supporting check passes."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Reject: mean unusual move negative with t <= -2 over at least 30 cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "Inconclusive: t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of one day combined", "value": t} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": {"cases": int(N), "days": int(D)},
        "decided_by": decided,
        "reading": "Chop is read from the recorded regime and the break from the raw distance > 0 (prices where unrecorded); each 20-bar grid cell keeps its first bet, cases whose 20-bar return leaves the window are dropped, the drift is the coin's mean non-overlapping 20-bar return over all windows, and cases at the median forecast are left out of the supporting check.",
    }
