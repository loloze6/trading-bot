import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 30
    REG = "mean_reversion"
    RAW = "debug_info.components.ret30.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            # fallback: 30-bar percent return from prices inside the window
            ret30_px = close / close.shift(H) - 1.0
            ret30 = raw.where(raw.notna(), ret30_px)
            in_reg = df["regime"].astype(str) == REG
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & in_reg & ret30.notna() & (np.sign(fc) == np.sign(ret30))
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS slope of 30-bar forward excess return on forecast, regime mean_reversion, non-overlapping 30-bar grid"
    threshold = "confirm: slope t >= 2 with supporting check positive and >= 40 cases; reject: slope t <= -2"
    reading = ("The regime detector's r90 component is not recorded and cannot be rebuilt from ~122-bar windows "
               "(it needs 90+365 bars), so the situation is read from the detector's own `regime` == mean_reversion "
               "and the expected side is the sign of the 30-day return (ret30 last_history_value, else recomputed "
               "from closes); the grid is rows 0, 30, 60, ... of each window, all regime bars on it with a forward "
               "return are cases (forecast 0 included in the regression), the coin's mean 30-bar return is the mean "
               "over the same grid of all its windows and all regimes, and the plan's 40-case minimum is applied "
               "as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "cases": 0},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are mean_reversion-regime bars "
                           "whose forecast sign matches the sign of the 30-day return (long when it rose, short when it fell)."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    coin_mean = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if reg[i] == REG and np.isfinite(fc[i]):
                    rows.append((coin, r, float(fc[i])))
        coin_mean[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    x, y = [], []
    for coin, r, f in rows:
        m = coin_mean.get(coin, np.nan)
        if np.isfinite(m):
            x.append(f)
            y.append(r - m)
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n_cases = int(len(x))

    slope = t = None
    if n_cases >= 3 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    pos = y[x > 0]
    neg = y[x < 0]
    diff = float(pos.mean() - neg.mean()) if len(pos) > 0 and len(neg) > 0 else None
    check_passed = (diff > 0) if diff is not None else None

    counts = {"cases": n_cases, "cases forecast > 0": int(len(pos)),
              "cases forecast < 0": int(len(neg)), "active bars": n_active}

    if n_cases < 40:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 40."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif t >= 2 and check_passed is True:
        status = "confirmed"
        decided = "The slope's t is 2 or more, the supporting check is positive, with at least 40 cases."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: steadied falls do worse than falls still accelerating."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check is not positive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean excess return forecast>0 minus forecast<0",
                             "value": diff, "passed": check_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
