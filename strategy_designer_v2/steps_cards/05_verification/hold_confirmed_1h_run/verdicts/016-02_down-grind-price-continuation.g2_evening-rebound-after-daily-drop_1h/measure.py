import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fall24.last_history_value"
    H = 2

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            # The bar that follows starts at 21:00 or 22:00 UTC, so this bar is stamped 20:00 or 21:00.
            next_hour = ((ts + pd.Timedelta(hours=1)).dt.hour).to_numpy()
            in_slot = np.isin(next_hour, [21, 22])
            fell = np.where(np.isnan(raw), False, raw < 0)
            active = np.where(np.isnan(fc), False, fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & in_slot & fell & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "OLS slope of 2-bar excess return on forecast at 20:00-stamped bars"
    threshold = "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"
    reading = ("The situation is bars whose next bar starts at 21:00 or 22:00 UTC with a negative raw 24-bar "
               "vol-scaled return and a positive forecast. The regression pools all coins' 20:00-stamped decision "
               "bars, including those with a zero forecast. Each coin's mean 2-bar return is taken on the "
               "non-overlapping grid 0,2,4,... of every window, pooled across windows. A shortfall from the "
               "300-case minimum is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars in the 21:00-22:00 "
                           "UTC slot after a 24-hour fall, which is the situation the plan's Fidelity describes."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # Coin mean 2-bar return over all windows (non-overlapping grid)
        grid_rets = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fwd = np.full(len(close), np.nan)
            if len(close) > H:
                fwd[:-H] = close[H:] / close[:-H] - 1.0
            g = fwd[0::H]
            grid_rets.append(g[~np.isnan(g)])
            per_win.append((df, fwd))
        if not grid_rets:
            continue
        allg = np.concatenate(grid_rets)
        if len(allg) == 0:
            continue
        mu = float(np.mean(allg))
        for df, fwd in per_win:
            ts = pd.to_datetime(df["timestamp"], utc=True)
            is_dec = ((ts.dt.hour == 20) & (ts.dt.minute == 0)).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            m = is_dec & ~np.isnan(fc) & ~np.isnan(fwd)
            xs.append(fc[m])
            ys.append(fwd[m] - mu)

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n_dec = int(len(x))
    n_pos = int((x > 0).sum())

    counts = {"decision bars": n_dec, "decision bars with a positive forecast": n_pos}

    slope, tstat = None, None
    if n_dec >= 3 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tstat = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    sup_val, sup_pass = None, None
    if n_pos > 0:
        pos = x > 0
        med = np.median(x[pos])
        sel = pos & (x > med)
        counts["decision bars above the median positive forecast"] = int(sel.sum())
        if sel.sum() > 0:
            sup_val = float(np.mean(y[sel]))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {
        "name": main_name,
        "value": slope,
        "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
        "threshold": threshold,
    }
    support = {"name": "mean excess 2-bar return above median positive forecast",
               "value": sup_val, "passed": sup_pass}

    if n_pos < 300:
        status = "not observable"
        decided = (f"Only {n_pos} decision bars have a positive forecast, below the plan's minimum of 300.")
    elif tstat is None or slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm rule nor the reject rule is met."
    elif slope > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the supporting check passes."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
