import numpy as np
import pandas as pd


def measure(bars):
    H = 8
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.fail_depth.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            active = np.isfinite(f) & (f != 0)
            situation = np.isfinite(raw) & (raw != 0)  # a failed re-entry sits 2 bars back (lag inside the component)
            n_active += int(active.sum())
            n_agree += int((active & situation & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on which the "
                           "fail_depth component reports a failed re-entry 2 bars back (raw value non-zero)"
                           if n_active > 0 else "The forecast is never non-zero, so the plan's short bets on failed re-entries never occur."),
            "reading": "The situation is read as a non-zero raw fail_depth value (the component already applies lag 2), the expected side as short.",
        }

    # ---------- 2. criterion ----------
    # normal 8-bar drift per coin: non-overlapping grid of all its windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    xs, ws = [], []
    for coin, wins in bars.items():
        d = drift.get(coin, np.nan)
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(f)
            # short-side bets: rise of the short forecast of >= band from its lowest level since last bet
            s = np.where(f < 0, -f, 0.0)
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                if s[i] == 0:
                    ref = 0.0
                    continue
                ref = min(ref, s[i])
                if s[i] - ref >= BAND:
                    bet[i] = True
                    ref = s[i]
            # one case per non-overlapping 8-bar grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n or not np.isfinite(d):
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                xs.append(-(r - d))
                ws.append(abs(f[t]))

    x = np.array(xs, dtype=float)
    wt = np.array(ws, dtype=float)
    n_cases = int(len(x))

    wmean, tval = None, None
    if n_cases >= 2 and wt.sum() > 0:
        wmean = float(np.sum(wt * x) / np.sum(wt))
        se = float(np.sqrt(np.sum((wt ** 2) * (x - wmean) ** 2)) / np.sum(wt))
        tval = float(wmean / se) if se > 0 else None
    elif n_cases == 1:
        wmean = float(x[0])

    diff, n_deep, n_shallow = None, 0, 0
    if n_cases >= 2:
        med = float(np.median(wt))
        deep = wt > med
        shallow = ~deep
        n_deep, n_shallow = int(deep.sum()), int(shallow.sum())
        if n_deep > 0 and n_shallow > 0:
            diff = float(np.mean(x[deep]) - np.mean(x[shallow]))
    sup_pass = (diff > 0) if diff is not None else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30 cases."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the weighted mean cannot be computed (no dispersion), so neither confirm nor reject is met."
    elif wmean > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The weighted mean short-side excess fall is positive with t >= 2 over at least 30 cases, and the deeper half's excess fall exceeds the shallower half's."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (t >= 2) but the deep-minus-shallow difference is not above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The weighted mean short-side excess fall has t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the weighted mean short-side excess fall lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "|forecast|-weighted mean 8-bar short-side excess fall",
            "value": wmean,
            "statistic": ({"name": "t of the weighted mean", "value": tval} if tval is not None else None),
            "threshold": "confirm: positive with t >= 2 over at least 30 cases; reject: t <= -2 over at least 30 cases",
        },
        "supporting_check": {
            "name": "deeper-half minus shallower-half mean excess fall (split at median |forecast|)",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "deeper half": n_deep, "shallower half": n_shallow},
        "decided_by": decided,
        "reading": ("Situation = non-zero raw fail_depth value (lag inside the component) with a short forecast; a case is the first "
                    "short-side bet (forecast falling >= 2 points from its least-short level since the last bet, reset at flat) in each "
                    "8-bar grid cell from each window's first row, dropped if its 8-bar return leaves the window; drift is the coin's mean "
                    "non-overlapping 8-bar return over all windows; the weighted mean's t uses the weighted (sandwich) standard error "
                    "sqrt(sum w^2 (x-m)^2)/sum w; the halves are |forecast| above the median versus at or below it, compared by unweighted means."),
    }
