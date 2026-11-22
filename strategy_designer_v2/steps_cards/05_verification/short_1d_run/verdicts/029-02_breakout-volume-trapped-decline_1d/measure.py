import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    PERIOD = 20
    LAGS = (1, 2, 3)  # fail_window 4: breakout 1 to 3 bars back
    RAW = "debug_info.components.fb_vol.last_history_value"
    POST = "debug_info.components.fb_vol.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin], key=lambda s: int(str(s).lstrip("w") or 0)):
            df = bars[coin][w].sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            high = df["high"].astype(float).values
            fc = df["forecast"].astype(float).values
            raw = df[RAW].astype(float).values if RAW in df.columns else np.full(len(df), np.nan)
            n = len(df)
            # prior 20-bar high (current bar excluded) and breakout flag
            prior_high = pd.Series(high).shift(1).rolling(PERIOD, min_periods=PERIOD).max().values
            breakout = np.zeros(n, dtype=bool)
            ok = ~np.isnan(prior_high)
            breakout[ok] = close[ok] > prior_high[ok]
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                raw_ok = np.isfinite(raw[t]) and raw[t] > 0
                computable = (t - max(LAGS) - PERIOD) >= 0
                if computable:
                    price_ok = False
                    for k in LAGS:
                        b = t - k
                        if b >= 0 and breakout[b] and close[t] < prior_high[b]:
                            price_ok = True
                            break
                else:
                    price_ok = True  # price history too short in the window: rely on the raw value
                if raw_ok and price_ok and f < 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars where the close sits below a 20-day high broken 1 to 3 days earlier, as the plan's Fidelity requires.",
            "reading": "Situation taken as a positive raw fb_vol value with the close below the prior 20-bar high (from highs) broken by a close 1 to 3 bars earlier, checked on prices where the window has enough history; expected side short.",
        }

    # ---------- 2. drift per coin (non-overlapping 5-bar returns, all windows) ----------
    drift = {}
    for coin in bars:
        rets = []
        for w in bars[coin]:
            df = bars[coin][w].sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases: short bets, once per 5-bar grid cell ----------
    moves, sizes = [], []
    for coin in sorted(bars):
        if not np.isfinite(drift[coin]):
            continue
        for w in bars[coin]:
            df = bars[coin][w].sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            post = df[POST].astype(float).values if POST in df.columns else np.full(len(df), np.nan)
            n = len(df)
            ref = 0.0
            prev_short = False
            taken_cells = set()
            for t in range(n):
                f = fc[t]
                if f >= 0:
                    ref = 0.0
                    prev_short = False
                    continue
                if not prev_short:
                    ref = 0.0
                prev_short = True
                if ref - f >= BAND:
                    ref = f
                    cell = t // H
                    if cell in taken_cells:
                        continue
                    taken_cells.add(cell)
                    if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                        r = c[t + H] / c[t] - 1.0
                        moves.append(-(r - drift[coin]))
                        sizes.append(abs(post[t]) if np.isfinite(post[t]) else np.nan)
                else:
                    ref = max(ref, f)

    moves = np.asarray(moves, dtype=float)
    sizes = np.asarray(sizes, dtype=float)
    n_cases = int(len(moves))

    mean = float(np.mean(moves)) if n_cases > 0 else None
    tval = None
    if n_cases > 1:
        sd = float(np.std(moves, ddof=1))
        tval = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    slope = None
    m = np.isfinite(sizes) & np.isfinite(moves)
    if m.sum() > 2 and np.ptp(sizes[m]) > 0:
        slope = float(stats.linregress(sizes[m], moves[m]).slope)
    slope_passed = None if slope is None else bool(slope > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases across all coins and windows, below the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (no spread in the cases), so neither rule is met."
    elif mean > 0 and tval >= 2:
        if slope_passed:
            status = "confirmed"
            decided = "The mean unusual short move is above 0 with t >= 2 and the slope on the forecast size is above 0."
        else:
            status = "inconclusive"
            decided = "The main t is >= 2 but the supporting slope is at or below 0 (or not computable), which the plan calls inconclusive."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean unusual short move is below 0 with t <= -2: the coin rises more than its drift after failed breakouts."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual short move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": "mean unusual 5-bar short move (return minus coin drift, short direction)",
            "value": mean,
            "statistic": None if tval is None else {"name": "t of the mean", "value": tval},
            "threshold": "confirm if mean > 0 with t >= 2 (and slope > 0); reject if mean < 0 with t <= -2; at least 30 cases",
        },
        "supporting_check": {
            "name": "slope of unusual short move on abs post_pipeline_value of fb_vol",
            "value": slope,
            "passed": slope_passed,
        },
        "counts": {"cases across all coins and windows": n_cases},
        "decided_by": decided,
        "reading": "A short bet is a fall of the forecast of at least 2 points from its least negative level since the last bet (reset to 0 after a flat or long bar), the first bet in each 5-bar grid cell from the window's first row is the case, cases without 5 bars left in the window are dropped, and the plan's 'fewer than 30 cases' rule is reported as not observable.",
    }
