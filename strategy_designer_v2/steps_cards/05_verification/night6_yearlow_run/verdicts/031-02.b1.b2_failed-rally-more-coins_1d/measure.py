import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    COL_RAW = "debug_info.components.dist_low.last_history_value"
    COL_PP = "debug_info.components.dist_low.post_pipeline_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            regime = df["regime"].astype(str).values
            raw = pd.to_numeric(df[COL_RAW], errors="coerce").values if COL_RAW in df.columns else np.full(len(df), np.nan)
            pp = pd.to_numeric(df[COL_PP], errors="coerce").values if COL_PP in df.columns else np.full(len(df), np.nan)

            # 60-day return from prices where the window holds 60 prior bars; else the detector's own decision
            r60 = np.full(len(df), np.nan)
            if len(df) > 60:
                r60[60:] = close[60:] / close[:-60] - 1.0
            cond60 = np.where(np.isnan(r60), regime == "trending", r60 > 0)

            for i in range(len(df)):
                if fc[i] == 0 or np.isnan(fc[i]):
                    continue
                n_active += 1
                in_sit = bool(cond60[i]) and np.isfinite(raw[i]) and raw[i] >= 0 and np.isfinite(pp[i])
                if not in_sit:
                    continue
                # Expected side: short when nearer the yearly low than usual (standardised distance < 10),
                # long when farther (> 10).
                exp_side = np.sign(pp[i] - 10.0)
                if exp_side != 0 and np.sign(fc[i]) == exp_side:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90
    reading = ("The 60-day return is recomputed from closes inside each window where 60 prior bars exist and taken "
               "from the recorded regime otherwise; 'nearer than usual' is the standardised dist_low "
               "(post_pipeline_value) below 10; the coin's mean 20-bar return is the mean over the non-overlapping "
               "grid returns of all its windows; the main measure's value is the mean product per case and its t is "
               "the ordinary t of the per-day sums; per the instructions, fewer than 100 cases or 60 distinct days "
               "gives 'not observable'.")
    main_name = "mean of forecast/10 x (20-bar return - coin mean 20-bar return)"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of active bars have a forecast whose sign follows the plan's "
                           "situation (60-day return > 0) and side (short nearer the yearly low than usual, long farther); "
                           "90% is required."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            regime = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                grid_rets.append(r)
                if regime[i] == "trending" and np.isfinite(fc[i]) and fc[i] != 0:
                    coin_cases.append((ts.iloc[i].normalize(), float(fc[i]), r))
        if not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for day, f, r in coin_cases:
            rows.append({"day": day, "fc": f, "excess": r - mu, "prod": f / 10.0 * (r - mu)})

    cases = pd.DataFrame(rows, columns=["day", "fc", "excess", "prod"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_val = float(cases["prod"].mean()) if n_cases else None
    t_val = None
    if n_days >= 2:
        ds = cases.groupby("day")["prod"].sum().values
        sd = np.std(ds, ddof=1)
        if sd > 0:
            t_val = float(np.mean(ds) / (sd / np.sqrt(len(ds))))

    neg = cases[cases["fc"] < 0]
    sup_val = float(neg["excess"].mean()) if len(neg) else None
    sup_pass = (sup_val is not None) and (sup_val < 0)

    counts = {"cases": n_cases, "distinct days": n_days, "cases with forecast below 0": int(len(neg))}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (100 needed) on {n_days} distinct days (60 needed).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the main measure cannot be computed (no variation across days), so it meets neither rule."
    elif mean_val > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The main measure's mean is above 0 with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "The main measure's t confirms (mean > 0, t >= 2) but the supporting check fails."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The main measure's mean is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2 (or its sign disagrees with the mean's)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean (cases summed per day)", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 20-bar return on cases with forecast < 0 is below 0",
            "value": sup_val,
            "passed": bool(sup_pass) if sup_val is not None else None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
