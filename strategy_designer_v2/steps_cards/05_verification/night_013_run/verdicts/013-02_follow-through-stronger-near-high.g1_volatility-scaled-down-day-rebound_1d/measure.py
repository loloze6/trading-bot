import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"
    MIN_BARS = 500
    T_THR = 2.0

    def _raw_from_prices(close):
        # VolatilityScaledReturnComponent(period=1, vol_period=20): 1-day return / std of last 20 one-day returns
        r = close.pct_change(1)
        vol = r.rolling(20, min_periods=20).std()
        return r / vol

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            recomputed = _raw_from_prices(close)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: a fall on the day (scaled return below 0); expected side: long (forecast > 0)
            agree = active & (raw < 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.90)

    main_name = "t of OLS slope of next-bar excess return on forecast, forecast > 0 bars, pooled"
    thr_words = "slope t >= +2 (with forecast-weighted mean excess > 0) confirms; t <= -2 rejects; otherwise inconclusive; at least 500 bars with forecast > 0"
    sup_name = "forecast-weighted mean next-bar excess return over forecast > 0 bars, above 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are down days (scaled return < 0) with a long forecast, as the Fidelity's situation and side require.",
            "reading": "Situation taken as the raw scaled return below 0 (recomputed from prices where not recorded), expected side long.",
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin's mean daily return over all its windows together (returns inside windows only)
        all_r = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fwd = close.shift(-1) / close - 1.0
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            all_r.append(fwd.dropna().values)
            per_win.append((fc, fwd))
        if not all_r:
            continue
        allr = np.concatenate(all_r)
        if len(allr) == 0:
            continue
        mu = float(np.mean(allr))
        for fc, fwd in per_win:
            m = fc.notna() & fwd.notna() & (fc > 0)
            xs.append(fc[m].values.astype(float))
            ys.append((fwd[m].values - mu).astype(float))

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n = int(len(x))
    counts = {"bars with forecast > 0": n}
    reading = ("Bars with forecast > 0 counted where the next bar's close exists in the same window; "
               "the coin's mean daily return is the mean of all its in-window next-bar returns over all windows; "
               "the slope t is the ordinary OLS t (slope / its standard error); the plan's 500-bar minimum, when unmet, is reported as not observable.")

    if n < MIN_BARS or n < 3 or np.allclose(x, x[0] if n else 0):
        return {
            "status": "not observable",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"The plan's minimum of 500 bars with forecast > 0 is not reached ({n}).",
            "reading": reading,
        }

    lr = stats.linregress(x, y)
    t_slope = float(lr.slope / lr.stderr) if lr.stderr > 0 else float("nan")
    wmean = float(np.sum(x * y) / np.sum(x))
    sup_pass = bool(wmean > 0)

    if t_slope >= T_THR and sup_pass:
        status = "confirmed"
        decided = "The slope's t is +2 or more and the forecast-weighted mean next-bar excess return is above 0."
    elif t_slope <= -T_THR:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger scaled falls are followed by smaller next-day returns than holding."
    elif t_slope >= T_THR:
        status = "inconclusive"
        decided = "The slope's t is +2 or more but the forecast-weighted mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {"name": main_name, "value": t_slope,
                         "statistic": {"name": "OLS slope t", "value": t_slope},
                         "threshold": thr_words},
        "supporting_check": {"name": sup_name, "value": wmean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
