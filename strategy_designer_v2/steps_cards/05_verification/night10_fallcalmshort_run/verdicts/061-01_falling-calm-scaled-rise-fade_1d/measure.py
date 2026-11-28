import numpy as np
import pandas as pd


def _component_series(df, comp_id, field="last_history_value"):
    """Return the recorded value of a strategy component, NaN where it is not recorded."""
    flat = "debug_info.components.%s.%s" % (comp_id, field)
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    out = pd.Series(np.nan, index=df.index, dtype=float)
    if "debug_info.components" in df.columns:
        for idx, v in df["debug_info.components"].items():
            try:
                if isinstance(v, str):
                    import json
                    v = json.loads(v)
                if isinstance(v, dict) and comp_id in v and isinstance(v[comp_id], dict):
                    val = v[comp_id].get(field)
                    if val is not None:
                        out.at[idx] = float(val)
            except Exception:
                pass
    return out


def measure(bars):
    BAND = 2.0
    THRESH = 2.0
    H = 1

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            rec = _component_series(d, "scaled_rise", "last_history_value")
            r1 = close.pct_change()
            vol = r1.rolling(30, min_periods=30).std(ddof=1)
            recomputed = r1 / vol
            rise = rec.where(rec.notna(), recomputed)
            active = fc != 0
            situ = (rise >= THRESH - 1e-9) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
            prepared[(coin, w)] = (d, close, fc)

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    main_name = "mean next-day unusual move of short bets (drift removed, short direction)"
    thr_words = "confirm: mean > 0 with t >= 2 over >= 30 case-days and supporting check passing; reject: mean < 0 with t <= -2 over >= 30 case-days"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"active bars": n_active, "case-days": None},
            "decided_by": ("Fewer than 90% of the active bars are short bars with a 1-day scaled rise of at least 2 "
                           "standard deviations, the plan's situation and side." if n_active > 0 else
                           "The record has no active bar, so the config never takes the plan's short on large scaled rises."),
            "reading": "The situation is checked as a scaled rise >= 2 (recorded scaled_rise raw value, else recomputed from closes) with a negative forecast; the falling calm profile cannot be rebuilt inside the short windows and is not checked.",
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w in wins:
            d, close, fc = prepared[(coin, w)]
            fr = (close.shift(-H) / close - 1.0).iloc[::H]
            rets.append(fr.dropna())
        allr = pd.concat(rets) if rets else pd.Series(dtype=float)
        drift[coin] = float(allr.mean()) if len(allr) else np.nan

    # ---------- cases ----------
    rows = []
    for (coin, w), (d, close, fc) in prepared.items():
        fr = close.shift(-H) / close - 1.0
        ts = pd.to_datetime(d["timestamp"], utc=True)
        low = 0.0
        for i in range(len(d)):
            f = float(fc.iloc[i])
            mag = -f if f < 0 else 0.0
            if mag <= 0:
                low = 0.0
                continue
            low = min(low, mag)
            if mag - low >= BAND - 1e-12:
                low = mag
                if i % H == 0 and np.isfinite(fr.iloc[i]) and np.isfinite(drift[coin]):
                    rows.append({"day": ts.iloc[i].floor("D"),
                                 "x": -(float(fr.iloc[i]) - drift[coin]),
                                 "absf": abs(f)})
    cases = pd.DataFrame(rows, columns=["day", "x", "absf"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean = float(cases["x"].mean()) if n_cases else None
    tval = None
    if n_cases and n_days >= 2:
        dev = cases["x"] - mean
        sday = dev.groupby(cases["day"]).sum()
        var = (n_days / (n_days - 1.0)) * float((sday ** 2).sum()) / (n_cases ** 2)
        se = np.sqrt(var)
        if se > 0:
            tval = float(mean / se)

    # supporting check
    sup_val = None
    sup_pass = None
    if n_cases:
        med = float(cases["absf"].median())
        big = cases.loc[cases["absf"] > med, "x"]
        small = cases.loc[cases["absf"] <= med, "x"]
        if len(big) and len(small):
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"case-days": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = "Fewer than 30 case-days (%d), the plan's minimum count, so the data cannot show the idea." % n_days
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 over at least 30 case-days and the larger-forecast half beats the smaller half."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 over at least 30 case-days."
    elif mean > 0 and tval >= 2:
        status = "inconclusive"
        decided = "A confirming t with the supporting check failing is inconclusive under the plan."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean, cases' deviations summed per day", "value": tval}
                                       if tval is not None else None),
                         "threshold": thr_words},
        "supporting_check": {"name": "mean unusual move of larger-|forecast| half minus smaller half",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are short bets (a rise of the short forecast of at least 2 points from its low since the last bet) "
                    "on every bar, the mean is over cases and its t sums the cases' deviations per UTC day, the drift is the "
                    "coin's mean 1-day return over all its windows, and the supporting split puts |forecast| above the median "
                    "in the larger half and at or below it in the smaller half."),
    }
