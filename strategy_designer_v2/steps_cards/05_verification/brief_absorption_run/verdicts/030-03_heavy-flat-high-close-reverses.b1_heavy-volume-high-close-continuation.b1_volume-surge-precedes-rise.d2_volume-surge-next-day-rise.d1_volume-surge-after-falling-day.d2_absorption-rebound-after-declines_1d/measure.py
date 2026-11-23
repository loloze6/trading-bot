import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.absorb.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            close = pd.to_numeric(df["close"], errors="coerce")
            prev = close.shift(1)
            # down day where computable within the window (no previous close on the first bar)
            down_ok = prev.isna() | (close < prev)
            situation = (raw > 0) & down_ok
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of next-bar excess return on forecast"
    threshold = "confirm: t >= 2 with mean excess return on forecast > 0 bars above 0; reject: t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long on a down day with a positive "
                           "fall x volume ratio x prior-decline component, as the plan's Fidelity requires."),
            "reading": "The situation is taken as a positive raw component value on a close-to-close down day, on the long side.",
        }

    # ---------- 2. Criterion ----------
    # next-bar returns within windows, per coin
    per_coin = {}
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            df = df.sort_values("timestamp")
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if len(close) < 2:
                continue
            r = np.full(len(close), np.nan)
            r[:-1] = close[1:] / close[:-1] - 1.0
            frames.append(pd.DataFrame({"r": r, "f": fc}))
        if frames:
            per_coin[coin] = pd.concat(frames, ignore_index=True)

    rows = []
    for coin, d in per_coin.items():
        mu = d["r"].dropna().mean()
        d = d.copy()
        d["x"] = d["r"] - mu
        rows.append(d[["x", "f"]])
    if rows:
        allr = pd.concat(rows, ignore_index=True).dropna()
    else:
        allr = pd.DataFrame({"x": [], "f": []})
    allr = allr[np.isfinite(allr["x"]) & np.isfinite(allr["f"])]

    n_bars = int(len(allr))
    pos = allr[allr["f"] > 0]
    n_pos = int(len(pos))

    slope = None
    t_slope = None
    if n_bars >= 3 and allr["f"].nunique() > 1:
        lr = stats.linregress(allr["f"].to_numpy(), allr["x"].to_numpy())
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    mean_pos = float(pos["x"].mean()) if n_pos > 0 else None
    sup_pass = (mean_pos > 0) if mean_pos is not None else None

    counts = {"bars": n_bars, "bars with forecast > 0": n_pos}

    if n_pos < 100 or t_slope is None:
        status = "not observable"
        decided = (f"Only {n_pos} bars with forecast > 0, below the plan's minimum of 100."
                   if n_pos < 100 else "The slope's t could not be computed.")
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope has t >= 2 and the mean excess return on forecast > 0 bars is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope has t <= -2."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the mean excess return on forecast > 0 bars is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean next-bar excess return on forecast > 0 bars",
            "value": mean_pos,
            "passed": None if sup_pass is None else bool(sup_pass),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The slope is an ordinary least-squares regression over every bar with a next bar in its window "
                    "(horizon 1, so every bar is its own grid cell), the coin mean is the mean of all its next-bar "
                    "returns over all windows, and the plan's 'fewer than 100 forecast > 0 bars' minimum is "
                    "treated as 'not observable' as the workflow requires."),
    }
