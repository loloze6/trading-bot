import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fade.last_history_value"

    # ---------- collect per-window data ----------
    sit_active = 0
    sit_agree = 0
    reg_x, reg_y_raw = [], []
    all_next_rets = []          # coin daily returns, all windows pooled (close-based)
    book_rets = []
    held_positions = []

    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = bars[coin][win].copy()
            if df is None or len(df) == 0:
                continue
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").astype(float)

            # --- situation check: fade the day's move (raw sign = day's return sign) ---
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").astype(float)
            else:
                raw = pd.Series(np.nan, index=df.index)
            day_ret = close / close.shift(1) - 1.0
            move_sign = np.sign(raw)
            move_sign = move_sign.where(raw.notna(), np.sign(day_ret))
            active = fc.notna() & (fc != 0)
            sit_active += int(active.sum())
            ok = active & move_sign.notna() & (move_sign != 0) & (np.sign(fc) == -move_sign)
            sit_agree += int(ok.sum())

            # --- main measure data: next-bar return inside the window ---
            nxt = close.shift(-1) / close - 1.0
            all_next_rets.extend(nxt.dropna().tolist())
            m = nxt.notna() & fc.notna()
            reg_x.extend(fc[m].tolist())
            reg_y_raw.extend(nxt[m].tolist())

            # --- book daily returns (value after rebalance, last bar of each UTC day) ---
            if "timestamp" in df.columns:
                ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
                day = ts.dt.floor("D")
            else:
                day = pd.Series(np.arange(len(df)), index=df.index)
            val = pd.to_numeric(df["postRebalance_total_value"], errors="coerce").astype(float)
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").astype(float)
            g = pd.DataFrame({"day": day, "val": val, "alloc": alloc}).dropna(subset=["day"])
            daily = g.groupby("day", sort=True).last()
            br = daily["val"] / daily["val"].shift(1) - 1.0
            pos_held = daily["alloc"].shift(1)   # position held into the day
            mm = br.notna() & pos_held.notna()
            book_rets.extend(br[mm].tolist())
            held_positions.extend(pos_held[mm].tolist())

    agreement = (sit_agree / sit_active) if sit_active > 0 else 0.0
    passed = bool(sit_active > 0 and agreement >= 0.9)
    threshold_txt = "confirm: slope > 0 with t >= 2 and timing gain > 0; reject: slope < 0 with t <= -2; otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "OLS slope of demeaned next-bar return on forecast",
                             "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"bars with a non-zero forecast": int(sit_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast fade the day's move "
                           "(forecast sign opposite to the day's return), as the plan's situation and outcome require."),
            "reading": "The day's move sign is taken from the fade component's raw value, or from the close-to-close return where the raw value is missing.",
        }

    # ---------- main measure ----------
    mu = float(np.mean(all_next_rets)) if len(all_next_rets) else np.nan
    x = np.asarray(reg_x, dtype=float)
    y = np.asarray(reg_y_raw, dtype=float) - mu
    n_nonzero = int(np.sum(x != 0))

    slope, tval = None, None
    if len(x) >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- supporting check: timing gain ----------
    timing = None
    if len(book_rets) > 0 and np.isfinite(mu):
        timing = float(np.mean(book_rets) - np.mean(np.asarray(held_positions) * mu))
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- decision ----------
    if n_nonzero < 1000:
        status = "not observable"
        decided = f"Only {n_nonzero} bars with a non-zero forecast, below the plan's minimum of 1000."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed."
    elif slope > 0 and tval >= 2:
        if timing_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the timing gain is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the timing gain is not positive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "OLS slope of demeaned next-bar return on forecast",
                         "value": slope,
                         "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
                         "threshold": threshold_txt},
        "supporting_check": {"name": "book timing gain (mean daily return minus position x coin mean daily return)",
                             "value": timing, "passed": timing_pass},
        "counts": {"bars with a non-zero forecast": n_nonzero, "bars in regression": int(len(x))},
        "decided_by": decided,
        "reading": ("The 1000-bar minimum is counted on the regression bars (those with a next-bar return in the same window) "
                    "with a non-zero forecast, and the coin's mean daily return is the mean of all close-to-close daily returns pooled over windows."),
    }
