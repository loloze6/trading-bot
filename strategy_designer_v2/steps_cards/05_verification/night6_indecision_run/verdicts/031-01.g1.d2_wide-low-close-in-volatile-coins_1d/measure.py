import numpy as np
import pandas as pd


def _to_time(s):
    if np.issubdtype(s.dtype, np.number):
        v = s.astype(float)
        med = np.nanmedian(np.abs(v)) if len(v) else 0.0
        unit = "ms" if med > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    TOL = 1e-9
    situation_rows = []   # (active, in_situation_or_nan, sign_ok)
    case_frames = []
    all_returns = {}

    for coin, wins in bars.items():
        rets_coin = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            o = df["open"].astype(float)
            h = df["high"].astype(float)
            l = df["low"].astype(float)
            c = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ts = _to_time(df["timestamp"])

            # next-bar return inside the window
            r1 = c.shift(-1) / c - 1.0
            rets_coin.append(r1.dropna())

            # --- recompute the plan's situation from prices, inside the window ---
            rng = (h - l)
            mean20 = rng.rolling(20, min_periods=20).mean()           # 20-day mean range incl. today
            mbr = mean20 / rng.replace(0, np.nan)                     # long / short (short = 1 bar)
            cl = (c - l) / rng.replace(0, np.nan)                     # close location from the low
            lr = np.log(c / c.shift(1))
            vol20 = lr.rolling(20, min_periods=20).std()
            vol_avg = vol20.rolling(60, min_periods=60).mean()
            vr = vol20 / vol_avg

            cond_known = mbr.notna() & cl.notna() & vr.notna()
            situ = (mbr <= 0.6667 + TOL) & (cl <= 0.25 + TOL) & (vr >= 1.0 - TOL)

            active = fc != 0
            for i in np.where(active.values)[0]:
                if bool(cond_known.iloc[i]):
                    situation_rows.append(bool(situ.iloc[i]) and fc.iloc[i] > 0)
                # bars where the situation cannot be recomputed (not enough history
                # inside the window) are left out of the agreement share

            # --- cases ---
            reg = df["regime"].astype(str)
            mask = (reg == "mean_reversion") & (fc > 0) & r1.notna()
            if mask.any():
                case_frames.append(pd.DataFrame({
                    "coin": coin,
                    "day": ts[mask].dt.floor("D").values,
                    "ret": r1[mask].values,
                    "fc": fc[mask].values,
                }))
        if rets_coin:
            all_returns[coin] = pd.concat(rets_coin)

    n_sit = len(situation_rows)
    agreement = float(np.mean(situation_rows)) if n_sit > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean next-day unusual move on mean_reversion days with forecast > 0"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    reading = ("Situation recomputed per window from prices (range = high-low, 20-bar mean range including "
               "the day over the day's range <= 0.6667, close location (close-low)/(high-low) <= 0.25, "
               "20-bar log-return std over its 60-bar mean >= 1), active bars lacking that history left out of "
               "the agreement; t clusters cases by UTC day (deviations summed per day, small-sample factor G/(G-1)); "
               "the plan's 30 distinct case days is treated as a minimum count, giving 'not observable' if unmet.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_sit)},
            "decided_by": ("Fewer than 90% of the active bars are long bars on days with a range >= 1.5x its "
                           "20-day mean, a close in the lowest quarter and 20-day volatility at or above its "
                           "60-day mean" if n_sit > 0 else
                           "No active bar could be checked against the plan's situation"),
            "reading": reading,
        }

    drift = {k: float(v.mean()) for k, v in all_returns.items() if len(v) > 0}
    if case_frames:
        cases = pd.concat(case_frames, ignore_index=True)
        cases["u"] = cases["ret"] - cases["coin"].map(drift)
        cases = cases.dropna(subset=["u", "fc"])
    else:
        cases = pd.DataFrame(columns=["coin", "day", "ret", "fc", "u"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct case days": n_days}

    mean_u = float(cases["u"].mean()) if n_cases else None
    t = None
    if n_cases > 1 and n_days > 1:
        d = cases["u"] - mean_u
        S = d.groupby(cases["day"]).sum()
        G = len(S)
        se = np.sqrt((S ** 2).sum()) / n_cases * np.sqrt(G / (G - 1))
        t = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases and cases["fc"].sum() > 0:
        wmean = float((cases["u"] * cases["fc"]).sum() / cases["fc"].sum())
        sup_val = wmean - mean_u
        sup_pass = bool(wmean > mean_u)

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases clustered by day", "value": t} if t is not None else None,
            "threshold": thr}
    supp = {"name": "forecast-weighted mean minus unweighted mean of unusual move",
            "value": sup_val, "passed": sup_pass}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed."
    elif mean_u > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 and the forecast-weighted mean above the unweighted mean."
        else:
            status = "inconclusive"
            decided = "Mean unusual move above 0 with t >= 2, but the supporting check failed."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
