import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.scaled_rise.last_history_value"
    PROFILE = "unknown"  # default regime of the detector = falling and agitated (both vetoes failed)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(d["close"], errors="coerce").values
            reg = d["regime"].astype(str).values
            prev_close = np.concatenate([[np.nan], close[:-1]])
            up_px = close > prev_close
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
                up = np.where(np.isnan(raw), up_px, raw > 0)
            else:
                up = up_px
            situ = (reg == PROFILE) & up.astype(bool)
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are up days in the falling-agitated "
                           "profile with a short forecast" if n_active > 0 else "no bar has a non-zero forecast"),
            "reading": "the profile is the regime 'unknown' (both chop vetoes failed) and an up day is a positive raw scaled rise (close above previous close where not recorded)",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, return, |forecast|)
    base = {}   # coin -> list of 3-bar returns of profile grid bars
    for coin, wins in bars.items():
        base.setdefault(coin, [])
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            n = len(d)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(d["close"], errors="coerce").values
            reg = d["regime"].astype(str).values
            days = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D").values

            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = close[H:] / close[:n - H] - 1.0

            # profile grid bars for the coin's baseline
            for i in range(0, n, H):
                if reg[i] == PROFILE and np.isfinite(fwd[i]):
                    base[coin].append(fwd[i])

            # new short bets
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_short = False
            for i in range(n):
                if f[i] < 0:
                    m = -f[i]
                    if not prev_short:
                        ref = 0.0
                    if m - ref >= BAND:
                        bet[i] = True
                        ref = m
                    else:
                        ref = min(ref, m)
                    prev_short = True
                else:
                    prev_short = False
                    ref = 0.0

            # once per grid cell: the first bet in the cell
            for c0 in range(0, n, H):
                idx = [i for i in range(c0, min(c0 + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if np.isfinite(fwd[i]):
                    cases.append((coin, days[i], fwd[i], abs(f[i])))

    base_mean = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in base.items()}
    vals, dys, absf = [], [], []
    for coin, day, r, af in cases:
        b = base_mean.get(coin, np.nan)
        if not np.isfinite(b):
            continue
        vals.append(-(r - b))
        dys.append(day)
        absf.append(af)
    vals = np.array(vals, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(vals))
    n_days = int(len(set(dys)))

    mean = float(vals.mean()) if n_cases else None
    tstat = None
    if n_cases and n_days >= 2:
        s = pd.Series(vals - mean).groupby(pd.Series(dys)).sum().values
        G = len(s)
        se = np.sqrt((G / (G - 1)) * np.sum(s ** 2)) / n_cases
        tstat = float(mean / se) if se > 0 else None

    sup_val, sup_pass = None, None
    if n_cases >= 2:
        med = float(np.median(absf))
        hi = vals[absf > med]
        lo = vals[absf <= med]
        if len(hi) and len(lo):
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_days < 30:
        status = "not observable"
        decided = f"only {n_days} case-days, fewer than the plan's minimum of 30"
    elif tstat is not None and mean > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "main measure above 0 with t >= 2 over at least 30 case-days and the supporting check passes"
        else:
            status = "inconclusive"
            decided = "confirming t but the supporting check (upper minus lower half above 0) fails"
        
    elif tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "main measure below 0 with t <= -2 over at least 30 case-days"
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (neither confirm nor reject rule met)"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 3-day fall after new short bets vs coin's falling-agitated grid mean",
            "value": mean,
            "statistic": {"name": "t of the mean, cases of one day pooled", "value": tstat} if tstat is not None else None,
            "threshold": "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject; at least 30 case-days",
        },
        "supporting_check": {
            "name": "unusual move of upper |forecast| half minus lower half",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"case-days": n_days, "cases": n_cases},
        "decided_by": decided,
        "reading": ("the profile is regime 'unknown'; a case is the first new short bet (short forecast magnitude rising >= 2 "
                    "from its lowest since the last bet) in each 3-bar grid cell from each window's first row, with a 3-bar return inside the window; "
                    "the baseline pools each coin's profile grid bars over all its windows; the day-pooled t uses a clustered standard error "
                    "with G/(G-1) correction; the median split puts |forecast| above the median in the upper half and the rest in the lower; "
                    "fewer than 30 case-days is reported as not observable"),
    }
