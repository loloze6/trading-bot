import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.up_day_in_usual_moves.last_history_value"

    def ordered_windows(d):
        def key(w):
            try:
                return int(str(w).lstrip("w"))
            except Exception:
                return str(w)
        return sorted(d.keys(), key=key)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in ordered_windows(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ret1 = np.full(len(df), np.nan)
            if len(df) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # up day: raw vol-scaled one-day return > 0; where not recorded, from the prices
            up = np.where(np.isnan(raw), ret1 > 0, raw > 0)
            up = np.where(np.isnan(raw) & np.isnan(ret1), False, up)
            # falling agitated profile: the detector's regime with a strategy ("unknown", no veto)
            prof = df["regime"].astype(str).str.lower().values == "unknown"
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & prof & up & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    main_name = "mean unusual 3-bar move of short cases, in the short direction, before costs"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and larger-half minus smaller-half > 0; reject: mean < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "days with cases": 0},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are short bets on up days inside the "
                           "falling agitated profile (regime 'unknown'), as the Fidelity requires"
                           if n_active > 0 else "the record has no bar with a non-zero forecast"),
            "reading": "the profile is read from the recorded regime ('unknown' = no veto, the falling agitated profile) and the up day from the component's raw value > 0 (price return where not recorded).",
        }

    # ---------- 2. criterion ----------
    case_u, case_absf, case_day = [], [], []
    for coin in bars:
        wins = ordered_windows(bars[coin])
        # normal drift: mean non-overlapping 3-bar return over all windows of the coin
        grid_rets = []
        for w in wins:
            df = bars[coin][w].reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w in wins:
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            # short bets: rise of the short size by >= band from its lowest level since the last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                s = max(-f[i], 0.0)
                if s == 0.0:
                    ref = 0.0
                    continue
                if s - ref >= BAND - 1e-12:
                    bet[i] = True
                    ref = s
                else:
                    ref = min(ref, s)
            seen = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r) or pd.isna(ts.iloc[i]):
                    continue
                case_u.append(-(r - drift))
                case_absf.append(abs(f[i]))
                case_day.append(ts.iloc[i].floor("D"))

    u = np.array(case_u, dtype=float)
    absf = np.array(case_absf, dtype=float)
    N = len(u)
    days = pd.Series(case_day)
    G = int(days.nunique()) if N > 0 else 0

    mean_u = float(u.mean()) if N > 0 else None
    t = None
    if N > 1 and G > 1:
        dev = pd.Series(u - u.mean()).groupby(days.values).sum().values
        var = (G / (G - 1)) * float(np.sum(dev ** 2)) / (N ** 2)
        if var > 0:
            t = float(mean_u / np.sqrt(var))

    diff = None
    if N > 0:
        med = float(np.median(absf))
        big = u[absf > med]
        small = u[absf <= med]
        if len(big) > 0 and len(small) > 0:
            diff = float(big.mean() - small.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    counts = {"cases": int(N), "days with cases": int(G)}

    if G < 30:
        status = "not observable"
        decided = f"only {G} days with cases, below the plan's minimum of 30 days with cases."
    elif t is None:
        status = "inconclusive"
        decided = "the t of the mean unusual move cannot be computed, so no confirm or reject rule is met."
    elif t >= 2 and mean_u > 0:
        if sup_pass:
            status = "confirmed"
            decided = "the mean unusual move is positive with t >= 2 and the larger-half minus smaller-half difference is above 0."
        else:
            status = "inconclusive"
            decided = "a confirming t (>= 2) but the larger half is not above the smaller half: inconclusive by the plan."
    elif t <= -2 and mean_u < 0:
        status = "rejected"
        decided = "the mean unusual move is negative with t <= -2: prices rise further after up days, against the short."
    else:
        status = "inconclusive"
        decided = "the t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t is None else {"name": "t of the mean, cases of one day taken together", "value": t},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean unusual move, larger minus smaller half of |forecast|",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("a case is the first short bet (short size up >= 2 points from its lowest level since the last bet, "
                    "reset at flat) in each 3-bar grid cell from each window's first row, with its 3-bar return inside "
                    "the window; the larger half is |forecast| strictly above the median and the smaller half the rest; "
                    "the day-clustered t uses the G/(G-1) correction; the profile is read from the recorded regime "
                    "'unknown'; fewer than 30 days with cases is reported as not observable."),
    }
