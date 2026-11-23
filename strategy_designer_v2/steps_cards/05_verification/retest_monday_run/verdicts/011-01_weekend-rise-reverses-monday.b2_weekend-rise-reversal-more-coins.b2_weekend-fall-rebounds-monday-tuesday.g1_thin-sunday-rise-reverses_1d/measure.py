import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.thin_sunday_rise.last_history_value"
    H = 2
    MIN_CASES = 200

    def _ts(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            mx = np.nanmax(v.values) if len(v) else 0
            unit = "ms" if mx > 1e11 else "s"
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
            d = df.reset_index(drop=True).copy()
            d["_ts"] = _ts(d["timestamp"])
            d = d.sort_values("_ts").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            sunday = d["_ts"].dt.dayofweek == 6
            price_rise = (close / close.shift(1) - 1) > 0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                rise = np.where(raw.notna(), raw > 0, price_rise)
            else:
                rise = price_rise.values
            rise = pd.Series(rise, index=d.index).astype(bool)
            situation = sunday & rise
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())
            prepared[coin][w] = (close.values.astype(float), fc.values.astype(float), sunday.values)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 2-bar move in the short's direction (Sunday close to Tuesday close, minus coin drift, negated)"
    main_thr = "confirm: mean > 0 with t >= 2 and supporting difference > 0; reject: mean < 0 with t <= -2; fewer than 200 cases: not observable"
    reading = ("Sunday bars are those whose UTC start timestamp falls on a Sunday and a rise is the raw component value > 0 "
               "(close over previous row's close when raw is missing); the return is close at row t+2 over close at t inside the window; "
               "the coin's drift is the mean of non-overlapping 2-bar returns at positions 0,2,4,... of each window pooled over all its windows; "
               "the median split puts cases with |forecast| strictly above the pooled median in the larger half and the rest in the smaller half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": None, "active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of the {n_active} active bars are Sunday bars after a Sunday rise with a short forecast, "
                           "below the 90% required by the plan's situation (short only on rising Sundays)."),
            "reading": reading,
        }

    # ---------- criterion ----------
    unusual = []
    absf = []
    for coin, wins in prepared.items():
        grid = []
        for w, (close, fc, sunday) in wins.items():
            n = len(close)
            for i in range(0, n - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid.append(b / a - 1)
        if len(grid) == 0:
            continue
        drift = float(np.mean(grid))
        for w, (close, fc, sunday) in wins.items():
            n = len(close)
            for t in range(n - H):
                if sunday[t] and fc[t] < 0:
                    a, b = close[t], close[t + H]
                    if np.isfinite(a) and np.isfinite(b) and a > 0:
                        r = b / a - 1
                        unusual.append(-(r - drift))
                        absf.append(abs(fc[t]))

    u = np.array(unusual, dtype=float)
    f = np.array(absf, dtype=float)
    n = len(u)

    mean = float(np.mean(u)) if n > 0 else None
    if n > 1:
        sd = float(np.std(u, ddof=1))
        tstat = float(mean / (sd / np.sqrt(n))) if sd > 0 else None
    else:
        tstat = None

    sup_val, sup_pass = None, None
    n_large = n_small = 0
    if n > 0:
        med = float(np.median(f))
        large = u[f > med]
        small = u[f <= med]
        n_large, n_small = len(large), len(small)
        if n_large > 0 and n_small > 0:
            sup_val = float(np.mean(large) - np.mean(small))
            sup_pass = bool(sup_val > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases across coins and windows, below the plan's minimum of 200."
    elif mean is not None and tstat is not None and mean > 0 and tstat >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the larger-|forecast| half minus the smaller half is above 0."
    elif mean is not None and tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2: rising Sundays keep rising over the 2 days more than the coin's drift."
    else:
        status = "inconclusive"
        if tstat is not None and tstat >= 2 and mean is not None and mean > 0:
            decided = "The main t is >= 2 but the supporting difference is at or below 0 (or not computable)."
        else:
            decided = "The main t lies between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "ordinary t of the mean", "value": tstat} if tstat is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "mean unusual move of larger-|forecast| half minus smaller half (> 0)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": int(n), "larger half": int(n_large), "smaller half": int(n_small), "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
