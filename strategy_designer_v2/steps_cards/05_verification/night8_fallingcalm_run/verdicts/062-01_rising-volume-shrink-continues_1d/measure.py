import numpy as np
import pandas as pd
from scipy import stats

def measure(bars):
    H = 5
    RAW = "debug_info.components.vol_dryup.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            # situation: rising profile (component recorded) and volume shrank (raw log ratio < 0); side long
            situ = raw.notna() & (raw < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = (agreement is not None) and (agreement >= 0.9)

    main_name = "OLS slope of excess 5-bar forward return on forecast, in-profile grid bars, coins pooled"
    main_thr = "confirm: slope > 0 with t >= 2 (and supporting difference > 0); reject: slope < 0 with t <= -2"
    sup_name = "mean excess 5-bar return, forecast > 0 minus forecast = 0 (Welch)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active), "active_bars_in_situation_long": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the rising profile "
                           "with a shrinking 30-day volume (raw log ratio < 0)." if n_active > 0 else
                           "No active bars: the forecast never takes the plan's position."),
            "reading": "The rising profile is read as the bars where the vol_dryup component is recorded, and the shrink as its raw log ratio below 0.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values if "forecast" in df.columns else np.full(len(df), np.nan)
            raw = pd.to_numeric(df[RAW], errors="coerce").values if RAW in df.columns else np.full(len(df), np.nan)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, c1 / c0 - 1.0, fc[i], raw[i]))
    g = pd.DataFrame(rows, columns=["coin", "window", "ret", "fc", "raw"])

    if len(g):
        drift = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(drift)
        prof = g[g["raw"].notna() & g["fc"].notna()].copy()
    else:
        prof = pd.DataFrame(columns=["coin", "window", "ret", "fc", "raw", "excess"])

    n_case = int(len(prof))
    pos = prof[prof["fc"] > 0]["excess"].astype(float).values
    zer = prof[prof["fc"] == 0]["excess"].astype(float).values
    n_pos, n_zero = int(len(pos)), int(len(zer))
    counts = {"in-profile grid cases": n_case, "forecast > 0": n_pos, "forecast = 0": n_zero}

    slope = t_slope = None
    if n_case >= 3 and prof["fc"].astype(float).std() > 0:
        x = prof["fc"].astype(float).values
        y = prof["excess"].astype(float).values
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    diff = welch_t = None
    if n_pos >= 2 and n_zero >= 2:
        diff = float(pos.mean() - zer.mean())
        welch_t = float(stats.ttest_ind(pos, zer, equal_var=False).statistic)
    elif n_pos >= 1 and n_zero >= 1:
        diff = float(pos.mean() - zer.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    reading = ("In-profile grid bars are those where the vol_dryup component is recorded; the normal drift is the coin's "
               "mean 5-bar return over the non-overlapping grid of all its windows; the slope's t is the OLS slope over "
               "its standard error; the supporting check passes when the difference is above 0, its Welch t being reported.")

    if n_case < 100 or n_pos < 30 or n_zero < 30:
        status = "not observable"
        miss = []
        if n_case < 100: miss.append(f"in-profile grid cases {n_case} < 100")
        if n_pos < 30: miss.append(f"forecast > 0 cases {n_pos} < 30")
        if n_zero < 30: miss.append(f"forecast = 0 cases {n_zero} < 30")
        decided = "Minimum count not reached: " + "; ".join(miss) + "."
    elif slope is None or t_slope is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t_slope >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Confirm: the slope is positive with t >= 2 and the supporting difference is above 0."
        else:
            status = "inconclusive"
            decided = "Inconclusive: the slope confirms (t >= 2) but the supporting difference is not above 0."
    elif slope < 0 and t_slope <= -2:
        status = "rejected"
        decided = "Reject: the slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass,
                             "welch_t": welch_t},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
