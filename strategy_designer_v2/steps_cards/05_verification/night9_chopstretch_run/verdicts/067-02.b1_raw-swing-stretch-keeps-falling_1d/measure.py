import numpy as np
import pandas as pd

RAW = "debug_info.components.stretch_below.last_history_value"
H = 10
MIN_CASES = 60
STRATEGY_REGIME = "unknown"   # the only regime with a strategy: the choppy profile


def _grid(df):
    """Non-overlapping 10-bar grid of one window: positions 0, 10, 20, ... with a forward return inside the window."""
    close = df["close"].to_numpy(dtype=float)
    n = len(close)
    pos = np.arange(0, n - H, H)
    ret = close[pos + H] / close[pos] - 1.0
    return pos, ret


def measure(bars):
    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            sma = close.rolling(20, min_periods=20).mean()
            below_px = close < sma
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            below = np.where(raw.notna(), raw < 0, below_px.fillna(False))
            choppy = df["regime"].astype(str) == STRATEGY_REGIME
            active = fc != 0
            situ = choppy.to_numpy() & below.astype(bool) & (fc < 0).to_numpy()
            n_active += int(active.sum())
            n_agree += int((active.to_numpy() & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are choppy-profile bars with the close "
                           "below its 20-day average and a short (negative) forecast, as the Fidelity states."),
            "reading": "The choppy profile is read as the regime with a strategy ('unknown'); below the average is the raw stretch < 0 (close < 20-bar SMA where the raw value is not recorded).",
        }

    # ---------------- 2. criterion ----------------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) <= H:
                continue
            pos, ret = _grid(df)
            coin_rets.extend(list(ret))
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            raw = (pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
                   if RAW in df.columns else np.full(len(df), np.nan))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for p, r in zip(pos, ret):
                if np.isfinite(fc[p]) and fc[p] < 0 and np.isfinite(raw[p]) and np.isfinite(r):
                    coin_cases.append((ts.iloc[p].floor("D"), raw[p], r))
        coin_rets = np.array([x for x in coin_rets if np.isfinite(x)])
        if len(coin_rets) == 0:
            continue
        mu = float(coin_rets.mean())
        for d, x, r in coin_cases:
            rows.append((d, x, r - mu))

    n_cases = len(rows)
    days = sorted(set(r[0] for r in rows))
    n_days = len(days)
    counts = {"grid cases": int(n_cases), "days": int(n_days)}
    threshold = "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"
    reading = ("Choppy profile = regime 'unknown' (the only regime with a strategy); cases = grid bars (0,10,20,... of each window) "
               "with forecast < 0 and a 10-bar return inside the window; coin mean = mean of all its grid 10-bar returns over all windows; "
               "slope t = OLS slope over a day-clustered standard error (scores summed per day, G/(G-1) correction); "
               "the plan's 'fewer than 60 grid cases' is treated as a minimum count, so 'not observable'.")

    if n_cases < MIN_CASES or n_days < 3:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": "slope of excess 10-bar return on raw stretch", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean short-direction excess 10-bar return > 0", "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Fewer than {MIN_CASES} grid cases ({n_cases}).",
            "reading": reading,
        }

    d = pd.DataFrame(rows, columns=["day", "x", "y"])
    x = d["x"].to_numpy(dtype=float)
    y = d["y"].to_numpy(dtype=float)
    xc = x - x.mean()
    sxx = float((xc ** 2).sum())
    if sxx <= 0:
        slope, t = None, None
    else:
        slope = float((xc * (y - y.mean())).sum() / sxx)
        a = y.mean() - slope * x.mean()
        e = y - a - slope * x
        d["s"] = xc * e
        g = d.groupby("day")["s"].sum().to_numpy()
        G = len(g)
        var = (G / (G - 1)) * float((g ** 2).sum()) / sxx ** 2
        t = float(slope / np.sqrt(var)) if var > 0 else None

    short_excess = float(np.mean(-y))
    sup_pass = bool(short_excess > 0)

    if slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed (no spread in the stretch), so neither rule is met."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: the slope is positive with t >= 2 and the mean short-direction excess return is above 0."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "Inconclusive: a confirming slope (t >= 2) whose supporting check fails (mean short-direction excess <= 0)."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "Reject: the slope is negative with t <= -2 (deeper stretches followed by a return toward the average)."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "slope of excess 10-bar return on raw stretch",
                         "value": slope,
                         "statistic": ({"name": "slope t, day-clustered", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean short-direction excess 10-bar return > 0",
                             "value": short_excess, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
