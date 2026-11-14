import numpy as np
import pandas as pd


def measure(bars):
    MOVE_COL = "debug_info.components.move.last_history_value"
    MIN_ACTIVE = 60

    frames = []
    for coin in bars:
        for win in bars[coin]:
            df = bars[coin][win].copy().reset_index(drop=True)
            df["close"] = pd.to_numeric(df["close"], errors="coerce")
            df["volume"] = pd.to_numeric(df["volume"], errors="coerce")
            df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce")
            # next-bar return inside the window only
            df["ret1"] = df["close"].shift(-1) / df["close"] - 1.0
            # volume regime: volume at or above its 20-bar mean (including the current bar), inside the window only
            vmean = df["volume"].rolling(20, min_periods=20).mean()
            df["vol_on"] = np.where(vmean.notna() & df["volume"].notna(),
                                    (df["volume"] >= vmean).astype(float), np.nan)
            if MOVE_COL in df.columns:
                df["move_raw"] = pd.to_numeric(df[MOVE_COL], errors="coerce")
            else:
                df["move_raw"] = df["close"] / df["close"].shift(1) - 1.0
            df["coin"] = coin
            df["window"] = win
            frames.append(df)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "forecast-weighted mean excess next-bar return", "value": None,
                             "statistic": None, "threshold": "above 0 with t >= 2 confirms; below 0 with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": 0},
            "decided_by": "No bars in the record, so the minimum of 60 active bars is not reached.",
            "reading": "none",
        }

    allb = pd.concat(frames, ignore_index=True)

    # ---- situation check ----
    act = allb[(allb["forecast"].notna()) & (allb["forecast"] != 0)]
    chk = act[act["vol_on"].notna() & act["move_raw"].notna()]
    if len(chk) > 0:
        in_sit = (chk["vol_on"] == 1.0) & (chk["move_raw"] > 0) & (chk["forecast"] > 0)
        agreement = float(in_sit.mean())
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The volume regime is computed as volume >= its 20-bar rolling mean (current bar included) within each "
               "window, with the window's first 19 bars left out of the situation check; the drift is the mean next-bar "
               "return over all bars of all windows pooled; the t-statistic of the forecast-weighted mean uses the "
               "weighted standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w); the top and bottom fifths are the "
               "floor(n/5) active bars with the highest and lowest forecast after a stable sort.")

    main_name = "forecast-weighted mean next-bar return on active bars minus buy-and-hold drift"
    threshold = "above 0 with t >= 2 confirms; below 0 with t <= -2 rejects; otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(len(act))},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long on bars where volume is at or "
                           "above its 20-bar mean and the bar rose, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---- main measure ----
    valid_all = allb[allb["ret1"].notna()]
    drift = float(valid_all["ret1"].mean()) if len(valid_all) else np.nan

    a = act[act["ret1"].notna()].copy()
    a["excess"] = a["ret1"] - drift
    n_active = int(len(a))

    value = None
    tstat = None
    if n_active > 1:
        w = a["forecast"].abs().values.astype(float)
        x = a["excess"].values.astype(float)
        sw = w.sum()
        if sw > 0:
            m = float((w * x).sum() / sw)
            var = (n_active / (n_active - 1.0)) * float((w ** 2 * (x - m) ** 2).sum())
            se = np.sqrt(var) / sw
            value = m
            tstat = float(m / se) if se > 0 else None
    elif n_active == 1:
        value = float(a["excess"].iloc[0])

    # ---- supporting check ----
    sup = {"name": "top-fifth minus bottom-fifth mean excess next-bar return (top must be > 0 and > bottom)",
           "value": None, "passed": None}
    k = n_active // 5
    if k >= 1:
        s = a.sort_values("forecast", kind="mergesort")
        bottom = float(s["excess"].iloc[:k].mean())
        top = float(s["excess"].iloc[-k:].mean())
        sup["value"] = top - bottom
        sup["passed"] = bool(top > 0 and top > bottom)

    counts = {"active bars": n_active}

    if n_active < MIN_ACTIVE:
        status = "not observable"
        decided = f"Only {n_active} active bars across the windows, fewer than the plan's minimum of 60."
    elif value is None or tstat is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif value > 0 and tstat >= 2:
        status = "confirmed"
        decided = "The forecast-weighted mean excess next-bar return is above 0 with a t-statistic of 2 or more."
    elif value < 0 and tstat <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess next-bar return is below 0 with a t-statistic of -2 or less."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": value,
            "statistic": ({"name": "t of the forecast-weighted mean", "value": tstat} if tstat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
