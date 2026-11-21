import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    MIN_CASES = 30
    COL_BREAK = "debug_info.components.break.last_history_value"

    def fnum(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        return None if not np.isfinite(x) else x

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    cases = []  # (coin, adj_fall, ret30)

    for coin, wins in bars.items():
        prepared = {}
        drift_samples = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp")
            d = d.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(d)
            # 30-bar return from closes, inside the window
            r30 = np.full(n, np.nan)
            if n > 30:
                r30[30:] = close[30:] / close[:-30] - 1.0
            regime = d["regime"].astype(str).to_numpy() if "regime" in d.columns else np.array([""] * n)
            in_regime = np.where(np.isfinite(r30), r30 < 0, regime == "mean_reversion")
            if COL_BREAK in d.columns:
                brk = pd.to_numeric(d[COL_BREAK], errors="coerce").to_numpy(dtype=float)
            else:
                brk = np.full(n, np.nan)
            fresh_break = np.isfinite(brk) & (brk > 0)
            situation = in_regime & fresh_break

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # drift samples: grid positions 0, H, 2H ...
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    drift_samples.append(close[p + H] / close[p] - 1.0)
            prepared[w] = (close, fc, r30, n)

        drift = float(np.mean(drift_samples)) if len(drift_samples) else np.nan

        # ---------- cases: short bets, once per 10-bar grid cell ----------
        for w, (close, fc, r30, n) in prepared.items():
            ref = 0.0
            side_prev = 0
            used_cells = set()
            for t in range(n):
                f = fc[t]
                side = 0 if f == 0 else (1 if f > 0 else -1)
                if side == 0 or side != side_prev:
                    ref = 0.0
                if side == 0:
                    side_prev = 0
                    continue
                m = abs(f)
                is_bet = (m - ref) >= BAND
                if is_bet:
                    ref = m
                else:
                    ref = min(ref, m)
                side_prev = side
                if not is_bet or side != -1:
                    continue
                cell = t // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if t + H >= n or not np.isfinite(drift):
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                ret = close[t + H] / close[t] - 1.0
                adj_fall = -(ret - drift)
                cases.append((coin, adj_fall, r30[t]))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean drift-adjusted 10-bar fall after short cases"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and deeper-half minus shallower-half > 0; reject: mean is a rise with t <= -2 over >= 30 cases"
    reading = ("The plan's situation is computed as a fresh resistance break (raw break component > 0) on a bar whose 30-bar "
               "close-to-close return is below 0 (from the window's closes, or the recorded regime where 30 past closes are not in the "
               "window), on the short side; a case is a short bet of the forecast (a rise of at least 2 points on the short side), "
               "the first one per 10-bar grid cell from each window's first row, with the drift the mean of the coin's grid 10-bar returns "
               "over all windows; the deeper-decline half is the cases with 30-bar return below the median, the rest the shallower half; "
               "the plan's 'fewer than 30 cases' is applied as the minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": fnum(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": int(len(cases))},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars of a fresh resistance break inside a "
                           "negative 30-bar return; the config's forecast does not follow the plan's situation and side."
                           if agreement is not None else "No bar has a non-zero forecast, so the situation cannot be matched."),
            "reading": reading,
        }

    vals = np.array([c[1] for c in cases], dtype=float)
    n_cases = int(len(vals))
    mean = float(vals.mean()) if n_cases else None
    tstat = None
    if n_cases >= 2:
        sd = float(vals.std(ddof=1))
        if sd > 0:
            tstat = mean / (sd / np.sqrt(n_cases))

    # supporting check
    r30s = np.array([c[2] for c in cases], dtype=float)
    ok = np.isfinite(r30s) & np.isfinite(vals)
    support_val = None
    n_deep = n_shallow = 0
    if ok.sum() >= 2:
        rv = r30s[ok]
        fv = vals[ok]
        med = float(np.median(rv))
        deep = rv < med
        shallow = ~deep
        n_deep, n_shallow = int(deep.sum()), int(shallow.sum())
        if n_deep > 0 and n_shallow > 0:
            support_val = float(fv[deep].mean() - fv[shallow].mean())
    support_pass = None if support_val is None else bool(support_val > 0)

    counts = {"cases": n_cases, "deeper-half cases": n_deep, "shallower-half cases": n_shallow}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30 cases."
    elif tstat is not None and mean > 0 and tstat >= 2 and support_pass is True:
        status = "confirmed"
        decided = "The mean drift-adjusted fall is above 0 with t >= 2 over at least 30 cases, and the deeper-decline half falls more."
    elif tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean drift-adjusted 10-bar move after cases is a rise with t <= -2 over at least 30 cases."
    elif tstat is not None and tstat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the deeper-decline half does not fall more than the shallower half."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": fnum(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": fnum(mean),
                         "statistic": ({"name": "t of the mean", "value": fnum(tstat)} if tstat is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "deeper-decline half minus shallower half, mean drift-adjusted fall",
                             "value": fnum(support_val), "passed": support_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
