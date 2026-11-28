import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.scaled_week_rise.last_history_value"
    POST = "debug_info.components.scaled_week_rise.post_pipeline_value"
    PROFILE_REGIME = "unknown"  # the regime left when neither falling-calm veto fires

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            close = pd.to_numeric(df["close"], errors="coerce").values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            # 7-day rise from prices, inside the window, as a fallback where raw is not recorded
            r7 = np.full(len(df), np.nan)
            if len(df) > 7:
                r7[7:] = close[7:] / close[:-7] - 1.0
            rise = np.where(~np.isnan(raw), raw > 0, np.where(~np.isnan(r7), r7 > 0, False))
            in_profile = reg == PROFILE_REGIME
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & in_profile & rise & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.90)

    main_name = "mean unusual 3-bar move of the cases (long)"
    threshold = "confirm: mean > 0 with t >= 2 (day-clustered); reject: mean < 0 with t <= -2"
    sup_name = "OLS slope of unusual move on case-bar post_pipeline_value"

    reading_base = ("The falling-calm profile is read from the recorded regime ('unknown' = neither veto fired) and the "
                    "7-day rise from the raw component sign (price 7-day return where unrecorded); a case is the first "
                    "bet (forecast rise >= 2 points from its lowest long level since the last bet, reset at 0) in each "
                    "3-bar grid cell from each window's first row; the day-clustered t uses the D/(D-1) correction; "
                    "the slope t is the ordinary OLS t; unmet minimum counts give 'not observable' per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active), "agreeing_bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the falling-calm "
                           "profile with a positive 7-day rise, so the config does not trade the plan's situation."),
            "reading": reading_base,
        }

    # ---------- 2. Criterion ----------
    case_rows = []  # (coin, ret, post, day)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            post = (pd.to_numeric(df[POST], errors="coerce").values
                    if POST in df.columns else np.full(len(df), np.nan))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.strftime("%Y-%m-%d").values
            n = len(df)
            # normal drift grid
            for i in range(0, n - H, H):
                if np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    grid_rets.append(close[i + H] / close[i] - 1.0)
            # bets
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[i] = True
                    low = f
                else:
                    low = min(low, f)
            # one case per grid cell
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if bet[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                case_rows.append((coin, close[t + H] / close[t] - 1.0, post[t], days[t]))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    cases = pd.DataFrame(case_rows, columns=["coin", "ret", "post", "day"])
    if len(cases):
        cases["drift"] = cases["coin"].map(drift)
        cases = cases[np.isfinite(cases["drift"])]
        cases["u"] = cases["ret"] - cases["drift"]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_u = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["u"] - mean_u
        s_d = dev.groupby(cases["day"]).sum().values
        var = (n_days / (n_days - 1.0)) * np.sum(s_d ** 2) / n_cases ** 2
        t_u = float(mean_u / np.sqrt(var)) if var > 0 else None

    slope = None
    slope_t = None
    if n_cases >= 3:
        sc = cases[np.isfinite(cases["post"]) & np.isfinite(cases["u"])]
        if len(sc) >= 3 and np.ptp(sc["post"].values) > 0:
            lr = stats.linregress(sc["post"].values, sc["u"].values)
            slope = float(lr.slope)
            slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    counts = {"cases": n_cases, "distinct days": n_days}
    main = {"name": main_name, "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_u}
                          if t_u is not None else None),
            "threshold": threshold}
    sup_pass = None if slope is None else bool(slope > 0)
    sup = {"name": sup_name, "value": slope, "passed": sup_pass}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = (f"The plan's minimum of 100 cases on 50 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    else:
        main_conf = mean_u is not None and t_u is not None and mean_u > 0 and t_u >= 2
        main_rej = mean_u is not None and t_u is not None and mean_u < 0 and t_u <= -2
        slope_rej = slope is not None and slope_t is not None and slope < 0 and slope_t <= -2
        if main_rej or slope_rej:
            status = "rejected"
            decided = ("Reject rule met: " +
                       ("the mean unusual move is below 0 with t <= -2" if main_rej else
                        "the slope is negative with t <= -2") + ".")
        elif main_conf and slope is not None and slope > 0:
            status = "confirmed"
            decided = "Confirm rule met: mean unusual move above 0 with t >= 2 and a positive slope."
        else:
            status = "inconclusive"
            if main_conf:
                decided = "The main measure meets the confirm rule but the slope is at or below 0 with t above -2."
            else:
                decided = "Neither the confirm nor the reject rule is met (the mean is not above 0 with t >= 2)."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
