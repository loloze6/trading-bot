import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.scaled_rise.last_history_value"
    H = 2

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # one-day rise: the raw scaled return > 0 where recorded, else recomputed from prices
            price_ret = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                rise = np.where(raw.notna(), raw > 0, price_ret > 0)
            else:
                rise = (price_ret > 0).values
            rise = pd.Series(rise, index=df.index).astype(bool)
            # calm profile: the regime detector did not veto to "chop"
            if "regime" in df.columns:
                calm = df["regime"].astype(str) != "chop"
            else:
                calm = pd.Series(True, index=df.index)
            active = fc.notna() & (fc != 0)
            agree = active & rise & calm & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "OLS slope of excess 2-bar forward return on forecast (forecast > 0, 2-bar grid)",
                             "value": None, "statistic": None,
                             "threshold": "slope t >= 2 confirms (with positive weighted mean); t <= -2 rejects"},
            "supporting_check": {"name": "forecast-weighted mean excess 2-bar return > 0", "value": None, "passed": None},
            "counts": {"grid bars with forecast > 0": 0},
            "decided_by": "No bar has a non-zero forecast, so neither the situation nor the criterion can be observed.",
            "reading": "Situation bars: raw scaled_rise > 0 (price return > 0 where not recorded) on a bar whose regime is not 'chop', with forecast > 0.",
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    reading = ("Situation bars are those with raw scaled_rise > 0 (price return > 0 where the raw value is not recorded) "
               "and regime not 'chop' (the calm profile), on the long side (forecast > 0); the coin's mean 2-bar return "
               "is the mean over all its windows' 2-bar grid bars, and the slope comes from an OLS with intercept.")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "OLS slope of excess 2-bar forward return on forecast (forecast > 0, 2-bar grid)",
                             "value": None, "statistic": None,
                             "threshold": "slope t >= 2 confirms (with positive weighted mean); t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Only %.1f%% of the bars with a non-zero forecast are calm one-day rises with a long forecast, "
                           "below the 90%% the plan's Fidelity requires." % (100 * agreement)),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c2 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c2)) or c0 == 0:
                    continue
                grid_rows.append((c2 / c0 - 1.0, fc[t]))
        if not grid_rows:
            continue
        rets = np.array([r for r, _ in grid_rows], dtype=float)
        fcs = np.array([f for _, f in grid_rows], dtype=float)
        coin_mean = float(np.mean(rets))
        sel = np.isfinite(fcs) & (fcs > 0)
        xs.extend(fcs[sel].tolist())
        ys.extend((rets[sel] - coin_mean).tolist())

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(x))

    slope = None
    t_slope = None
    wmean = None
    if n_cases >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    if n_cases > 0 and x.sum() > 0:
        wmean = float(np.sum(y * x) / np.sum(x))
    check_pass = None if wmean is None else bool(wmean > 0)

    if n_cases < 100:
        status = "not observable"
        decided = "Fewer than 100 grid bars with forecast > 0 across all coins and windows (%d), the plan's minimum." % n_cases
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger calm rises are followed by smaller two-day returns than the drift."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the forecast-weighted mean excess return is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "OLS slope of excess 2-bar forward return on forecast (forecast > 0, 2-bar grid)",
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": "slope t >= 2 confirms (with positive weighted mean); t <= -2 rejects; between is inconclusive",
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess 2-bar return > 0",
            "value": wmean,
            "passed": check_pass,
        },
        "counts": {"grid bars with forecast > 0": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
