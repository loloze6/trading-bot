import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    FC = "forecast"
    SLOPE = "debug_info.components.slope200.last_history_value"
    DIST = "debug_info.components.dist200.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or FC not in df.columns:
                continue
            f = pd.to_numeric(df[FC], errors="coerce")
            slope = pd.to_numeric(df[SLOPE], errors="coerce") if SLOPE in df.columns else pd.Series(np.nan, index=df.index)
            if DIST in df.columns:
                dist = pd.to_numeric(df[DIST], errors="coerce")
                below = dist < 0
                below_valid = dist.notna()
            else:
                reg = df["regime"] if "regime" in df.columns else df.get("debug_info.regime")
                if reg is None:
                    reg = pd.Series(np.nan, index=df.index)
                below = reg.astype(str) == "trending"
                below_valid = reg.notna()
            active = f.notna() & (f != 0) & slope.notna() & below_valid
            n_active += int(active.sum())
            agree = active & (f < 0) & below & (slope < 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are short bars with the close below its 200-day SMA "
                           "(trending regime) and a falling 20-bar slope of that SMA."
                           if n_active > 0 else "No active bars to compare with the plan's situation."),
            "reading": "Below the 200-day SMA is read from the dist200 value if recorded, otherwise from the 'trending' regime label; falling is a raw 20-bar SMA slope below 0.",
        }

    # ---------- 2. criterion ----------
    # coin mean 10-bar return over all windows together (all bars, within-window returns)
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > H:
                r = c[H:] / c[:-H] - 1.0
                rets.append(r[np.isfinite(r)])
        rets = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(rets)) if len(rets) else np.nan

    grid_rows = []   # (abs forecast, main value, excess)
    all_active_abs = []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:-H] = c[H:] / c[:-H] - 1.0
            for i in range(n):
                if np.isfinite(f[i]) and f[i] != 0 and np.isfinite(fwd[i]):
                    all_active_abs.append(abs(f[i]))
            for i in range(0, n, H):
                if np.isfinite(f[i]) and f[i] != 0 and np.isfinite(fwd[i]):
                    ex = fwd[i] - mu
                    grid_rows.append((abs(f[i]), -f[i] / 10.0 * ex, ex))

    n_cases = len(grid_rows)
    vals = np.array([g[1] for g in grid_rows], dtype=float)
    mean_v = float(np.mean(vals)) if n_cases > 0 else None
    t_v = None
    if n_cases >= 2:
        sd = float(np.std(vals, ddof=1))
        if sd > 0:
            t_v = float(mean_v / (sd / np.sqrt(n_cases)))

    # supporting check: top quartile of |forecast| among active bars
    sup_val, sup_pass, n_top = None, None, 0
    if all_active_abs and grid_rows:
        q75 = float(np.quantile(np.array(all_active_abs), 0.75))
        top = [g[2] for g in grid_rows if g[0] >= q75]
        n_top = len(top)
        if n_top > 0:
            sup_val = float(np.mean(top))
            sup_pass = bool(sup_val < 0)

    counts = {"non-overlapping active cases": int(n_cases),
              "non-overlapping top-quartile cases": int(n_top)}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping active cases, below the plan's minimum of 30."
    elif t_v is None:
        status = "inconclusive"
        decided = "The t-statistic is undefined (zero dispersion), so neither confirm nor reject is met."
    elif mean_v > 0 and t_v >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Main-measure mean above 0 with t >= 2 over at least 30 non-overlapping active cases, and the top-quartile excess return is negative."
    elif mean_v < 0 and t_v <= -2:
        status = "rejected"
        decided = "Main-measure mean below 0 with t <= -2 over at least 30 non-overlapping active cases: the steep-decline shorts lose against usual drift."
    else:
        status = "inconclusive"
        if t_v >= 2:
            decided = "t >= 2 but the supporting check is not negative, so the confirm rule is not met."
        else:
            decided = "t lies between -2 and 2, which neither confirms nor rejects."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean of -forecast/10 x (10-bar forward return - coin's all-window mean 10-bar return)",
            "value": mean_v,
            "statistic": {"name": "t of the mean", "value": t_v} if t_v is not None else None,
            "threshold": "mean > 0 with t >= 2 to confirm, mean < 0 with t <= -2 to reject, over at least 30 non-overlapping active cases",
        },
        "supporting_check": {
            "name": "mean 10-bar excess return on top-quartile |forecast| bars, non-overlapping",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The coin's mean 10-bar return uses every bar of all its windows (within-window returns); the top quartile is |forecast| at or above "
                    "the 75th percentile over all active bars, then taken on the 0,10,20,... grid; below-average is read from dist200 if recorded, else the 'trending' label; "
                    "fewer than 30 cases is reported as not observable."),
    }
