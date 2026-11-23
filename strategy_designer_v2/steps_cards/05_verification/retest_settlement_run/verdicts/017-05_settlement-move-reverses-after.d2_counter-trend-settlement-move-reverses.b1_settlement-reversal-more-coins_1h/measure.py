import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype("float64")
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0.0
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 8
    MIN_CASES = 200
    LHV = "debug_info.components.trend24.last_history_value"

    active_total = 0
    active_agree = 0
    coin_frames = {}
    coin_drift = {}

    # ---------- per coin, per window preparation ----------
    for coin in sorted(bars.keys()):
        grid_rets = []
        frames = []
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype("float64")
            fc = pd.to_numeric(df["forecast"], errors="coerce").astype("float64").fillna(0.0)
            ts = _to_utc(df["timestamp"]).reset_index(drop=True)
            regime = df["regime"].astype(str).reset_index(drop=True)

            # returns inside the window only
            r2 = close / close.shift(2) - 1.0
            r24_price = close / close.shift(24) - 1.0
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce").astype("float64")
                r24 = lhv.where(lhv.notna(), r24_price)
            else:
                r24 = r24_price
            r8 = close.shift(-H) / close - 1.0

            # the bar closing at a settlement: the coming bar starts at 00, 08 or 16 UTC
            next_hour = (ts + pd.Timedelta(hours=1)).dt.hour
            at_settle = next_hour.isin([0, 8, 16]).values
            against = ((r2 * r24_price) < 0).fillna(False).values
            situation = at_settle & against
            exp_side = np.sign(r24.values)

            act = fc.values != 0
            active_total += int(act.sum())
            agree = act & situation & (np.sign(fc.values) == exp_side) & (exp_side != 0)
            active_agree += int(agree.sum())

            # coin's normal drift: non-overlapping 8-bar grid from each window's first row
            idx = np.arange(0, len(close), H)
            g = r8.values[idx]
            grid_rets.extend([x for x in g if np.isfinite(x)])

            frames.append(pd.DataFrame({
                "fc": fc.values,
                "r8": r8.values,
                "settle": at_settle,
                "mr": (regime == "mean_reversion").values,
            }))
        coin_frames[coin] = frames
        coin_drift[coin] = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

    agreement = (active_agree / active_total) if active_total > 0 else 0.0
    passed = bool(active_total > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x drift-adjusted 8-bar return over settlement mean_reversion cases"
    main_thr = "confirm: mean > 0 with t >= 2 and supporting difference > 0; reject: mean < 0 with t <= -2"
    sup_name = "top-half minus bottom-half |forecast| drift-adjusted 8-bar return in forecast direction"
    reading = ("Settlement bar = bar whose next bar (timestamp + 1h) starts at 00/08/16 UTC, 2- and 24-bar returns "
               "taken positionally inside each window, expected side = sign of the 24-bar return; cases with no "
               "8-bar forward return in their window are left out; halves are the upper and lower floor(n/2) cases "
               "sorted by |forecast| (stable sort, middle case dropped when n is odd); fewer than 200 cases is "
               "reported as not observable per the workflow's minimum-count rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are settlement-close bars where the 2-bar and "
                           "24-bar returns disagree with the forecast on the 24-bar trend's side."),
            "reading": reading,
        }

    # ---------- cases ----------
    vals, fcs, dirret = [], [], []
    for coin in sorted(coin_frames.keys()):
        d = coin_drift[coin]
        if not np.isfinite(d):
            continue
        for f in coin_frames[coin]:
            m = f["settle"].values & f["mr"].values & (f["fc"].values != 0) & np.isfinite(f["r8"].values)
            if not m.any():
                continue
            fc = f["fc"].values[m]
            adj = f["r8"].values[m] - d
            vals.extend(list(fc / 10.0 * adj))
            fcs.extend(list(fc))
            dirret.extend(list(np.sign(fc) * adj))

    vals = np.asarray(vals, dtype=float)
    fcs = np.asarray(fcs, dtype=float)
    dirret = np.asarray(dirret, dtype=float)
    n = int(len(vals))

    mean = float(np.mean(vals)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(vals, ddof=1))
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    diff = None
    half = n // 2
    if half >= 1:
        order = np.argsort(np.abs(fcs), kind="mergesort")
        bottom = dirret[order[:half]]
        top = dirret[order[n - half:]]
        diff = float(np.mean(top) - np.mean(bottom))
    sup_pass = (diff > 0) if diff is not None else None

    counts = {"cases": n, "top half": int(half), "bottom half": int(half)}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 200."
    elif mean is not None and t is not None and mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Main mean > 0 with t >= 2 and the top-half minus bottom-half difference > 0."
    elif mean is not None and t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Main mean < 0 with t <= -2."
    else:
        status = "inconclusive"
        if t is not None and t >= 2 and not sup_pass:
            decided = "t >= 2 but the supporting check's difference is not > 0."
        else:
            decided = "t lies between -2 and 2 (or is undefined), meeting neither confirm nor reject."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
