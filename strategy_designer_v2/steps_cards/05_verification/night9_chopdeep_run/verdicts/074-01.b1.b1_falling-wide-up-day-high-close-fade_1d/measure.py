import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    WCOL = "debug_info.components.width.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    n_agree_fallback = 0

    per_coin_rets = {}
    case_rows = []

    for coin, wins in bars.items():
        coin_rets = []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            fc = d["forecast"].astype(float)
            regime = d["regime"].astype(str)

            # Situation, recomputed inside the window only
            ret1 = close / close.shift(1) - 1.0
            rng = high - low
            mean_rng = rng.rolling(20, min_periods=20).mean()
            rmult = rng / mean_rng
            if WCOL in d.columns:
                rec = pd.to_numeric(d[WCOL], errors="coerce")
                rmult = rec.where(rec.notna(), rmult)
            trend60 = (close / close.shift(60) - 1.0) * 100.0

            up = ret1 > 0
            wide = rmult >= 1.5
            falling = trend60 < -10
            computable = ret1.notna() & rmult.notna() & trend60.notna()
            situation = up & wide & falling

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok_c = active & computable
            n_agree += int((ok_c & situation & (fc < 0)).sum())
            unc = active & ~computable
            n_active_uncomputable += int(unc.sum())
            # Bars whose 60-day trend is not in the window: up day and width
            # still checked where computable, falling taken from the detector's regime
            part_ok = (
                (up | ret1.isna())
                & (wide | rmult.isna())
                & (regime == "mean_reversion")
                & (fc < 0)
            )
            n_agree_fallback += int((unc & part_ok).sum())

            # Next-day returns inside the window
            fwd = close.shift(-1) / close - 1.0
            coin_rets.append(fwd.dropna().values)

            is_case = (regime == "mean_reversion") & (fc <= -2) & fwd.notna()
            for i in np.where(is_case.values)[0]:
                case_rows.append({
                    "coin": coin,
                    "day": pd.Timestamp(d["timestamp"].iloc[i]).floor("D"),
                    "ret": float(fwd.iloc[i]),
                    "absf": abs(float(fc.iloc[i])),
                })
        per_coin_rets[coin] = np.concatenate(coin_rets) if coin_rets else np.array([])

    if n_active == 0:
        agreement = None
        passed = False
    else:
        agreement = (n_agree + n_agree_fallback) / n_active
        passed = agreement >= 0.9

    situation_check = {"agreement": None if agreement is None else float(agreement),
                       "passed": bool(passed)}

    reading = ("Falling market read as the 60-bar simple return in percent below -10 "
               "(the veto at gte -10), recomputed inside each window, and the detector's "
               "regime used for it only where 60 bars of history are missing. The range "
               "multiple is taken as high-low over its 20-bar mean including the day, or "
               "the recorded width where present. Horizon 1, so every bar is on the grid. "
               "The day-clustered t uses deviations summed per UTC day with a G/(G-1) "
               "correction. The larger half is |forecast| above the median and the smaller "
               "half the rest. The plan's 'fewer than 30 distinct days' rule is applied as "
               "the minimum count, giving 'not observable'.")

    main_name = "mean short-direction excess next-day return"
    main_thr = "confirm: >0 with day-clustered t >= 2 (and larger-minus-smaller > 0); reject: <0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The active bars are not, at 90% or more, short bars where the 60-day "
                           "trend is below -10%, the close is above the prior close and the range "
                           "is at least 1.5x its 20-day mean range."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = pd.DataFrame(case_rows, columns=["coin", "day", "ret", "absf"])
    mu = {c: (float(np.mean(r)) if len(r) else np.nan) for c, r in per_coin_rets.items()}
    if len(cases):
        cases["mu"] = cases["coin"].map(mu)
        cases["x"] = -(cases["ret"] - cases["mu"])
        cases = cases.dropna(subset=["x"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"distinct days with cases": n_days, "cases": n_cases}

    mean_x = float(cases["x"].mean()) if n_cases else None
    t_main = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["x"] - mean_x
        dsum = dev.groupby(cases["day"]).sum().values
        G = len(dsum)
        var = np.sum(dsum ** 2) / (n_cases ** 2) * (G / (G - 1))
        if var > 0:
            t_main = float(mean_x / np.sqrt(var))

    sup_val = None
    sup_t = None
    sup_pass = None
    if n_cases >= 2:
        med = float(cases["absf"].median())
        big = cases.loc[cases["absf"] > med, "x"].values
        small = cases.loc[cases["absf"] <= med, "x"].values
        if len(big) >= 1 and len(small) >= 1:
            sup_val = float(np.mean(big) - np.mean(small))
            if len(big) >= 2 and len(small) >= 2:
                tt = stats.ttest_ind(big, small, equal_var=False)
                sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
            sup_pass = bool(sup_val > 0)
    counts["larger-forecast half cases"] = int((cases["absf"] > cases["absf"].median()).sum()) if n_cases else 0
    counts["smaller-forecast half cases"] = n_cases - counts["larger-forecast half cases"]

    main = {"name": main_name, "value": mean_x,
            "statistic": None if t_main is None else {"name": "day-clustered t of the mean", "value": t_main},
            "threshold": main_thr}
    support = {"name": "larger-|forecast| half minus smaller half mean excess (Welch t "
                       + ("n/a" if sup_t is None else f"{sup_t:.3f}") + ")",
               "value": sup_val, "passed": sup_pass}

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 distinct days with cases ({n_days}), the plan's minimum."
    elif t_main is None or mean_x is None:
        status = "inconclusive"
        decided = "The main t could not be computed, so it does not meet the confirm or reject rule."
    elif mean_x > 0 and t_main >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean short-direction excess > 0 with t >= 2 and larger-minus-smaller half > 0."
        else:
            status = "inconclusive"
            decided = "Main confirm met but the larger-minus-smaller difference is <= 0 (or not computable): inconclusive."
    elif mean_x < 0 and t_main <= -2:
        status = "rejected"
        decided = "Mean short-direction excess < 0 with t <= -2: these days rise more than the drift next day."
    else:
        status = "inconclusive"
        decided = "Main t between -2 and 2 (or sign and t disagree): neither confirm nor reject."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
