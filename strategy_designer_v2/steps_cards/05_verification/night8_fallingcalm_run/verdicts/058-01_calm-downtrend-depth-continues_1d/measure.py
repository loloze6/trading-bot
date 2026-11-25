import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    FALL_COL = "debug_info.components.fall30.last_history_value"

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce")
            if FALL_COL in df.columns:
                fall = pd.to_numeric(df[FALL_COL], errors="coerce")
            else:
                fall = pd.Series(np.nan, index=df.index)
            # fall back to prices (inside the window) where the component is not recorded
            fall_px = (close / close.shift(30) - 1.0) * 100.0
            fall = fall.where(fall.notna(), fall_px).values
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array(["unknown"] * len(df))
            active = fc != 0
            # situation: falling calm profile (regime not vetoed to chop) and a 30-day fall; side: short
            situ = (regime != "chop") & np.isfinite(fall) & (fall < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the active bars are short bars in the falling calm profile "
                           "(regime not chop) with the coin below its close of 30 days ago."
                           if n_active > 0 else "The record has no active bar, so the config never takes the plan's short position."),
            "reading": "The falling calm profile is read from the recorded regime (not 'chop'), the 30-day fall from fall30's raw value.",
        }

    # ---------------- 2. criterion ----------------
    # coin drift: mean 5-bar return over the non-overlapping grids of all windows
    drift = {}
    cells = []
    for coin, wins in bars.items():
        all_r = []
        coin_cells = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_r.append(r)
                f = fc[i]
                if np.isfinite(f) and f < 0 and pd.notna(ts.iloc[i]):
                    coin_cells.append((coin, ts.iloc[i].floor("D"), r, abs(float(f))))
        drift[coin] = float(np.mean(all_r)) if len(all_r) else np.nan
        cells.extend(coin_cells)

    rows = [(c, d, -(r - drift[c]), a) for (c, d, r, a) in cells if np.isfinite(drift[c])]
    n_cases = len(rows)
    n_days = len(set(r[1] for r in rows))
    counts = {"grid cases in a position (forecast < 0)": int(n_cases), "days": int(n_days)}

    mean = None
    t = None
    supp_val = None
    supp_pass = None
    if n_cases > 0:
        x = np.array([r[2] for r in rows], dtype=float)
        wgt = np.array([r[3] for r in rows], dtype=float)
        days = [r[1] for r in rows]
        sw = wgt.sum()
        if sw > 0:
            mean = float((x * wgt).sum() / sw)
            dev = pd.Series(wgt * (x - mean)).groupby(pd.Series(days)).sum().values
            J = len(dev)
            if J > 1:
                var = (dev ** 2).sum() / sw ** 2 * J / (J - 1)
                se = np.sqrt(var)
                t = float(mean / se) if se > 0 else None
        # supporting check: larger-|forecast| half minus smaller half (unweighted means)
        if n_cases >= 2:
            order = np.argsort(wgt, kind="mergesort")
            k = n_cases // 2
            low = x[order[:k]]
            high = x[order[n_cases - k:]]
            supp_val = float(high.mean() - low.mean())
            supp_pass = bool(supp_val > 0)

    main = {
        "name": "|forecast|-weighted mean signed 5-bar excess return (short side)",
        "value": mean,
        "statistic": {"name": "t of the weighted mean, cases of one day pooled", "value": t} if t is not None else None,
        "threshold": "confirm above 0 with t >= 2 and the supporting check above 0; reject below 0 with t <= -2",
    }
    supp = {"name": "larger-|forecast| half minus smaller-|forecast| half signed excess return",
            "value": supp_val, "passed": supp_pass}
    reading = ("The falling calm profile is read from the recorded regime (not 'chop'); halves are split by rank of "
               "|forecast| (middle case left out when odd) and compared by their unweighted mean; the day-pooled t "
               "sums the weighted deviations per UTC day (cluster-robust, J/(J-1) correction); the plan's 'fewer than "
               "30 grid cases' minimum is reported as not observable.")

    if n_cases < 30:
        return {"status": "not observable",
                "situation_check": {"agreement": agreement, "passed": True},
                "main_measure": main, "supporting_check": supp, "counts": counts,
                "decided_by": f"Only {n_cases} grid cases with forecast < 0 on the coins together, fewer than the plan's 30.",
                "reading": reading}

    if mean is not None and t is not None and mean > 0 and t >= 2 and supp_pass:
        status = "confirmed"
        dec = "The weighted mean signed excess return is above 0 with t >= 2 and the supporting check is above 0."
    elif mean is not None and t is not None and mean < 0 and t <= -2:
        status = "rejected"
        dec = "The weighted mean signed excess return is below 0 with t <= -2."
    elif mean is not None and t is not None and mean > 0 and t >= 2:
        status = "inconclusive"
        dec = "A confirming t with a failed supporting check is inconclusive."
    else:
        status = "inconclusive"
        dec = "The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive."

    return {"status": status,
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main, "supporting_check": supp, "counts": counts,
            "decided_by": dec, "reading": reading}
