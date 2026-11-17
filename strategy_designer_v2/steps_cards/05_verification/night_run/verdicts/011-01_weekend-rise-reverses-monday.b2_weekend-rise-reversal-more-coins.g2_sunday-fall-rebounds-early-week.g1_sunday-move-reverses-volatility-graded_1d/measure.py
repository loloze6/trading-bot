import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    MIN_CASES = 300
    RET_COL = "debug_info.components.sun_ret.last_history_value"

    # ---------- per-coin mean 2-bar return over all windows (non-overlapping grid) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            idx = np.arange(0, len(c) - H, H)
            if len(idx) == 0:
                continue
            r = c[idx + H] / c[idx] - 1.0
            r = r[np.isfinite(r)]
            rets.extend(r.tolist())
        coin_mean[coin] = float(np.mean(rets)) if len(rets) > 0 else np.nan

    # ---------- situation check + case collection ----------
    n_active = 0
    n_agree = 0
    case_f = []
    case_ex = []

    for coin, wins in bars.items():
        mu = coin_mean.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))

            # Sunday's raw 1-bar return: recorded component where present, else recomputed from closes within the window
            ret_calc = np.full(len(close), np.nan)
            if len(close) > 1:
                ret_calc[1:] = close[1:] / close[:-1] - 1.0
            if RET_COL in df.columns:
                rec = pd.to_numeric(df[RET_COL], errors="coerce").to_numpy(dtype=float)
                sun_ret = np.where(np.isfinite(rec), rec, ret_calc)
            else:
                sun_ret = ret_calc

            # Sunday bar: bar starting on Sunday (UTC), so the coming bar is Monday
            is_sunday = (ts.dt.dayofweek == 6).to_numpy()

            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            side_ok = np.isfinite(sun_ret) & (np.sign(fc) == -np.sign(sun_ret)) & (np.sign(sun_ret) != 0)
            n_agree += int((active & is_sunday & side_ok).sum())

            # cases: Sunday bars, regime mean_reversion, forecast not 0, 2-bar return inside window
            for t in range(len(close)):
                if not active[t] or regime[t] != "mean_reversion":
                    continue
                if t + H >= len(close):
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] != 0):
                    continue
                if not np.isfinite(mu):
                    continue
                r2 = close[t + H] / close[t] - 1.0
                case_f.append(fc[t])
                case_ex.append(r2 - mu)

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of mean of (forecast/10) x excess 2-bar return on Sunday bars"
    threshold = "confirm if t >= 2 with supporting check passing; reject if t <= -2"
    reading = ("Sunday bars are those whose UTC start timestamp is a Sunday (closing into Monday) with regime "
               "mean_reversion and forecast not 0, the expected side is opposite to the sign of Sunday's 1-bar return, "
               "the coin's mean 2-bar return is taken on the non-overlapping grid (positions 0, 2, 4, ...) pooled over its "
               "windows, and the 'top third' is the ceil(n/3) cases with the largest |forecast|.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"Sunday cases": int(len(case_f)), "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Sunday bars whose forecast fades "
                           "Sunday's move, so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    f = np.asarray(case_f, dtype=float)
    ex = np.asarray(case_ex, dtype=float)
    n = int(len(f))
    vals = (f / 10.0) * ex

    mean_val = float(np.mean(vals)) if n > 0 else None
    t_val = None
    if n > 1:
        sd = float(np.std(vals, ddof=1))
        t_val = float(mean_val / (sd / np.sqrt(n))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_top = 0
    if n > 0:
        n_top = int(np.ceil(n / 3.0))
        order = np.argsort(-np.abs(f), kind="mergesort")[:n_top]
        sup_val = float(np.mean(np.sign(f[order]) * ex[order]))
        sup_pass = bool(sup_val > 0)

    counts = {"Sunday cases": n, "top-third cases": n_top}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} Sunday cases, below the plan's minimum of {MIN_CASES}."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure's t is >= 2 and the supporting check passes (confirm rule)."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main measure's t is <= -2: Sunday moves continue rather than reverse (reject rule)."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The main measure's t is >= 2 but the supporting check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The main measure's t is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean sign(forecast) x excess 2-bar return, top third by |forecast|",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
