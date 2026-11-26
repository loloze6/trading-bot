import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RR_MAX = 0.6667
    FLAT_MIN = 0.9
    COL_RAW = "debug_info.components.prior_rise.last_history_value"

    def prep(df):
        d = df.copy()
        if "timestamp" in d.columns:
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            d = d.sort_values("timestamp")
        d = d.reset_index(drop=True)
        for c in ["open", "high", "low", "close", "forecast"]:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        return d

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_unknown = 0
    prepared = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = prep(df)
            prepared[(coin, w)] = d
            o, h, l, c = d["open"], d["high"], d["low"], d["close"]
            rng = h - l
            # rise6: recorded raw value where present, else from prices
            rise_px = c / c.shift(6) - 1.0
            if COL_RAW in d.columns:
                raw = pd.to_numeric(d[COL_RAW], errors="coerce")
                rise = raw.where(raw.notna(), rise_px)
            else:
                rise = rise_px
            mean20 = rng.rolling(20, min_periods=20).mean()
            rr = mean20 / rng.replace(0, np.nan)
            flat = 1.0 - (c - o).abs() / rng.replace(0, np.nan)
            known = rise.notna() & rr.notna() & flat.notna()
            situ = (rise > 0) & (rr <= RR_MAX + 1e-9) & (flat >= FLAT_MIN - 1e-9)
            f = d["forecast"].fillna(0.0)
            active = f != 0
            n_unknown += int((active & ~known).sum())
            act_k = active & known
            n_active += int(act_k.sum())
            n_agree += int((act_k & situ & (f > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean unusual 3-day move per case (long), before costs"
    thr = "confirm: mean > 0 with t >= 2 and positive slope; reject: mean < 0 with t <= -2"
    reading_check = ("active bars whose 20-day mean range cannot be rebuilt from the window's own prices "
                     "(the first 19 bars of a window) are left out of the agreement share")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active), "active bars not checkable": int(n_unknown)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars of the plan's situation "
                           "(6-day rise > 0, 20-day mean range / day range <= 0.667, body <= 10% of range)."),
            "reading": reading_check + ".",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean of non-overlapping 3-bar returns over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w in wins:
            d = prepared.get((coin, w))
            if d is None:
                continue
            c = d["close"].values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual, entry_forecast)
    for (coin, w), d in prepared.items():
        f = d["forecast"].fillna(0.0).values
        c = d["close"].values
        ts = d["timestamp"] if "timestamp" in d.columns else pd.Series(range(len(d)))
        base = 0.0
        prev = 0.0
        bets = []
        for i in range(len(f)):
            fi = f[i]
            if fi <= 0:
                base = 0.0
            else:
                if prev <= 0:
                    base = 0.0
                if fi - base >= BAND:
                    bets.append(i)
                    base = fi
                else:
                    base = min(base, fi)
            prev = fi
        seen = set()
        for i in bets:
            cell = i // H
            if cell in seen:
                continue
            seen.add(cell)
            if i + H >= len(c):
                continue
            if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                continue
            dr = drift.get(coin, np.nan)
            if not np.isfinite(dr):
                continue
            u = c[i + H] / c[i] - 1.0 - dr
            t = ts.iloc[i]
            day = pd.Timestamp(t).strftime("%Y-%m-%d") if isinstance(t, pd.Timestamp) else str(t)
            cases.append((day, float(u), float(f[i])))

    n_cases = len(cases)
    days = sorted(set(cs[0] for cs in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_u = None
    t_stat = None
    slope = None
    if n_cases > 0:
        u = np.array([cs[1] for cs in cases])
        x = np.array([cs[2] for cs in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby([cs[0] for cs in cases]).sum().values
        if n_days > 1:
            var = (dev ** 2).sum() / n_cases ** 2 * n_days / (n_days - 1)
            if var > 0:
                t_stat = float(mean_u / np.sqrt(var))
        if n_cases >= 2 and np.unique(x).size >= 2:
            slope = float(np.polyfit(x, u, 1)[0])

    reading = (reading_check + "; a case is the first bet (forecast rise of >= 2 points from its low since the last "
               "bet, from 0 after flat) in each 3-bar grid cell of its window, its return taken from the signal bar's "
               "close, the t clusters cases by calendar day (deviations summed per day, D/(D-1) correction), and the "
               "plan's 'fewer than 30 cases or days' rule is applied as the minimum count giving 'not observable'.")

    supp = {"name": "OLS slope of unusual move on entry forecast",
            "value": slope, "passed": (None if slope is None else bool(slope > 0))}
    main = {"name": main_name, "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean, cases clustered by day", "value": t_stat},
            "threshold": thr}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"Minimum not reached: {n_cases} cases on {n_days} distinct days, the plan needs at least 30 of each.")
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_stat >= 2 and slope is not None and slope > 0:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and a positive slope on the entry forecast (confirm rule)."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 (reject rule)."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on the entry forecast is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
