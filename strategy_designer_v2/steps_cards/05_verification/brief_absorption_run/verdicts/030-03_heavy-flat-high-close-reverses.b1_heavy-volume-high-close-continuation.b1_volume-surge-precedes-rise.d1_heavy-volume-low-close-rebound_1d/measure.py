import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.absorb_low.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            rng = (high - low)
            loc = ((high - close) / rng.where(rng > 0)).fillna(0.0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # graded situation: positive product of close's nearness to the low and the volume ratio
            sit_raw = raw > 0
            sit_price = (loc > 0) & (vol > 0)
            situation = sit_raw.where(raw.notna(), sit_price).astype(bool)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("The situation is taken as graded, so it holds on every bar where the raw component value "
               "(close's nearness to the low times the volume ratio) is positive (from prices when the raw value "
               "is missing), on the long side; the coin's mean 10-bar return is taken over the same "
               "non-overlapping grid of all its windows; the slope's t is the ordinary least-squares t; "
               "missing a minimum count gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars with a positive "
                           "volume-weighted close-near-low value, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                coin_rows.append((fc[i], c1 / c0 - 1.0))
        if not coin_rows:
            continue
        arr = np.array(coin_rows, dtype=float)
        mu = np.nanmean(arr[:, 1])
        for f, r in arr:
            rows.append((f, r - mu))

    data = np.array(rows, dtype=float) if rows else np.empty((0, 2))
    if len(data):
        data = data[np.isfinite(data[:, 0]) & np.isfinite(data[:, 1])]
    n_cases = int(len(data))
    strong = data[data[:, 0] >= 10] if n_cases else np.empty((0, 2))
    n_strong = int(len(strong))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(data[:, 0]) > 0:
        res = stats.linregress(data[:, 0], data[:, 1])
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr > 0 else None

    mean_strong = float(np.mean(strong[:, 1])) if n_strong > 0 else None
    check_pass = bool(mean_strong is not None and mean_strong > 0 and n_strong >= 30)

    counts = {"grid cases": n_cases, "cases with a forecast of 10 or more": n_strong}

    main = {
        "name": "pooled OLS slope of excess next-10-bar return on forecast",
        "value": slope,
        "statistic": {"name": "OLS t of the slope", "value": t_slope} if t_slope is not None else None,
        "threshold": "t >= 2.0 confirms (with the check), t <= -2.0 rejects",
    }
    supporting = {
        "name": "mean excess 10-bar return on grid bars with forecast >= 10",
        "value": mean_strong,
        "passed": check_pass if n_strong > 0 else None,
    }

    if n_cases < 300 or n_strong < 30:
        status = "not observable"
        decided_by = (f"A minimum count is not reached: {n_cases} grid cases (300 needed) and "
                      f"{n_strong} cases with a forecast of 10 or more (30 needed).")
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2.0 and check_pass:
        status = "confirmed"
        decided_by = "The slope's t is 2.0 or more and the mean excess return on forecast >= 10 cases is above 0."
    elif t_slope >= 2.0:
        status = "inconclusive"
        decided_by = "The slope's t is 2.0 or more but the supporting check fails."
    elif t_slope <= -2.0:
        status = "rejected"
        decided_by = "The slope's t is -2.0 or less: a lower return the heavier the volume and the lower the close."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2.0 and 2.0."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
