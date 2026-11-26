import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    NH_RAW = "debug_info.components.near_high.last_history_value"
    NH_POST = "debug_info.components.near_high.post_pipeline_value"
    STD_WIN, STD_MIN = 60, 20

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            raw = (pd.to_numeric(df[NH_RAW], errors="coerce").to_numpy(dtype=float)
                   if NH_RAW in df.columns else np.full(len(df), np.nan))
            post = (pd.to_numeric(df[NH_POST], errors="coerce").to_numpy(dtype=float)
                    if NH_POST in df.columns else np.full(len(df), np.nan))
            n = len(df)
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                exp_side = 0
                # Rebuild standardise from raw values when the window holds the 60 prior raw values.
                if i >= STD_WIN and np.isfinite(raw[i]):
                    past = raw[i - STD_WIN:i]
                    past = past[np.isfinite(past)]
                    if len(past) >= STD_MIN:
                        m = np.mean(np.abs(past))
                        if m == 0:
                            s = 0.0
                        else:
                            s = float(np.clip(raw[i] * 10.0 / m, -20, 20))
                        comb = (s + 10.0) / 2.0
                        if comb > 1e-9:
                            exp_side = 1
                        elif comb < -1e-9:
                            exp_side = -1
                    else:
                        exp_side = 1  # standardise gives 0 -> offset only -> long
                else:
                    # Prior raw values not in the record (warm-up): use the recorded value after transforms.
                    if np.isfinite(post[i]):
                        comb = (post[i] + 10.0) / 2.0
                        if comb > 1e-9:
                            exp_side = 1
                        elif comb < -1e-9:
                            exp_side = -1
                if exp_side != 0 and np.sign(f) == exp_side:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The situation is the close nearer its 28-day closing high than its mean absolute distance over the 60 "
               "prior raw values (long) and, by the graded forecast, farther than usual (short), rebuilt from "
               "last_history_value where 60 prior values are in the window and from post_pipeline_value otherwise; "
               "the grid is positions 0,10,20,... of each window with the 10-bar return inside the window, all grid "
               "cells (forecast 0 included, gain 0) are cases, the coin's mean 10-bar return is the mean of its grid "
               "returns over all windows, the t sums each day's deviations, and the plan's minimum counts not "
               "reached give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean timing gain forecast/10 x excess 10-bar return",
                             "value": None, "statistic": None,
                             "threshold": "positive with t >= 2 to confirm, negative with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the active bars have the forecast's sign equal to the side of the "
                           "plan's situation (long when nearer the 28-day high than the 60-day usual distance, short "
                           "when farther)."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1, f = close[i], close[i + H], fc[i]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 <= 0:
                    continue
                coin_rows.append({"coin": coin, "day": ts.iloc[i].floor("D"),
                                  "f": float(f), "r": c1 / c0 - 1.0})
        if coin_rows:
            mu = float(np.mean([x["r"] for x in coin_rows]))
            for x in coin_rows:
                x["ex"] = x["r"] - mu
                x["g"] = x["f"] / 10.0 * x["ex"]
            rows.extend(coin_rows)

    n_cases = len(rows)
    n_days = len(set(x["day"] for x in rows)) if rows else 0
    counts = {"grid cases": int(n_cases), "distinct days": int(n_days)}

    mean_g, t = None, None
    if n_cases >= 2 and n_days >= 2:
        d = pd.DataFrame(rows)
        mean_g = float(d["g"].mean())
        dev = d["g"] - mean_g
        per_day = dev.groupby(d["day"]).sum().to_numpy()
        G = len(per_day)
        var = np.sum(per_day ** 2) * G / (G - 1) / (n_cases ** 2)
        se = float(np.sqrt(var))
        t = float(mean_g / se) if se > 0 else None

    sup_val, sup_pass = None, None
    if rows:
        d = pd.DataFrame(rows)
        hi = d.loc[d["f"] >= 2, "ex"]
        lo = d.loc[d["f"] <= -2, "ex"]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False
    counts["cells forecast >= +2"] = int(sum(1 for x in rows if x["f"] >= 2))
    counts["cells forecast <= -2"] = int(sum(1 for x in rows if x["f"] <= -2))

    if n_cases < 300 or n_days < 150:
        status = "not observable"
        decided_by = (f"The plan's minimum of 300 grid cases on 150 distinct days is not reached "
                      f"({n_cases} cases on {n_days} days).")
    elif t is None:
        status = "inconclusive"
        decided_by = "The t of the mean timing gain could not be computed (zero spread)."
    elif mean_g > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "The mean timing gain is positive with t >= 2 and the supporting check passes."
    elif mean_g < 0 and t <= -2:
        status = "rejected"
        decided_by = "The mean timing gain is negative with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided_by = "t >= 2 but the supporting check (high-forecast minus low-forecast excess return > 0) fails."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean timing gain lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean timing gain forecast/10 x excess 10-bar return",
                         "value": mean_g,
                         "statistic": ({"name": "t of the mean, cases of one day summed", "value": t}
                                       if t is not None else None),
                         "threshold": "positive with t >= 2 to confirm, negative with t <= -2 to reject"},
        "supporting_check": {"name": "excess 10-bar return, forecast >= +2 minus forecast <= -2, above 0",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
