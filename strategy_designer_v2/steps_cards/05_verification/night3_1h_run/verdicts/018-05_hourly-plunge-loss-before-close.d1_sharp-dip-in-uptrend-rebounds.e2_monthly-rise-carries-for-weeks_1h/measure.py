import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 336
    RAW = "debug_info.components.scaled_30d_return.last_history_value"
    PERIOD = 720

    # ---------- 1. Situation check: raw scaled 30-day return > 0, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # price-based fallback inside the window only: sign of the 720-bar return
            # (the mean absolute scale is positive, so the sign equals the raw value's sign)
            ret720 = close / close.shift(PERIOD) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            sit_val = raw.where(raw.notna(), ret720)
            situation = (sit_val > 0).fillna(False)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of 336-bar forward return minus coin drift on forecast (grid bars with forecast > 0)"
    thr = "confirm if slope t >= 2 (with top-tercile mean excess > 0 and >= 100 cases); reject if t <= -2 (>= 100 cases)"
    sup_name = "top-tercile (by forecast) mean 336-bar excess return over drift > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the scaled 30-day return "
                           "is positive, as the plan's situation requires." if n_active > 0 else
                           "No bar has a non-zero forecast, so the config never takes the plan's situation."),
            "reading": "The situation is read as the component's raw value (last_history_value) above 0, with the 720-bar price return's sign as fallback where it is missing; the side is long.",
        }

    # ---------- 2. Criterion ----------
    rows = []          # (coin, forecast, fwd return)
    drift_samples = {}  # coin -> list of all grid forward returns
    for coin, wins in bars.items():
        drift_samples.setdefault(coin, [])
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                c0, c1 = close[i], close[j]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                drift_samples[coin].append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    rows.append((coin, float(fc[i]), r))

    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in drift_samples.items()}
    data = pd.DataFrame(rows, columns=["coin", "forecast", "ret"])
    if len(data):
        data["excess"] = data["ret"] - data["coin"].map(drift)
        data = data.dropna(subset=["excess", "forecast"])
    n_cases = int(len(data))

    slope = None
    t_slope = None
    if n_cases >= 3 and data["forecast"].nunique() > 1:
        lr = stats.linregress(data["forecast"].to_numpy(), data["excess"].to_numpy())
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)

    top_mean = None
    n_top = 0
    if n_cases >= 3:
        rk = data["forecast"].rank(method="first")
        terc = pd.qcut(rk, 3, labels=[0, 1, 2])
        top = data.loc[terc == 2, "excess"]
        n_top = int(len(top))
        if n_top > 0:
            top_mean = float(top.mean())
    sup_passed = None if top_mean is None else bool(top_mean > 0)

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with forecast > 0, fewer than the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "Slope t is 2 or more, the top-tercile mean excess return is above 0, with at least 100 cases."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t is -2 or less, with at least 100 cases."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Slope t is 2 or more but the top-tercile mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": top_mean, "passed": sup_passed},
        "counts": {"grid cases with forecast > 0": n_cases, "top tercile cases": n_top},
        "decided_by": decided,
        "reading": ("The regression pools all coins' grid bars with forecast > 0 (grid from each window's first row, "
                    "returns inside the window), the drift is each coin's mean 336-bar return over all its windows' grid bars, "
                    "and the top tercile is the top third of those bars ranked by forecast (ties broken by order)."),
    }
