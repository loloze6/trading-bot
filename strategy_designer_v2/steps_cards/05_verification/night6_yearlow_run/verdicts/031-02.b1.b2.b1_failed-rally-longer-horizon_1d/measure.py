import numpy as np
import pandas as pd


def measure(bars):
    H = 40
    FC = "forecast"
    LP_RAW = "debug_info.components.low_prox.last_history_value"
    LP_POST = "debug_info.components.low_prox.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            post = (pd.to_numeric(df[LP_POST], errors="coerce").values
                    if LP_POST in df.columns else np.full(len(df), np.nan))
            raw = (pd.to_numeric(df[LP_RAW], errors="coerce").values
                   if LP_RAW in df.columns else np.full(len(df), np.nan))
            for t in range(len(df)):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                # situation: 60-day close-to-close return above 0
                if t >= 60 and close[t - 60] > 0:
                    in_sit = close[t] / close[t - 60] - 1.0 > 0
                else:
                    in_sit = regime[t] == "mean_reversion"
                if not in_sit:
                    continue
                # expected side: short when nearer the 365-day low than usual (x > 10),
                # long when farther (x < 10); x = standardised proximity = -post (negated)
                if not np.isfinite(post[t]) or not np.isfinite(raw[t]) or raw[t] <= 0:
                    continue
                x = -post[t]
                exp_sign = np.sign(10.0 - x)
                if exp_sign != 0 and np.sign(f) == exp_sign:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x drift-removed 40-bar forward return on grid cases"
    thr = "confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2"
    reading = ("The 60-day return is recomputed from closes inside the window where 60 prior bars exist and taken from the "
               "recorded regime (mean_reversion) on earlier bars; the expected side is graded as the Fidelity's comparison "
               "says (short when the standardised low proximity is above its usual level 10, long when below, read from "
               "low_prox post_pipeline_value since the 365-bar standardise history is not in the record); grid cases are "
               "positions 0, 40, 80, ... of each window with a full 40-bar forward return inside the window; the drift is "
               "the coin's mean 40-bar return over the same grid of all its windows; the t is clustered by day (deviations "
               "summed per day); the plan's 'fewer than 30 grid cases on separate days' is applied as a minimum count of "
               "30 distinct days, reported as not observable; a check with no case at forecast <= -2 counts as failed.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are bars with a positive 60-day return whose forecast sign "
                           "matches the side of the low-proximity comparison (short when nearer the 365-day low than usual)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin drift: mean 40-bar return over the non-overlapping grid of all its windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df.sort_values("timestamp")["close"].astype(float).values
            for t in range(0, len(c) - H, H):
                if c[t] > 0 and np.isfinite(c[t]) and np.isfinite(c[t + H]):
                    rets.append(c[t + H] / c[t] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    rows = []
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for t in range(0, len(df) - H, H):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                ex = c[t + H] / c[t] - 1.0 - drift[coin]
                rows.append({"day": ts.iloc[t].normalize(), "fc": float(f),
                             "ex": ex, "prod": float(f) / 10.0 * ex})

    n_cases = len(rows)
    cases = pd.DataFrame(rows)
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_prod = float(cases["prod"].mean()) if n_cases else None
    t_stat = None
    if n_cases and n_days >= 2:
        dev = cases["prod"] - mean_prod
        D = dev.groupby(cases["day"]).sum().values
        G = len(D)
        se = np.sqrt(np.sum(D ** 2)) / n_cases * np.sqrt(G / (G - 1))
        if se > 0:
            t_stat = float(mean_prod / se)

    sub = cases[cases["fc"] <= -2] if n_cases else pd.DataFrame()
    n_short = int(len(sub))
    sup_val = float(sub["ex"].mean()) if n_short else None
    sup_pass = bool(sup_val is not None and sup_val < 0)

    counts = {"grid cases": int(n_cases), "grid cases on separate days": n_days,
              "cases with forecast <= -2": n_short, "active bars": int(n_active)}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} separate days among the grid cases, fewer than the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean product could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_prod > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean product is above 0 with t >= 2 and the drift-removed return at forecast <= -2 is below 0."
        else:
            status = "inconclusive"
            decided = "A t >= 2 with a failed supporting check (drift-removed return at forecast <= -2 not below 0) is inconclusive."
    elif mean_prod < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean product is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_prod,
                         "statistic": ({"name": "t of the mean, cases summed per day", "value": t_stat}
                                       if t_stat is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean drift-removed 40-bar return when forecast <= -2 below 0",
                             "value": sup_val, "passed": sup_pass if sup_val is not None else False},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
