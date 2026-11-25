import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.rise_in_ranges.last_history_value"
    PPV = "debug_info.components.rise_in_ranges.post_pipeline_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            rng = (d["high"].astype(float) - d["low"].astype(float))
            # rebuild the raw value from prices where the record lacks it
            base = rng.shift(1).rolling(30, min_periods=30).mean()
            rise_px = (close - close.shift(1)).clip(lower=0) / base
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), rise_px)
            else:
                raw = rise_px
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            in_profile = d["regime"].astype(str) == "unknown"
            situation = (raw > 0) & in_profile
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "slope of next-day excess return on forecast (bars with forecast < 0)"
    thr = "confirm: slope > 0 with day-clustered t >= 2 (and supporting check); reject: slope < 0 with t <= -2"
    sup_name = "mean next-day unusual move in the short direction > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are up-days inside the falling agitated profile "
                           "with a short forecast, as the plan's Fidelity requires."),
            "reading": "The profile is read from the recorded regime ('unknown' = profile holds, 'chop' = vetoed); "
                       "an up-day is a raw rise_in_ranges value above 0.",
        }

    # ---------- 2. Criterion ----------
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        # coin's mean daily return over all windows
        all_r = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            all_r.append((c.shift(-1) / c - 1.0).dropna())
        allr = pd.concat(all_r) if all_r else pd.Series(dtype=float)
        if len(allr) == 0:
            continue
        drift = float(allr.mean())
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            nxt = c.shift(-1) / c - 1.0
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            x = pd.to_numeric(d[PPV], errors="coerce") if PPV in d.columns else pd.Series(np.nan, index=d.index)
            ts = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D")
            m = (fc < 0) & nxt.notna() & x.notna()
            xs.extend(x[m].tolist())
            ys.extend((nxt[m] - drift).tolist())
            days.extend(ts[m].tolist())

    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    days = pd.Series(days)
    n_cases = int(len(x))
    n_days = int(days.nunique()) if n_cases else 0

    reading = ("The profile is read from the recorded regime and an up-day from the raw value > 0; the slope's t is an "
               "OLS slope with standard error clustered by calendar day (correction G/(G-1)), the supporting check is "
               "the plain mean over all cases of -(next-day return - drift), and the plan's '30 independent days' "
               "minimum is the number of distinct days with a negative forecast, whose shortfall gives 'not observable'.")

    slope = None
    t = None
    sup_val = None
    if n_cases >= 3 and np.var(x) > 0:
        xc = x - x.mean()
        sxx = float((xc ** 2).sum())
        slope = float((xc * (y - y.mean())).sum() / sxx)
        a = y.mean() - slope * x.mean()
        e = y - a - slope * x
        g = pd.Series(xc * e).groupby(days.values).sum().values
        G = len(g)
        if G > 1:
            var = (G / (G - 1)) * float((g ** 2).sum()) / sxx ** 2
            t = float(slope / np.sqrt(var)) if var > 0 else None
    if n_cases > 0:
        sup_val = float(np.mean(-y))
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    counts = {"independent days with a negative forecast": n_days, "cases (bars with a negative forecast)": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} independent days with a negative forecast, fewer than the plan's minimum of 30."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed on the cases, so neither confirm nor reject is met."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean next-day unusual move in the short direction is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: larger rises are followed by larger next-day gains."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "The slope confirms (positive, t >= 2) but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": None if t is None else {"name": "OLS slope t, clustered by day", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
