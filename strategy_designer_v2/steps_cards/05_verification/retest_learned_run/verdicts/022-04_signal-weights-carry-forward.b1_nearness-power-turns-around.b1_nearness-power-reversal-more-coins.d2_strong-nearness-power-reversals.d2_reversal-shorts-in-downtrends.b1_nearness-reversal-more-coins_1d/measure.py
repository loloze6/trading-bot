import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.excess_power.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            # 20-day return recomputed from closes inside the window; where not computable
            # (first 20 rows), the detector's own decision (regime) stands in for r20 < 0.
            r20 = close / close.shift(20) - 1.0
            reg_mr = d["regime"].astype(str) == "mean_reversion" if "regime" in d.columns else pd.Series(False, index=d.index)
            down = np.where(r20.notna(), r20 < 0.0, reg_mr)
            active = fc != 0
            situ = (raw > 0).fillna(False).values & down & (fc < 0).values
            n_active += int(active.sum())
            n_agree += int((situ & active.values).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "drift-removed 5-bar fall after shorts, weighted by abs(forecast)/mean abs(forecast)"
    threshold = "confirm: mean > 0 with t >= 2 and slope < 0; reject: mean < 0 with t <= -2; min 100 non-overlapping cases"
    slope_name = "least-squares slope of drift-removed 5-bar return on abs(forecast)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "non-overlapping cases": None},
            "decided_by": ("fewer than 90% of active bars are shorts on bars where the raw excess-power reading is positive "
                           "(implies a rise) and the 20-day return is below 0" if n_active > 0
                           else "no active bars: the config never takes the plan's short"),
            "reading": "situation = raw excess_power > 0 and 20-day return (recomputed from closes, else regime) < 0, side short",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    coin_cases.append((r, abs(fc[i])))
        if len(coin_rets) == 0:
            continue
        drift = float(np.mean(coin_rets))
        for r, a in coin_cases:
            rows.append((coin, r - drift, a))

    n_cases = len(rows)
    counts = {"non-overlapping cases": int(n_cases), "active bars": int(n_active)}
    reading = ("situation = raw excess_power > 0 and 20-day return (recomputed from closes, else regime) < 0, side short; "
               "cases are grid bars 0,5,10,... of each window with forecast < 0 and a full 5-bar return inside the window, "
               "drift = the coin's mean 5-bar grid return over all its windows, t = ordinary t of the mean of weighted values")

    if n_cases < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": slope_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"fewer than 100 non-overlapping cases over all coins and windows ({n_cases})",
            "reading": reading,
        }

    dr = np.array([x[1] for x in rows], dtype=float)
    a = np.array([x[2] for x in rows], dtype=float)
    w = a / a.mean()
    vals = -dr * w
    mean = float(vals.mean())
    sd = float(vals.std(ddof=1))
    t = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else float("nan")

    if np.var(a) > 0:
        slope = float(np.polyfit(a, dr, 1)[0])
        slope_pass = bool(slope < 0)
    else:
        slope = None
        slope_pass = False

    if mean > 0 and np.isfinite(t) and t >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "the weighted mean fall is above 0 with t >= 2 and the slope is below 0"
        else:
            status = "inconclusive"
            decided = "t >= 2 but the slope of the drift-removed return on abs(forecast) is not below 0"
    elif mean < 0 and np.isfinite(t) and t <= -2:
        status = "rejected"
        decided = "the weighted mean is below 0 with t <= -2: coins rose beyond their drift after the shorts"
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": {"name": "t of the mean", "value": t if np.isfinite(t) else None},
                         "threshold": threshold},
        "supporting_check": {"name": slope_name, "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
