import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    EPS = 1e-9
    WCOL = "debug_info.components.width.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            for c in ["open", "high", "low", "close", "forecast"]:
                d[c] = pd.to_numeric(d[c], errors="coerce")
            rng = d["high"] - d["low"]
            mean20 = rng.rolling(20, min_periods=20).mean()
            width_px = rng / mean20.replace(0, np.nan)
            if WCOL in d.columns:
                wrec = pd.to_numeric(d[WCOL], errors="coerce")
                width = wrec.where(wrec.notna(), width_px)
            else:
                width = width_px
            d["_width"] = width
            fall = d["close"].shift(1) < d["close"].shift(6)
            fall_ok = d["close"].shift(6).notna() & d["close"].shift(1).notna()
            loc = (d["close"] - d["low"]) / rng.replace(0, np.nan)
            computable = fall_ok & width.notna() & loc.notna()
            situation = fall & (width >= 1.5 - EPS) & (loc >= 0.75 - EPS)
            active = d["forecast"].fillna(0) != 0
            n_active_uncomputable += int((active & ~computable).sum())
            act_c = active & computable
            n_active += int(act_c.sum())
            n_agree += int((act_c & situation & (d["forecast"] < 0)).sum())
            prepared[coin][w] = d

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    threshold_words = "mean short-direction unusual move > 0 with day-clustered t >= 2 to confirm; < 0 with t <= -2 to reject; at least 30 distinct case days"
    reading_base = ("Situation from prices (close[t-1]<close[t-6], range over 20-bar mean range incl. the day >= 1.5 using the recorded width where present, "
                    "(close-low)/(high-low) >= 0.75), active bars whose 20-bar range mean cannot be computed inside the window are left out of the agreement; "
                    "cases are short bets (rise of -forecast of >= 2 from its low since the last bet), one per 3-bar grid cell of each window, "
                    "t clusters deviations by UTC day, and the 30-case minimum is counted on distinct days.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active, "active bars on situation and short": n_agree},
            "decided_by": ("Fewer than 90% of the active bars are bars where the prior 5-day fall, a >=1.5x wide range and a close in the top quarter "
                           "hold with a short forecast." if n_active > 0 else "No active bar could be checked against the situation."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    case_rows = []
    for coin, wins in prepared.items():
        grid_rets = []
        for w, d in wins.items():
            c = d["close"].values
            for p in range(0, len(d) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1)
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, d in wins.items():
            f = d["forecast"].fillna(0).values
            c = d["close"].values
            base = 0.0
            used_cells = set()
            for i in range(len(d)):
                s = -f[i] if f[i] < 0 else 0.0
                if s <= 0:
                    base = 0.0
                    continue
                if s - base >= BAND - EPS:
                    base = s
                    cell = i // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if i + H < len(d) and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0 and np.isfinite(drift):
                        r = c[i + H] / c[i] - 1
                        case_rows.append({
                            "day": d["timestamp"].iloc[i].floor("D"),
                            "unusual": -(r - drift),
                            "width": d["_width"].iloc[i],
                        })
                else:
                    base = min(base, s)

    cases = pd.DataFrame(case_rows, columns=["day", "unusual", "width"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["unusual"].mean()) if n_cases else None
    t_val = None
    if n_cases and n_days >= 2:
        dev = cases["unusual"] - mean_u
        g = dev.groupby(cases["day"]).sum().values
        var = (n_days / (n_days - 1)) * np.sum(g ** 2) / (n_cases ** 2)
        if var > 0:
            t_val = float(mean_u / np.sqrt(var))

    slope = None
    reg = cases.dropna(subset=["width", "unusual"])
    if len(reg) >= 3 and reg["width"].nunique() > 1:
        slope = float(stats.linregress(reg["width"].values, reg["unusual"].values).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"cases": n_cases, "cases counted on distinct days": n_days}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, below the plan's minimum of 30 cases counted on distinct days."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither confirm nor reject rule is met."
    elif mean_u > 0 and t_val >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean short-direction unusual move above 0 with t >= 2 and a positive slope on the range multiple."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean short-direction unusual move below 0 with t <= -2: the coin rises more than its drift after these days."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t of 2 or more but the supporting slope is at or below 0 (or not computable), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean short-direction 3-bar unusual move per case",
            "value": mean_u,
            "statistic": {"name": "t of the mean, cases clustered by day", "value": t_val} if t_val is not None else None,
            "threshold": threshold_words,
        },
        "supporting_check": {"name": "OLS slope of unusual move on raw range multiple", "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
