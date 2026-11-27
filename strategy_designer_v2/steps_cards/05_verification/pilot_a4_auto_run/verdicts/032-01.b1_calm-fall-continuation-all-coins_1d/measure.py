import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.fall30.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    case_frames = []
    coin_means = {}

    for coin, wins in bars.items():
        all_r = []
        per_window = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            # Raw 30-day percent return; recompute from closes inside the window where not recorded.
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            recomputed = (close / close.shift(30) - 1.0) * 100.0
            raw = raw.where(raw.notna(), recomputed)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)

            active = fc != 0
            situation = (regime == "unknown") & (raw < 0)
            agree = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            # Next-day return, inside the window only.
            r_next = close.shift(-1) / close - 1.0
            all_r.append(r_next.dropna().values)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            per_window.append(pd.DataFrame({
                "coin": coin,
                "day": ts.dt.floor("D"),
                "fc": fc.values,
                "r": r_next.values,
            }))
        if all_r:
            allr = np.concatenate(all_r)
            coin_means[coin] = float(np.mean(allr)) if len(allr) else np.nan
        for pw in per_window:
            case_frames.append(pw)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = (agreement >= 0.9) if agreement is not None else None

    threshold_txt = ("confirm: slope < 0 with t <= -2 and mean short-direction excess return > 0; "
                     "reject: slope > 0 with t >= +2; inconclusive otherwise; "
                     "minimum 300 cases on at least 100 distinct days")
    main_name = "slope of next-day excess return on |forecast|"
    reading = ("The falling calm profile is read from the recorded `regime` column (the detector's non-vetoed "
               "regime 'unknown'), the 30-day fall from fall30's raw value (recomputed from closes inside the "
               "window if missing), the coin's mean daily return is the mean of all its in-window next-day "
               "returns over all windows, and the slope's t is an OLS slope with day-clustered standard errors "
               "(CR1 factor G/(G-1)).")

    if agreement is not None and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars of the falling calm "
                           "profile with a 30-day fall and a short forecast, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    if case_frames:
        allc = pd.concat(case_frames, ignore_index=True)
    else:
        allc = pd.DataFrame(columns=["coin", "day", "fc", "r"])
    cases = allc[(allc["fc"] < 0) & allc["r"].notna()].copy()
    cases["mu"] = cases["coin"].map(coin_means)
    cases = cases[cases["mu"].notna()]
    cases["ex"] = cases["r"] - cases["mu"]
    cases["x"] = cases["fc"].abs()

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    slope = None
    tstat = None
    mean_short = None
    if n_cases >= 3:
        x = cases["x"].values.astype(float)
        y = cases["ex"].values.astype(float)
        xd = x - x.mean()
        sxx = float(np.sum(xd ** 2))
        if sxx > 0:
            b = float(np.sum(xd * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            e = y - a - b * x
            sc = pd.Series(xd * e).groupby(cases["day"].values).sum().values
            G = len(sc)
            var_b = float(np.sum(sc ** 2)) / sxx ** 2
            if G > 1:
                var_b *= G / (G - 1)
            slope = b
            tstat = b / np.sqrt(var_b) if var_b > 0 else None
        mean_short = float(np.mean(-y))
    elif n_cases > 0:
        mean_short = float(np.mean(-cases["ex"].values))

    sup_pass = (mean_short > 0) if mean_short is not None else None

    if n_cases < 300 or n_days < 100:
        status = "not observable"
        decided = (f"The plan's minimum of 300 cases on at least 100 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed (no spread in |forecast|), meeting neither rule."
    elif slope < 0 and tstat <= -2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is negative with t <= -2 and the mean short-direction excess return is above 0."
        else:
            status = "inconclusive"
            decided = ("The slope is negative with t <= -2 but the mean short-direction excess return is at "
                       "or below 0.")
    elif slope > 0 and tstat >= 2:
        status = "rejected"
        decided = "The slope is positive with t >= +2: larger past falls are followed by a rebound."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None),
                            "passed": (bool(passed) if passed is not None else None)},
        "main_measure": {"name": main_name,
                         "value": (float(slope) if slope is not None else None),
                         "statistic": ({"name": "day-clustered OLS slope t", "value": float(tstat)}
                                       if tstat is not None else None),
                         "threshold": threshold_txt},
        "supporting_check": {"name": "mean short-direction next-day excess return > 0",
                             "value": (float(mean_short) if mean_short is not None else None),
                             "passed": (bool(sup_pass) if sup_pass is not None else None)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
