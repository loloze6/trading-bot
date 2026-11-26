import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    PPV = "debug_info.components.depth_below_high.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            f = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            r1 = c / c.shift(1) - 1.0
            r3 = c / c.shift(3) - 1.0
            active = f != 0
            computable = r1.notna() & r3.notna()
            n_active_uncomputable += int((active & ~computable).sum())
            act = active & computable
            n_active += int(act.sum())
            situ = (r1 > 0) & (r3 < 0) & (f < 0)
            n_agree += int((act & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The situation is checked as the regime rule rebuilt from closes inside each window "
               "(1-day return > 0 and 3-day return < 0, short side), on active bars whose 3 prior closes "
               "are in the window, without recomputing the falling-agitated profile whose 365-day volatility "
               "percentile needs history the record does not hold; the coin's mean daily return is the mean of "
               "all its 1-day returns pooled over its windows; the day-clustered t sums the cases' deviations "
               "per UTC day, with a D/(D-1) correction; the slope uses cases with a recorded post_pipeline_value.")

    threshold = "confirm: >= 100 cases, mean > 0 with t >= 2 and slope > 0; reject: >= 100 cases, mean < 0 with t <= -2"
    mm_name = "mean short-direction next-day excess return over cases (forecast < 0)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active),
                       "active bars agreeing": int(n_agree),
                       "active bars without enough prior closes": int(n_active_uncomputable)},
            "decided_by": ("Fewer than 90% of the active bars are up days with a negative 3-day return held short, "
                           "so the config's forecast does not follow the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_r = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            nxt = c.shift(-1) / c - 1.0
            all_r.append(nxt.dropna().values)
            per_win.append((d, nxt))
        if not all_r:
            continue
        pooled = np.concatenate(all_r)
        if pooled.size == 0:
            continue
        mu = float(np.mean(pooled))
        for d, nxt in per_win:
            f = pd.to_numeric(d[FC], errors="coerce")
            ppv = pd.to_numeric(d[PPV], errors="coerce") if PPV in d.columns else pd.Series(np.nan, index=d.index)
            mask = (f < 0) & nxt.notna()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in np.where(mask.values)[0]:
                rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].normalize(),
                    "x": -(float(nxt.iloc[i]) - mu),
                    "absf": abs(float(ppv.iloc[i])) if pd.notna(ppv.iloc[i]) else np.nan,
                })

    cases = pd.DataFrame(rows, columns=["coin", "day", "x", "absf"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean = float(cases["x"].mean()) if n_cases else None
    tval = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["x"] - mean
        s = dev.groupby(cases["day"]).sum().values
        var = float(np.sum(s ** 2)) / (n_cases ** 2) * (n_days / (n_days - 1))
        if var > 0:
            tval = float(mean / np.sqrt(var))

    slope = None
    sub = cases.dropna(subset=["absf", "x"])
    if len(sub) >= 3 and sub["absf"].nunique() > 1:
        slope = float(stats.linregress(sub["absf"].values, sub["x"].values).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"cases": n_cases, "days with cases": n_days, "cases in slope": int(len(sub))}

    if n_cases < 100:
        status = "not observable"
        decided = f"Fewer than 100 cases ({n_cases}), the plan's minimum count, so the data could not show the idea."
    elif mean is not None and tval is not None and mean > 0 and tval >= 2 and slope_pass is True:
        status = "confirmed"
        decided = "Confirm rule: at least 100 cases, mean short-direction excess return above 0 with t >= 2, and supporting slope above 0."
    elif mean is not None and tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject rule: at least 100 cases, mean short-direction excess return below 0 with t <= -2 (the coin rises after these days)."
    else:
        status = "inconclusive"
        if mean is not None and tval is not None and mean > 0 and tval >= 2:
            decided = "Inconclusive rule: a confirming mean whose supporting slope is not above 0."
        else:
            decided = "Inconclusive rule: t between -2 and 2 (or not computable) with at least 100 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": mm_name,
                         "value": mean,
                         "statistic": ({"name": "t of the mean, cases of one day taken together", "value": tval}
                                       if tval is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "slope of short excess next-day return on |forecast| (post_pipeline_value)",
                             "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
