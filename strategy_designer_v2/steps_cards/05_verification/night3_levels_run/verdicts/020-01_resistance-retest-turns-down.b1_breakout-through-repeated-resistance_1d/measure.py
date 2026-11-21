import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.break.last_history_value"

    def _f(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        return None if not np.isfinite(x) else x

    def _wkey(w):
        s = "".join(ch for ch in str(w) if ch.isdigit())
        return (int(s) if s else 0, str(w))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin in sorted(bars.keys()):
        prepared[coin] = {}
        for w in sorted(bars[coin].keys(), key=_wkey):
            df = bars[coin][w].copy()
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp")
            df = df.reset_index(drop=True)
            prepared[coin][w] = df
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                # situation: the raw component is positive only on a fresh upward close
                # through a repeated swing-high level (N x margin above it > 0)
                sit = np.isfinite(raw[i]) and raw[i] > 0
                # price consistency: close above a level that yesterday's close was at or below
                if sit and i > 0 and np.isfinite(close[i]) and np.isfinite(close[i - 1]):
                    sit = close[i] > close[i - 1]
                side_ok = fc[i] > 0  # expected side: long (a rise)
                if sit and side_ok:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean 10-bar excess return of the bets over the coin's normal 10-bar drift"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("A case is the first bet (a rise of the long forecast of at least 2 points from its lowest level since "
               "the last bet, from 0 after flat) in each 10-bar grid cell of a window counted from its first row, with its "
               "10-bar return taken from that bet's own close and dropped if the window ends first; the normal drift is the "
               "mean of the coin's non-overlapping 10-bar grid returns over all its windows; the median split sorts cases by "
               "entry forecast (ties by coin, window and time) and compares the top n//2 against the bottom n//2, leaving out "
               "the middle case when n is odd; the plan's 'fewer than 30 cases' is reported as not observable, per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": _f(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a fresh upward close "
                           "through a repeated 90-day swing-high level (raw component > 0)"
                           if n_active > 0 else "The forecast is never active, so no bar shows the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (forecast, excess, coin, window index, bar index)
    for coin in sorted(prepared.keys()):
        wins = sorted(prepared[coin].keys(), key=_wkey)
        # normal drift: non-overlapping 10-bar grid returns, all windows pooled
        grid_rets = []
        for w in wins:
            close = pd.to_numeric(prepared[coin][w]["close"], errors="coerce").values
            for i in range(0, len(close) - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for wi, w in enumerate(wins):
            df = prepared[coin][w]
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            # bets on the long side
            bets = np.zeros(len(df), dtype=bool)
            low = 0.0
            for i in range(len(df)):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bets[i] = True
                    low = f
                else:
                    low = min(low, f)
            # one case per grid cell
            for start in range(0, len(df), H):
                idx = [i for i in range(start, min(start + H, len(df))) if bets[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= len(df):
                    continue
                a, b = close[i], close[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                ex = (b / a - 1.0) - drift  # long direction
                cases.append((float(fc[i]), float(ex), coin, wi, i))

    n = len(cases)
    ex = np.array([c[1] for c in cases], dtype=float)
    mean_ex = float(np.mean(ex)) if n > 0 else None
    t = None
    if n >= 2:
        sd = float(np.std(ex, ddof=1))
        if sd > 0:
            t = mean_ex / (sd / np.sqrt(n))

    supp_val = None
    supp_pass = None
    if n >= 2:
        order = sorted(cases, key=lambda c: (c[0], c[2], c[3], c[4]))
        k = n // 2
        low_half = np.array([c[1] for c in order[:k]])
        high_half = np.array([c[1] for c in order[n - k:]])
        if k > 0:
            supp_val = float(np.mean(high_half) - np.mean(low_half))
            supp_pass = bool(supp_val > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, below the plan's minimum of 30 cases."
    elif t is not None and mean_ex > 0 and t >= 2:
        if supp_pass:
            status = "confirmed"
            decided = "Mean excess return positive with t >= 2 over at least 30 cases and the larger-forecast half beats the smaller half."
        else:
            status = "inconclusive"
            decided = "A confirming t with a failed supporting check is inconclusive."
    elif t is not None and mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess return negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": _f(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": _f(mean_ex),
            "statistic": ({"name": "ordinary t of the mean", "value": _f(t)} if _f(t) is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess return of larger-forecast half minus smaller half",
            "value": _f(supp_val),
            "passed": supp_pass,
        },
        "counts": {"cases": int(n)},
        "decided_by": decided,
        "reading": reading,
    }
