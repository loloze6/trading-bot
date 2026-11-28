import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    CL = "debug_info.components.close_loc.last_history_value"

    # ---------- gather per window, never across windows ----------
    frames = []
    coin_rets = {}
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            d["ret1"] = close.shift(-1) / close - 1.0  # inside the window only
            rets_all.append(d["ret1"].dropna())
            d["coin"] = coin
            d["window"] = w
            frames.append(d)
        coin_rets[coin] = float(pd.concat(rets_all).mean()) if rets_all else np.nan
    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "abs(forecast)-weighted mean short-direction excess next-day return",
                             "value": None, "statistic": None,
                             "threshold": "above 0 with t >= 2 to confirm; t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"independent days with a nonzero forecast": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }
    allb = pd.concat(frames, ignore_index=True)
    allb[FC] = pd.to_numeric(allb[FC], errors="coerce").fillna(0.0)

    # ---------- situation check ----------
    rng = (allb["high"] - allb["low"]).astype(float)
    loc_px = np.where(rng > 0, (allb["close"] - allb["low"]) / rng.replace(0, np.nan), np.nan)
    if CL in allb.columns:
        loc_raw = pd.to_numeric(allb[CL], errors="coerce")
        loc = loc_raw.where(loc_raw.notna(), pd.Series(loc_px, index=allb.index))
    else:
        loc = pd.Series(loc_px, index=allb.index)
    in_profile = allb["regime"].astype(str) == "unknown"
    situation = in_profile & (loc > 0)
    active = allb[FC] != 0
    n_active = int(active.sum())
    agree = (situation & (allb[FC] < 0) & active).sum()
    agreement = float(agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "abs(forecast)-weighted mean short-direction excess next-day return"
    threshold = "above 0 with day-clustered t >= 2 to confirm; t <= -2 to reject"
    reading = ("The falling agitated profile is read from the recorded regime (the detector's decision, "
               "'unknown' = not vetoed to chop) with a close location above the low as the graded situation, "
               "the 1-bar grid is every bar, the coin's mean is over all its bars in all windows, the "
               "weighted t clusters per UTC day with a G/(G-1) correction, terciles are pooled over all "
               "cases by abs(forecast) with unweighted means, and the plan's 'fewer than 150 days' is "
               "reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars inside the "
                           "falling agitated profile with a close above the day's low."),
            "reading": reading,
        }

    # ---------- main measure ----------
    cases = allb[(allb[FC] < 0) & allb["ret1"].notna()].copy()
    cases["mu"] = cases["coin"].map(coin_rets)
    cases["x"] = -(cases["ret1"] - cases["mu"])
    cases["w"] = cases[FC].abs()
    cases["day"] = cases["timestamp"].dt.floor("D")
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique())
    counts = {"independent days with a nonzero forecast": n_days, "cases": n_cases}

    if n_days < 150:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n_days} independent days with a nonzero forecast, below the plan's minimum of 150.",
            "reading": reading,
        }

    sw = cases["w"].sum()
    m = float((cases["w"] * cases["x"]).sum() / sw)
    cases["dev"] = cases["w"] * (cases["x"] - m)
    S = cases.groupby("day")["dev"].sum().values
    G = len(S)
    var = (S ** 2).sum() / sw ** 2 * (G / (G - 1)) if G > 1 else np.nan
    se = float(np.sqrt(var)) if np.isfinite(var) else np.nan
    t = float(m / se) if se and np.isfinite(se) and se > 0 else np.nan

    # ---------- supporting check ----------
    srt = cases.sort_values(["w", "timestamp", "coin"], kind="mergesort").reset_index(drop=True)
    k = n_cases // 3
    if k >= 1:
        diff = float(srt["x"].iloc[-k:].mean() - srt["x"].iloc[:k].mean())
        sup_pass = bool(diff > 0)
    else:
        diff, sup_pass = None, None

    if np.isfinite(t) and m > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The weighted mean excess short return is above 0 with t >= 2 and the top-minus-bottom third check is above 0."
    elif np.isfinite(t) and t <= -2:
        status = "rejected"
        decided = "The weighted mean excess short return has t <= -2: next-day returns rise above the drift after high closes."
    elif np.isfinite(t) and t >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "t >= 2 but the top-minus-bottom third check is not above 0."
    else:
        status = "inconclusive"
        decided = "The weighted mean's t lies between -2 and 2 (or the confirm rule is not met)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": m,
                         "statistic": {"name": "day-clustered t of weighted mean",
                                       "value": t if np.isfinite(t) else None},
                         "threshold": threshold},
        "supporting_check": {"name": "top third minus bottom third by abs(forecast), short excess next-day return",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
