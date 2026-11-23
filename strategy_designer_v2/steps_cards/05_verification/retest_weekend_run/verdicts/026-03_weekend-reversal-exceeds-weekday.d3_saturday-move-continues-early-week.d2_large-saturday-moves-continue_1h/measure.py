import numpy as np
import pandas as pd


def measure(bars):
    H = 48
    LB = 24
    HV = "debug_info.components.sat_move.last_history_value"

    total_active = 0
    agree_active = 0
    case_rows = []  # (coin, forecast, fwd_ret)
    drift_by_coin = {}

    for coin, wins in bars.items():
        # coin's normal 48-bar drift: non-overlapping grid 0, H, 2H, ... per window, pooled over all windows
        grid_rets = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        drift = float(np.mean(grid_rets)) if len(grid_rets) > 0 else np.nan
        drift_by_coin[coin] = drift

        for w, df in wins.items():
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close_time = ts + pd.Timedelta(hours=1)
            situ = ((close_time.dt.dayofweek == 6) & (close_time.dt.hour == 0)
                    & (close_time.dt.minute == 0)).values
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(d["close"], errors="coerce").values
            n = len(d)

            # raw Saturday move: the component's raw value, else the 24-bar return from prices
            raw = (pd.to_numeric(d[HV], errors="coerce").values if HV in d.columns
                   else np.full(n, np.nan))
            ret24 = np.full(n, np.nan)
            if n > LB:
                ret24[LB:] = c[LB:] / c[:-LB] - 1.0
            side_src = np.where(np.isfinite(raw), raw, ret24)
            expected = np.sign(side_src)

            active = f != 0
            total_active += int(active.sum())
            ok = active & situ & np.isfinite(side_src) & (np.sign(f) == expected) & (expected != 0)
            agree_active += int(ok.sum())

            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:-H] = c[H:] / c[:-H] - 1.0
            idx = np.where(situ & active & np.isfinite(fwd))[0]
            for i in idx:
                case_rows.append((coin, float(f[i]), float(fwd[i])))

    agreement = (agree_active / total_active) if total_active > 0 else 0.0
    passed = bool(total_active > 0 and agreement >= 0.9)
    reading = ("The situation bars are those whose close (timestamp + 1 hour) is Sunday 00:00 UTC, with the "
               "expected side the sign of Saturday's raw scaled 24-bar move; the coin's drift is the mean of its "
               "non-overlapping 48-bar grid returns pooled over all windows; cases are all such bars with non-zero "
               "forecast and a full 48-bar forward return in the window; the top quartile is the ceil(n/4) cases "
               "with the largest |forecast| (stable sort) and the rest are all other cases.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "t of mean convex-sized excess 48-bar return", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"active bars": int(total_active), "agreeing active bars": int(agree_active)},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are Saturday-end bars (close Sunday 00:00 UTC) "
                           "with forecast sign equal to the sign of Saturday's move."),
            "reading": reading,
        }

    cdf = pd.DataFrame(case_rows, columns=["coin", "f", "r"])
    if len(cdf):
        cdf["drift"] = cdf["coin"].map(drift_by_coin)
        cdf = cdf[np.isfinite(cdf["drift"])].reset_index(drop=True)
    n_cases = int(len(cdf))
    n_top = int(np.ceil(n_cases * 0.25)) if n_cases > 0 else 0

    mean_x = None
    t = None
    diff = None
    if n_cases >= 2:
        x = (cdf["f"] / 10.0) * (cdf["r"] - cdf["drift"])
        mean_x = float(x.mean())
        sd = float(x.std(ddof=1))
        t = float(mean_x / (sd / np.sqrt(n_cases))) if sd > 0 else None
        y = np.sign(cdf["f"]) * (cdf["r"] - cdf["drift"])
        order = np.argsort(-cdf["f"].abs().values, kind="mergesort")
        top_idx = order[:n_top]
        rest_idx = order[n_top:]
        if len(top_idx) > 0 and len(rest_idx) > 0:
            diff = float(y.values[top_idx].mean() - y.values[rest_idx].mean())

    sup_pass = None if diff is None else bool(diff > 0)
    counts = {"cases": n_cases, "top quartile cases": n_top}

    if n_cases < 100 or n_top < 25:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (need 100) and {n_top} in the top quartile "
                   f"(need 25).")
    elif t is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so neither rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Main t >= 2 and the top quartile's directional excess return beats the rest's."
    elif t <= -2:
        status = "rejected"
        decided = "Main t <= -2: the convexly sized position loses against the coin's drift over the two days."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top quartile does not beat the rest."
    else:
        status = "inconclusive"
        decided = "-2 < t < 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean of (forecast/10) x (48-bar return - drift)",
                         "value": mean_x,
                         "statistic": None if t is None else {"name": "ordinary t of the mean", "value": t},
                         "threshold": "t >= 2 (with supporting check) confirms; t <= -2 rejects"},
        "supporting_check": {"name": "top-quartile |forecast| directional excess minus rest",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
