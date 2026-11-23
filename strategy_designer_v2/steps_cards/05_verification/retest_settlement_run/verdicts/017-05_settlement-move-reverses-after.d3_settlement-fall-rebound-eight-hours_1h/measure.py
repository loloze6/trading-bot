import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 8
    RAW = "debug_info.components.fall2h.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close_hour = (ts + pd.Timedelta(hours=1)).dt.hour
            settle = close_hour.isin([0, 16]).values
            c = d["close"].astype(float)
            ret2 = (c / c.shift(2) - 1.0).values
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
            else:
                raw = np.full(len(d), np.nan)
            fallval = np.where(np.isnan(raw), ret2, raw)
            fall = np.where(np.isnan(fallval), False, fallval < 0)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & settle & fall & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    reading = ("Settlement bars are those whose close (timestamp + 1h) is at 00:00 or 16:00 UTC and a fall is a negative raw fall2h value "
               "(2-bar price return where not recorded); cases are bars with regime mean_reversion and forecast >= 2, 8-bar returns by row "
               "position inside a window, the coin's normal drift is the mean of its non-overlapping 8-bar returns (positions 0, 8, 16, ...) "
               "over all its windows, the t of the weighted mean uses the robust standard error sqrt(n/(n-1)*sum(w^2 (x-m)^2))/sum(w), "
               "and the median split puts forecasts above the median in the upper half and the rest in the lower half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are settlement bars (close at 00:00 or 16:00 UTC) after a 2-bar fall "
                           "with a long forecast, so the config does not do what the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ws = [], []
    for coin, wins in bars.items():
        grid = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = d["close"].astype(float).values
            n = len(c)
            if n > H:
                idx = np.arange(0, n - H, H)
                r = c[idx + H] / c[idx] - 1.0
                grid.extend(list(r[np.isfinite(r)]))
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = c[H:] / c[: n - H] - 1.0
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).values
            mask = (reg == "mean_reversion") & np.isfinite(fc) & (fc >= 2) & np.isfinite(fwd)
            per_win.append((fwd[mask], fc[mask]))
        if len(grid) == 0:
            continue
        drift = float(np.mean(grid))
        for r, f in per_win:
            xs.extend(list(r - drift))
            ws.extend(list(f))

    x = np.asarray(xs, dtype=float)
    wgt = np.asarray(ws, dtype=float)
    n_cases = int(len(x))
    counts = {"cases across all coins and windows": n_cases}

    m = None
    t = None
    if n_cases > 1 and wgt.sum() > 0:
        m = float(np.sum(wgt * x) / np.sum(wgt))
        se = np.sqrt(n_cases / (n_cases - 1) * np.sum(wgt ** 2 * (x - m) ** 2)) / np.sum(wgt)
        t = float(m / se) if se > 0 else 0.0

    diff = None
    welch = None
    if n_cases >= 2:
        med = float(np.median(wgt))
        up = x[wgt > med]
        lo = x[wgt <= med]
        counts["upper half cases"] = int(len(up))
        counts["lower half cases"] = int(len(lo))
        if len(up) >= 1 and len(lo) >= 1:
            diff = float(np.mean(up) - np.mean(lo))
        if len(up) >= 2 and len(lo) >= 2:
            tt = stats.ttest_ind(up, lo, equal_var=False)
            welch = float(tt.statistic) if np.isfinite(tt.statistic) else None
    sup_pass = (diff > 0) if diff is not None else None

    main = {
        "name": "forecast-weighted mean 8-bar excess return of settlement cases with forecast >= 2",
        "value": m,
        "statistic": {"name": "t of the weighted mean", "value": t} if t is not None else None,
        "threshold": "confirm: above 0 with t >= 2; reject: below 0 with t <= -2; otherwise inconclusive",
    }
    support = {
        "name": "upper-half minus lower-half mean excess return (median forecast split), Welch t "
                + (f"{welch:.3f}" if welch is not None else "n/a"),
        "value": diff,
        "passed": bool(sup_pass) if sup_pass is not None else None,
    }

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} cases across all coins and windows, fewer than the plan's minimum of 100."
    elif m is not None and t is not None and m > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The forecast-weighted mean excess return is above 0 with t >= 2 and the upper-minus-lower half difference is above 0."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule but the upper-minus-lower half difference is not above 0, which the plan calls inconclusive."
    elif m is not None and t is not None and m < 0 and t <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the forecast-weighted mean excess return lies between -2 and 2 (or the sign and t do not meet a rule), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
