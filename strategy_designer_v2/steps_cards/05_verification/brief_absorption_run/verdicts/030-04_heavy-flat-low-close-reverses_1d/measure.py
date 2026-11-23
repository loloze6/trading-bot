import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    VR_MIN = 2.0
    BODY_MAX = 0.3333

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            o = df["open"].astype(float).values
            h = df["high"].astype(float).values
            l = df["low"].astype(float).values
            c = df["close"].astype(float).values
            v = df["volume"].astype(float)
            f = df["forecast"].astype(float).values
            rng = h - l
            prior_mean = v.shift(1).rolling(20, min_periods=20).mean().values
            with np.errstate(divide="ignore", invalid="ignore"):
                vr = v.values / prior_mean
                body = np.abs(c - o) / rng
                loc = 2.0 * (c - l) / rng - 1.0
            regime = df["regime"].astype(str).values if "regime" in df.columns else None
            for i in range(len(df)):
                if not np.isfinite(f[i]) or f[i] == 0:
                    continue
                n_active += 1
                if np.isfinite(vr[i]):
                    heavy = vr[i] >= VR_MIN
                else:
                    # no 20 prior bars inside the window: use the detector's recorded decision
                    heavy = regime is not None and regime[i] == "mean_reversion"
                flat = np.isfinite(body[i]) and body[i] <= BODY_MAX
                low_close = np.isfinite(loc[i]) and loc[i] < 0
                if heavy and flat and low_close and f[i] > 0:
                    n_agree += 1

    reading = ("The situation is a day with volume >= 2x its prior 20-day mean, body <= 1/3 of range and the close in "
               "the lower half of the range (close location < 0), expected side long; bars without 20 prior bars in "
               "their window use the recorded regime for the volume rule; cases are bets of both signs, the first bet "
               "in each 5-bar grid cell, weighted by the signed forecast at the case bar.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "forecast-weighted excess 5-bar return", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject, over at least 30 cases"},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": "No active bars: fewer than the plan's minimum of 30 cases.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "forecast-weighted excess 5-bar return", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject, over at least 30 cases"},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are heavy, flat, lower-half-close days with a long forecast: "
                           "the config's forecast does not bet only long on the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    vals = []
    for coin, wins in bars.items():
        # coin's mean 5-bar return over all its windows (non-overlapping grid)
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            n = len(df)
            for p in range(0, n - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
            prepared.append((c, f))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))

        for c, f in prepared:
            n = len(c)
            side = 0
            trough = 0.0
            seen_cells = set()
            for i in range(n):
                fi = f[i] if np.isfinite(f[i]) else 0.0
                s = int(np.sign(fi))
                if s == 0:
                    side = 0
                    trough = 0.0
                    continue
                if s != side:
                    side = s
                    trough = 0.0
                a = abs(fi)
                if a - trough >= BAND:
                    trough = a
                    cell = i // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                        r = c[i + H] / c[i] - 1.0
                        vals.append((fi / 10.0) * (r - drift))
                else:
                    trough = min(trough, a)

    vals = np.array(vals, dtype=float)
    n_cases = int(len(vals))
    mean_val = float(np.mean(vals)) if n_cases > 0 else None
    if n_cases >= 2:
        sd = float(np.std(vals, ddof=1))
        t = float(mean_val / (sd / np.sqrt(n_cases))) if sd > 0 else None
    else:
        t = None

    threshold = "confirm if positive with t >= 2, reject if negative with t <= -2, over at least 30 cases"
    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} cases, below the plan's minimum of 30 cases."
    elif t is not None and mean_val > 0 and t >= 2:
        status = "confirmed"
        decided_by = "The forecast-weighted excess 5-bar return is positive with t >= 2 over at least 30 cases."
    elif t is not None and mean_val < 0 and t <= -2:
        status = "rejected"
        decided_by = "The forecast-weighted excess 5-bar return is negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided_by = "The t lies between -2 and 2 (inconclusive rule) with at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "forecast-weighted excess 5-bar return",
                         "value": mean_val,
                         "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
                         "threshold": threshold},
        "supporting_check": None,
        "counts": {"cases": n_cases},
        "decided_by": decided_by,
        "reading": reading,
    }
