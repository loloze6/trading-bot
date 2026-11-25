import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    LHV = "debug_info.components.break_dist.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin in sorted(bars.keys()):
        prepared[coin] = {}
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].copy()
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
            df = df.sort_values("timestamp").reset_index(drop=True)
            prepared[coin][w] = df
            high = df["high"].astype(float)
            close = df["close"].astype(float)
            prior_max = high.shift(1).rolling(20, min_periods=20).max()
            dist_px = (close - prior_max) / prior_max * 100.0
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
                dist = raw.where(raw.notna(), dist_px)
            else:
                dist = dist_px
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            situ = (dist > 0).fillna(False)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 5-bar move per long bet (return minus coin's normal 5-bar drift)"
    threshold = "confirm: mean > 0 with day-pooled t >= 2 and graded-size check passes; reject: mean < 0 with t <= -2"
    check_name = "graded size: mean unusual move of cases with forecast above the cases' median minus that at or below"
    reading = ("Bets are rises of the positive forecast of at least 2 points from its lowest level since the last bet "
               "(reset to 0 when flat), the first bet in each 5-bar cell counted from each window's first row; the "
               "normal drift is the mean of each coin's non-overlapping 5-bar returns on that grid over all windows; "
               "the t sums deviations per signal day (UTC date) with a D/(D-1) correction; the plan's 'fewer than 30 "
               "distinct case days' is applied as a minimum count, giving 'not observable'.")

    if agreement is None:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": check_name, "value": None, "passed": None},
            "counts": {"distinct case days": 0, "cases": 0},
            "decided_by": "No bar has a non-zero forecast, so fewer than 30 distinct case days.",
            "reading": reading,
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with the close above "
                           "the prior 20-bar high, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_rows = []
    for coin, wins in prepared.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)
            floor = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    floor = 0.0
                    continue
                if f - floor >= BAND:
                    floor = f
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n and np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0:
                        coin_cases.append({
                            "day": df["timestamp"].iloc[t].normalize(),
                            "ret": close[t + H] / close[t] - 1.0,
                            "forecast": float(f),
                        })
                else:
                    floor = min(floor, f)
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan
        for c in coin_cases:
            c["u"] = c["ret"] - drift
            c["coin"] = coin
            case_rows.append(c)

    cases = pd.DataFrame(case_rows, columns=["day", "ret", "forecast", "u", "coin"])
    cases = cases.dropna(subset=["u"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_stat = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["u"] - mean_u
        s_d = dev.groupby(cases["day"]).sum().values
        var = (n_days / (n_days - 1.0)) * np.sum(s_d ** 2) / (n_cases ** 2)
        if var > 0:
            t_stat = float(mean_u / np.sqrt(var))

    check_val = None
    check_pass = None
    if n_cases:
        med = cases["forecast"].median()
        hi = cases.loc[cases["forecast"] > med, "u"]
        lo = cases.loc[cases["forecast"] <= med, "u"]
        if len(hi) and len(lo):
            check_val = float(hi.mean() - lo.mean())
            check_pass = bool(check_val > 0)
        else:
            check_pass = False

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_stat >= 2:
        if check_pass:
            status = "confirmed"
            decided = "The mean unusual move is above 0 with t >= 2 and the graded-size check passes."
        else:
            status = "inconclusive"
            decided = "The mean unusual move is above 0 with t >= 2 but the graded-size check fails."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases pooled by day", "value": t_stat}
                          if t_stat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": check_name, "value": check_val, "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
