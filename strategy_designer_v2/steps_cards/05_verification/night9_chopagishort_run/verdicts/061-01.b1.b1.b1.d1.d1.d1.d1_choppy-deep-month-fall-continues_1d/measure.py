import numpy as np
import pandas as pd


def _to_float(x):
    try:
        v = float(x)
    except Exception:
        return None
    if not np.isfinite(v):
        return None
    return v


def _parse_ts(s):
    if pd.api.types.is_numeric_dtype(s):
        v = pd.to_numeric(s, errors="coerce")
        med = np.nanmedian(v.values) if len(v) else 0
        unit = "ms" if med > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True, errors="coerce")
    return pd.to_datetime(s, utc=True, errors="coerce")


def measure(bars):
    H = 5
    BAND = 2.0
    EPS = 1e-9
    col_lhv = "debug_info.components.fall20.last_history_value"
    col_alloc = "postRebalance_current_allocation"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    n_active_unknown = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float)
            pe20_px = (close / close.shift(20) - 1.0) * 100.0
            if col_lhv in df.columns:
                lhv = pd.to_numeric(df[col_lhv], errors="coerce").astype(float)
                pe20 = lhv.where(lhv.notna(), pe20_px)
            else:
                pe20 = pe20_px
            pe60 = (close / close.shift(60) - 1.0) * 100.0
            active = fc != 0
            for i in np.where(active.values)[0]:
                a = pe20.iloc[i]
                b = pe60.iloc[i]
                if not (np.isfinite(a) and np.isfinite(b)):
                    n_active_unknown += 1
                    continue
                n_active += 1
                sit = (a <= -10.0 + EPS) and (b >= -10.0 - EPS) and (b <= 10.0 + EPS)
                if sit and fc.iloc[i] < 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation bars: 20-day return (recorded fall20 raw value, else from closes) at or below -10 "
               "and 60-day return from closes between -10 and +10 inclusive, short side; active bars in a "
               "window's first 60 rows, where the 60-day return cannot be computed inside the window, are left "
               "out of the agreement; a case is a short bet (forecast rising on the short side by at least 2 "
               "points from its lowest level since the last bet), the first one in each 5-bar grid cell of its "
               "window, its return from that bar's close over 5 bars; position size is the absolute "
               "postRebalance_current_allocation on the case bar, the larger-short half being the top floor(n/2) "
               "cases by size; the day-clustered t uses a G/(G-1) correction.")

    main_name = "mean unusual move of short cases over 5 bars (short side positive)"
    threshold = "t of 2 or more (with supporting check above 0) confirms; t of -2 or less rejects; at least 30 distinct days of cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": _to_float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active), "active bars agreeing": int(n_agree)},
            "decided_by": ("Fewer than 90 percent of the active bars are bars of the plan's situation "
                           "(20-day return at or below -10 inside a choppy 60-day return of -10 to +10) on the short side."),
            "reading": reading,
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").astype(float).values
            for p in range(0, len(close) - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    rets.append(c1 / c0 - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    cases = []
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float).values
            alloc = (pd.to_numeric(df[col_alloc], errors="coerce").astype(float).values
                     if col_alloc in df.columns else np.full(len(df), np.nan))
            ts = _parse_ts(df["timestamp"])
            # bet detection, short side
            ref = 0.0
            bet = np.zeros(len(df), dtype=bool)
            for i in range(len(df)):
                m = -fc[i] if fc[i] < 0 else 0.0
                if m <= 0:
                    ref = 0.0
                    continue
                if m - ref >= BAND - EPS:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            n = len(df)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                r = c1 / c0 - 1.0
                u = -(r - drift[coin])
                t_i = ts.iloc[i]
                day = str(t_i.date()) if pd.notna(t_i) else coin + "_" + str(w) + "_" + str(i)
                size = abs(alloc[i]) if np.isfinite(alloc[i]) else np.nan
                cases.append({"u": u, "day": day, "size": size, "key": (str(t_i), coin)})

    n_cases = len(cases)
    days = sorted(set(c["day"] for c in cases))
    n_days = len(days)

    mean_u = None
    t_val = None
    if n_cases > 0:
        u = np.array([c["u"] for c in cases])
        mean_u = float(np.mean(u))
        dev = pd.Series(u - mean_u).groupby([c["day"] for c in cases]).sum().values
        G = len(dev)
        if G > 1:
            var = (G / (G - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t_val = float(mean_u / se) if se > 0 else None

    # supporting check
    sup_val = None
    sized = [c for c in cases if np.isfinite(c["size"])]
    if len(sized) >= 2:
        sized_sorted = sorted(sized, key=lambda c: (-c["size"], c["key"]))
        k = len(sized_sorted) // 2
        big = [c["u"] for c in sized_sorted[:k]]
        small = [c["u"] for c in sized_sorted[k:]]
        if big and small:
            sup_val = float(np.mean(big) - np.mean(small))
    sup_passed = None if sup_val is None else bool(sup_val > 0)

    counts = {"cases": int(n_cases), "distinct days of cases": int(n_days)}

    if n_days < 30:
        status = "not observable"
        decided = "Fewer than 30 distinct days of cases (" + str(n_days) + "), the plan's minimum."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed."
    elif t_val >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The main measure has a t of 2 or more and the larger-minus-smaller-short difference is above 0."
        else:
            status = "inconclusive"
            decided = "A confirm-level t with the supporting check at or below 0 is inconclusive."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main measure has a t of -2 or less: prices rose more than their drift after deep 20-day falls."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": _to_float(agreement), "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": _to_float(mean_u),
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": _to_float(t_val)}
                          if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean unusual move of larger-short half minus smaller-short half",
            "value": _to_float(sup_val),
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
