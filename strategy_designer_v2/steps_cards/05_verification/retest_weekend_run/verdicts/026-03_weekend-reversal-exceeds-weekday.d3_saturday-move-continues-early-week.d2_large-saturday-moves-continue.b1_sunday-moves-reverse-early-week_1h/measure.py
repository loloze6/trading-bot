import numpy as np
import pandas as pd
from scipy import stats


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        med = float(np.nanmedian(s.values.astype(float))) if len(s) else 0.0
        unit = "ms" if med > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 48
    RAW = "debug_info.components.sunday_move.last_history_value"
    POST = "debug_info.components.sunday_move.post_pipeline_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0

    # ---------- cases ----------
    case_rows = []  # (coin, forward return)
    drift = {}

    for coin in sorted(bars.keys()):
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin].keys(), key=lambda x: (len(str(x)), str(x))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            n = len(df)

            # non-overlapping 48-bar returns for the coin's drift (positions 0, H, 2H, ...)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)

            ts = _to_utc(df["timestamp"])
            close_time = ts + pd.Timedelta(hours=1)  # timestamp is the bar's start
            is_sit = ((close_time.dt.weekday == 0) & (close_time.dt.hour == 0)).values

            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            raw = (pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
                   if RAW in df.columns else np.full(n, np.nan))
            post = (pd.to_numeric(df[POST], errors="coerce").values.astype(float)
                    if POST in df.columns else np.full(n, np.nan))

            # fallback: Sunday's 24-bar return from prices
            ret24 = np.full(n, np.nan)
            if n > 24:
                ret24[24:] = close[24:] / close[:-24] - 1.0
            move = np.where(np.isfinite(raw), raw, ret24)

            active = fc != 0
            expected_sign = -np.sign(move)
            agree = active & is_sit & np.isfinite(move) & (np.sign(fc) == expected_sign) & (expected_sign != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            # cases: Monday 00:00 bars with non-zero forecast
            idx = np.where(active & is_sit)[0]
            for i in idx:
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                x = post[i]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0 and np.isfinite(x)):
                    continue
                coin_cases.append((x, c1 / c0 - 1.0))

        drift[coin] = float(np.mean(grid_rets)) if len(grid_rets) else np.nan
        for x, r in coin_cases:
            if np.isfinite(drift[coin]):
                case_rows.append((coin, x, r - drift[coin]))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The situation is the bar whose close (timestamp + 1h) is Monday 00:00 UTC, with the side "
               "opposite to the sign of the raw sunday_move (or Sunday's 24-bar price return where not recorded); "
               "the drift is each coin's mean of non-overlapping 48-bar returns (positions 0, 48, ... of each window) "
               "pooled over its windows; the regression is OLS with intercept of the drift-adjusted return on "
               "post_pipeline_value, and |forecast| and its sign in the supporting check are read from "
               "post_pipeline_value; cases without 48 bars ahead in their window are left out; fewer than 200 cases "
               "gives 'not observable' as the workflow requires.")

    main_name = "OLS slope of drift-adjusted 48-bar return on post_pipeline_value of sunday_move"
    threshold = "slope > 0 with t >= 2 to confirm (with check); slope < 0 with t <= -2 to reject"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Monday 00:00 bars with a "
                           "forecast against Sunday's move, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    n_cases = len(case_rows)
    xs = np.array([c[1] for c in case_rows], dtype=float)
    ys = np.array([c[2] for c in case_rows], dtype=float)

    slope = None
    tval = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    big = np.abs(xs) >= 2 if n_cases else np.array([], dtype=bool)
    n_big = int(big.sum()) if n_cases else 0
    sup_val = float(np.mean(ys[big] * np.sign(xs[big]))) if n_big > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    counts = {"cases across all coins and windows": int(n_cases),
              "cases with |forecast| >= 2": n_big}

    if n_cases < 200:
        status = "not observable"
        decided = f"The plan needs at least 200 cases across all coins and windows; only {n_cases} were found."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the supporting check passes (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails (inconclusive rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: Sunday's move continues rather than reverses (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean of drift-adjusted 48-bar return x sign(forecast) over |forecast| >= 2",
            "value": sup_val,
            "passed": (bool(sup_pass) if sup_pass is not None else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
