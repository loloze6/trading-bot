import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    LHV = "debug_info.components.week_loss.last_history_value"
    BAND = 2.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            lhv = (pd.to_numeric(df[LHV], errors="coerce").values
                   if LHV in df.columns else np.full(len(df), np.nan))
            n = len(df)
            for i in range(n):
                if fc[i] == 0:
                    continue
                if i < 1:
                    continue  # r1 cannot be computed inside the window
                r1 = close[i] / close[i - 1] - 1.0
                if i >= 5:
                    r5 = close[i] / close[i - 5] - 1.0
                elif not np.isnan(lhv[i]):
                    r5 = lhv[i]  # vol-scaled 5-day return has the sign of the 5-day return
                else:
                    continue
                n_active += 1
                if r1 > 0 and r5 < 0 and fc[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the active bars are up days (close above prior close) with a negative "
                           "5-day return carrying a short forecast, as the Fidelity's situation and side require."),
            "reading": ("Active bars whose 1-day return cannot be computed inside the window are left out; the 5-day "
                        "sign is taken from the closes, or from the recorded vol-scaled 5-day return on the first bars."),
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        cases = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            if n >= 2:
                all_rets.extend(list(close[1:] / close[:-1] - 1.0))
            ref = 0.0
            prev_short = False
            for i in range(n):
                f = fc[i]
                if f < 0:
                    mag = -f
                    if not prev_short:
                        ref = 0.0
                    if mag - ref >= BAND - 1e-12:
                        if i + 1 < n:
                            ret = close[i + 1] / close[i] - 1.0
                            if np.isfinite(ret):
                                cases.append((ts.iloc[i].floor("D"), ret, mag))
                        ref = mag
                    else:
                        ref = min(ref, mag)
                    prev_short = True
                else:
                    prev_short = False
                    ref = 0.0
        all_rets = np.array(all_rets, dtype=float)
        all_rets = all_rets[np.isfinite(all_rets)]
        if len(all_rets) == 0:
            continue
        mu = float(all_rets.mean())
        for day, ret, mag in cases:
            rows.append({"day": day, "u": -(ret - mu), "absf": mag})

    cases_df = pd.DataFrame(rows, columns=["day", "u", "absf"])
    n_cases = int(len(cases_df))
    n_days = int(cases_df["day"].nunique()) if n_cases else 0

    main_val = None
    t_val = None
    if n_cases > 0:
        main_val = float(cases_df["u"].mean())
        dev = cases_df["u"] - main_val
        S = dev.groupby(cases_df["day"]).sum().values
        D = len(S)
        if D > 1:
            var = (S ** 2).sum() / (n_cases ** 2) * D / (D - 1)
            se = np.sqrt(var)
            t_val = float(main_val / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        srt = cases_df.sort_values("absf", kind="mergesort").reset_index(drop=True)
        h = n_cases // 2
        shallow = srt["u"].iloc[:h]
        deep = srt["u"].iloc[h:]
        sup_val = float(deep.mean() - shallow.mean())
        sup_pass = bool(sup_val > 0)

    if n_days < 100:
        status = "not observable"
        decided = f"Only {n_days} case days, below the plan's minimum of 100 case days."
    elif t_val is None or main_val is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed: any other result is inconclusive."
    elif main_val > 0 and t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure is above 0 with t >= 2 and the deeper-minus-shallower check is above 0."
    elif main_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The main measure is below 0 with t <= -2."
    else:
        status = "inconclusive"
        if main_val > 0 and t_val >= 2:
            decided = "The main t is >= 2 but the supporting check failed, which the plan calls inconclusive."
        else:
            decided = "The main measure's t lies between -2 and 2 (or its sign disagrees), which is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual next-day move in the short direction on case bars",
            "value": main_val,
            "statistic": ({"name": "t of the mean, cases of one day grouped", "value": t_val}
                          if t_val is not None else None),
            "threshold": "confirm above 0 with t >= 2 (and check above 0); reject below 0 with t <= -2",
        },
        "supporting_check": {
            "name": "deeper half minus shallower half of |forecast|, mean unusual move",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"case days": n_days, "cases": n_cases, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": ("Cases are short-side forecast rises of at least 2 points from the lowest level since the last bet "
                    "on every bar (1-bar grid), the coin's mean is its mean next-bar return over all its windows, the "
                    "halves split the cases sorted by |forecast| at n//2 (shallower first, odd case to the deeper "
                    "half), and the situation check uses r1>0 and r5<0 from closes (profile not recomputed)."),
    }
