import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RISE = "debug_info.components.scaled_rise.last_history_value"
    FALL = "debug_info.components.fall_depth.last_history_value"

    def to_days(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            v = s.astype(float)
            unit = "ms" if v.abs().max() > 1e11 else "s"
            d = pd.to_datetime(v, unit=unit, utc=True)
        else:
            d = pd.to_datetime(s, utc=True)
        return d.dt.strftime("%Y-%m-%d").values

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ret1 = np.full(len(df), np.nan)
            if len(df) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            if RISE in df.columns:
                rise = pd.to_numeric(df[RISE], errors="coerce").values
            else:
                rise = np.full(len(df), np.nan)
            rise_pos = np.where(np.isnan(rise), ret1 > 0, rise > 0)
            if FALL in df.columns:
                fall = pd.to_numeric(df[FALL], errors="coerce").values
            else:
                fall = np.full(len(df), np.nan)
            falling = np.where(np.isnan(fall), False, fall < -10.0)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            agitated = regime == "trending"
            active = fc != 0
            ok = active & rise_pos & falling & agitated & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The rise and the 60-day fall are read from the recorded raw values (rise > 0, fall < -10 as the "
               "config's veto), the agitation (365-day volatility percentile, not recomputable inside ~122-bar "
               "windows) from the detector's regime being 'trending', a case is the first short bet in each 3-bar "
               "grid cell of a window, and the t clusters deviations by signal day with a G/(G-1) correction.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on a rise day inside "
                           "the falling agitated profile" if n_active > 0 else
                           "No bar has a non-zero forecast, so the config never takes the plan's short"),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin drift: mean of non-overlapping 3-bar returns over all windows
    drift = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rs.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rs)) if rs else np.nan

    cases = []  # (day, |forecast|, unusual move short)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            days = to_days(df["timestamp"])
            ref = 0.0
            bet = np.zeros(len(df), dtype=bool)
            for i in range(len(df)):
                if fc[i] < 0:
                    m = -fc[i]
                    if m - ref >= BAND:
                        bet[i] = True
                        ref = m
                    else:
                        ref = min(ref, m)
                else:
                    ref = 0.0
            for start in range(0, len(df), H):
                idx = [j for j in range(start, min(start + H, len(df))) if bet[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= len(df):
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                d = drift.get(coin, np.nan)
                if not np.isfinite(d):
                    continue
                r = c[t + H] / c[t] - 1.0
                u = -(r - d)
                cases.append((days[t], abs(fc[t]), u))

    n_cases = len(cases)
    case_days = len(set(x[0] for x in cases))
    counts = {"cases": n_cases, "distinct case days": case_days}

    mean_u = None
    t_stat = None
    corr = None
    if n_cases > 0:
        cd = pd.DataFrame(cases, columns=["day", "absf", "u"])
        mean_u = float(cd["u"].mean())
        dev = cd["u"] - mean_u
        S = dev.groupby(cd["day"]).sum().values
        G = len(S)
        if G > 1:
            var = (G / (G - 1.0)) * float(np.sum(S ** 2)) / (n_cases ** 2)
            if var > 0:
                t_stat = float(mean_u / np.sqrt(var))
        if n_cases > 2 and cd["absf"].std() > 0 and cd["u"].std() > 0:
            corr = float(np.corrcoef(cd["absf"].values, cd["u"].values)[0, 1])

    sup_pass = (corr is not None and corr > 0)
    main = {
        "name": "mean unusual 3-day move after short bets, short direction",
        "value": mean_u,
        "statistic": ({"name": "t of the mean, same-day cases together", "value": t_stat}
                      if t_stat is not None else None),
        "threshold": "confirm: mean > 0 with t >= 2 and correlation > 0; reject: mean < 0 with t <= -2",
    }
    sup = {"name": "correlation of |forecast| with unusual move", "value": corr,
           "passed": sup_pass if corr is not None else None}

    if case_days < 30:
        status = "not observable"
        decided = "Fewer than 30 distinct case days across all coins and windows (%d)." % case_days
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the unusual move could not be computed, so neither confirm nor reject is met."
    elif mean_u > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the correlation is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t whose correlation between |forecast| and the unusual move is not above 0."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: prices rose after the shorts."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
