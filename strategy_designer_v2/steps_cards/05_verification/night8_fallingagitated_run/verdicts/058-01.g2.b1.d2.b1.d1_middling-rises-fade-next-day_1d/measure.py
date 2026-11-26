import numpy as np
import pandas as pd


def measure(bars):
    LIN_RAW = "debug_info.components.rise_lin.last_history_value"
    LIN_POST = "debug_info.components.rise_lin.post_pipeline_value"
    BAND = 2.0

    # ---------- gather per-window frames ----------
    frames = []
    for coin, wins in bars.items():
        for win, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["coin"] = coin
            d["window"] = win
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            d["ret_prev"] = close / close.shift(1) - 1.0   # the day's own return (inside window)
            d["ret_next"] = close.shift(-1) / close - 1.0  # next-day return (inside window)
            d["fc"] = pd.to_numeric(d["forecast"], errors="coerce")

            # bets on the short side (holding-period definition, band 2 points)
            fc = d["fc"].fillna(0.0).values
            is_case = np.zeros(len(d), dtype=bool)
            anchor = 0.0  # lowest short size since last bet, 0 at window start / after flat or long
            for i in range(len(d)):
                f = fc[i]
                if f < 0:
                    size = -f
                    if size - anchor >= BAND - 1e-12:
                        is_case[i] = True
                        anchor = size
                    else:
                        anchor = min(anchor, size)
                else:
                    anchor = 0.0
            d["is_case"] = is_case
            frames.append(d)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean short-direction unusual next-day move of cases",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"cases": 0, "distinct case days": 0, "largest-rise days": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    allb = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    raw = pd.to_numeric(allb[LIN_RAW], errors="coerce") if LIN_RAW in allb.columns else pd.Series(np.nan, index=allb.index)
    up = np.where(raw.notna(), raw > 0, allb["ret_prev"] > 0)
    in_profile = allb["regime"].astype(str) == "unknown"
    active = allb["fc"].notna() & (allb["fc"] != 0)
    n_active = int(active.sum())
    agree = active & in_profile & pd.Series(up, index=allb.index) & (allb["fc"] < 0)
    agreement = float(agree.sum() / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    main_name = "mean short-direction unusual next-day move of cases (forecast falls >= 2 points)"
    main_thr = "confirm: mean > 0 with day-pooled t >= 2 (and supporting diff > 0); reject: mean < 0 with t <= -2"
    sup_name = "mean unusual move of middling cases (forecast <= -5) minus that of largest rises (rise_lin post <= -18)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bets on up days inside the "
                           "falling agitated profile (regime 'unknown'), as the Fidelity requires."),
            "reading": ("Profile taken from the recorded regime ('unknown' = neither veto fired); up day from the "
                        "rise_lin raw value's sign, or the close-to-close return where it is missing."),
        }

    # ---------- drift: coin mean 1-day return over all its windows ----------
    drift = allb.groupby("coin")["ret_next"].mean()
    allb["unusual_short"] = -(allb["ret_next"] - allb["coin"].map(drift))
    allb["day"] = allb["timestamp"].dt.floor("D")

    cases = allb[allb["is_case"] & allb["unusual_short"].notna()]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique())

    post = pd.to_numeric(allb[LIN_POST], errors="coerce") if LIN_POST in allb.columns else pd.Series(np.nan, index=allb.index)
    largest = allb[(post <= -18) & pd.Series(up, index=allb.index) & allb["unusual_short"].notna()]
    n_largest_days = int(largest["day"].nunique())
    middling = cases[cases["fc"] <= -5]

    # main measure and day-pooled t
    mean_main, t_main = None, None
    if n_cases > 0:
        x = cases["unusual_short"].values
        mean_main = float(x.mean())
        dev = pd.Series(x - mean_main, index=cases.index).groupby(cases["day"]).sum().values
        G = len(dev)
        if G > 1:
            se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n_cases
            t_main = float(mean_main / se) if se > 0 else None

    diff = None
    if len(middling) > 0 and len(largest) > 0:
        diff = float(middling["unusual_short"].mean() - largest["unusual_short"].mean())
    sup_pass = (diff > 0) if diff is not None else None

    counts = {"cases": n_cases, "distinct case days": n_days,
              "largest-rise days": n_largest_days, "middling cases": int(len(middling))}

    reading = ("Cases are short-side bets per the holding-period rule (forecast size rising >= 2 points from its "
               "lowest short size since the last bet, from 0 at a window's start or after a flat), on every bar "
               "since the grid is 1 bar; largest rises are up-day bars with rise_lin post_pipeline_value <= -18 "
               "whether or not they are cases, counted as distinct days; day-pooled t uses per-day summed "
               "deviations with a G/(G-1) factor.")

    if n_cases < 100 or n_days < 50 or n_largest_days < 20:
        status = "not observable"
        missing = []
        if n_cases < 100:
            missing.append(f"{n_cases} cases < 100")
        if n_days < 50:
            missing.append(f"{n_days} distinct days < 50")
        if n_largest_days < 20:
            missing.append(f"{n_largest_days} largest-rise days < 20")
        decided = "Minimum count not reached: " + "; ".join(missing) + "."
    elif mean_main is not None and t_main is not None and mean_main > 0 and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and the middling-minus-largest difference above 0."
    elif mean_main is not None and t_main is not None and mean_main < 0 and t_main <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: up days are followed by further rises beyond drift."
    else:
        status = "inconclusive"
        if mean_main is not None and t_main is not None and mean_main > 0 and t_main >= 2:
            decided = "Positive main measure with t >= 2 but the supporting difference is at or below 0 (or missing)."
        else:
            decided = "The main measure's t lies between -2 and 2 (neither confirm nor reject rule met)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_main,
            "statistic": ({"name": "t of the mean, cases pooled by day", "value": t_main}
                          if t_main is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
