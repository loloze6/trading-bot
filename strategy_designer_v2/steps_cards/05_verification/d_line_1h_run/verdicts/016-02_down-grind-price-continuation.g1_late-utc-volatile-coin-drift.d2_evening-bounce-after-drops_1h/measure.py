import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.fall24.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            # Coming bar's hour: the hour at which this bar closes.
            coming_hour = (ts.dt.hour + 1) % 24
            in_hours = coming_hour.isin([21, 22])
            # Fall over 24 bars: the raw component value, or the price return when it is not recorded.
            ret24 = close / close.shift(24) - 1.0
            if LHV in d.columns:
                raw = pd.to_numeric(d[LHV], errors="coerce")
                fall_sign = raw.where(raw.notna(), ret24)
            else:
                fall_sign = ret24
            fallen = fall_sign < 0
            situation = in_hours & fallen
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "ordinary t of the mean of (excess 2-bar return x forecast/10) on 20:00 UTC decision bars"
    threshold = "confirm if t >= 2 and supporting slope > 0; reject if t <= -2; otherwise inconclusive; at least 200 decision bars with forecast > 0"
    reading = ("Coming hour is taken as the bar's start hour + 1; the fall is the sign of the raw fall24 value "
               "(the 24-bar price return where it is not recorded); the main mean pools all 20:00 decision bars, "
               "including those with forecast 0 (product 0); the coin mean 2-bar return is pooled over all its windows "
               "on a grid at positions 0, 2, 4, ... of each window; a shortfall of the plan's 200-bar minimum is reported "
               "as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars whose coming hour is 21 or 22 UTC "
                           "after a 24-bar fall, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    products = []
    excess_pos = []
    fc_pos = []
    n_decision = 0
    for coin, wins in bars.items():
        # Coin mean 2-bar return on a non-overlapping grid, pooled over all windows.
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            idx = np.arange(0, len(c) - 2, 2)
            if len(idx) == 0:
                continue
            r = c[idx + 2] / c[idx] - 1.0
            grid_rets.append(r[np.isfinite(r)])
        if not grid_rets:
            continue
        allr = np.concatenate(grid_rets)
        if len(allr) == 0:
            continue
        coin_mean = float(np.mean(allr))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            fwd = c.shift(-2) / c - 1.0
            dec = (ts.dt.hour == 20) & (ts.dt.minute == 0)
            sel = dec & fwd.notna() & fc.notna() & np.isfinite(fwd)
            ex = (fwd[sel] - coin_mean).to_numpy(dtype=float)
            f = fc[sel].to_numpy(dtype=float)
            n_decision += len(ex)
            products.append(ex * f / 10.0)
            pos = f > 0
            excess_pos.append(ex[pos])
            fc_pos.append(f[pos])

    prod = np.concatenate(products) if products else np.array([])
    ex_p = np.concatenate(excess_pos) if excess_pos else np.array([])
    f_p = np.concatenate(fc_pos) if fc_pos else np.array([])
    n_pos = int(len(f_p))

    mean_val = float(np.mean(prod)) if len(prod) > 0 else None
    t_val = None
    if len(prod) > 1:
        sd = float(np.std(prod, ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(len(prod))))

    slope = None
    if n_pos >= 3 and np.ptp(f_p) > 0:
        slope = float(stats.linregress(f_p, ex_p).slope)
    slope_passed = None if slope is None else bool(slope > 0)

    counts = {"decision bars with forecast > 0": n_pos, "decision bars": int(n_decision)}

    if n_pos < 200:
        status = "not observable"
        decided = f"The plan needs at least 200 decision bars with forecast > 0; the record has {n_pos}."
    elif t_val is None:
        status = "inconclusive"
        decided = "The main t could not be computed (no variance in the product)."
    elif t_val >= 2 and slope_passed:
        status = "confirmed"
        decided = "The main t is 2 or more and the supporting slope is above 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main t is -2 or less."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The main t is 2 or more, but the supporting slope is 0 or below."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "ordinary t of the mean", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of excess 2-bar return on forecast, decision bars with forecast > 0",
            "value": slope,
            "passed": slope_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
