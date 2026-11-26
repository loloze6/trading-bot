import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    SR = "debug_info.components.scaled_rise.last_history_value"
    RD = "debug_info.components.rise_x_depth.last_history_value"
    BAND = 2.0

    # ---------- prepare per-window frames ----------
    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["coin"] = coin
            d["window"] = w
            d["close"] = pd.to_numeric(d["close"], errors="coerce")
            d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            d["ret_next"] = d["close"].shift(-1) / d["close"] - 1.0   # inside window only
            d["ret_prev"] = d["close"] / d["close"].shift(1) - 1.0
            frames.append(d)
    if not frames:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": None, "supporting_check": None,
                "counts": {"distinct case days": 0},
                "decided_by": "no bars in the record", "reading": "none"}

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for d in frames:
        reg = d["regime"].astype(str) if "regime" in d.columns else pd.Series(["unknown"] * len(d))
        in_profile = reg == "unknown"  # vetoes send the bar to 'chop' (flat) outside the falling-agitated profile
        if SR in d.columns:
            sr = pd.to_numeric(d[SR], errors="coerce")
        else:
            sr = pd.Series(np.nan, index=d.index)
        up = sr > 0
        # where the component is not recorded, recompute the up day from prices inside the window
        up = up.where(sr.notna(), d["ret_prev"] > 0).fillna(False).astype(bool)
        situation = in_profile & up
        active = d["forecast"] != 0
        n_active += int(active.sum())
        n_agree += int((active & situation & (d["forecast"] < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    reading = ("The plan's situation is taken as an up day (raw scaled_rise > 0, or a positive in-window close-to-close "
               "return where it is not recorded) on a bar whose regime is 'unknown' (inside the falling-agitated profile), "
               "with the depth graded so any close at or below its 20-day high qualifies; the expected side is short; "
               "cases are the holding-period bets (forecast rising in size on the short side by >= 2 points from its "
               "smallest size since the last bet, from 0 after flat or side change); the main value is the mean unusual "
               "move over cases with t over daily sums; the supporting split excludes cases exactly at the median; "
               "fewer than 30 case days is reported as 'not observable'.")

    if not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": float(agreement), "passed": False},
                "main_measure": None, "supporting_check": None,
                "counts": {"active bars": int(n_active)},
                "decided_by": (f"only {agreement:.1%} of the {n_active} active bars are short bars on up days inside the "
                               "falling-agitated profile, below the 90 % the plan's Fidelity requires"),
                "reading": reading}

    # ---------- coin drift: mean daily return over all windows ----------
    drift = {}
    for coin in bars.keys():
        r = pd.concat([d.loc[d["coin"] == coin, "ret_next"] for d in frames if d["coin"].iloc[0] == coin]
                      ) if any(d["coin"].iloc[0] == coin for d in frames if len(d)) else pd.Series(dtype=float)
        r = r.dropna()
        drift[coin] = float(r.mean()) if len(r) else np.nan

    # ---------- cases ----------
    rows = []
    for d in frames:
        if len(d) == 0:
            continue
        coin = d["coin"].iloc[0]
        f = d["forecast"].values
        ref = 0.0
        prev_short = False
        for i in range(len(d)):
            fi = f[i]
            if fi < 0:
                mag = -fi
                if not prev_short:
                    ref = 0.0
                if mag - ref >= BAND - 1e-12:
                    rn = d["ret_next"].iloc[i]
                    if pd.notna(rn) and pd.notna(drift[coin]):
                        ts = pd.to_datetime(d["timestamp"].iloc[i], utc=True, errors="coerce")
                        rows.append({"coin": coin, "day": ts.floor("D") if pd.notna(ts) else None,
                                     "absf": mag, "um": -(rn - drift[coin])})
                    ref = mag
                else:
                    ref = min(ref, mag)
                prev_short = True
            else:
                prev_short = False
                ref = 0.0
    cases = pd.DataFrame(rows, columns=["coin", "day", "absf", "um"]).dropna(subset=["day", "um"])

    n_cases = int(len(cases))
    daily = cases.groupby("day")["um"].sum() if n_cases else pd.Series(dtype=float)
    n_days = int(len(daily))

    mean_um = float(cases["um"].mean()) if n_cases else None
    if n_days >= 2 and daily.std(ddof=1) > 0:
        t_main = float(daily.mean() / (daily.std(ddof=1) / np.sqrt(n_days)))
    else:
        t_main = None

    # ---------- supporting check ----------
    diff = None
    t_sup = None
    n_large = n_small = 0
    if n_cases:
        med = cases["absf"].median()
        large = cases.loc[cases["absf"] > med, "um"]
        small = cases.loc[cases["absf"] < med, "um"]
        n_large, n_small = int(len(large)), int(len(small))
        if n_large >= 1 and n_small >= 1:
            diff = float(large.mean() - small.mean())
        if n_large >= 2 and n_small >= 2:
            tt = stats.ttest_ind(large, small, equal_var=False)
            t_sup = float(tt.statistic) if np.isfinite(tt.statistic) else None

    counts = {"distinct case days": n_days, "cases": n_cases,
              "larger cases": n_large, "smaller cases": n_small}
    main = {"name": "unusual move after short bets, next day, before costs (fall positive)",
            "value": mean_um,
            "statistic": {"name": "t of the mean over case days (cases summed per day)", "value": t_main}
            if t_main is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2"}
    sup_passed = None if diff is None else bool(diff > 0)
    sup = {"name": "unusual move of cases above median |forecast| minus below median (Welch t "
                   + (f"{t_sup:.3f}" if t_sup is not None else "n/a") + ")",
           "value": diff, "passed": sup_passed}

    # ---------- decision ----------
    if n_days < 30:
        status = "not observable"
        decided = f"only {n_days} distinct case days, fewer than the plan's minimum of 30"
    elif t_main is None:
        status = "inconclusive"
        decided = "the main t could not be computed, so it is not at or beyond +/-2"
    elif mean_um < 0 and t_main <= -2:
        status = "rejected"
        decided = "the main measure's mean is negative with a t of -2 or less (up days followed by further rises)"
    elif mean_um > 0 and t_main >= 2:
        if t_sup is not None and t_sup <= -2:
            status = "rejected"
            decided = "main t >= 2 but the supporting difference has a Welch t of -2 or less (the give-back shrinks with size)"
        elif diff is not None and diff > 0:
            status = "confirmed"
            decided = "the main mean is positive with t >= 2 and the larger-minus-smaller difference is above 0"
        else:
            status = "inconclusive"
            decided = "main t >= 2 but the supporting difference is at or below 0 (or missing) with a t above -2"
    else:
        status = "inconclusive"
        decided = "the main t lies between -2 and 2 (or its sign disagrees with the mean's)"

    return {"status": status,
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": main,
            "supporting_check": sup,
            "counts": counts,
            "decided_by": decided,
            "reading": reading}
