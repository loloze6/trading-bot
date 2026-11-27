import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    FC = "forecast"
    RAW5 = "debug_info.components.fall5.last_history_value"

    def pct_ret(close, p):
        return (close / close.shift(p) - 1.0) * 100.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            f = d[FC].astype(float)
            pe30 = pct_ret(close, 30)
            pe60 = pct_ret(close, 60)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            # choppy profile and 30-day fall: from prices where computable, else the detector's recorded decision
            price_ok = pe30.notna() & pe60.notna()
            sit_price = (pe30 < 0) & (pe60 >= -10) & (pe60 <= 10)
            sit_regime = regime == "trending"
            regime_sit = np.where(price_ok, sit_price, sit_regime)
            # 5-day fall: raw component value, else recomputed from prices
            if RAW5 in d.columns:
                r5 = d[RAW5].astype(float)
                r5 = r5.where(r5.notna(), pct_ret(close, 5))
            else:
                r5 = pct_ret(close, 5)
            fell5 = (r5 < 0).fillna(False).values
            active = (f != 0) & f.notna()
            ok = active.values & regime_sit.astype(bool) & fell5 & (f < 0).values
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    main_name = "mean unusual 10-bar move per case, short direction"
    thr = "confirm t >= 2 (day-clustered) with larger-minus-smaller half > 0; reject t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars in a choppy market "
                          "(60-day return within +-10%) with a 30-day fall and a 5-day fall, as the Fidelity states.",
            "reading": "Situation computed from prices where the 30/60-bar lookback fits inside the window, else from the recorded regime; 5-day fall from fall5's raw value.",
        }

    # ---------- 2. criterion ----------
    cases = []  # (unusual_short, abs_forecast, day, timestamp, coin)
    for coin, wins in bars.items():
        # normal drift: mean 10-bar return on non-overlapping grid over all windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = d["close"].astype(float).values
            f = d[FC].astype(float).fillna(0.0).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            ref = 0.0
            taken_cells = set()
            for i in range(len(d)):
                fi = f[i]
                if fi >= 0:
                    ref = 0.0
                    continue
                s = -fi
                ref = min(ref, s)
                if s - ref >= BAND - 1e-12:
                    ref = s
                    cell = i // H
                    if cell in taken_cells:
                        continue
                    taken_cells.add(cell)
                    if i + H < len(c) and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                        ret = c[i + H] / c[i] - 1.0
                        u = -(ret - drift)
                        cases.append((u, abs(fi), ts.iloc[i].strftime("%Y-%m-%d"), ts.iloc[i].value, coin))

    n = len(cases)
    days = sorted(set(cs[2] for cs in cases))
    n_days = len(days)
    counts = {"cases": int(n), "distinct days": int(n_days)}
    reading = ("A case is the first short bet (forecast falling >= 2 points from its lowest short level since the last bet) "
               "in each 10-bar grid cell of a window; the median split puts the top floor(n/2) cases by |forecast| "
               "(ties ordered by time and coin) in the larger half; the situation uses prices where the lookback fits "
               "in the window, else the recorded regime.")

    if n < 30 or n_days < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The plan's minimum of 30 cases on at least 30 distinct days is not reached.",
            "reading": reading,
        }

    u = np.array([cs[0] for cs in cases], dtype=float)
    mean_u = float(u.mean())
    dev = u - mean_u
    day_sum = {}
    for k, cs in enumerate(cases):
        day_sum[cs[2]] = day_sum.get(cs[2], 0.0) + dev[k]
    S = np.array(list(day_sum.values()), dtype=float)
    D = len(S)
    var = (S ** 2).sum() * (D / (D - 1.0)) if D > 1 else np.nan
    se = np.sqrt(var) / n if np.isfinite(var) else np.nan
    t = float(mean_u / se) if (np.isfinite(se) and se > 0) else 0.0

    order = sorted(range(n), key=lambda k: (cases[k][1], cases[k][3], cases[k][4]))
    half = n // 2
    small_idx = order[: n - half]
    large_idx = order[n - half:]
    diff = float(u[large_idx].mean() - u[small_idx].mean()) if half > 0 else None
    sup_pass = bool(diff is not None and diff > 0)

    if t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move in the short direction is positive with t >= 2 and the larger-half minus smaller-half difference is above 0."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (larger half minus smaller half > 0) fails, which the plan calls inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "Mean unusual move in the short direction has t <= -2: the coins rise more than their drift after the signal."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": {"name": "t of the mean, cases of one day taken together", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "larger-half minus smaller-half mean unusual move (|forecast| median split)",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
