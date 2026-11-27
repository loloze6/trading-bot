import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    LHV = "debug_info.components.slide.last_history_value"

    # ---------- helpers ----------
    def window_frames():
        for coin in sorted(bars.keys()):
            for w in sorted(bars[coin].keys(), key=lambda s: (len(str(s)), str(s))):
                df = bars[coin][w]
                if df is None or len(df) == 0:
                    continue
                df = df.reset_index(drop=True).copy()
                yield coin, w, df

    # Unit of PriceEvolutionComponent: the plan reads it in percent (veto at +-10 on the 60-day return).
    # Check against the recorded 30-day raw values where they can be rebuilt from prices.
    ratios = []
    for coin, w, df in window_frames():
        if LHV in df.columns:
            c = pd.to_numeric(df["close"], errors="coerce")
            frac30 = c / c.shift(30) - 1.0
            v = pd.to_numeric(df[LHV], errors="coerce")
            m = v.notna() & frac30.notna() & (frac30.abs() > 1e-4)
            if m.any():
                ratios.extend((v[m] / frac30[m]).tolist())
    scale = 100.0
    if len(ratios) > 0:
        med = float(np.median(ratios))
        if np.isfinite(med) and abs(med - 1.0) < abs(med - 100.0):
            scale = 1.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, w, df in window_frames():
        c = pd.to_numeric(df["close"], errors="coerce")
        f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
        reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
        ret30_p = (c / c.shift(30) - 1.0) * scale
        ret60_p = (c / c.shift(60) - 1.0) * scale
        if LHV in df.columns:
            r30 = pd.to_numeric(df[LHV], errors="coerce")
            r30 = r30.where(r30.notna(), ret30_p)
        else:
            r30 = ret30_p
        fall = r30 < 0
        fall = fall.where(r30.notna(), reg == "trending")
        choppy = (ret60_p >= -10) & (ret60_p <= 10)
        choppy = choppy.where(ret60_p.notna(), reg != "chop")
        active = f != 0
        agree = active & fall.astype(bool) & choppy.astype(bool) & (f < 0)
        n_active += int(active.sum())
        n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual move in the short direction over 10 bars, top third of position size (fraction of price)"
    main_thr = "confirm: positive with day-clustered t >= 2; reject: negative with t <= -2; on >= 30 cases over >= 30 distinct days"
    reading = ("Situation = 30-day return < 0 (recorded raw value, else rebuilt from closes, else regime 'trending') and "
               "60-day return within [-10, 10] % (rebuilt from closes, else regime not 'chop'), short side; a case is the first "
               "bet bar (forecast rise on the short side of >= 2 from its lowest level since the last bet) in each 10-bar grid "
               "cell with a full 10-bar forward return in its window, position size is |postRebalance_current_allocation| on "
               "that bar, top/bottom thirds are cases at or above the 2/3 / at or below the 1/3 quantile of all cases pooled, "
               "drift is each coin's mean non-overlapping 10-bar return over all its windows, and t clusters cases by UTC date.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars in a 30-day fall within the "
                           "choppy profile, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. drift per coin ----------
    drift_samples = {}
    for coin, w, df in window_frames():
        c = pd.to_numeric(df["close"], errors="coerce").values
        for i in range(0, len(c) - H, H):
            if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                drift_samples.setdefault(coin, []).append(c[i + H] / c[i] - 1.0)
    drift = {k: float(np.mean(v)) for k, v in drift_samples.items() if len(v) > 0}

    # ---------- 3. cases ----------
    cases = []
    for coin, w, df in window_frames():
        c = pd.to_numeric(df["close"], errors="coerce").values
        f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
        alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").values
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        n = len(df)
        bet = np.zeros(n, dtype=bool)
        side = 0
        ref = 0.0
        for i in range(n):
            fi = f[i]
            s = int(np.sign(fi))
            if s == 0:
                side, ref = 0, 0.0
                continue
            if s != side:
                side, ref = s, 0.0
            mag = abs(fi)
            if s < 0 and mag - ref >= BAND:
                bet[i] = True
                ref = mag
            else:
                ref = min(ref, mag)
        for start in range(0, n, H):
            idx = [i for i in range(start, min(start + H, n)) if bet[i]]
            if not idx:
                continue
            i = idx[0]
            if i + H >= n or coin not in drift:
                continue
            if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0 and np.isfinite(alloc[i])):
                continue
            if pd.isna(ts.iloc[i]):
                continue
            r = c[i + H] / c[i] - 1.0
            cases.append({"day": ts.iloc[i].strftime("%Y-%m-%d"),
                          "size": abs(float(alloc[i])),
                          "u": -(r - drift[coin])})

    def clustered_t(sub):
        x = np.array([d["u"] for d in sub], dtype=float)
        m = len(x)
        if m < 2:
            return (float(np.mean(x)) if m else None), None
        mu = float(np.mean(x))
        dev = pd.Series(x - mu).groupby([d["day"] for d in sub]).sum().values
        se = float(np.sqrt(np.sum(dev ** 2))) / m
        return mu, (mu / se if se > 0 else None)

    if len(cases) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": "top-third minus bottom-third mean unusual move > 0", "value": None, "passed": None},
            "counts": {"top-third cases": 0, "top-third distinct days": 0, "all cases": 0},
            "decided_by": "No case exists, so the minimum of 30 top-third cases over 30 distinct days is not reached.",
            "reading": reading,
        }

    sizes = np.array([d["size"] for d in cases])
    q_hi = float(np.quantile(sizes, 2.0 / 3.0))
    q_lo = float(np.quantile(sizes, 1.0 / 3.0))
    top = [d for d in cases if d["size"] >= q_hi]
    bot = [d for d in cases if d["size"] <= q_lo]
    n_top = len(top)
    days_top = len(set(d["day"] for d in top))

    mu_top, t_top = clustered_t(top)
    mu_bot = float(np.mean([d["u"] for d in bot])) if bot else None
    diff = (mu_top - mu_bot) if (mu_top is not None and mu_bot is not None) else None
    sup_pass = (bool(diff > 0) if diff is not None else None)

    counts = {"top-third cases": int(n_top), "top-third distinct days": int(days_top),
              "bottom-third cases": int(len(bot)), "all cases": int(len(cases))}
    stat = {"name": "t of the mean, cases of one day taken together", "value": (float(t_top) if t_top is not None else None)}

    if n_top < 30 or days_top < 30:
        status = "not observable"
        decided = (f"The minimum of 30 top-third cases over 30 distinct days is not reached "
                   f"({n_top} cases, {days_top} days).")
    elif t_top is None:
        status = "inconclusive"
        decided = "The t of the top-third unusual move cannot be computed, so neither rule is met."
    elif mu_top > 0 and t_top >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The top-third unusual move is positive with t >= 2 on enough cases and days, and top minus bottom > 0."
        else:
            status = "inconclusive"
            decided = "The top-third unusual move confirms (t >= 2) but the convexity check (top minus bottom > 0) fails."
    elif mu_top < 0 and t_top <= -2:
        status = "rejected"
        decided = "The top-third unusual move is negative with t <= -2 on at least 30 cases over at least 30 days."
    else:
        status = "inconclusive"
        decided = "The top-third unusual move has a t between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": (float(mu_top) if mu_top is not None else None),
                         "statistic": stat,
                         "threshold": main_thr},
        "supporting_check": {"name": "top-third minus bottom-third mean unusual move > 0",
                             "value": (float(diff) if diff is not None else None),
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
