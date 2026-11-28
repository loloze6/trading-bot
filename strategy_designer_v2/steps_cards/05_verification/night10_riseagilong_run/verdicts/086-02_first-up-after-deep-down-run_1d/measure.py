import json
import numpy as np
import pandas as pd
from scipy import stats

H = 5
MIN_CASE_DAYS = 30


def _depth_lhv(df):
    """Raw value of the 'depth' component (last_history_value), NaN where not recorded."""
    col = "debug_info.components.depth.last_history_value"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce").astype(float)
    out = pd.Series(np.nan, index=df.index, dtype=float)
    if "debug_info.components" in df.columns:
        vals = []
        for v in df["debug_info.components"].values:
            x = np.nan
            try:
                if isinstance(v, str):
                    v = json.loads(v)
                if isinstance(v, dict):
                    d = v.get("depth")
                    if isinstance(d, dict) and d.get("last_history_value") is not None:
                        x = float(d.get("last_history_value"))
            except Exception:
                x = np.nan
            vals.append(x)
        out = pd.Series(vals, index=df.index, dtype=float)
    return out


def _situation(df, depth):
    """First up close ending a run of >= 2 lower closes, on a bar whose regime passed the
    rising-agitated profile vetoes (regime 'trending')."""
    c = df["close"].astype(float).values
    n = len(c)
    reg = df["regime"].astype(str).values
    sit = np.zeros(n, dtype=bool)
    for t in range(n):
        if reg[t] != "trending":
            continue
        if t >= 3:
            sit[t] = (c[t] > c[t - 1]) and (c[t - 1] < c[t - 2]) and (c[t - 2] < c[t - 3])
        else:
            # not enough in-window history to rebuild the run: rely on the recorded run loss
            d = depth.iloc[t]
            sit[t] = bool(np.isfinite(d) and d > 0)
    return sit


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = []
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").astype(float)
            depth = _depth_lhv(df)
            sit = _situation(df, depth)
            active = fc.notna().values & (fc.fillna(0).values != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc.fillna(0).values > 0)).sum())
            prepared.append((coin, w, df, fc, depth))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean 5-day excess return of trending cases with forecast > 0 (vs coin's mean 5-day return)"
    main_thr = "confirm: mean > 0 with t >= 2 (day-clustered); reject: t <= -2"
    sup_name = "OLS slope of 5-day excess return on depth last_history_value"
    reading = ("Situation rebuilt from closes (up close after >= 2 lower closes) on bars with regime 'trending' "
               "(the profile vetoes cannot be recomputed in-window, so their pass is read from the regime, and the "
               "first 3 bars of a window use depth > 0); a case is the first trending bar with forecast > 0 in each "
               "5-bar grid cell of its window, its return taken from that bar's close over 5 bars inside the window; "
               "the coin's mean is over all its windows' non-overlapping grid returns; the plan's '< 30 case-days' "
               "minimum is reported as 'not observable'.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"independent case-days": 0, "cases": 0},
            "decided_by": "No bar has a non-zero forecast, so fewer than 30 independent case-days exist.",
            "reading": reading,
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation, long": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on a first up close "
                           "after >= 2 down closes in the trending (rising agitated) regime."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    coin_grid_rets = {}
    cases = []  # (coin, day, ret, depth)
    for coin, w, df, fc, depth in prepared:
        c = df["close"].astype(float).values
        n = len(c)
        reg = df["regime"].astype(str).values
        ts = pd.to_datetime(df["timestamp"], utc=True)
        days = ts.dt.floor("D").values
        for t in range(0, n - H, H):
            if c[t] > 0 and np.isfinite(c[t]) and np.isfinite(c[t + H]):
                coin_grid_rets.setdefault(coin, []).append(c[t + H] / c[t] - 1.0)
        for start in range(0, n, H):
            for t in range(start, min(start + H, n)):
                f = fc.iloc[t]
                if reg[t] == "trending" and np.isfinite(f) and f > 0:
                    if t + H < n and c[t] > 0 and np.isfinite(c[t + H]):
                        cases.append((coin, days[t], c[t + H] / c[t] - 1.0, float(depth.iloc[t])))
                    break

    coin_mean = {k: float(np.mean(v)) for k, v in coin_grid_rets.items() if len(v) > 0}
    rows = [(co, d, r - coin_mean[co], dep) for co, d, r, dep in cases if co in coin_mean]
    cdf = pd.DataFrame(rows, columns=["coin", "day", "excess", "depth"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_ex, t_mean = None, None
    if n_cases > 0:
        mean_ex = float(cdf["excess"].mean())
        if n_days > 1:
            dev = cdf["excess"] - mean_ex
            s = dev.groupby(cdf["day"]).sum().values
            var = float(np.sum(s ** 2)) / (n_cases ** 2) * n_days / (n_days - 1)
            se = np.sqrt(var)
            t_mean = float(mean_ex / se) if se > 0 else None

    slope, t_slope = None, None
    sd = cdf.dropna(subset=["excess", "depth"]) if n_cases else cdf
    if len(sd) >= 3 and sd["depth"].nunique() > 1:
        lr = stats.linregress(sd["depth"].values, sd["excess"].values)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_pass = None if t_slope is None else bool(slope > 0 and t_slope >= 2)
    counts = {"independent case-days": n_days, "cases": n_cases}

    if n_days < MIN_CASE_DAYS:
        status = "not observable"
        decided = f"Only {n_days} independent case-days, below the plan's minimum of 30."
    elif t_mean is None:
        status = "inconclusive"
        decided = "The mean excess return's t could not be computed, so neither rule is met."
    else:
        rej = (t_mean <= -2) or (t_slope is not None and t_slope <= -2)
        conf = (mean_ex > 0 and t_mean >= 2 and sup_pass is True)
        if rej:
            status = "rejected"
            decided = "Reject rule: the mean excess 5-day return has t <= -2 or the depth slope has t <= -2."
        elif conf:
            status = "confirmed"
            decided = "Confirm rule: mean excess 5-day return > 0 with t >= 2 and depth slope > 0 with t >= 2."
        else:
            status = "inconclusive"
            decided = "Inconclusive rule: neither confirm nor reject is met (a t between -2 and 2 on at least one measure)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": ({"name": "t of the mean, same-day cases summed", "value": t_mean}
                                       if t_mean is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name + " (t)", "value": t_slope, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
