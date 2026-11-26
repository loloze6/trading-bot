import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.scaled_rise.last_history_value"
    HORIZON = 1
    MIN_CASES = 100
    MIN_DAYS = 60
    T_THR = 2.0

    def to_ts(s):
        if pd.api.types.is_numeric_dtype(s):
            mx = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    case_frames = []

    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["_ts"] = to_ts(d["timestamp"])
            d = d.sort_values("_ts").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)

            # falling profile = the regime with a strategy ("unknown"; the veto sends trend >= -10 to "chop")
            falling = regime == "unknown"
            rise = raw > 0
            situation = falling & rise

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # next-bar return inside the window (horizon 1: every bar is on the grid)
            nxt = close.shift(-HORIZON) / close - 1.0
            coin_rets.append(nxt.dropna())

            sel = (fc < 0) & nxt.notna()
            if sel.any():
                coin_cases.append(pd.DataFrame({
                    "coin": coin,
                    "day": d.loc[sel, "_ts"].dt.floor("D").values,
                    "ret": nxt[sel].values,
                    "w": fc[sel].abs().values,
                }))
        if coin_cases:
            allr = pd.concat(coin_rets) if coin_rets else pd.Series(dtype=float)
            mu = float(allr.mean()) if len(allr) else np.nan
            cc = pd.concat(coin_cases, ignore_index=True)
            cc["excess"] = cc["ret"] - mu
            case_frames.append(cc)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "abs(forecast)-weighted mean excess next-bar return on forecast<0 bars"
    thr_text = "negative with t <= -2 confirms (with slope < 0); positive with t >= +2 rejects; 100 cases over 60 days minimum"
    reading = ("Falling profile read from the recorded regime 'unknown' (the detector's 60-bar trend is not recorded); "
               "the situation is raw scaled_rise > 0 in that regime, expected side short; the day-clustered t uses "
               "per-day sums of w*(excess - weighted mean) over sum(w) with a D/(D-1) correction; days are UTC dates of the case bar.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_text},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the active bars are short bars on a one-day rise (raw scaled_rise > 0) "
                           "inside the falling profile; the config does not trade the plan's situation on its side"
                           if n_active > 0 else "The record has no active bars, so the config never trades the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    if case_frames:
        cases = pd.concat(case_frames, ignore_index=True)
        cases = cases.dropna(subset=["excess", "w"])
    else:
        cases = pd.DataFrame(columns=["coin", "day", "ret", "w", "excess"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    m = None
    t = None
    slope = None
    if n_cases > 0 and cases["w"].sum() > 0:
        w = cases["w"].values.astype(float)
        x = cases["excess"].values.astype(float)
        W = w.sum()
        m = float(np.sum(w * x) / W)
        dev = pd.Series(w * (x - m)).groupby(cases["day"].values).sum().values
        D = len(dev)
        if D > 1:
            var = (D / (D - 1)) * np.sum(dev ** 2) / W ** 2
            se = np.sqrt(var)
            t = float(m / se) if se > 0 else None
        if n_cases > 2 and np.ptp(w) > 0:
            slope = float(stats.linregress(w, x).slope)

    slope_pass = None if slope is None else bool(slope < 0)
    out = {
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": m,
                         "statistic": None if t is None else {"name": "day-clustered t of weighted mean", "value": t},
                         "threshold": thr_text},
        "supporting_check": {"name": "OLS slope of excess next-bar return on abs(forecast) below 0",
                             "value": slope, "passed": slope_pass},
        "counts": {"cases": n_cases, "distinct days": n_days},
        "reading": reading,
    }

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        out["status"] = "not observable"
        out["decided_by"] = (f"Minimum counts not reached: {n_cases} cases (need 100) over {n_days} distinct days (need 60).")
        return out

    if m is None or t is None:
        out["status"] = "inconclusive"
        out["decided_by"] = "The weighted mean or its t could not be computed, so neither the confirm nor the reject rule is met."
        return out

    if m < 0 and t <= -T_THR:
        if slope_pass:
            out["status"] = "confirmed"
            out["decided_by"] = "Confirm: weighted mean excess return negative with t <= -2 on >= 100 cases over >= 60 days, and the slope is below 0."
        else:
            out["status"] = "inconclusive"
            out["decided_by"] = "Inconclusive: a confirming t (<= -2) with a slope at or above 0."
    elif m > 0 and t >= T_THR:
        out["status"] = "rejected"
        out["decided_by"] = "Reject: weighted mean excess return positive with t >= +2 on >= 100 cases over >= 60 days."
    else:
        out["status"] = "inconclusive"
        out["decided_by"] = "Inconclusive: the t lies between -2 and +2."
    return out
