import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    REG = "regime"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce")
            reg = df[REG].astype(str)
            rise3 = close / close.shift(3) - 1.0  # inside the window only
            rise_ok = np.where(rise3.notna(), rise3 > 0.0, True)
            situation = (reg == "trending").values & rise_ok
            active = (fc.notna() & (fc != 0)).values
            long_side = (fc > 0).values
            n_active += int(active.sum())
            n_agree += int((active & situation & long_side).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "slope t of 5-bar excess return on forecast, trending grid cases",
                "value": None,
                "statistic": None,
                "threshold": "slope t >= 2 confirms, <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the falling-calm "
                           "profile (regime 'trending') with a 3-bar rise (close above its value 3 bars earlier)."
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": ("The falling-calm profile is read from the recorded regime (its detector components are not "
                        "recorded); the 3-bar rise is recomputed from closes, and on a window's first 3 bars, where it "
                        "cannot be, the regime alone is used."),
        }

    # ---------- 2. criterion ----------
    # coin's mean 5-bar return over all windows (non-overlapping grid, all bars)
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True).values
            n = len(close)
            for i in range(0, n, H):
                if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] != 0:
                    rets.append(close[i + H] / close[i] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    xs, ys = [], []
    for coin, wins in bars.items():
        cm = coin_mean[coin]
        if not np.isfinite(cm):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            reg = df[REG].astype(str).values
            n = len(df)
            for i in range(0, n, H):
                if reg[i] != "trending":
                    continue
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] != 0 and np.isfinite(fc[i])):
                    continue
                r = close[i + H] / close[i] - 1.0
                xs.append(float(fc[i]))
                ys.append(float(r - cm))

    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    n_regime = int(len(xs))
    pos = xs > 0
    n_pos = int(pos.sum())

    slope = None
    t_slope = None
    if n_regime >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)

    mean_pos = float(np.mean(ys[pos])) if n_pos > 0 else None
    check_pass = (mean_pos > 0) if mean_pos is not None else None

    counts = {
        "grid cases in the regime": n_regime,
        "grid cases with forecast > 0": n_pos,
        "active bars": int(n_active),
    }

    if n_pos < 30 or n_regime < 60:
        status = "not observable"
        decided_by = (f"Minimum counts not reached: {n_pos} grid cases with forecast > 0 (need 30) and "
                      f"{n_regime} grid cases in the regime (need 60).")
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed (no variation in the forecast), so neither confirm nor reject holds."
    elif t_slope >= 2:
        if check_pass:
            status = "confirmed"
            decided_by = "Slope t is 2 or more with at least 30 cases with forecast > 0, and the mean excess return of those cases is above 0."
        else:
            status = "inconclusive"
            decided_by = "A confirming slope t of 2 or more whose supporting check fails (mean excess return of forecast > 0 cases not above 0)."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "Slope t is -2 or less with at least 30 cases with forecast > 0."
    else:
        status = "inconclusive"
        decided_by = "Slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of 5-bar excess return on forecast, trending grid cases",
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": "slope t >= 2 (with >= 30 cases forecast > 0 and check passing) confirms; <= -2 rejects",
        },
        "supporting_check": {
            "name": "mean excess 5-bar return of grid cases with forecast > 0 above 0",
            "value": mean_pos,
            "passed": (bool(check_pass) if check_pass is not None else None),
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Cases are the regime-'trending' bars at grid positions 0,5,10,... of each window with a 5-bar "
                    "forward return inside the window, the regression includes their zero forecasts, the coin's mean "
                    "5-bar return is taken on the same grid over all bars of all its windows, the profile is read from "
                    "the recorded regime, and the plan's 'too few cases' rule is reported as 'not observable'."),
    }
