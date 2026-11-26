import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.rise_in_usual_moves.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("unknown", index=df.index)
            in_profile = regime != "chop"
            situation = raw.notna() & (raw > 0) & in_profile
            agree = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the active bars are up days (raw one-day return over 30-day std > 0) "
                           "inside the falling agitated profile with a short forecast, as the Fidelity requires."),
            "reading": ("The situation is a raw rise_in_usual_moves value above 0 on a bar whose regime is the profile "
                        "(not 'chop'), and the expected side is short."),
        }

    # ---------- 2. criterion ----------
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        grid_rows = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in range(0, len(d) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rows.append((c1 / c0 - 1.0, fc[i], ts.iloc[i].floor("D")))
        if not grid_rows:
            continue
        rets = np.array([r[0] for r in grid_rows])
        coin_mean = float(np.mean(rets))
        for r, f, t in grid_rows:
            if np.isfinite(f) and f < 0:
                xs.append(abs(f))
                ys.append(r - coin_mean)
                days.append(t)

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(y))
    n_days = int(len(set(days)))

    slope = None
    slope_t = None
    if n_cases >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            slope_t = float(lr.slope / lr.stderr)

    mean_ex = float(np.mean(y)) if n_cases > 0 else None
    mean_t = None
    if n_cases >= 2:
        sd = float(np.std(y, ddof=1))
        if sd > 0:
            mean_t = float(mean_ex / (sd / np.sqrt(n_cases)))
    support_pass = None if mean_ex is None else bool(mean_ex < 0)

    reading = ("Cases are grid bars (positions 0, 3, 6, ... of each window) with forecast below 0 and a 3-bar forward "
               "return inside the window; the coin's mean 3-day return is the mean of its grid returns over all its "
               "windows; the slope's t is OLS slope over its standard error; the mean excess return's t is the ordinary "
               "t of the mean; the plan's 'fewer than 30 cases or days' rule is reported as not observable.")

    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases < 30 or n_days < 30 or slope_t is None:
        status = "not observable"
        decided_by = ("Minimum count not reached: fewer than 30 cases or cases on fewer than 30 distinct days "
                      f"({n_cases} cases on {n_days} days)."
                      if (n_cases < 30 or n_days < 30) else "The slope's t could not be computed.")
    elif slope_t >= 2 or (mean_ex is not None and mean_ex > 0 and mean_t is not None and mean_t >= 2):
        status = "rejected"
        decided_by = ("Reject: the slope's t is +2 or more, or the mean excess 3-day return is above 0 with a t of "
                      "+2 or more.")
    elif slope_t <= -2 and support_pass:
        status = "confirmed"
        decided_by = ("Confirm: the slope's t is -2 or less and the mean excess 3-day return over the cases is "
                      "below 0.")
    else:
        status = "inconclusive"
        if slope_t <= -2:
            decided_by = ("Inconclusive: the slope's t is -2 or less but the mean excess return is at or above 0 "
                          "with a t below +2.")
        else:
            decided_by = "Inconclusive: the slope's t is between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of excess 3-day return on abs(forecast), short grid bars",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": slope_t} if slope_t is not None else None,
            "threshold": "confirm at t <= -2 with the supporting check; reject at t >= +2",
        },
        "supporting_check": {
            "name": "mean excess 3-day return below 0",
            "value": mean_ex,
            "passed": support_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
