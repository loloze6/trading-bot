import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    MIN_CASES = 100

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    per_coin = {}  # coin -> list of (window df prepared)

    for coin, wins in bars.items():
        per_coin[coin] = []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            end = ts + pd.Timedelta(hours=1)  # the bar's close time
            is_fri0 = (end.dt.weekday == 4) & (end.dt.hour == 0) & (end.dt.minute == 0)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)

            raw_col = "debug_info.components.rise48.last_history_value"
            if raw_col in d.columns:
                raw = pd.to_numeric(d[raw_col], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            recomputed = close / close.shift(H) - 1.0
            raw = raw.where(raw.notna(), recomputed)

            situation = is_fri0 & (raw > 0)
            active = fc != 0
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            fwd = close.shift(-H) / close - 1.0  # inside this window only
            per_coin[coin].append({"close": close, "fc": fc, "fri0": is_fri0, "fwd": fwd})

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the OLS slope of excess 48-bar return on forecast, Friday 00:00 cases"
    threshold = "confirm: t >= 2 with forecast-weighted mean excess > 0; reject: t <= -2"
    sup_name = "forecast-weighted mean excess 48-bar return > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars closing at "
                           "Friday 00:00 UTC after a positive 48-bar return, as the plan's situation states."),
            "reading": ("The situation bar is the one whose close (timestamp + 1h) is Friday 00:00 UTC, with a "
                        "positive raw 48-bar return (recomputed from closes where not recorded)."),
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wlist in per_coin.items():
        # coin's mean 48-bar return over all its windows, non-overlapping grid 0, H, 2H...
        grid_rets = []
        for w in wlist:
            c = w["close"].values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.append(r[np.isfinite(r)])
        if not grid_rets:
            continue
        allr = np.concatenate(grid_rets)
        if len(allr) == 0:
            continue
        mean_ret = float(np.mean(allr))
        for w in wlist:
            mask = w["fri0"] & (w["fc"] > 0) & w["fwd"].notna()
            if mask.any():
                xs.extend(w["fc"][mask].astype(float).tolist())
                ys.extend((w["fwd"][mask].astype(float) - mean_ret).tolist())

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n = int(len(x))

    wmean = float(np.sum(x * y) / np.sum(x)) if n > 0 and np.sum(x) > 0 else None

    slope = None
    tval = None
    if n >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            tval = float(lr.slope / lr.stderr)

    sup_pass = (wmean > 0) if wmean is not None else None
    counts = {"cases across coins and windows": n}
    reading = ("Cases are bars whose close (timestamp + 1h) is Friday 00:00 UTC with forecast > 0 and a full "
               "48-row forward return inside the window; the coin's mean 48-bar return is taken on the "
               "non-overlapping grid of all its windows pooled; one pooled OLS across all coins.")

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of {MIN_CASES} across coins and windows."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the forecast-weighted mean excess return is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": wmean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
