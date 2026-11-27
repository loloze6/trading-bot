import numpy as np
import pandas as pd


def measure(bars):
    """Apply plan 077-01 (choppy-agitated wide low-close rebound, 1d) to its backtest record."""
    fc_col = "forecast"

    # ---------- 1. Situation check: wide day (range >= its 30-bar mean range), close in bottom quarter, long ----------
    n_active = 0
    n_agree = 0
    n_active_unchecked = 0

    # ---------- 2. Data for the criterion ----------
    case_rows = []  # (coin, day, excess, forecast)

    for coin, wins in bars.items():
        # coin's mean daily return over all its windows together (inside each window only)
        all_rets = []
        per_win = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            d["_next_ret"] = nxt
            all_rets.append(nxt.dropna().values)
            per_win[w] = d
        if not per_win:
            continue
        cat = np.concatenate(all_rets) if all_rets else np.array([])
        coin_mean = float(np.mean(cat)) if cat.size > 0 else np.nan

        for w, d in per_win.items():
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[fc_col], errors="coerce").fillna(0.0)

            rng = high - low
            mean_rng = rng.rolling(30, min_periods=30).mean()  # exclude_current 0: current bar included
            wide = rng / mean_rng.replace(0, np.nan)
            loc = (close - low) / rng.replace(0, np.nan)

            active = fc != 0
            checkable = active & wide.notna() & loc.notna()
            n_active += int(active.sum())
            n_active_unchecked += int((active & ~checkable).sum())
            situ = (wide >= 1.0) & (loc <= 0.25)
            agree = checkable & situ & (fc > 0)
            n_agree += int(agree.sum())

            # cases: forecast > 0, with a next-day return inside the window
            cases = (fc > 0) & d["_next_ret"].notna()
            if np.isfinite(coin_mean):
                ts = pd.to_datetime(d["timestamp"], utc=True)
                days = ts.dt.floor("D")
                for i in np.where(cases.values)[0]:
                    case_rows.append((coin, days.iloc[i], float(d["_next_ret"].iloc[i] - coin_mean),
                                      float(fc.iloc[i])))

    n_checked = n_active - n_active_unchecked
    agreement = (n_agree / n_checked) if n_checked > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The situation is checked on its core conditions (range / mean of the last 30 bar ranges, current bar "
               "included, at least 1.0; (close - low)/(high - low) at most 0.25; forecast positive) over active bars "
               "with 30 bars of in-window history, the code-added profile vetoes being only removals and not rebuildable "
               "from in-window bars; cases are all bars with forecast > 0 (every bar, horizon 1), the day-clustered t "
               "sums deviations per UTC day with a G/(G-1) correction, and the plan's 30-distinct-case-day minimum is "
               "treated as a minimum count (not observable).")

    main_name = "mean next-day excess return on case bars (forecast > 0)"
    main_thr = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    stat_name = "t of the mean, cases clustered by day"
    sup_name = "OLS slope of next-day excess return on forecast size"

    if agreement is None or not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars checked": int(n_checked),
                       "active bars in situation on long side": int(n_agree)},
            "decided_by": ("No active bar could be checked against the plan's situation."
                           if agreement is None else
                           "Fewer than 90 % of the active bars are wide days (range >= 30-day mean range) closing in "
                           "the bottom quarter of their range with a long forecast, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- criterion ----------
    if case_rows:
        cr = pd.DataFrame(case_rows, columns=["coin", "day", "excess", "fc"])
    else:
        cr = pd.DataFrame(columns=["coin", "day", "excess", "fc"])
    n_cases = int(len(cr))
    n_days = int(cr["day"].nunique()) if n_cases else 0

    mean_ex = float(cr["excess"].mean()) if n_cases else None
    t_val = None
    if n_cases > 0 and n_days > 1:
        dev = cr["excess"] - mean_ex
        S = dev.groupby(cr["day"]).sum().values
        G = len(S)
        var = (G / (G - 1.0)) * float(np.sum(S ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_ex / se) if se > 0 else None

    slope = None
    if n_cases >= 2:
        x = cr["fc"].values.astype(float)
        y = cr["excess"].values.astype(float)
        vx = np.var(x)
        if vx > 0:
            slope = float(np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2))
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"case bars": n_cases, "distinct case days": n_days}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and t_val >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "Mean next-day excess return above 0 with t >= 2 and slope on forecast size above 0."
        else:
            status = "inconclusive"
            decided = "A confirming mean (t >= 2) with a slope on forecast size at or below 0 is inconclusive."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean next-day excess return below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": None if t_val is None else {"name": stat_name, "value": t_val},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
