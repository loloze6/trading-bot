import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.rev.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: situation = last 1h return scaled by 24h volatility (graded, every bar).
    # Expected side = opposite to the move: short after an up hour, long after a down hour.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            last_ret = close / close.shift(1) - 1.0  # inside the window only
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                move_sign = np.sign(raw)
                # Where the component is not recorded, use the price move's sign.
                move_sign = move_sign.where(raw.notna(), np.sign(last_ret))
            else:
                move_sign = np.sign(last_ret)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            expected_side = -move_sign
            agree = active & move_sign.notna() & (move_sign != 0) & (np.sign(fc) == expected_side)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "OLS slope of next-bar excess return on forecast, pooled"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with a non-zero forecast": int(n_active)},
            "decided_by": ("The forecast's sign does not run opposite to the last hour's vol-scaled move on at least 90% "
                           "of active bars, so the config does not do what the plan's Fidelity says."),
            "reading": "Expected side taken as minus the sign of the recorded raw component (the price move where it is missing).",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp")
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if len(close) < 2:
                continue
            nxt = np.full(len(close), np.nan)
            nxt[:-1] = close[1:] / close[:-1] - 1.0
            coin_rows.append((fc, nxt))
        if not coin_rows:
            continue
        all_r = np.concatenate([r for _, r in coin_rows])
        all_r = all_r[np.isfinite(all_r)]
        if len(all_r) == 0:
            continue
        mu = float(all_r.mean())
        for fc, nxt in coin_rows:
            m = np.isfinite(fc) & np.isfinite(nxt)
            xs.append(fc[m])
            ys.append(nxt[m] - mu)

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n_nonzero = int(np.sum(x != 0))
    n_bars = int(len(x))
    counts = {"bars with a non-zero forecast": n_nonzero, "bars in the regression": n_bars}
    reading = ("Every bar with a forecast and a next-bar return inside its window enters the pooled OLS (with intercept), "
               "the coin mean is over all its windows' 1-bar returns, and the minimum count is of those bars with a non-zero forecast.")

    if n_nonzero < 1000 or n_bars < 3 or np.var(x) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "Fewer than the plan's minimum of 1,000 bars with a non-zero forecast.",
            "reading": reading,
        }

    res = stats.linregress(x, y)
    slope = float(res.slope)
    se = float(res.stderr)
    t = float(slope / se) if se > 0 else 0.0

    if slope > 0 and t >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 (confirm rule)."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "OLS slope t", "value": t},
                         "threshold": threshold},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
