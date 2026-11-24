import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    eps = 1e-9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            h = d["high"].astype(float)
            l = d["low"].astype(float)
            c = d["close"].astype(float)
            rng = h - l
            # today's range over the mean bar range of the last 20 bars, today included (exclude_current 0)
            mean_rng = rng.rolling(20, min_periods=20).mean()
            ratio = rng / mean_rng.replace(0, np.nan)
            # where the close sits in today's bar, from the low
            loc = (c - l) / rng.replace(0, np.nan)
            f = pd.to_numeric(d[FC], errors="coerce")
            active = f.notna() & (f != 0) & ratio.notna() & loc.notna()
            situ = (ratio >= 1.5 - eps) & (loc <= 0.25 + eps)
            agree = active & situ & (f > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess next-day return on forecast > 0 bars"
    main_thr = "mean > 0 with day-clustered t >= 2 confirms (with slope > 0); mean < 0 with t <= -2 rejects"
    sup_name = "OLS slope of excess next-day return on forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of the plan's "
                           "situation (range >= 1.5x its 20-day mean and close in the bottom quarter of the bar)."),
            "reading": ("The situation is recomputed from prices inside each window with the 20-bar mean range "
                        "including the current bar; active bars where it cannot be computed are left out."),
        }

    # ---------- 2. criterion ----------
    # coin mean daily return over all windows
    coin_mean = {}
    per_coin_frames = {}
    for coin, wins in bars.items():
        allr = []
        frames = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            r = c.shift(-1) / c - 1.0
            allr.append(r.dropna().values)
            frames.append(pd.DataFrame({
                "timestamp": pd.to_datetime(d["timestamp"], utc=True),
                "forecast": pd.to_numeric(d[FC], errors="coerce"),
                "ret": r,
            }))
        allr = np.concatenate(allr) if allr else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan
        per_coin_frames[coin] = frames

    rows = []
    for coin, frames in per_coin_frames.items():
        for fr in frames:
            sel = fr[(fr["forecast"] > 0) & fr["ret"].notna()].copy()
            if sel.empty:
                continue
            sel["excess"] = sel["ret"] - coin_mean[coin]
            sel["day"] = sel["timestamp"].dt.floor("D")
            rows.append(sel[["day", "forecast", "excess"]])
    cases = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["day", "forecast", "excess"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct case days": n_days}

    mean_ex = float(cases["excess"].mean()) if n_cases else None
    t_val = None
    if n_cases and n_days >= 2:
        dev = cases["excess"] - mean_ex
        u = dev.groupby(cases["day"]).sum().values
        se = np.sqrt(np.sum(u ** 2) * n_days / (n_days - 1)) / n_cases
        t_val = float(mean_ex / se) if se > 0 else None

    slope = None
    if n_cases >= 2 and cases["forecast"].astype(float).var() > 0:
        x = cases["forecast"].astype(float).values
        y = cases["excess"].astype(float).values
        xm = x - x.mean()
        slope = float(np.sum(xm * (y - y.mean())) / np.sum(xm ** 2))
    slope_pass = None if slope is None else bool(slope > 0)

    reading = ("The situation is recomputed from prices inside each window (20-bar mean range including the current "
               "bar); every bar with forecast > 0 is a case on the 1-bar grid; the coin's mean is over all its "
               "1-day returns in all windows; the t clusters deviations per UTC day with a D/(D-1) correction; "
               "the plan's 'fewer than 30 distinct case days' is applied as the minimum count (not observable).")

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed (zero spread), so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and t_val >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean excess next-day return is positive with t >= 2 and the slope is positive."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean excess next-day return is negative with t <= -2."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on the forecast is not positive, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day summed", "value": t_val},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
