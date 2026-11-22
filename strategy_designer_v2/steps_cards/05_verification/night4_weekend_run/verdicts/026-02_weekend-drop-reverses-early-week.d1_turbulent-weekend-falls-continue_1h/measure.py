import numpy as np
import pandas as pd


def measure(bars):
    H = 48
    RAW = "debug_info.components.wkend_fall_volratio.last_history_value"

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        d["close"] = pd.to_numeric(d["close"], errors="coerce")
        d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
        return d

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = prep(df)
            prepared[coin][w] = d
            ts = d["timestamp"]
            # Bar stamped Sunday 23:00 UTC (start time), closing at Monday 00:00
            is_slot = (ts.dt.dayofweek == 6) & (ts.dt.hour == 23)
            # Weekend return: the 48-bar return up to this bar's close, within the window
            ret48 = d["close"] / d["close"].shift(H) - 1.0
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            fell = raw.where(raw.notna(), ret48) < 0
            situation = is_slot & fell.fillna(False)
            active = d["forecast"] != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (d["forecast"] < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of mean |forecast|/10 x short-direction 48-bar excess return, cases forecast <= -2"
    threshold = "t >= 2 over at least 100 cases confirms (with check); t <= -2 over at least 100 cases rejects"
    reading = ("Situation bars are those stamped Sunday 23:00 UTC (start time) whose raw component value (or, if missing, "
               "48-bar price return) is negative; drift is each coin's mean 48-bar return on the grid 0,48,... of every "
               "window pooled; cases are bars with forecast <= -2 whose t+48 bar is in the same window, pooled over coins; "
               "the upper half is |forecast| strictly above the median of case |forecast|, the lower half the rest.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of active (non-zero forecast) bars are Sunday 23:00 bars after a weekend fall "
                           "with a short forecast, so the config does not do what the Fidelity situation and side say."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    vals, absf, excess_short = [], [], []
    for coin, wins in prepared.items():
        grid = []
        for w, d in wins.items():
            c = d["close"].values
            for i in range(0, len(c) - H, H):
                a, b = c[i], c[i + H]
                if np.isfinite(a) and np.isfinite(b) and a != 0:
                    grid.append(b / a - 1.0)
        if len(grid) == 0:
            continue
        drift = float(np.mean(grid))
        for w, d in wins.items():
            c = d["close"].values
            f = d["forecast"].values
            n = len(d)
            for i in np.where(f <= -2)[0]:
                if i + H >= n:
                    continue
                a, b = c[i], c[i + H]
                if not (np.isfinite(a) and np.isfinite(b)) or a == 0:
                    continue
                r = b / a - 1.0
                ex = -(r - drift)
                vals.append(abs(f[i]) / 10.0 * ex)
                absf.append(abs(f[i]))
                excess_short.append(ex)

    vals = np.array(vals, dtype=float)
    absf = np.array(absf, dtype=float)
    excess_short = np.array(excess_short, dtype=float)
    n_cases = int(len(vals))

    mean_val = float(np.mean(vals)) if n_cases > 0 else None
    t = None
    if n_cases >= 2:
        sd = float(np.std(vals, ddof=1))
        t = float(mean_val / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    check_pass = None
    n_up = n_lo = 0
    if n_cases >= 2:
        med = float(np.median(absf))
        up = absf > med
        lo = ~up
        n_up, n_lo = int(up.sum()), int(lo.sum())
        if n_up > 0 and n_lo > 0:
            diff = float(np.mean(excess_short[up]) - np.mean(excess_short[lo]))
            check_pass = bool(diff > 0)

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} cases with forecast <= -2, fewer than the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither confirm nor reject rule is met."
    elif t >= 2 and check_pass:
        status = "confirmed"
        decided = "t >= 2 over at least 100 cases and the upper |forecast| half's short excess exceeds the lower half's."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 over at least 100 cases but the supporting check fails, which the plan calls inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "t <= -2 over at least 100 cases: weekend falls are followed by excess rises early in the week."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 over at least 100 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_val,
                         "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "upper minus lower |forecast| half mean short excess return",
                             "value": diff, "passed": check_pass},
        "counts": {"cases": n_cases, "upper half cases": n_up, "lower half cases": n_lo},
        "decided_by": decided,
        "reading": reading,
    }
