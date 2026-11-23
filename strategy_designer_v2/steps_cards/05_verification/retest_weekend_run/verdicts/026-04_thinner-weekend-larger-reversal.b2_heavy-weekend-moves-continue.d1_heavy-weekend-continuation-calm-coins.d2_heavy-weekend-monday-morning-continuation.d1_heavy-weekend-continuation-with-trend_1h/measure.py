import numpy as np
import pandas as pd


def measure(bars):
    H = 12
    WK, MO, VS, VB = 48, 720, 48, 120

    # ---------- per-coin normal 12-bar drift (non-overlapping, all windows) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                rets.extend(r[np.isfinite(r)].tolist())
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    n_active = 0
    n_eval = 0
    n_agree = 0
    cases = []  # (coin, week_key, unusual, abs_forecast)

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            v = pd.to_numeric(df["volume"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            col = "debug_info.components.wkmove.last_history_value"
            raw = (pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
                   if col in df.columns else np.full(len(df), np.nan))
            close_end = ts + pd.Timedelta(hours=1)
            n = len(df)
            vcum = np.concatenate([[0.0], np.nancumsum(np.nan_to_num(v))])

            active = np.where(f != 0)[0]
            for t in active:
                n_active += 1
                # situation: bar whose close ends Sunday (next bar Monday 00:00 UTC)
                is_sun_close = (close_end.iloc[t].weekday() == 0 and close_end.iloc[t].hour == 0)
                r48 = c[t] / c[t - WK] - 1.0 if t >= WK else np.nan
                if not np.isfinite(r48) and np.isfinite(raw[t]):
                    r48 = raw[t]  # sign of the recorded weekend move
                r720 = c[t] / c[t - MO] - 1.0 if t >= MO else np.nan
                if t >= VS + VB - 1:
                    vrec = (vcum[t + 1] - vcum[t + 1 - VS]) / VS
                    vpri = (vcum[t + 1 - VS] - vcum[t + 1 - VS - VB]) / VB
                    vr = vrec / vpri if vpri > 0 else np.nan
                else:
                    vr = np.nan
                if not (np.isfinite(r48) and np.isfinite(r720) and np.isfinite(vr)):
                    continue  # situation not evaluable from the record
                n_eval += 1
                sit = (is_sun_close and r48 != 0 and np.sign(r48) == np.sign(r720) and vr > 1.0)
                if sit and np.sign(f[t]) == np.sign(r48):
                    n_agree += 1

            # cases for the criterion
            seen = set()
            for t in active:
                iso = ts.iloc[t].isocalendar()
                key = (int(iso[0]), int(iso[1]))
                if key in seen:
                    continue
                seen.add(key)
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r) or not np.isfinite(drift[coin]):
                    continue
                cases.append((coin, (r - drift[coin]) * np.sign(f[t]), abs(f[t])))

    agreement = float(n_agree / n_eval) if n_eval else None
    passed = bool(agreement is not None and agreement >= 0.9)
    reading_base = ("situation bar read as the bar whose close (timestamp + 1h) is Monday 00:00 UTC, with 48/720-bar "
                    "returns and the 48-vs-prior-120-bar volume ratio rebuilt from in-window prices, active bars "
                    "lacking that history left out of the agreement share; cases deduplicated to the first nonzero "
                    "bar per coin per ISO week, and the median split puts |forecast| above the median in the upper half")

    main_name = "mean unusual 12-bar move in the forecast's direction"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "evaluable active bars": int(n_eval)},
            "decided_by": ("fewer than 90% of the evaluable active bars are Sunday-close bars with same-sign 48/720-bar "
                           "returns, weekend volume above the prior 120 weekday bars, and the forecast on the weekend "
                           "move's side"),
            "reading": reading_base,
        }

    u = np.array([x[1] for x in cases], dtype=float)
    a = np.array([x[2] for x in cases], dtype=float)
    nc = len(u)
    mean = float(np.mean(u)) if nc else None
    if nc >= 2 and np.std(u, ddof=1) > 0:
        tstat = float(mean / (np.std(u, ddof=1) / np.sqrt(nc)))
    else:
        tstat = None

    sup_val = None
    sup_pass = None
    if nc >= 2:
        med = np.median(a)
        up, lo = u[a > med], u[a <= med]
        if len(up) and len(lo):
            sup_val = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(sup_val > 0)

    if nc < 100:
        status = "not observable"
        decided = f"only {nc} cases over all coins and windows, fewer than the plan's minimum of 100"
    elif tstat is not None and mean > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "mean unusual move > 0 with t >= 2 and the upper-minus-lower |forecast| half difference is above 0"
        else:
            status = "inconclusive"
            decided = "mean unusual move > 0 with t >= 2 but the supporting check fails, which the plan calls inconclusive"
    elif tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "mean unusual move < 0 with t <= -2"
    else:
        status = "inconclusive"
        decided = "t between -2 and 2, which the plan calls inconclusive"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean", "value": tstat} if tstat is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "upper minus lower half of |forecast|, mean unusual move",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"cases over all coins and windows": int(nc),
                   "active bars": int(n_active), "evaluable active bars": int(n_eval)},
        "decided_by": decided,
        "reading": reading_base,
    }
