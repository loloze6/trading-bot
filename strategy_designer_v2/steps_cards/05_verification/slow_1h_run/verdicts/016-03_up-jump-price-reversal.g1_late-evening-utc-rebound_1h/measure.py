import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    RAW = "debug_info.components.fall24.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            # coming bar starts at timestamp + 1h; it must start at 20:00 or 21:00 UTC
            next_hour = (ts + pd.Timedelta(hours=1)).dt.hour
            in_hours = next_hour.isin([20, 21]).to_numpy()
            close = pd.to_numeric(d["close"], errors="coerce")
            recomputed = (close / close.shift(24) - 1.0).to_numpy()
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").to_numpy()
                raw = np.where(np.isnan(raw), recomputed, raw)
            else:
                raw = recomputed
            fell = np.where(np.isnan(raw), False, raw < 0)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy()
            active = np.where(np.isnan(fc), False, fc != 0)
            situation = in_hours & fell & (np.nan_to_num(fc) > 0)
            n_active += int(active.sum())
            n_agree += int((active & situation).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast x 2-bar excess return on 19:00 UTC decision bars"
    threshold = "confirm if positive with t >= 2 (and supporting difference > 0); reject if negative with t <= -2"

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars whose coming bar starts at "
                           "20:00 or 21:00 UTC after a 24-bar fall with a long forecast, as the plan's situation requires."),
            "reading": "The situation is read as: bar stamped 19:00 or 20:00 UTC, raw 24-bar change below 0 "
                       "(recomputed from closes where not recorded), forecast above 0.",
        }

    # ---------- 2. criterion ----------
    # coin baseline: mean 2-bar return on the non-overlapping grid (positions 0,2,4,...) over all windows
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy()
            n = len(d)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            grid_idx = np.arange(0, n, H)
            g = fwd[grid_idx]
            grid_rets.append(g[~np.isnan(g)])
            ts = pd.to_datetime(d["timestamp"], utc=True)
            dec = ((ts.dt.hour == 19) & (ts.dt.minute == 0)).to_numpy()
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy()
            for i in np.where(dec)[0]:
                if np.isnan(fwd[i]) or np.isnan(fc[i]):
                    continue
                coin_rows.append((coin, w, float(fc[i]), float(fwd[i])))
        allg = np.concatenate(grid_rets) if grid_rets else np.array([])
        base = float(np.mean(allg)) if len(allg) > 0 else np.nan
        for (c, w, f, r) in coin_rows:
            if np.isnan(base):
                continue
            rows.append((c, w, f, r - base))

    if rows:
        fc_all = np.array([r[2] for r in rows])
        ex_all = np.array([r[3] for r in rows])
    else:
        fc_all = np.array([])
        ex_all = np.array([])

    n_dec = int(len(fc_all))
    n_pos = int((fc_all > 0).sum())

    prod = fc_all * ex_all
    if n_dec >= 2:
        mean_val = float(np.mean(prod))
        sd = float(np.std(prod, ddof=1))
        t_val = float(mean_val / (sd / np.sqrt(n_dec))) if sd > 0 else 0.0
    elif n_dec == 1:
        mean_val, t_val = float(prod[0]), None
    else:
        mean_val, t_val = None, None

    # supporting check
    pos_fc = fc_all[fc_all > 0]
    diff = None
    n_top = 0
    n_zero = int((fc_all == 0).sum())
    if len(pos_fc) > 0 and n_zero > 0:
        q = float(np.quantile(pos_fc, 0.8))
        top_mask = (fc_all > 0) & (fc_all >= q)
        n_top = int(top_mask.sum())
        diff = float(np.mean(ex_all[top_mask]) - np.mean(ex_all[fc_all == 0]))
    elif len(pos_fc) > 0:
        q = float(np.quantile(pos_fc, 0.8))
        n_top = int(((fc_all > 0) & (fc_all >= q)).sum())
    supp_passed = None if diff is None else bool(diff > 0)

    counts = {
        "decision bars with a forecast above 0": n_pos,
        "decision bars": n_dec,
        "top-fifth decision bars": n_top,
        "zero-forecast decision bars": n_zero,
    }

    if n_pos < 500:
        status = "not observable"
        decided = f"Only {n_pos} decision bars have a forecast above 0, below the plan's minimum of 500."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the forecast-weighted mean excess return could not be computed."
    elif mean_val > 0 and t_val >= 2:
        if supp_passed:
            status = "confirmed"
            decided = "The forecast-weighted mean excess return is positive with t >= 2 and the top-fifth minus zero difference is above 0."
        else:
            status = "inconclusive"
            decided = "The mean is positive with t >= 2 but the supporting top-fifth minus zero difference is not above 0."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "ordinary t", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess return, top fifth of positive forecasts minus zero forecasts",
            "value": diff,
            "passed": supp_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The coin's mean 2-bar return is taken on the workflow's non-overlapping grid (positions 0, 2, 4, ... "
                    "of each window) pooled over all windows, the mean of forecast x excess uses all decision bars "
                    "including zero forecasts, and the top fifth is the positive decision-bar forecasts at or above "
                    "their pooled 80th percentile."),
    }
