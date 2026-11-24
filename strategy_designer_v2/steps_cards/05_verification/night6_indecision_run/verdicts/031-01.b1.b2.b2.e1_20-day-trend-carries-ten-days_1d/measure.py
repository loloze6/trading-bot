import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.vsr20.last_history_value"

    def raw_values(df):
        # Raw component value as recorded; recompute from prices where missing.
        close = df["close"].astype(float).reset_index(drop=True)
        if RAW in df.columns:
            raw = pd.to_numeric(df[RAW], errors="coerce").reset_index(drop=True)
        else:
            raw = pd.Series(np.nan, index=close.index)
        r1 = close.pct_change()
        ret20 = close / close.shift(20) - 1.0
        vol = r1.rolling(20, min_periods=20).std() * np.sqrt(20)
        recomputed = ret20 / vol.replace(0, np.nan)
        return raw.where(raw.notna(), recomputed)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            raw = raw_values(df)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: positive scaled 20-day return; expected side: long
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"grid bars with a forecast above 0": None},
            "decided_by": ("Fewer than 90% of the active bars are long bars with a positive scaled "
                           "20-day return, the plan's situation and side."),
            "reading": "none",
        }

    # ---------- 2. main measure: slope of excess 10-bar return on forecast ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            for i in range(0, len(close), H):
                if i + H < len(close):
                    fwd = close[i + H] / close[i] - 1.0
                    rows.append((fwd, fc[i]))
        if not rows:
            continue
        fwds = np.array([r[0] for r in rows], dtype=float)
        fcs = np.array([r[1] for r in rows], dtype=float)
        ok_f = np.isfinite(fwds)
        if ok_f.sum() == 0:
            continue
        drift = float(np.mean(fwds[ok_f]))  # coin's normal 10-bar drift over all windows
        ok = ok_f & np.isfinite(fcs)
        xs.extend(fcs[ok].tolist())
        ys.extend((fwds[ok] - drift).tolist())

    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    n_grid = int(len(xs))
    n_pos = int((xs > 0).sum())

    slope = None
    t_slope = None
    if n_grid >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. supporting check: timing gain ----------
    book_parts, mkt_parts = [], []
    for coin, wins in bars.items():
        # coin's mean daily return over all its windows
        all_r = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            all_r.append(df["close"].astype(float).pct_change().iloc[1:])
        if not all_r:
            continue
        mu = float(pd.concat(all_r).dropna().mean())
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.copy()
            d["day"] = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D")
            last = d.groupby("day", sort=True).tail(1).set_index("day")
            val = pd.to_numeric(last["postRebalance_total_value"], errors="coerce")
            alloc = pd.to_numeric(last["postRebalance_current_allocation"], errors="coerce")
            book_r = val.pct_change().iloc[1:]
            mkt_g = (alloc.shift(1) * mu).iloc[1:]
            book_parts.append(pd.DataFrame({"coin": coin, "r": book_r}))
            mkt_parts.append(pd.DataFrame({"coin": coin, "g": mkt_g}))

    timing = None
    if book_parts:
        b = pd.concat(book_parts).dropna()
        m = pd.concat(mkt_parts).dropna()
        book_daily = b.groupby(level=0)["r"].mean()
        mkt_daily = m.groupby(level=0)["g"].mean()
        if len(book_daily) > 0 and len(mkt_daily) > 0:
            timing = float(book_daily.mean() - mkt_daily.mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. decision ----------
    if n_pos < 100:
        status = "not observable"
        decided_by = f"Only {n_pos} grid bars have a forecast above 0, below the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and timing_pass:
        status = "confirmed"
        decided_by = "The slope has t >= 2 and the timing gain is above 0."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope has t >= 2 but the timing gain is not above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope has t <= -2."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement),
                            "passed": passed},
        "main_measure": {
            "name": "OLS slope of 10-bar forward return minus coin's normal 10-bar drift on the forecast",
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": "confirm if t >= 2 (with timing gain > 0); reject if t <= -2",
        },
        "supporting_check": {
            "name": "book mean daily return minus gain from the market's own rise (timing)",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": {"grid bars with a forecast above 0": n_pos, "grid bars": n_grid},
        "decided_by": decided_by,
        "reading": ("The slope is an ordinary least-squares regression over all pooled non-overlapping "
                    "grid bars (positions 0, 10, 20, ... with a full 10-bar forward return in the window), "
                    "flat bars with forecast 0 included, with each coin's drift being its mean 10-bar "
                    "return on that grid over all its windows; the plan's 'else inconclusive' minimum of 100 "
                    "grid bars with forecast above 0 is applied as 'not observable', as the workflow requires."),
    }
