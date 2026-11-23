import numpy as np
import pandas as pd

RAW = "debug_info.components.absorb_low.last_history_value"


def _raw_from_prices(df):
    vol = df["volume"].astype(float)
    prior = vol.shift(1).rolling(20, min_periods=20).mean()
    rng = (df["high"] - df["low"]).astype(float)
    loc = (df["high"] - df["close"]).astype(float) / rng.replace(0, np.nan)
    return (vol / prior.replace(0, np.nan)) * loc


def _bets(fc, band=2.0):
    out = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f <= 0:
            ref = 0.0
            continue
        if f - ref >= band:
            out[i] = True
            ref = f
        else:
            ref = min(ref, f)
    return out


def measure(bars):
    coins = sorted(bars.keys())

    # ---------- situation check ----------
    n_active, n_agree = 0, 0
    for c in coins:
        for w in sorted(bars[c].keys()):
            df = bars[c][w]
            fc = df["forecast"].astype(float)
            if RAW in df.columns:
                raw = df[RAW].astype(float)
                rec = _raw_from_prices(df)
                raw = raw.where(raw.notna(), rec)
            else:
                raw = _raw_from_prices(df)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars where the graded "
                           "situation (volume over prior 20-day mean times (high-close)/(high-low)) is positive."),
            "reading": "The situation is taken as a positive raw component value (graded heavy-volume close-near-low) on the long side.",
        }

    # ---------- coin mean daily return over all windows ----------
    mu = {}
    for c in coins:
        rs = []
        for w in sorted(bars[c].keys()):
            cl = bars[c][w]["close"].astype(float).values
            if len(cl) > 1:
                rs.append(cl[1:] / cl[:-1] - 1.0)
        allr = np.concatenate(rs) if rs else np.array([])
        allr = allr[np.isfinite(allr)]
        mu[c] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- cases ----------
    excess = []
    for c in coins:
        for w in sorted(bars[c].keys()):
            df = bars[c][w]
            fc = df["forecast"].astype(float).values
            cl = df["close"].astype(float).values
            bet = _bets(fc)
            for i in np.where(bet)[0]:
                if i + 1 < len(cl):
                    r = cl[i + 1] / cl[i] - 1.0
                    if np.isfinite(r) and np.isfinite(mu[c]):
                        excess.append(r - mu[c])
    excess = np.array(excess, dtype=float)
    n_cases = int(len(excess))
    mean_ex = float(np.mean(excess)) if n_cases else None
    if n_cases > 1 and np.std(excess, ddof=1) > 0:
        t = float(mean_ex / (np.std(excess, ddof=1) / np.sqrt(n_cases)))
    else:
        t = None

    # ---------- supporting check: timing part ----------
    rows = []
    for c in coins:
        for w in sorted(bars[c].keys()):
            df = bars[c][w].copy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            df["day"] = ts.dt.floor("D")
            g = df.groupby("day", sort=True).last()
            v = g["postRebalance_total_value"].astype(float)
            pos = g["postRebalance_current_allocation"].astype(float)
            ret = v / v.shift(1) - 1.0
            mkt = pos.shift(1) * mu[c]
            d = pd.DataFrame({"day": g.index, "ret": ret.values, "mkt": mkt.values}).iloc[1:]
            rows.append(d)
    if rows:
        allb = pd.concat(rows, ignore_index=True).dropna(subset=["ret", "mkt"])
        daily = allb.groupby("day").agg(ret=("ret", "mean"), mkt=("mkt", "mean"))
        timing = float(daily["ret"].mean() - daily["mkt"].mean()) if len(daily) else None
    else:
        timing = None
    sup_pass = None if timing is None else bool(timing > 0)

    main = {
        "name": "mean excess next-day return over bet cases (return minus coin mean daily return)",
        "value": mean_ex,
        "statistic": {"name": "ordinary t of the mean", "value": t} if t is not None else None,
        "threshold": "confirm: positive with t >= 2 and timing > 0; reject: negative with t <= -2",
    }
    sup = {"name": "timing part of the book's mean daily return", "value": timing, "passed": sup_pass}
    counts = {"cases": n_cases}
    reading = ("Situation bars are those with a positive raw component value on the long side; cases are the "
               "holding-period bets (forecast rise >= 2 on the long side from its lowest level since the last bet), "
               "every bar being a 1-bar grid cell, excluding a window's last bar; the plan's 'fewer than 100 cases' "
               "is treated as the minimum count giving 'not observable'.")

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, below the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean excess next-day return is positive with t >= 2 and the timing part is above 0."
        else:
            status = "inconclusive"
            decided = "Mean excess next-day return is positive with t >= 2 but the timing part is at or below 0."
    elif mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess next-day return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess next-day return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
