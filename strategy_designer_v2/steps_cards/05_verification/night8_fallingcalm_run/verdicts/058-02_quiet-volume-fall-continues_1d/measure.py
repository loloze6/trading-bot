import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.quiet_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            reg = df["regime"].astype(str)
            # falling-calm profile = regime detector passed both vetoes -> "unknown";
            # deep fall on light volume = raw thin-volume-scaled return < 0; side short
            situ = (reg == "unknown") & raw.notna() & (raw < 0) & (f < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of drift-removed 5-bar return x -forecast/10 on non-overlapping grid bars with forecast < 0"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    reading_base = ("Situation taken as regime 'unknown' (the falling-calm profile passed) with raw component < 0 and a "
                    "short forecast; the per-day t is a day-clustered t of the case mean; the minimum is read as at "
                    "least 30 grid cases and at least 30 distinct days; the median split excludes cases equal to the "
                    "median; drift is the coin's mean grid 5-bar return over all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are short bars in the falling-calm profile with a "
                           "negative thin-volume-scaled 30-day return, as the Fidelity's situation requires."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in range(0, len(d) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append({"coin": coin, "day": str(ts.iloc[i].date()),
                                  "ret": c1 / c0 - 1.0, "f": f[i]})
        if coin_rows:
            cdf = pd.DataFrame(coin_rows)
            cdf["drift"] = cdf["ret"].mean()
            rows.append(cdf)

    if rows:
        g = pd.concat(rows, ignore_index=True)
    else:
        g = pd.DataFrame(columns=["coin", "day", "ret", "f", "drift"])
    cases = g[g["f"].notna() & (g["f"] < 0)].copy()
    cases["dr"] = cases["ret"] - cases["drift"]
    cases["val"] = cases["dr"] * (-cases["f"] / 10.0)

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days": n_days}

    # main measure: mean, day-clustered t
    mean_v = float(cases["val"].mean()) if n_cases else None
    t_v = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["val"] - mean_v
        S = dev.groupby(cases["day"]).sum().values
        G = len(S)
        var = (G / (G - 1.0)) * np.sum(S ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t_v = float(mean_v / se) if se > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        a = cases["f"].abs()
        med = a.median()
        hi = cases.loc[a > med, "dr"]
        lo = cases.loc[a < med, "dr"]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val < 0)

    main = {"name": main_name, "value": mean_v,
            "statistic": ({"name": "t of the mean, cases of one day summed", "value": t_v} if t_v is not None else None),
            "threshold": thr}
    sup = {"name": "drift-removed 5-bar return, |forecast| above median minus below",
           "value": sup_val, "passed": sup_pass}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"Minimum not reached: {n_cases} grid cases on {n_days} distinct days, "
                   "the plan needs at least 30 of each.")
    elif mean_v is None or t_v is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed, so neither confirm nor reject rule is met."
    elif mean_v > 0 and t_v >= 2:
        if sup_pass is True:
            status = "confirmed"
            decided = "Main measure mean > 0 with t >= 2 and the supporting check (above minus below < 0) passes."
        else:
            status = "inconclusive"
            decided = "Main measure meets the confirm rule but the supporting check fails, which the plan calls inconclusive."
    elif mean_v < 0 and t_v <= -2:
        status = "rejected"
        decided = "Main measure mean < 0 with t <= -2, the plan's reject rule."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2 (or its sign disagrees), the plan's inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
