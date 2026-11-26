import numpy as np
import pandas as pd


def measure(bars):
    DEPTH = "debug_info.components.depth.last_history_value"

    # ---------- collect per-bar data ----------
    rows = []
    drift = {}
    for coin, wins in bars.items():
        coin_next = []
        for w, df in wins.items():
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            r1 = close / close.shift(1) - 1.0
            vol30 = r1.rolling(30, min_periods=30).std()
            today_s = r1 / vol30
            # prior four-day return ending yesterday (sign only needed)
            fall4_px = close.shift(1) / close.shift(5) - 1.0
            if DEPTH in d.columns:
                fall4 = pd.to_numeric(d[DEPTH], errors="coerce")
                fall4 = fall4.where(fall4.notna(), fall4_px)
            else:
                fall4 = fall4_px
            nxt = close.shift(-1) / close - 1.0
            coin_next.append(nxt.dropna())
            out = pd.DataFrame({
                "coin": coin,
                "window": w,
                "day": d["timestamp"].dt.floor("D"),
                "forecast": pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0),
                "r1": r1,
                "today_s": today_s,
                "fall4": fall4,
                "nxt": nxt,
            })
            rows.append(out)
        if coin_next:
            allr = pd.concat(coin_next)
            drift[coin] = float(allr.mean()) if len(allr) else np.nan
    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": "No bars in the record.", "reading": "none",
        }
    allb = pd.concat(rows, ignore_index=True)

    # ---------- situation check ----------
    active = allb[allb["forecast"] != 0]
    verifiable = active[active["today_s"].notna() & active["fall4"].notna()]
    n_ver = len(verifiable)
    if n_ver > 0:
        in_sit = ((verifiable["today_s"] > 0) & (verifiable["today_s"] <= 1.0)
                  & (verifiable["fall4"] < 0) & (verifiable["forecast"] < 0))
        agreement = float(in_sit.mean())
    else:
        agreement = None

    reading = ("Situation checked as today's return above 0 and at most 1 standard deviation of the last 30 daily "
               "returns (ddof 1, today included), the recorded depth value (four-day scaled return to yesterday) below 0 "
               "and a short forecast, on active bars where 30 returns of history exist in the window, the falling-agitated "
               "profile being left to step 3's code; cases are all bars with forecast below 0 and a next bar in the window, "
               "drift is the coin's mean next-day return over all its windows, the day-clustered t uses per-day summed "
               "deviations with a G/(G-1) correction, and the deeper half is |forecast| strictly above the median, the "
               "shallower half at or below it; the plan's 'inconclusive' for too few cases is reported as 'not observable'.")

    if agreement is not None and agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"active bars checked": int(n_ver)},
            "decided_by": ("Fewer than 90% of active bars are modest one-day rises (0 < today <= 1 usual move) after a "
                           "four-day fall with a short forecast, as the plan's situation requires."),
            "reading": reading,
        }
    sit_passed = agreement is not None

    # ---------- main measure ----------
    cases = allb[(allb["forecast"] < 0) & allb["nxt"].notna()].copy()
    cases["drift"] = cases["coin"].map(drift)
    cases = cases[cases["drift"].notna()]
    cases["x"] = -(cases["nxt"] - cases["drift"])
    n = len(cases)
    n_days = int(cases["day"].nunique()) if n else 0
    counts = {"cases": int(n), "distinct days": n_days}

    mean = float(cases["x"].mean()) if n else None
    t = None
    if n >= 2 and n_days >= 2:
        dev = cases["x"] - mean
        S = dev.groupby(cases["day"]).sum()
        G = len(S)
        var = (S ** 2).sum() / (n ** 2) * G / (G - 1)
        if var > 0:
            t = float(mean / np.sqrt(var))

    # ---------- supporting check ----------
    diff = None
    if n:
        a = cases["forecast"].abs()
        med = a.median()
        deep = cases.loc[a > med, "x"]
        shallow = cases.loc[a <= med, "x"]
        if len(deep) and len(shallow):
            diff = float(deep.mean() - shallow.mean())
    sup_passed = None if diff is None else bool(diff > 0)

    main = {
        "name": "mean short-side next-day return minus the coin's drift",
        "value": mean,
        "statistic": None if t is None else {"name": "t of the mean, cases of a day taken together", "value": t},
        "threshold": "confirm: mean > 0 with t >= 2 (and supporting difference > 0); reject: mean < 0 with t <= -2",
    }
    sup = {"name": "deeper-half minus shallower-half mean short-side unusual move (split at median |forecast|)",
           "value": diff, "passed": sup_passed}

    def result(status, decided):
        return {
            "status": status,
            "situation_check": {"agreement": agreement, "passed": sit_passed},
            "main_measure": main, "supporting_check": sup,
            "counts": counts, "decided_by": decided, "reading": reading,
        }

    if n < 50 or n_days < 30:
        return result("not observable",
                      f"The plan's minimum of 50 cases on 30 distinct days is not reached ({n} cases, {n_days} days).")
    if t is None or mean is None:
        return result("inconclusive", "The t of the main mean could not be computed, so neither rule is met.")
    if mean > 0 and t >= 2:
        if sup_passed:
            return result("confirmed", "The main mean is above 0 with t >= 2 and the deeper-minus-shallower difference is above 0.")
        return result("inconclusive", "t >= 2 but the supporting difference is not above 0, which the plan calls inconclusive.")
    if mean < 0 and t <= -2:
        return result("rejected", "The main mean is below 0 with t <= -2.")
    return result("inconclusive", "The t of the main mean lies between -2 and 2, which the plan calls inconclusive.")
