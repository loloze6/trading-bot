import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    COMP = "debug_info.components.weekend_rev.last_history_value"
    MIN_CASES = 200

    # ---------- per-coin normal drift over 48 bars (non-overlapping grid, all windows) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            for p in range(0, n - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if len(rets) else np.nan

    active_total = 0
    active_agree = 0
    xs, ys, dir_moves = [], [], []
    n_cases_all = 0

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            vol = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            raw = (pd.to_numeric(df[COMP], errors="coerce").to_numpy(dtype=float)
                   if COMP in df.columns else np.full(n, np.nan))

            # weekend (last 48 bars, t-47..t) vs weekday base (120 bars, t-167..t-48), log ratio
            short_mean = vol.rolling(48, min_periods=48).mean()
            long_mean = vol.shift(48).rolling(120, min_periods=120).mean()
            with np.errstate(divide="ignore", invalid="ignore"):
                logratio = np.log(short_mean.to_numpy(dtype=float) / long_mean.to_numpy(dtype=float))

            # 48-bar weekend return from prices
            ret48 = np.full(n, np.nan)
            if n > H:
                ret48[H:] = close[H:] / close[:-H] - 1.0

            is_sun23 = ((ts.dt.dayofweek == 6) & (ts.dt.hour == 23)).to_numpy()
            thin = np.where(np.isfinite(logratio), logratio < 0.0, False)
            situation = is_sun23 & thin

            # weekend move sign: raw component where recorded, else price return
            move = np.where(np.isfinite(raw), raw, ret48)
            move_sign = np.sign(np.where(np.isfinite(move), move, 0.0))
            expected_side = -move_sign  # lean against the weekend move

            active = fc != 0
            agree = active & situation & (np.sign(fc) == expected_side) & (expected_side != 0)
            active_total += int(active.sum())
            active_agree += int(agree.sum())

            # cases for the criterion
            case_mask = is_sun23 & (regime == "mean_reversion") & active
            d = drift.get(coin, np.nan)
            for i in np.where(case_mask)[0]:
                n_cases_all += 1
                if i + H >= n:
                    continue
                a, b = close[i], close[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0 and np.isfinite(d)):
                    continue
                unusual = (b / a - 1.0) - d
                xs.append(fc[i])
                ys.append(unusual)
                dir_moves.append(np.sign(fc[i]) * unusual)

    agreement = (active_agree / active_total) if active_total > 0 else 0.0
    passed = bool(active_total > 0 and agreement >= 0.9)

    main_name = "t of slope of 48-bar forward return minus normal drift regressed on forecast, pooled"
    thr = "confirm if t >= 2 (with positive mean unusual move); reject if t <= -2"
    reading = ("Cases are Sunday 23:00 UTC bars (bar start) in regime mean_reversion with nonzero forecast and a full "
               "48-bar forward return inside the window, the regressed variable is the undirected unusual return "
               "(OLS with intercept), and the plan's 'fewer than 200 cases' minimum is applied as 'not observable' "
               "per the workflow's rule on minimum counts.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "cases": int(len(xs))},
            "decided_by": ("Fewer than 90% of nonzero-forecast bars are Sunday 23:00 thin-volume weekend bars with "
                           "the forecast against the weekend move (agreement %.3f)." % agreement),
            "reading": reading,
        }

    n = len(xs)
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    slope = t_val = None
    if n >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    mean_dir = float(np.mean(dir_moves)) if n > 0 else None
    sup_pass = (mean_dir > 0) if mean_dir is not None else None

    counts = {"cases over all coins": int(n), "case bars before forward-return filter": int(n_cases_all)}

    if n < MIN_CASES:
        status = "not observable"
        decided = "Fewer than 200 cases over all coins (%d), so the data could not show the idea." % n
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast)."
    elif t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope's t is 2 or more and the mean unusual move in the forecast's direction is positive."
        else:
            status = "inconclusive"
            decided = "A confirming slope t (>= 2) whose mean unusual move in the forecast's direction is not positive."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: forecasts against the weekend move are followed by continuation."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t_val} if t_val is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move in forecast's direction > 0",
                             "value": mean_dir, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
