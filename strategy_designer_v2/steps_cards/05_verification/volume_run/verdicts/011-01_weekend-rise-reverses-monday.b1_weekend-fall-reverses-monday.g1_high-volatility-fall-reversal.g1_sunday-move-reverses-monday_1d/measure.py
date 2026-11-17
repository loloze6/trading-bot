import numpy as np
import pandas as pd


def measure(bars):
    MV = "debug_info.components.sunday_move.last_history_value"
    VOL = "debug_info.components.sunday_volume.last_history_value"

    def ols(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        n = len(x)
        if n < 3:
            return None, None, n
        xm = x - x.mean()
        sxx = float((xm ** 2).sum())
        if sxx <= 0:
            return None, None, n
        b = float((xm * (y - y.mean())).sum() / sxx)
        a = y.mean() - b * x.mean()
        resid = y - a - b * x
        s2 = float((resid ** 2).sum() / (n - 2))
        se = np.sqrt(s2 / sxx) if s2 > 0 else 0.0
        return b, se, n

    # ---------- situation check ----------
    active = 0
    agree = 0
    rows = []  # (coin, forecast, excess next return, volume value)
    for coin, wins in bars.items():
        # coin mean daily return over all windows together
        all_r = []
        prepared = {}
        for w, df in wins.items():
            d = df.copy()
            d["_ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("_ts").reset_index(drop=True)
            c = d["close"].astype(float)
            d["_fwd"] = c.shift(-1) / c - 1.0
            d["_back"] = c / c.shift(1) - 1.0
            prepared[w] = d
            all_r.append(d["_fwd"].dropna().values)
        allr = np.concatenate(all_r) if all_r else np.array([])
        mu = float(np.mean(allr)) if len(allr) else np.nan

        for w, d in prepared.items():
            f = pd.to_numeric(d["forecast"], errors="coerce")
            mv = pd.to_numeric(d[MV], errors="coerce") if MV in d.columns else pd.Series(np.nan, index=d.index)
            vv = pd.to_numeric(d[VOL], errors="coerce") if VOL in d.columns else pd.Series(np.nan, index=d.index)
            is_sun = d["_ts"].dt.dayofweek == 6
            for i in range(len(d)):
                fi = f.iloc[i]
                if pd.notna(fi) and fi != 0:
                    active += 1
                    move = mv.iloc[i]
                    if pd.isna(move):
                        move = d["_back"].iloc[i]
                    if bool(is_sun.iloc[i]) and pd.notna(move) and move != 0 and np.sign(fi) == -np.sign(move):
                        agree += 1
            # cases for the criterion
            reg = d["regime"].astype(str) == "mean_reversion"
            for i in np.where(reg.values)[0]:
                fi = f.iloc[i]
                r = d["_fwd"].iloc[i]
                if pd.isna(fi) or pd.isna(r) or pd.isna(mu):
                    continue
                rows.append((coin, float(fi), float(r - mu), vv.iloc[i]))

    agreement = agree / active if active > 0 else 0.0
    passed = active > 0 and agreement >= 0.9

    main_name = "pooled OLS slope of Monday excess return on Sunday forecast"
    threshold = "confirm: slope > 0 with t >= 2 and volume difference > 0 with t >= 2; reject: slope < 0 with t <= -2 or difference < 0 with t <= -2"
    reading = ("Sunday cases are the regime 'mean_reversion' bars with a next bar in the same window, the slope is OLS with intercept on the "
               "'forecast' column, the volume split is per coin at the median of sunday_volume last_history_value over all its Sunday cases "
               "(high = above median, low = at or below), the difference t is (b_high - b_low)/sqrt(se_high^2 + se_low^2), and the situation "
               "side is taken from the sign of sunday_move last_history_value (price return if missing).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active)},
            "decided_by": "fewer than 90% of the bars with a non-zero forecast are Sunday bars whose forecast sign is opposite to the Sunday move, as the plan's situation requires",
            "reading": reading,
        }

    df = pd.DataFrame(rows, columns=["coin", "x", "y", "v"])
    n_total = int(len(df))
    b, se, _ = ols(df["x"], df["y"]) if n_total else (None, None, 0)
    t_main = (b / se) if (b is not None and se and se > 0) else None

    dv = df.dropna(subset=["v"]).copy()
    dv["v"] = dv["v"].astype(float)
    hi_mask = pd.Series(False, index=dv.index)
    for coin, g in dv.groupby("coin"):
        med = g["v"].median()
        hi_mask.loc[g.index] = g["v"] > med
    hi = dv[hi_mask]
    lo = dv[~hi_mask]
    n_hi, n_lo = int(len(hi)), int(len(lo))
    bh, seh, _ = ols(hi["x"], hi["y"])
    bl, sel, _ = ols(lo["x"], lo["y"])
    diff, t_diff = None, None
    if bh is not None and bl is not None:
        diff = bh - bl
        den = np.sqrt(seh ** 2 + sel ** 2)
        t_diff = diff / den if den > 0 else None

    counts = {"Sunday cases": n_total, "high-volume half": n_hi, "low-volume half": n_lo}

    sup_passed = None if (diff is None or t_diff is None) else bool(diff > 0 and t_diff >= 2)

    if n_total < 300 or n_hi < 100 or n_lo < 100:
        status = "not observable"
        decided = "the plan's minimum of 300 Sunday cases in total and 100 in each volume half is not reached"
    elif t_main is None or t_diff is None:
        status = "inconclusive"
        decided = "a slope or its t could not be computed, so neither the confirm nor the reject rule is met"
    else:
        main_rej = b < 0 and t_main <= -2
        diff_rej = diff < 0 and t_diff <= -2
        main_conf = b > 0 and t_main >= 2
        if main_rej or diff_rej:
            status = "rejected"
            decided = ("the main slope is negative with t <= -2 (Sunday moves continue into Monday)" if main_rej
                       else "the volume difference is negative with t <= -2 (reversal weaker on heavy-volume Sundays)")
        elif main_conf and sup_passed:
            status = "confirmed"
            decided = "the main slope is positive with t >= 2 and the volume difference is positive with t >= 2"
        else:
            status = "inconclusive"
            decided = "the result meets neither the confirm rule nor the reject rule, so it is inconclusive"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": None if b is None else float(b),
            "statistic": None if t_main is None else {"name": "OLS slope t", "value": float(t_main)},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "high-volume minus low-volume slope, t",
            "value": None if diff is None else float(diff),
            "passed": sup_passed,
            "t": None if t_diff is None else float(t_diff),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
