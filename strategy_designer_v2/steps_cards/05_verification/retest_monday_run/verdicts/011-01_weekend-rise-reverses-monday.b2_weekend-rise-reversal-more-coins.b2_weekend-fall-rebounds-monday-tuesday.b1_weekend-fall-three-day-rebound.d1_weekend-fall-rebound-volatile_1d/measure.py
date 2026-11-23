import numpy as np
import pandas as pd
from scipy import stats


def _ts(s):
    if pd.api.types.is_numeric_dtype(s):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "s" if mx < 1e11 else ("ms" if mx < 1e14 else "ns")
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 3
    RAW = "debug_info.components.wkfall_vol.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["ts"] = _ts(d["timestamp"])
            d = d.sort_values("ts").reset_index(drop=True)
            close = d["close"].astype(float)
            d["ret1"] = close / close.shift(1) - 1.0
            d["fwd"] = close.shift(-H) / close - 1.0
            d["fc"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            # the fall: sign of the raw component (return x positive vol ratio); from the prices where not recorded
            fall = np.where(raw.notna(), raw < 0, d["ret1"] < 0)
            sunday = (d["ts"].dt.dayofweek == 6).values
            d["situation"] = sunday & fall.astype(bool)
            prepared[coin][w] = d
            act = d["fc"] != 0
            n_active += int(act.sum())
            n_agree += int((act & d["situation"] & (d["fc"] > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    situation_check = {"agreement": agreement, "passed": bool(passed)}

    main_name = "t of mean of forecast x excess 3-bar return on Sunday-fall cases"
    threshold = "confirm t >= 2 with top-minus-bottom third > 0; reject t <= -2; at least 100 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are Sunday bars after a "
                           "Saturday-to-Sunday fall with a positive (long) forecast, as the plan's Fidelity requires."),
            "reading": "Sunday bar = bar whose UTC start is a Sunday; the fall is the sign of the raw component, or of the 1-bar close return where it is not recorded.",
        }

    # ---------- 2. criterion ----------
    case_fc, case_ex, case_key = [], [], []
    for coin in sorted(prepared):
        grid = []
        for w, d in prepared[coin].items():
            c = d["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                grid.append(c[i + H] / c[i] - 1.0)
        grid = np.array([g for g in grid if np.isfinite(g)])
        if len(grid) == 0:
            continue
        mu = float(grid.mean())
        for w in sorted(prepared[coin]):
            d = prepared[coin][w]
            sel = (d["ts"].dt.dayofweek == 6) & (d["fc"] > 0) & d["fwd"].notna()
            for i in np.where(sel.values)[0]:
                case_fc.append(float(d["fc"].iat[i]))
                case_ex.append(float(d["fwd"].iat[i]) - mu)
                case_key.append((coin, str(w), int(i)))

    fc = np.array(case_fc)
    ex = np.array(case_ex)
    n = len(fc)
    counts = {"cases": int(n)}

    tval = None
    mean_prod = None
    if n >= 2:
        prod = fc * ex
        mean_prod = float(prod.mean())
        sd = float(prod.std(ddof=1))
        tval = float(mean_prod / (sd / np.sqrt(n))) if sd > 0 else 0.0

    diff = None
    if n >= 3:
        order = sorted(range(n), key=lambda k: (fc[k], case_key[k]))
        k3 = n // 3
        bottom = ex[order[:k3]]
        top = ex[order[n - k3:]]
        diff = float(top.mean() - bottom.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    main = {"name": main_name, "value": mean_prod,
            "statistic": None if tval is None else {"name": "t of the mean", "value": tval},
            "threshold": threshold}
    supporting = {"name": "top-third minus bottom-third mean excess 3-bar return", "value": diff, "passed": sup_pass}
    reading = ("Sunday = UTC bar start on Sunday; cases need 3 bars ahead inside the window; the coin's mean is over "
               "its non-overlapping 3-bar grid (0,3,6,... per window) pooled across windows; thirds are the lowest and "
               "highest floor(n/3) cases sorted by forecast; the plan's 'fewer than 100 cases' is treated as the minimum count (not observable).")

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 100."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "t >= 2 and the top-minus-bottom-third difference is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The main measure has t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top-minus-bottom-third difference is at or below 0."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
