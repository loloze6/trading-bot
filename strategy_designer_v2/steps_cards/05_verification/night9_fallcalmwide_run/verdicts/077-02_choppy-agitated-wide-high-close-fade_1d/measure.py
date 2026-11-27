import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    LOC_COL = "debug_info.components.near_high.last_history_value"
    BAND = 2.0
    EPS = 1e-9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0

    # ---------- 2. criterion data ----------
    case_rows = []  # (coin, day, signed unusual move, abs forecast)

    for coin, wins in bars.items():
        # normal drift: mean 1-bar return over all windows of the coin (grid of step 1 = every bar)
        all_rets = []
        prepared = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            ret_next = close.shift(-1) / close - 1.0
            d["_ret_next"] = ret_next
            all_rets.append(ret_next.dropna().values)
            prepared[w] = d
        if not prepared:
            continue
        all_rets = np.concatenate(all_rets) if len(all_rets) else np.array([])
        drift = float(np.mean(all_rets)) if len(all_rets) else np.nan

        for w, d in prepared.items():
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            close = d["close"].astype(float)
            rngv = high - low
            mean_rng = rngv.rolling(30, min_periods=30).mean()
            rng_ratio = rngv / mean_rng.replace(0, np.nan)
            loc_px = (close - low) / rngv.replace(0, np.nan)
            if LOC_COL in d.columns:
                loc = pd.to_numeric(d[LOC_COL], errors="coerce").where(
                    lambda s: s.notna(), loc_px)
            else:
                loc = loc_px
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)

            # situation check on active bars
            active = fc != 0
            computable = rng_ratio.notna() & loc.notna()
            situ = (rng_ratio >= 1.0 - EPS) & (loc >= 0.75 - EPS)
            n_active += int((active & computable).sum())
            n_active_uncomputable += int((active & ~computable).sum())
            n_agree += int((active & computable & situ & (fc < 0)).sum())

            # short bets: a fall of the forecast of >= 2 points from its least-short level since last bet
            ref = 0.0
            fvals = fc.values
            for i in range(len(fvals)):
                f = fvals[i]
                if f < 0:
                    depth = -f
                    if depth - ref >= BAND - EPS:
                        r = d["_ret_next"].iat[i]
                        if pd.notna(r) and np.isfinite(drift):
                            um = -(float(r) - drift)
                            day = d["timestamp"].iat[i].floor("D")
                            case_rows.append((coin, day, um, abs(f)))
                        ref = depth
                    else:
                        ref = min(ref, depth)
                else:
                    ref = 0.0

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active,
                       "active bars agreeing": n_agree},
            "decided_by": ("Fewer than 90% of active bars are wide (range >= 30-day mean range) "
                           "high-closing (close location >= 0.75) bars with a short forecast"
                           if n_active > 0 else "No active bar could be checked against the situation."),
            "reading": ("Range is high minus low against the mean of the last 30 ranges including the current bar; "
                        "active bars in a window's first 29 rows, where that mean cannot be computed from the record, "
                        "are left out of the agreement."),
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "um", "absf"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_um = float(cases["um"].mean()) if n_cases else None
    t_val = None
    if n_cases > 0 and n_days > 1:
        dev = cases["um"] - mean_um
        S = dev.groupby(cases["day"]).sum().values
        var_mean = (n_days / (n_days - 1.0)) * np.sum(S ** 2) / (n_cases ** 2)
        if var_mean > 0:
            t_val = float(mean_um / np.sqrt(var_mean))

    supp_val = None
    supp_pass = None
    if n_cases > 0:
        med = float(cases["absf"].median())
        upper = cases.loc[cases["absf"] > med, "um"]
        lower = cases.loc[cases["absf"] <= med, "um"]
        if len(upper) > 0 and len(lower) > 0:
            supp_val = float(upper.mean() - lower.mean())
            supp_pass = bool(supp_val > 0)
        else:
            supp_pass = False

    if n_days < 100:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, below the plan's minimum of 100."
    elif t_val is not None and mean_um > 0 and t_val >= 2 and supp_pass:
        status = "confirmed"
        decided = "Mean unusual move positive with t >= 2 and the upper-half-minus-lower-half difference above 0."
    elif t_val is not None and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move has t <= -2: the coin rises more than its drift after wide high closes."
    else:
        status = "inconclusive"
        if t_val is not None and t_val >= 2:
            decided = "t >= 2 but the supporting check (upper minus lower half above 0) fails."
        else:
            decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean next-bar unusual move of short bets (signed for the short)",
            "value": mean_um,
            "statistic": {"name": "t of the mean, cases of one day taken together",
                          "value": t_val} if t_val is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 and supporting check passing; reject: t <= -2",
        },
        "supporting_check": {
            "name": "upper minus lower half mean unusual move, split at median |forecast|",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": {"distinct case days": n_days, "cases": n_cases},
        "decided_by": decided,
        "reading": ("Range is high minus low against the mean of the last 30 ranges including the current bar, "
                    "with active bars in a window's first 29 rows left out of the agreement; the upper half is the "
                    "cases strictly above the median |forecast| and ties go to the lower half; the day-clustered t "
                    "uses a D/(D-1) correction; the plan's 100-day minimum gives 'not observable' when not reached."),
    }
