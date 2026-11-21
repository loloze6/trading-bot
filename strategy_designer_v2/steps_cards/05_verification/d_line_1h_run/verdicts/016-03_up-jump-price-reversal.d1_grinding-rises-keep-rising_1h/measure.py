import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    RAW = "debug_info.components.grind.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan's situation: the 72-bar net return is above 0. Expected side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            n = len(df)

            # 72-bar past return, inside this window only
            past_ret = np.full(n, np.nan)
            if n > H:
                past_ret[H:] = close[H:] / close[:-H] - 1.0

            # Where the window holds too few bars to compute the past return,
            # use the recorded raw value: the residual is non-zero only after a rise.
            situation = np.where(
                ~np.isnan(past_ret),
                past_ret > 0,
                np.where(~np.isnan(raw), raw > 0, False),
            )

            active = (~np.isnan(fc)) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the slope of the 72-bar excess forward return on the forecast"
    threshold = "confirm if t >= 2 with forecast-weighted mean excess > 0; reject if t <= -2"
    reading = ("Grid is positions 0, 72, 144, ... of each window from its first row; the coin's mean 72-bar return "
               "is the mean over that grid in all of the coin's windows; the slope's t is the ordinary OLS t with an "
               "intercept; and a count below the plan's minimum of 100 is reported as not observable, as the workflow "
               "requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on the long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with a positive "
                           "72-bar net return, which is the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    coin_grid_rets = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if np.isnan(c0) or np.isnan(c1) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                rows.append((coin, r, fc[t]))
        coin_grid_rets[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    xs, ys = [], []
    for coin, r, f in rows:
        if np.isnan(f) or f <= 0 or np.isnan(coin_grid_rets[coin]):
            continue
        xs.append(f)
        ys.append(r - coin_grid_rets[coin])
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_cases = int(len(x))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    wmean = float(np.sum(y * x) / np.sum(x)) if n_cases > 0 and np.sum(x) > 0 else None
    sup_passed = (wmean > 0) if wmean is not None else None

    counts = {"independent grid cases with forecast > 0": n_cases}

    if n_cases < 100:
        status = "not observable"
        decided = (f"Only {n_cases} independent grid cases have forecast > 0, "
                   f"below the plan's minimum of 100.")
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: the more evenly built the rise, the less the coin rises next."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the forecast-weighted mean excess return is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess 72-bar forward return > 0",
            "value": wmean,
            "passed": (bool(sup_passed) if sup_passed is not None else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
