import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 14
    RAW = "debug_info.components.rsi_share.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: the situation is the share of the past 30 days with RSI above 50.
    # It is graded and centred at one half: above half is long, below half is short.
    # The raw value is share - 0.5, so the expected side is sign(raw).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw != 0) & (np.sign(raw) == np.sign(fc))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t-statistic of the slope of 14-bar excess forward return on forecast (pooled, non-overlapping)"
    threshold = "confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars on the situation's side": n_agree},
            "decided_by": ("The forecast's sign does not follow the sign of the 30-day RSI-above-50 share minus one half "
                           "on at least 90% of active bars, so the config does not do what the Fidelity says."),
            "reading": ("The expected side is sign(last_history_value), the share minus 0.5. Active bars with a missing "
                        "or zero raw value count as disagreeing."),
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[t]))

    samp = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(samp) > 0:
        coin_mean = samp.groupby("coin")["ret"].mean()
        samp["excess"] = samp["ret"] - samp["coin"].map(coin_mean)
        use = samp[samp["fc"].notna() & samp["excess"].notna()]
    else:
        use = samp
    n_cases = int(len(use))
    counts = {"non-overlapping cases with a recorded forecast": n_cases}

    reading = ("Grid at positions 0, 14, 28, ... of each window, keeping only bars with a bar 14 rows later in the "
               "same window. Each coin's mean 14-bar return is the mean over all of its grid returns in all windows. "
               "OLS with an intercept and its usual slope t. The plan's 'fewer than 200 cases' minimum is treated as "
               "'not observable'. Active bars with a missing or zero raw value count as disagreeing in the situation check.")

    if n_cases < 200:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n_cases} non-overlapping cases with a recorded forecast, below the plan's minimum of 200.",
            "reading": reading,
        }

    x = use["fc"].to_numpy(dtype=float)
    y = use["excess"].to_numpy(dtype=float)
    if np.std(x) == 0:
        slope, t_stat = 0.0, 0.0
    else:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_stat = float(res.slope / res.stderr) if res.stderr > 0 else 0.0

    if slope > 0 and t_stat >= 2:
        status = "confirmed"
        decided = f"The slope is positive with t = {t_stat:.2f} >= 2 over {n_cases} cases."
    elif slope < 0 and t_stat <= -2:
        status = "rejected"
        decided = f"The slope is negative with t = {t_stat:.2f} <= -2 over {n_cases} cases."
    else:
        status = "inconclusive"
        decided = f"t = {t_stat:.2f} lies between -2 and +2 over {n_cases} cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": t_stat,
            "statistic": {"name": "OLS slope t", "value": t_stat},
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
