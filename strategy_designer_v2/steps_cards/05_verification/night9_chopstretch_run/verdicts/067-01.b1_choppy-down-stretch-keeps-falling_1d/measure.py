import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.stretch_below.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            sma = close.rolling(20).mean()
            vol = close.pct_change().rolling(20).std()
            recomputed = (close - sma) / sma / vol
            if RAW in df.columns:
                raw = df[RAW].astype(float).where(df[RAW].notna(), recomputed)
            else:
                raw = recomputed
            fc = df["forecast"].astype(float)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw < 0) & (fc < 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90 % of the active bars are bars where the close is below its 20-day SMA "
                          "(raw stretch < 0) with a short forecast, as the plan's situation and side require.",
            "reading": "The situation is taken as the raw 20-day SMA distance in usual moves below 0 (recomputed "
                       "from prices where not recorded), on the short side; the choppy profile is left to the regime code.",
        }

    # ---------- 2. drift per coin: non-overlapping 5-bar grid over all windows ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = df["close"].astype(float).reset_index(drop=True).values
            for t in range(0, len(close) - H, H):
                if np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0:
                    rets.append(close[t + H] / close[t] - 1)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. main measure: regression on grid bars with forecast < 0 ----------
    xs, ys = [], []
    # ---------- supporting check: bets, once per grid cell ----------
    case_moves, case_days = [], []
    for coin, wins in bars.items():
        d = drift[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for t in range(0, n - H, H):
                if np.isfinite(fc[t]) and fc[t] < 0 and np.isfinite(close[t]) and np.isfinite(close[t + H]) \
                        and close[t] > 0 and np.isfinite(d):
                    xs.append(fc[t])
                    ys.append(close[t + H] / close[t] - 1 - d)
            # bets
            side_prev = 0
            ref = 0.0
            taken_cells = set()
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    side_prev = 0
                    ref = 0.0
                    continue
                side = 1 if f > 0 else -1
                s = abs(f)
                if side != side_prev:
                    ref = 0.0
                side_prev = side
                if s - ref >= BAND:
                    ref = s
                    cell = t // H
                    if side == -1 and cell not in taken_cells and t + H < n and np.isfinite(d) \
                            and np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0:
                        taken_cells.add(cell)
                        r = close[t + H] / close[t] - 1
                        case_moves.append(-(r - d))
                        case_days.append(ts.iloc[t].strftime("%Y-%m-%d"))
                else:
                    ref = min(ref, s)

    n_grid = len(xs)
    slope = None
    t_slope = None
    if n_grid >= 3 and np.std(xs) > 0:
        lr = stats.linregress(np.array(xs), np.array(ys))
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    n_cases = len(case_moves)
    mean_unusual = float(np.mean(case_moves)) if n_cases > 0 else None
    n_days = int(len(set(case_days)))
    supp_pass = None if mean_unusual is None else bool(mean_unusual > 0)

    counts = {"grid cases with forecast < 0": n_grid, "bets (cases)": n_cases, "days of bets": n_days}
    main = {
        "name": "slope of 5-bar excess return on forecast (grid bars, forecast < 0)",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
        "threshold": "confirm if t >= 2 (with supporting check), reject if t <= -2, otherwise inconclusive",
    }
    supp = {"name": "mean unusual move of bets in short direction", "value": mean_unusual, "passed": supp_pass}

    if n_grid < 100:
        status = "not observable"
        decided = f"Only {n_grid} grid cases with forecast < 0, below the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so it is not >= 2 nor <= -2."
    elif t_slope >= 2 and supp_pass:
        status = "confirmed"
        decided = "The slope's t is >= 2 and the mean unusual move in the short direction is above 0."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is >= 2 but the supporting check (mean unusual move above 0) fails."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is <= -2: deeper stretches below are followed by a relative rise."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": "The drift is each coin's mean non-overlapping 5-bar return over all its windows, the slope's t is "
                   "the OLS t pooled over coins and windows, the supporting check's cases are the short bets (forecast "
                   "deepening by >= 2 points) taken once per 5-bar grid cell with the mean over cases, and the plan's "
                   "'fewer than 100 grid cases' minimum is applied as not observable.",
    }
