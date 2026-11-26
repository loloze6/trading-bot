import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.vol_dryup.last_history_value"
    PROFILE_REGIME = "unknown"  # the regime the detector gives when neither veto (to chop) fires

    def recompute_raw(vol):
        # ln(mean volume of the last 30 bars / mean volume of the 30 bars before them), inside the window
        v = pd.Series(vol, dtype=float).reset_index(drop=True)
        short = v.rolling(30, min_periods=30).mean()
        prior = v.shift(30).rolling(30, min_periods=30).mean()
        with np.errstate(divide="ignore", invalid="ignore"):
            r = np.log(short / prior)
        r = r.replace([np.inf, -np.inf], np.nan)
        return r.values

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            regime = df["regime"].astype(str).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
            else:
                raw = np.full(len(df), np.nan)
            rec = recompute_raw(df["volume"].values)
            raw = np.where(np.isnan(raw), rec, raw)
            active = (~np.isnan(fc)) & (fc != 0)
            in_sit = (regime == PROFILE_REGIME) & (~np.isnan(raw)) & (raw < 0)
            ok = active & in_sit & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the slope of the excess 5-day return on the forecast, profile grid bars"
    threshold = "confirm if t >= +2 and check mean > 0; reject if t <= -2; inconclusive otherwise"
    check_name = "mean excess 5-day return on grid bars with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the rising agitated "
                           "profile with the 30-day volume shrunk against the 30 days before (raw log ratio < 0)."),
            "reading": "The profile is read as the detector's 'unknown' regime (neither chop veto fired); shrinkage as a raw log volume ratio below 0, recomputed from the window's volume where not recorded.",
        }

    # ---------- criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        rows = []
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            regime = df["regime"].astype(str).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if regime[i] == PROFILE_REGIME and np.isfinite(fc[i]):
                    rows.append((fc[i], r))
        if len(all_rets) == 0:
            continue
        mu = float(np.mean(all_rets))
        for f, r in rows:
            xs.append(f)
            ys.append(r - mu)

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_profile = int(len(x))
    pos = x > 0
    n_pos = int(pos.sum())

    t_slope = None
    slope = None
    if n_profile >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    check_mean = float(np.mean(y[pos])) if n_pos > 0 else None
    check_pass = (check_mean > 0) if check_mean is not None else None

    counts = {
        "non-overlapping grid cases with forecast > 0": n_pos,
        "profile grid bars in total": n_profile,
    }

    if n_pos < 30 or n_profile < 100:
        status = "not observable"
        if n_pos < 30:
            decided = f"Only {n_pos} non-overlapping grid cases with forecast > 0, under the plan's minimum of 30."
        else:
            decided = f"Only {n_profile} profile grid bars in total, under the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t is +2 or more and the mean excess 5-day return on forecast > 0 grid bars is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is +2 or more but the supporting check's mean is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t_slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": check_name, "value": check_mean, "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The profile is the detector's 'unknown' regime on the grid bar, the grid is positions 0,5,10,... of each "
                    "window, all coins are pooled in one regression, and the coin's mean 5-day return is taken over the "
                    "non-overlapping grid returns of all its windows."),
    }
