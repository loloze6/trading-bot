import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.thin_fall.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            active = fc != 0
            # The kept situation: the product of the 30-day scaled return and the volume factor
            # is negative, which means a 30-day fall, since the volume factor is positive. The
            # component is only recorded inside the profile, so a recorded value also places the
            # bar inside the profile. The expected side is short.
            situation = np.isfinite(raw) & (np.nan_to_num(raw, nan=0.0) < 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of next 5-bar excess return on forecast (nonzero-forecast grid cells)"
    threshold = "slope t >= 2 with check passing confirms; slope t <= -2 rejects"
    sup_name = "mean of minus excess 5-bar return on cells with forecast <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a nonzero forecast are short bars with a negative "
                           "thin-volume scaled 30-day return (the plan's fall situation)."
                           if n_active > 0 else "No bar carries a nonzero forecast."),
            "reading": "Situation taken as a recorded raw thin_fall value below 0, which places the bar in the profile and in a 30-day fall; the expected side is short.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        cells = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                cells.append((c1 / c0 - 1.0, fc[i]))
        if not cells:
            continue
        rets = np.array([c[0] for c in cells])
        fcs = np.array([c[1] for c in cells], dtype=float)
        coin_mean = rets.mean()  # coin's mean 5-bar return over all its windows (same grid)
        ok = np.isfinite(fcs) & (fcs != 0)
        xs.extend(fcs[ok].tolist())
        ys.extend((rets[ok] - coin_mean).tolist())

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cells = int(len(x))

    slope = None
    t_slope = None
    if n_cells >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    deep = x <= -2
    n_deep = int(deep.sum())
    sup_val = float(np.mean(-y[deep])) if n_deep > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    counts = {"grid cells with a nonzero forecast": n_cells,
              "grid cells with forecast <= -2": n_deep}

    if n_cells < 100:
        status = "not observable"
        decided = f"Only {n_cells} grid cells have a nonzero forecast, under the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean short gain on cells with forecast <= -2 is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: deeper, thinner-volume falls are followed by relatively higher returns."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cells from all coins are pooled into one OLS regression of the excess return on the forecast, "
                    "with the coin's mean 5-bar return taken over the same non-overlapping grid of all its windows; "
                    "the plan's minimum of 100 nonzero cells is treated as a minimum count, so missing it gives "
                    "'not observable'; and the supporting check fails when no cell has a forecast of -2 or below."),
    }
