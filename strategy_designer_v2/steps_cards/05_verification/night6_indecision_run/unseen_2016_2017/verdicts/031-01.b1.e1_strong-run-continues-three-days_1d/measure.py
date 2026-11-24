import numpy as np
import pandas as pd

RAW_COL = "debug_info.components.volscaled_rise.last_history_value"


def _raw_sign_from_prices(close):
    # Sign of the component recomputed from prices: 5-day return / (20-day std of daily returns) * sqrt(5);
    # the std is positive, so the sign is the sign of the 5-day return (inside the window only).
    r5 = close / close.shift(5) - 1.0
    return np.sign(r5)


def measure(bars):
    H = 3
    MIN_POS = 200

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw_sign = np.sign(raw)
            fb = _raw_sign_from_prices(close)
            raw_sign = raw_sign.where(raw.notna(), fb)
            active = fc.notna() & (fc != 0)
            # situation: a rise over 5 days (raw ratio > 0); expected side: long (forecast > 0)
            agree = active & (raw_sign > 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars after a 5-day rise "
                           "(positive volatility-scaled 5-day return), as the Fidelity's situation and side require"
                           if n_active > 0 else
                           "The forecast is never non-zero, so the config never takes the plan's long position after a 5-day rise"),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, float(fc[i]) if np.isfinite(fc[i]) else np.nan, c1 / c0 - 1.0))

    grid = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])
    if len(grid) > 0:
        coin_mean = grid.groupby("coin")["ret"].mean()
        grid["excess"] = grid["ret"] - grid["coin"].map(coin_mean)
    else:
        grid["excess"] = []

    g = grid.dropna(subset=["forecast", "excess"])
    n_grid = int(len(g))
    pos = g[g["forecast"] > 0]
    n_pos = int(len(pos))

    # slope of excess on forecast, OLS with intercept
    slope, t_slope = None, None
    if n_grid >= 3:
        x = g["forecast"].values.astype(float)
        y = g["excess"].values.astype(float)
        xm, ym = x.mean(), y.mean()
        sxx = float(((x - xm) ** 2).sum())
        if sxx > 0:
            b = float(((x - xm) * (y - ym)).sum() / sxx)
            a = ym - b * xm
            resid = y - a - b * x
            s2 = float((resid ** 2).sum() / (n_grid - 2))
            se = np.sqrt(s2 / sxx)
            slope = b
            t_slope = float(b / se) if se > 0 else None

    wmean = None
    if n_pos > 0 and float(pos["forecast"].sum()) > 0:
        wmean = float((pos["excess"] * pos["forecast"]).sum() / pos["forecast"].sum())
    support_pass = None if wmean is None else bool(wmean > 0)

    counts = {"grid bars with a forecast above 0": n_pos, "grid bars": n_grid}

    if n_pos < MIN_POS:
        status = "not observable"
        decided = f"Only {n_pos} grid bars have a forecast above 0, fewer than the plan's minimum of 200."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif t_slope >= 2 and support_pass:
        status = "confirmed"
        decided = "The slope's t is >= 2 and the forecast-weighted mean excess return on positive-forecast grid bars is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is <= -2."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is >= 2 but the forecast-weighted mean excess return on positive-forecast grid bars is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "OLS slope of excess 3-bar return on forecast (non-overlapping grid, pooled)",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": "t >= 2 confirms (with the supporting check), t <= -2 rejects, otherwise inconclusive",
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess 3-bar return on grid bars with forecast > 0",
            "value": wmean,
            "passed": support_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid bars at positions 0, 3, 6, ... of each window, dropping those without a bar t+3 in the window; "
                    "the coin's mean 3-bar return is the mean of its grid returns over all its windows; the slope is an "
                    "OLS with intercept and its ordinary t; the 200 minimum counts grid bars with forecast > 0 and a valid "
                    "3-bar return and, as a minimum count, gives 'not observable' when not reached."),
    }
