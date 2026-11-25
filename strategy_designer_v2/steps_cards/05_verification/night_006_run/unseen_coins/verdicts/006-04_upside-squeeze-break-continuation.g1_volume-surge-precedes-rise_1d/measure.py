import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    MIN_POS = 300
    RAW = "debug_info.components.vol_surge.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: the situation is the 5-day mean volume above the 30-day mean volume
    # (log ratio > 0), and the expected side is long (the price rises).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            # Fallback inside the window only, where the record has no raw value.
            recomputed = np.log(
                vol.rolling(5, min_periods=5).mean()
                / vol.rolling(30, min_periods=30).mean()
            )
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "t of slope of pooled coin-excess 3-bar return on forecast"
    threshold = ("confirm if t >= 2 with forecast-weighted mean excess > 0; "
                 "reject if t <= -2; at least 300 grid cases with forecast > 0")
    sup_name = "forecast-weighted mean excess 3-bar return > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "agreeing bars": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars "
                           "where the 5-day mean volume is above the 30-day mean volume "
                           "(raw log ratio > 0), as the plan's situation requires."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1, f = close[i], close[i + H], fc[i]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, f))

    g = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(g) > 0:
        g["excess"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")

    n_cases = int(len(g))
    n_pos = int((g["fc"] > 0).sum()) if n_cases else 0

    slope = None
    t_val = None
    if n_cases >= 3 and g["fc"].nunique() > 1:
        lr = stats.linregress(g["fc"].to_numpy(), g["excess"].to_numpy())
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_val = float(lr.slope / lr.stderr)

    wmean = None
    sup_pass = None
    if n_cases > 0:
        sw = float(g["fc"].sum())
        if sw != 0:
            wmean = float((g["excess"] * g["fc"]).sum() / sw)
            sup_pass = bool(wmean > 0)

    if n_pos < MIN_POS:
        status = "not observable"
        decided = (f"Only {n_pos} grid cases with forecast > 0, below the plan's minimum "
                   f"of 300, so the data could not show the idea.")
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = ("The slope's t is 2 or more, the forecast-weighted mean excess return is above 0, "
                   "with at least 300 grid cases where forecast > 0.")
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less, with at least 300 grid cases where forecast > 0."
    elif t_val >= 2:
        status = "inconclusive"
        decided = ("The slope's t is 2 or more but the forecast-weighted mean excess return is "
                   "at or below 0, which the plan calls inconclusive.")
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": wmean, "passed": sup_pass},
        "counts": {
            "grid cases with forecast > 0": n_pos,
            "grid cases": n_cases,
        },
        "decided_by": decided,
        "reading": ("The grid is positions 0, 3, 6, ... of each window, keeping only cases with a "
                    "full 3-bar forward return inside the window. The coin's mean 3-bar return is "
                    "taken over all its grid cases across windows. The slope's t is from ordinary "
                    "least squares on all pooled grid cases, zero forecasts included. Fewer than "
                    "300 forecast > 0 cases is reported as 'not observable', following the workflow's "
                    "rule for minimum counts rather than the plan's 'inconclusive'."),
    }
