import numpy as np
import pandas as pd


def measure(bars):
    BAND = 2.0
    H = 1
    MIN_CASES = 50
    MIN_DAYS = 30
    CLOSE_LOC_LEVEL = 0.75

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
        d = d.sort_values("timestamp").reset_index(drop=True)
        for c in ["open", "high", "low", "close", "forecast"]:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        return d

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = prep(df)
            prepared[coin][w] = d
            rng = d["high"] - d["low"]
            cl = (d["close"] - d["low"]) / rng.where(rng > 0)
            f = d["forecast"].fillna(0.0)
            active = f != 0
            situ = (cl >= CLOSE_LOC_LEVEL) & (f < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ.fillna(False)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading_check = ("The situation is checked as a close in the top quarter of the day's range, "
                     "(close-low)/(high-low) >= 0.75 from the prices, with a short forecast; the choppy-agitated "
                     "profile vetoes are not recomputed because their components are not recorded and need "
                     "more history than a window holds (vetoes only remove bars, they cannot add active bars)")

    main_name = "mean unusual move of the short cases over 1 day (next-day return minus coin drift, sign flipped)"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2 (and wider half beats narrower half); reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in the situation on the short side": n_agree},
            "decided_by": ("Fewer than 90% of the active bars are short bars closing in the top quarter of their "
                           "range: the config's forecast does not follow the plan's situation and side."),
            "reading": reading_check,
        }

    # ---------- 2. coin drift over all windows (1-bar non-overlapping grid = every bar) ----------
    drift = {}
    for coin, wins in prepared.items():
        rets = []
        for w, d in wins.items():
            c = d["close"].values
            if len(c) > H:
                r = c[H:] / c[:-H] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- 3. cases: short bets (rise of the short forecast by >= band) ----------
    case_u, case_f, case_day = [], [], []
    for coin, wins in prepared.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, d in wins.items():
            f = d["forecast"].fillna(0.0).values
            c = d["close"].values
            ts = d["timestamp"]
            ref = 0.0
            side = 0
            for i in range(len(d)):
                fi = f[i]
                s = 1 if fi > 0 else (-1 if fi < 0 else 0)
                if s != side:
                    ref = 0.0
                    side = s
                if s == 0:
                    ref = 0.0
                    continue
                m = abs(fi)
                is_bet = (m - ref) >= BAND
                if is_bet:
                    ref = m
                else:
                    ref = min(ref, m)
                if not is_bet or s != -1:
                    continue
                if i + H >= len(d):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                u = -(r - drift[coin])
                case_u.append(u)
                case_f.append(abs(fi))
                case_day.append(ts.iloc[i].date().isoformat() if pd.notna(ts.iloc[i]) else None)

    u = np.array(case_u, dtype=float)
    fa = np.array(case_f, dtype=float)
    days = pd.Series(case_day)
    n_cases = int(len(u))
    n_days = int(days.dropna().nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = float(np.mean(u)) if n_cases else None
    t_val = None
    if n_cases >= 2:
        dev = u - np.mean(u)
        D = pd.Series(dev).groupby(days.values).sum().values
        G = len(D)
        if G >= 2:
            var_mean = (G / (G - 1.0)) * np.sum(D ** 2) / (n_cases ** 2)
            se = np.sqrt(var_mean)
            t_val = float(mean_u / se) if se > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        med = float(np.median(fa))
        wide = u[fa >= med]
        narrow = u[fa < med]
        if len(wide) > 0 and len(narrow) > 0:
            sup_val = float(np.mean(wide) - np.mean(narrow))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False
    supporting = {"name": "wider-half minus narrower-half mean unusual move (split at median |forecast|)",
                  "value": sup_val, "passed": sup_pass}

    reading = (reading_check + "; cases are short bets (a rise of the short forecast of at least 2 points from its "
               "lowest level since the last bet) on every bar, the t clusters deviations by UTC day with a G/(G-1) "
               "correction, and the wider half is |forecast| at or above the median, the narrower half below it.")

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day taken together", "value": t_val}
            if t_val is not None else None,
            "threshold": main_thr}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (need 50) on {n_days} distinct days (need 30).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is above 0 with t >= 2 and the wider half beats the narrower half."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the wider half does not beat the narrower half, which the plan calls inconclusive."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2: the next day rises against the short beyond drift."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
