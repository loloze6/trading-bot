import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    LHV = "debug_info.components.thin_volume.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            vol = d["volume"].astype(float)
            prev_close = close.shift(1)
            up = close > prev_close
            # first bar of a window has no prior close in the window: use the detector's decision
            first = prev_close.isna()
            if "regime" in d.columns:
                up = up.where(~first, d["regime"] == "mean_reversion")
            # volume ratio, centred: raw recorded value, else recomputed from volumes
            ratio_rec = vol / vol.shift(1).rolling(20, min_periods=20).mean() - 1.0
            if LHV in d.columns:
                ratio = pd.to_numeric(d[LHV], errors="coerce").where(
                    lambda s: s.notna(), ratio_rec)
            else:
                ratio = ratio_rec
            light = ratio < 0
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            active = fc != 0
            agree = active & up & light & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            d["_coin"] = coin
            d["_win"] = w
            d["_fc"] = fc
            d["_ret"] = close.shift(-1) / close - 1.0  # inside the window only
            frames.append(d[["timestamp", "_coin", "_win", "_fc", "_ret"]])

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-direction unusual 1-bar move on bars with forecast <= -2"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 300 distinct case days"
    sup_name = "unusual move of top third minus bottom third by abs(forecast)"
    reading = ("Up day taken as close above the prior close within the window (the detector's regime on a window's first bar), "
               "light volume as the recorded centred volume ratio below 0; horizon 1 bar so every bar is a grid point; "
               "normal drift is each coin's mean 1-bar return over all its windows; the t sums case deviations per UTC day "
               "(no small-sample correction); thirds are equal-size splits of the cases sorted by abs(forecast); "
               "fewer than 300 case days gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are up days with volume below its "
                           "prior 20-day mean carrying a short forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    allb = pd.concat(frames, ignore_index=True)
    drift = allb.dropna(subset=["_ret"]).groupby("_coin")["_ret"].mean()
    allb["_drift"] = allb["_coin"].map(drift)
    cases = allb[(allb["_fc"] <= -2) & allb["_ret"].notna() & allb["_drift"].notna()].copy()
    cases["_u"] = -(cases["_ret"] - cases["_drift"])
    cases["_day"] = cases["timestamp"].dt.floor("D")

    n_cases = int(len(cases))
    n_days = int(cases["_day"].nunique()) if n_cases else 0

    mean = float(cases["_u"].mean()) if n_cases else None
    t = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["_u"] - mean
        s = dev.groupby(cases["_day"]).sum()
        se = float(np.sqrt((s ** 2).sum()) / n_cases)
        t = float(mean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        srt = cases.assign(_a=cases["_fc"].abs()).sort_values("_a", kind="mergesort")
        parts = np.array_split(np.arange(n_cases), 3)
        bottom = srt["_u"].iloc[parts[0]].mean()
        top = srt["_u"].iloc[parts[2]].mean()
        sup_val = float(top - bottom)
        sup_pass = bool(sup_val > 0)

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < 300:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, below the plan's minimum of 300."
    elif t is None or mean is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed."
    elif mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean short-direction unusual move is positive with t >= 2 and the top-minus-bottom third difference is above 0."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean short-direction unusual move is negative with t <= -2."
    elif mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "Confirming t >= 2 but the supporting check (top third minus bottom third above 0) failed."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean,
                         "statistic": ({"name": "t of the mean, cases of one day summed together", "value": t}
                                       if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
