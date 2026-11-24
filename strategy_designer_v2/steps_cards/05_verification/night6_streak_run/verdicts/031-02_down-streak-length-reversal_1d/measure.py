import numpy as np
import pandas as pd


def _to_day(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(v.values) if len(v) else 0.0
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        else:
            unit = "s"
        dt = pd.to_datetime(v, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.strftime("%Y-%m-%d").values


def _window_order(keys):
    def k(w):
        try:
            return int(str(w).lstrip("w"))
        except Exception:
            return str(w)
    return sorted(keys, key=k)


def measure(bars):
    H = 5
    BAND = 2.0
    LHV = "debug_info.components.down_streak.last_history_value"

    # ---------------- situation check ----------------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in _window_order(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce").values.astype(float)
            else:
                raw = np.full(len(df), np.nan)
            # fallback where the component is not recorded: last close below the prior close
            prev = np.concatenate([[np.nan], close[:-1]])
            down_px = close < prev
            in_streak = np.where(np.isnan(raw), down_px, raw < 0)
            active = np.isfinite(f) & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & in_streak & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of 5-bar excess return on forecast (grid, pooled)"
    thr = "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"
    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are down-streak bars "
                          "(raw down_streak value < 0) with a long (positive) forecast, as the Fidelity's "
                          "situation and expected side require.",
            "reading": "none",
        }

    # ---------------- grid samples ----------------
    rows = []      # (coin, fwd_ret, forecast, day)
    case_rows = [] # (coin, ret_from_signal, day)
    for coin in bars:
        for w in _window_order(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            days = _to_day(df["timestamp"].values)
            n = len(df)
            for g in range(0, n, H):
                if g + H < n:
                    r = close[g + H] / close[g] - 1.0
                    if np.isfinite(r):
                        rows.append((coin, r, f[g], days[g]))
            # bets: rises of the long-side forecast of at least the band from its lowest level since last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi) or fi <= 0:
                    ref = 0.0
                    continue
                if fi - ref >= BAND:
                    bet[i] = True
                    ref = fi
                else:
                    ref = min(ref, fi)
            for g in range(0, n, H):
                idx = np.where(bet[g:min(g + H, n)])[0]
                if len(idx) == 0:
                    continue
                i = g + int(idx[0])
                if i + H < n:
                    r = close[i + H] / close[i] - 1.0
                    if np.isfinite(r):
                        case_rows.append((coin, r, days[i]))

    gdf = pd.DataFrame(rows, columns=["coin", "ret", "fc", "day"])
    drift = gdf.groupby("coin")["ret"].mean() if len(gdf) else pd.Series(dtype=float)

    reg = gdf.dropna(subset=["ret", "fc"]).copy()
    pos = reg[reg["fc"] > 0]
    n_pos = int(len(pos))
    n_pos_days = int(pos["day"].nunique())

    slope = None
    tstat = None
    if len(reg) >= 3 and reg["fc"].nunique() > 1:
        y = (reg["ret"] - reg["coin"].map(drift)).values.astype(float)
        X = np.column_stack([np.ones(len(reg)), reg["fc"].values.astype(float)])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        sc = pd.DataFrame(X * u[:, None], columns=["a", "b"])
        sc["day"] = reg["day"].values
        S = sc.groupby("day")[["a", "b"]].sum().values
        G = S.shape[0]
        meat = S.T @ S
        V = XtX_inv @ meat @ XtX_inv
        if G > 1:
            V = V * G / (G - 1)
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tstat = float(slope / se) if np.isfinite(se) and se > 0 else None

    # ---------------- supporting check ----------------
    cdf = pd.DataFrame(case_rows, columns=["coin", "ret", "day"])
    if len(cdf):
        cdf["unusual"] = cdf["ret"] - cdf["coin"].map(drift)
        cdf = cdf.dropna(subset=["unusual"])
    n_cases = int(len(cdf))
    mean_unusual = float(cdf["unusual"].mean()) if n_cases > 0 else None
    sup_pass = (mean_unusual is not None) and (mean_unusual > 0)

    counts = {
        "grid bars with a forecast above 0": n_pos,
        "distinct days of those grid bars": n_pos_days,
        "grid bars in regression": int(len(reg)),
        "supporting cases": n_cases,
    }

    if n_pos < 300 or n_pos_days < 100:
        status = "not observable"
        decided = (f"Minimum not reached: {n_pos} grid bars with a forecast above 0 (need 300) "
                   f"on {n_pos_days} distinct days (need 100).")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean unusual move over the cases is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails (mean unusual move not above 0)."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed_sit},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "slope t, day-clustered (same-day cases summed)", "value": tstat}
                          if tstat is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean unusual 5-bar move over long cases (forecast rises >= 2)",
            "value": mean_unusual,
            "passed": bool(sup_pass) if mean_unusual is not None else None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The regression is OLS with intercept of every grid bar's (positions 0,5,10,... per window) excess "
                    "5-bar return (minus the coin's mean grid 5-bar return over all windows) on its forecast, with "
                    "standard errors from scores summed per UTC day (G/(G-1) correction); cases are the first "
                    "long-side forecast rise of >= 2 from its lowest level since the last bet in each grid cell, "
                    "measured from that bar's close; the minimum counts use grid bars with forecast > 0 and a valid "
                    "forward return, and a shortfall is reported as 'not observable'."),
    }
