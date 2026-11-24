import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    FC = "forecast"
    RAW = "debug_info.components.rise7.last_history_value"

    # ---------- 1. situation check: forecast active only on a positive 7-day return, short side ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin in sorted(bars.keys()):
        prepared[coin] = {}
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp")
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce").astype(float)
            # raw 7-day percent return: recorded value where present, else recomputed inside the window
            recomputed = (close / close.shift(H) - 1.0) * 100.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").astype(float)
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            prepared[coin][win] = (close, fc)

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc < 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "Pearson correlation of forecast with next 7-bar return minus normal 7-bar drift (non-overlapping grid, forecast < 0)"
    threshold = "confirm: correlation positive with t >= 2 and supporting check passes; reject: negative with t <= -2"
    sup_name = "mean unusual move in the signal's direction (fall beyond drift)"
    reading = ("Situation taken as a positive raw 7-day return (recorded rise7 value, recomputed from closes where missing) "
               "with a short forecast, profile not part of the check; drift is each coin's mean non-overlapping 7-bar return "
               "over all its windows; grid cases are grid bars with forecast < 0 and a full 7-bar return inside the window; "
               "the plan's 'fewer than 30 grid cases' minimum is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are bars with a positive 7-day return "
                           "carrying a short forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in prepared.items():
        grid_rows = []
        all_rets = []
        for win, (close, fc) in wins.items():
            n = len(close)
            for p in range(0, n, H):
                if p + H >= n:
                    continue
                c0, c1 = close.iloc[p], close.iloc[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                f = fc.iloc[p]
                if np.isfinite(f) and f < 0:
                    grid_rows.append((f, r))
        if len(all_rets) == 0:
            continue
        drift = float(np.mean(all_rets))
        for f, r in grid_rows:
            xs.append(float(f))
            ys.append(float(r - drift))

    n_cases = len(xs)
    counts = {"grid cases with a forecast below 0": int(n_cases)}

    if n_cases < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 30 grid cases with a forecast below 0 over all coins and windows.",
            "reading": reading,
        }

    x = np.asarray(xs)
    y = np.asarray(ys)
    sup_val = float(np.mean(-y))
    sup_pass = bool(sup_val > 0)

    if np.std(x) == 0 or np.std(y) == 0:
        r = None
        t = None
    else:
        r = float(stats.pearsonr(x, y)[0])
        if abs(r) >= 1.0:
            t = float(np.sign(r) * np.inf)
        else:
            t = float(r * np.sqrt((n_cases - 2) / (1.0 - r * r)))

    if t is None:
        status = "inconclusive"
        decided = "The correlation is undefined (no variation), so it meets neither the confirm nor the reject rule."
    elif r > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The correlation is positive with t >= 2 and the mean fall beyond drift is above 0."
        else:
            status = "inconclusive"
            decided = "The correlation is positive with t >= 2 but the supporting check (mean fall beyond drift above 0) fails."
    elif r < 0 and t <= -2:
        status = "rejected"
        decided = "The correlation is negative with t <= -2: larger rises are followed by larger further rises."
    else:
        status = "inconclusive"
        decided = "The correlation t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": r,
                         "statistic": ({"name": "t of Pearson correlation", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
