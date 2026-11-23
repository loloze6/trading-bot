import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.excess_power_nearness.last_history_value"
    MIN_CASES = 300

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0) & raw.notna()
            n_active += int(active.sum())
            # negate: the bet runs against the joint reading, so the forecast sign is minus the raw sign
            agree = active & (raw != 0) & (np.sign(f) == -np.sign(raw))
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Active bars are bars with a nonzero forecast and a recorded raw value, the expected side being "
               "the opposite of the raw (w - wbar) x z sign because of negate; the slope is the OLS slope (with "
               "intercept) of each grid case's 5-day return minus the coin's mean 5-day grid return over all its "
               "windows, on the forecast, pooled over all grid cases including zero forecasts; the timing part "
               "is the mean over days of the coins' mean gross daily gain (position after the previous bar's "
               "trade x the bar's return) minus the same with the coin's mean daily return over all windows; "
               "the plan's 'fewer than 300 grid cases with a nonzero forecast' is applied first as the minimum count.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars have a forecast sign opposite to the sign of the raw "
                           "excess-power x nearness-z reading, which the Fidelity's counter-bet requires."),
            "reading": reading,
        }

    # ---------- 2. main measure: pooled slope on the 5-bar grid ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        recs = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1.0 if c[i] and np.isfinite(c[i]) else np.nan
                recs.append((r, f[i]))
        if not recs:
            continue
        r_all = np.array([a for a, _ in recs], dtype=float)
        f_all = np.array([b for _, b in recs], dtype=float)
        ok_r = np.isfinite(r_all)
        if ok_r.sum() == 0:
            continue
        drift = float(np.mean(r_all[ok_r]))
        ok = ok_r & np.isfinite(f_all)
        xs.extend(f_all[ok].tolist())
        ys.extend((r_all[ok] - drift).tolist())
    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_grid = int(len(x))
    n_nonzero = int(np.sum(x != 0)) if n_grid else 0

    slope, tval = None, None
    if n_grid >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. supporting check: timing part of the book's gross mean daily return ----------
    book_rows, mkt_rows = [], []
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce")
            rets.append((c / c.shift(1) - 1.0).iloc[1:])
        if not rets:
            continue
        allr = pd.concat(rets)
        allr = allr[np.isfinite(allr)]
        if len(allr) == 0:
            continue
        mu = float(allr.mean())
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce")
            a = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            r = c / c.shift(1) - 1.0
            pos = a.shift(1)
            day = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            g = pd.DataFrame({"day": day, "gross": pos * r, "mkt": pos * mu}).iloc[1:]
            g = g.dropna()
            g["coin"] = coin
            book_rows.append(g)
    timing = None
    if book_rows:
        B = pd.concat(book_rows)
        per_coin_day = B.groupby(["day", "coin"])[["gross", "mkt"]].sum()
        per_day = per_coin_day.groupby(level="day").mean()
        if len(per_day):
            timing = float(per_day["gross"].mean() - per_day["mkt"].mean())
    sup_pass = None if timing is None else bool(timing > 0)

    counts = {"grid cases with a nonzero forecast": n_nonzero, "grid cases": n_grid}
    main = {
        "name": "pooled slope of drift-removed 5-day return on forecast",
        "value": slope,
        "statistic": None if tval is None else {"name": "OLS t of slope", "value": tval},
        "threshold": "confirm: slope > 0 with t >= 2 (and timing > 0); reject: slope < 0 with t <= -2",
    }
    sup = {"name": "timing part of book's mean daily return before costs", "value": timing, "passed": sup_pass}

    if n_nonzero < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_nonzero} grid cases with a nonzero forecast, fewer than the plan's minimum of 300."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the timing part of the book's mean daily return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope has t >= 2 but the timing part of the book's mean daily return is at or below 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
