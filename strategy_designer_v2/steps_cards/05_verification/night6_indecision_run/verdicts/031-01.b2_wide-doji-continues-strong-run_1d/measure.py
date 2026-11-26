import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    MIN_CASE_DAYS = 30
    EPS = 1e-9

    def _component_series(df, cid):
        col = f"debug_info.components.{cid}.last_history_value"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            def _get(x):
                try:
                    if isinstance(x, dict):
                        v = x.get(cid)
                        if isinstance(v, dict):
                            return v.get("last_history_value", np.nan)
                except Exception:
                    pass
                return np.nan
            return pd.to_numeric(df["debug_info.components"].apply(_get), errors="coerce")
        return pd.Series(np.nan, index=df.index)

    # ---------- situation check + case collection ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    cases = []          # (coin, day, ret3, forecast)
    drift_by_coin = {}

    for coin, wins in bars.items():
        coin_grid_rets = []
        coin_cases = []
        for wname, df0 in wins.items():
            if df0 is None or len(df0) == 0:
                continue
            df = df0.copy()
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            df = df.sort_values("timestamp").reset_index(drop=True)
            o = pd.to_numeric(df["open"], errors="coerce")
            h = pd.to_numeric(df["high"], errors="coerce")
            l = pd.to_numeric(df["low"], errors="coerce")
            c = pd.to_numeric(df["close"], errors="coerce")
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            # situation from prices (inside the window only)
            run5_px = c / c.shift(5) - 1.0
            run5_rec = _component_series(df, "run5_size")
            run5 = run5_rec.where(run5_rec.notna(), run5_px)
            rng = h - l
            mean_rng = rng.rolling(20, min_periods=20).mean()
            wide = rng / mean_rng.replace(0, np.nan)
            flat = 1.0 - (c - o).abs() / rng.replace(0, np.nan)
            computable = run5.notna() & wide.notna() & flat.notna()
            situ = computable & (run5 > 0) & (wide >= 1.5 - EPS) & (flat >= 0.9 - EPS)

            active = f != 0
            n_active += int(active.sum())
            n_active_uncomputable += int((active & ~computable).sum())
            n_agree += int((active & situ & (f > 0)).sum())

            # non-overlapping grid returns for the coin's normal drift
            n = len(df)
            cv = c.values
            for p in range(0, n - H, H):
                if np.isfinite(cv[p]) and np.isfinite(cv[p + H]) and cv[p] != 0:
                    coin_grid_rets.append(cv[p + H] / cv[p] - 1.0)

            # bets: rise of the forecast on the long side of at least the band
            fv = f.values
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                x = fv[i]
                if x > 0:
                    if x - ref >= BAND - EPS:
                        bet[i] = True
                        ref = x
                    else:
                        ref = min(ref, x)
                else:
                    ref = 0.0
            # one case per grid cell of the horizon
            seen = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(cv[i]) and np.isfinite(cv[i + H])) or cv[i] == 0:
                    continue
                day = df["timestamp"].iloc[i].floor("D")
                coin_cases.append((coin, day, cv[i + H] / cv[i] - 1.0, float(fv[i])))
        drift = float(np.mean(coin_grid_rets)) if coin_grid_rets else np.nan
        drift_by_coin[coin] = drift
        for (cn, d, r, fc) in coin_cases:
            if np.isfinite(drift):
                cases.append((cn, d, r - drift, fc))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    situation_check = {"agreement": None if agreement is None else float(agreement), "passed": passed}

    main_name = "mean unusual 3-day move after signal (return minus coin's normal 3-day drift)"
    threshold = "mean > 0 with day-clustered t >= 2 (confirm); mean < 0 with t <= -2 (reject)"
    reading = ("Situation recomputed per window from prices (5-bar close change, or the recorded run5_size raw value "
               "where present; range over the 20-bar mean range including bar t; 1 - |close-open|/range), active bars "
               "with too little in-window history counted as not agreeing; cases are long bets (forecast rise >= 2 "
               "points from its low since the last bet, from 0 after flat), the first per 3-bar grid cell, needing 3 "
               "bars ahead in the window; case-days are distinct UTC days with a case; t uses day-summed deviations "
               "with a G/(G-1) correction; the slope is an OLS of unusual move on the signal bar's forecast.")

    if n_active == 0 or not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars agreeing": int(n_agree),
                       "active bars without enough history": int(n_active_uncomputable)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the 5-day return > 0, "
                           "range >= 1.5x the 20-day mean range and flatness >= 0.9 hold"
                           if n_active > 0 else "No bar has a non-zero forecast, so the plan's situation is never traded."),
            "reading": reading,
        }

    # ---------- main measure ----------
    n_cases = len(cases)
    if n_cases > 0:
        cdf = pd.DataFrame(cases, columns=["coin", "day", "u", "f"])
        case_days = int(cdf["day"].nunique())
        mean_u = float(cdf["u"].mean())
        dev = cdf["u"] - mean_u
        S = dev.groupby(cdf["day"]).sum().values
        G = len(S)
        if G > 1:
            var = (S ** 2).sum() * G / (G - 1) / (n_cases ** 2)
            se = np.sqrt(var)
            t = float(mean_u / se) if se > 0 else None
        else:
            t = None
        # supporting check: slope of unusual move on forecast
        if n_cases >= 2 and cdf["f"].nunique() > 1:
            fx = cdf["f"].values
            uy = cdf["u"].values
            slope = float(np.sum((fx - fx.mean()) * (uy - uy.mean())) / np.sum((fx - fx.mean()) ** 2))
            slope_pass = bool(slope > 0)
        else:
            slope = None
            slope_pass = None
    else:
        case_days = 0
        mean_u = None
        t = None
        slope = None
        slope_pass = None

    counts = {"case-days": int(case_days), "cases": int(n_cases)}

    if case_days < MIN_CASE_DAYS:
        status = "not observable"
        decided = f"Only {case_days} case-days, fewer than the plan's minimum of 30 case-days."
    elif t is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t >= 2 and slope_pass is True:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2, slope above 0, and at least 30 case-days (confirm rule)."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 and at least 30 case-days (reject rule)."
    elif mean_u > 0 and t >= 2:
        status = "inconclusive"
        decided = "A confirming t whose slope is not above 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": {
            "name": main_name,
            "value": None if mean_u is None else float(mean_u),
            "statistic": None if t is None else {"name": "t of the mean, cases of one day taken together", "value": float(t)},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of unusual 3-day move on signal-bar forecast > 0",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
