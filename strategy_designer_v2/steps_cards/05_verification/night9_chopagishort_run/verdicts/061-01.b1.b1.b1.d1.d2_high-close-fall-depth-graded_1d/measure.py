import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0

    def get_comp(df, cid, field="last_history_value"):
        col = f"debug_info.components.{cid}.{field}"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].tolist():
                val = np.nan
                if isinstance(v, dict):
                    c = v.get(cid)
                    if isinstance(c, dict):
                        x = c.get(field)
                        try:
                            val = float(x) if x is not None else np.nan
                        except (TypeError, ValueError):
                            val = np.nan
                out.append(val)
            return np.array(out, dtype=float)
        return np.full(len(df), np.nan)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            hi = df["high"].to_numpy(dtype=float)
            lo = df["low"].to_numpy(dtype=float)
            cl = df["close"].to_numpy(dtype=float)
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                loc = np.where(rng > 0, (cl - lo) / rng, np.nan)
            r5_price = np.full(len(df), np.nan)
            if len(df) > H:
                r5_price[H:] = cl[H:] / cl[:-H] - 1.0
            r5_rec = get_comp(df, "fall5")
            r5 = np.where(np.isfinite(r5_rec), r5_rec, r5_price)
            active = np.isfinite(f) & (f != 0)
            sit = (loc >= 0.75) & (r5 < 0) & (f < 0)
            n_active += int(active.sum())
            n_agree += int((active & sit).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    main_name = "mean unusual 5-bar move of short cases (short direction)"
    thr = "confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars with a close in the top quarter of the day's range and a negative 5-day return, as the plan's situation requires.",
            "reading": "Situation computed from prices (close location (close-low)/(high-low) >= 0.75) and the recorded fall5 raw value (or the 5-bar price return) < 0, with a negative forecast; the profile vetoes are not re-checked.",
        }

    # ---------- cases ----------
    cases = []  # (coin, unusual, abs_forecast, day)
    for coin, wins in bars.items():
        # normal drift over all windows of the coin
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            cl = df["close"].to_numpy(dtype=float)
            for i in range(0, len(cl) - H, H):
                r = cl[i + H] / cl[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append(df)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for df in prepared:
            cl = df["close"].to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            # short bets: rise of the short forecast by >= band from its lowest level since last bet
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for t in range(n):
                ft = f[t]
                if not np.isfinite(ft) or ft >= 0:
                    ref = 0.0
                    continue
                s = -ft
                if s - ref >= BAND:
                    bet[t] = True
                    ref = s
                else:
                    ref = min(ref, s)
            for start in range(0, n, H):
                idx = [t for t in range(start, min(start + H, n)) if bet[t]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                r = cl[t + H] / cl[t] - 1.0
                if not np.isfinite(r):
                    continue
                unusual = -(r - drift)
                cases.append((coin, unusual, abs(f[t]), ts.iloc[t].strftime("%Y-%m-%d")))

    n_cases = len(cases)
    days = sorted(set(c[3] for c in cases))
    n_days = len(days)
    counts = {"cases": n_cases, "distinct days": n_days}
    reading = ("A case is the first short bet (a rise of the short forecast of at least 2 points) in each 5-bar grid cell "
               "counted from each window's first row; the t uses deviations from the mean summed per UTC day with no "
               "small-sample correction; the median split puts |forecast| above the median in the larger half and the rest "
               "in the smaller half; the situation check takes r5 from the recorded fall5 raw value and does not re-check the profile.")

    mean_u = None
    tstat = None
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        x = np.array([c[1] for c in cases], dtype=float)
        mean_u = float(x.mean())
        dev = pd.Series(x - mean_u).groupby([c[3] for c in cases]).sum().to_numpy()
        se = np.sqrt(np.sum(dev ** 2)) / n_cases
        tstat = float(mean_u / se) if se > 0 else None
        a = np.array([c[2] for c in cases], dtype=float)
        med = np.median(a)
        big = x[a > med]
        small = x[a <= med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": main_name, "value": mean_u,
            "statistic": ({"name": "t of the mean, cases summed per day", "value": tstat} if tstat is not None else None),
            "threshold": thr}
    sup = {"name": "mean unusual move, larger |forecast| half minus smaller half", "value": sup_val, "passed": sup_pass}
    sc = {"agreement": (float(agreement) if agreement is not None else None), "passed": True}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = f"Minimum count not reached: {n_cases} cases on {n_days} distinct days (the plan needs at least 30 of each)."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t could not be computed (zero standard error), so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule met: the mean unusual move is above 0 with t >= 2 and the larger-|forecast| half beats the smaller half."
    elif mean_u > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "Inconclusive rule: t >= 2 but the supporting check (larger half minus smaller half above 0) fails."
    elif mean_u < 0 and tstat <= -2:
        status = "rejected"
        decided = "Reject rule met: the mean unusual move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
