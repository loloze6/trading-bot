import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    VOL_PERIOD = 20
    VOL_MULT = 2.0
    BODY_MAX_PCT = 1.0
    EPS = 1e-9
    MIN_CASES = 30

    def win_key(w):
        s = str(w)
        digits = "".join(ch for ch in s if ch.isdigit())
        return (int(digits) if digits else 0, s)

    def prep(df):
        d = df.copy()
        if "timestamp" in d.columns:
            d = d.sort_values("timestamp")
        d = d.reset_index(drop=True)
        for c in ["open", "high", "low", "close", "volume", "forecast"]:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        return d

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=win_key):
            d = prep(bars[coin][w])
            if len(d) == 0:
                continue
            vol = d["volume"]
            prior_mean = vol.shift(1).rolling(VOL_PERIOD, min_periods=VOL_PERIOD).mean()
            volr = vol / prior_mean.replace(0, np.nan)
            body_pct = (d["close"] - d["open"]).abs() / d["open"].replace(0, np.nan) * 100.0
            f = d["forecast"]
            active = f.notna() & (f != 0)
            computable = volr.notna() & body_pct.notna()
            n_active_uncomputable += int((active & ~computable).sum())
            act = active & computable
            situation = (volr >= VOL_MULT - EPS) & (body_pct <= BODY_MAX_PCT + EPS)
            n_active += int(act.sum())
            n_agree += int((act & situation & (f < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean short-side unusual 5-bar move (minus the 5-bar return from the signal close, minus the coin's normal 5-bar drift)"
    threshold = "confirm: t >= 2 over at least 30 cases with correlation > 0; reject: t <= -2 over at least 30 cases"
    reading_check = ("Situation recomputed from prices as volume / mean of the prior 20 recorded bars of the same window >= 2 "
                     "and |close - open| / open <= 1 %, expected side short; active bars in a window's first 20 rows, "
                     "where the prior 20-bar mean cannot be computed, are left out of the agreement "
                     f"({n_active_uncomputable} such bars)")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bets on days of volume >= 2x "
                           "the prior 20-day mean with a body <= 1 % of the open, as the plan's Fidelity states"
                           if n_active > 0 else "No active bar could be checked against the plan's situation"),
            "reading": reading_check + ".",
        }

    # ---------- 2. criterion ----------
    case_rows = []  # (coin, ret, absf)
    for coin in sorted(bars.keys()):
        # normal drift: mean of non-overlapping 5-bar returns over all windows of the coin
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin].keys(), key=win_key):
            d = prep(bars[coin][w])
            n = len(d)
            if n == 0:
                continue
            c = d["close"].values
            f = d["forecast"].fillna(0.0).values
            for i in range(0, n - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
            # bets on the short side: a rise of the short forecast of at least the band
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                fi = f[i]
                if fi < 0:
                    m = -fi
                    if m - ref >= BAND - EPS:
                        bet[i] = True
                        ref = m
                    else:
                        ref = min(ref, m)
                else:
                    ref = 0.0
            # one case per 5-bar grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if bet[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] == 0:
                    continue
                coin_cases.append((c[t + H] / c[t] - 1.0, abs(f[t])))
        if coin_cases:
            drift = float(np.mean(grid_rets)) if grid_rets else np.nan
            for r, af in coin_cases:
                if np.isfinite(drift):
                    case_rows.append((coin, -(r - drift), af))

    n_cases = len(case_rows)
    unusual = np.array([x[1] for x in case_rows], dtype=float)
    absf = np.array([x[2] for x in case_rows], dtype=float)

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_u = None
    if n_cases >= 2:
        sd = float(np.std(unusual, ddof=1))
        if sd > 0:
            t_u = float(mean_u / (sd / np.sqrt(n_cases)))
    corr = None
    if n_cases >= 3 and np.std(absf) > 0 and np.std(unusual) > 0:
        corr = float(stats.pearsonr(absf, unusual)[0])
    corr_pass = None if corr is None else bool(corr > 0)

    reading = (reading_check + "; cases are the first short bet (a rise of the short forecast of at least 2 points from "
               "its lowest level since the last bet) in each 5-bar grid cell of each window, measured from that bet's "
               "close over 5 bars inside the window, with the coin's drift the mean of its non-overlapping 5-bar grid "
               "returns over all its windows.")

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n_cases}), the plan's minimum count, so the data could not show the idea."
    elif t_u is None:
        status = "inconclusive"
        decided = "The t of the mean short-side unusual move could not be computed (zero dispersion), so it is not >= 2 nor <= -2."
    elif t_u >= 2 and corr_pass:
        status = "confirmed"
        decided = "Confirm rule: t >= 2 over at least 30 cases and the correlation of |forecast| with the short-side unusual move is above 0."
    elif t_u <= -2:
        status = "rejected"
        decided = "Reject rule: t <= -2 over at least 30 cases (the coin rises more than its drift after these days)."
    elif t_u >= 2:
        status = "inconclusive"
        decided = "Inconclusive rule: t >= 2 but the correlation check is at or below 0 (or not computable)."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: t lies between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_u is None else {"name": "t of the mean", "value": t_u},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "correlation of |forecast| on the signal bar with the short-side unusual move, above 0",
            "value": corr,
            "passed": corr_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
