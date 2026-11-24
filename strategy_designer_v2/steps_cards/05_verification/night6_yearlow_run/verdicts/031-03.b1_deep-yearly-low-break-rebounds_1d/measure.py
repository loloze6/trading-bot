import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    COMP = "depth"
    FLAT_COL = "debug_info.components.%s.last_history_value" % COMP

    def raw_depth(df):
        # Raw value of the config's strategy component "depth" (same settings as the detector's "low").
        if FLAT_COL in df.columns:
            return pd.to_numeric(df[FLAT_COL], errors="coerce")
        out = pd.Series(np.nan, index=df.index, dtype=float)
        if "debug_info.components" in df.columns:
            for idx, v in df["debug_info.components"].items():
                d = v
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(COMP)
                    if isinstance(c, dict):
                        val = c.get("last_history_value")
                        try:
                            out.loc[idx] = float(val)
                        except (TypeError, ValueError):
                            pass
        return out

    def bet_flags(fc):
        # A bet: a rise of the forecast on its side of at least the band,
        # measured from its lowest level on that side since the last bet (from 0 after flat / side change).
        flags = np.zeros(len(fc), dtype=bool)
        side, ref = 0, 0.0
        for i, f in enumerate(fc):
            if not np.isfinite(f) or f == 0:
                side, ref = 0, 0.0
                continue
            s = 1 if f > 0 else -1
            if s != side:
                side, ref = s, 0.0
            mag = abs(f)
            if mag - ref >= BAND:
                flags[i] = True
                ref = mag
            else:
                ref = min(ref, mag)
        return flags

    # ---------- 1. situation check ----------
    n_active, n_agree = 0, 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            dep = raw_depth(df).values
            active = fc != 0
            situ = np.isfinite(dep) & (dep < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "mean unusual move per case over 10 bars (return from signal close minus coin's normal 10-bar drift)"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2; else inconclusive; at least 30 distinct case days"
    sup_name = "mean unusual move of cases with forecast above the median case forecast minus those at or below"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars whose close is below "
                           "the prior 365-day closing low (depth raw value < 0), as the Fidelity's situation and side require."
                           if n_active > 0 else "The record has no active bars, so the situation cannot be matched."),
            "reading": "The situation is read from the recorded raw value of the strategy component 'depth' (same settings as the detector's 'low'); an active bar without it counts as outside the situation.",
        }

    # ---------- 2. criterion ----------
    # normal 10-bar drift per coin: mean of non-overlapping 10-bar returns over all its windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual, forecast)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            flags = bet_flags(fc)
            seen_cells = set()
            for i in np.where(flags)[0]:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= len(c):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                if not np.isfinite(drift[coin]):
                    continue
                direction = 1.0 if fc[i] > 0 else -1.0
                u = direction * ((c[i + H] / c[i] - 1.0) - drift[coin])
                cases.append((ts.iloc[i].strftime("%Y-%m-%d"), u, float(fc[i])))

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)

    mean_u, t_u = None, None
    if n_cases > 0:
        u = np.array([x[1] for x in cases])
        mean_u = float(u.mean())
        if n_days >= 2:
            dev = pd.Series(u - mean_u).groupby([x[0] for x in cases]).sum().values
            var = (n_days / (n_days - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
            if var > 0:
                t_u = float(mean_u / np.sqrt(var))

    sup_val, sup_pass = None, None
    if n_cases > 0:
        f = np.array([x[2] for x in cases])
        u = np.array([x[1] for x in cases])
        med = np.median(f)
        hi, lo = u[f > med], u[f <= med]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = "Fewer than 30 distinct case days pooled over all coins and windows (%d), the plan's minimum." % n_days
    elif t_u is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_u >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and deeper breaks show a larger unusual move (supporting check above 0)."
    elif mean_u > 0 and t_u >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails (above-median forecast cases do not show a larger unusual move), which the plan calls inconclusive."
    elif mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: the coin falls more than its drift after a break of the yearly low."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_u} if t_u is not None else None),
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first bet (forecast rise of at least 2 points on its side) in each 10-bar grid cell of a window, "
                    "dropped when its 10-bar return would leave the window; the normal drift is the coin's mean non-overlapping "
                    "10-bar return over all its windows; the plan's 'count under 30 distinct case days' is applied as the minimum "
                    "count giving 'not observable'."),
    }
