import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    BAND = 2.0
    THRESH = -2.0
    MIN_DAYS = 30
    FALL_RAW = "debug_info.components.fall.last_history_value"
    FALL_POST = "debug_info.components.fall.post_pipeline_value"

    def vsr_from_prices(close):
        r = close.pct_change()
        sd = r.rolling(20, min_periods=20).std(ddof=1)
        return r / sd.replace(0, np.nan)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce")
            vsr = vsr_from_prices(close)
            if FALL_RAW in df.columns:
                rec = pd.to_numeric(df[FALL_RAW], errors="coerce")
                vsr = rec.where(rec.notna(), vsr)
            vsr = vsr.values
            active = fc != 0
            n_active += int(active.sum())
            sit = np.where(np.isnan(vsr), False, vsr <= THRESH)
            n_agree += int((active & sit & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean unusual 2-bar move per case (long), day-pooled"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    reading = ("Cases are long-side bets (forecast rise >= 2 points from its lowest level on that side since the last bet, "
               "from 0 after a flat), the first bet in each 2-bar grid cell from each window's first row; the normal drift is "
               "the mean of the coin's non-overlapping 2-bar returns on that grid over all its windows; the t pools cases "
               "of the same UTC date by summing their deviations; the slope is OLS of the unusual move on post_pipeline_value "
               "of fall; the plan's 30-distinct-case-day minimum is treated as a minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 1-day return "
                           "over the 20-day std is <= -2, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, ret, direction, post_value)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            post = (pd.to_numeric(df[FALL_POST], errors="coerce").values
                    if FALL_POST in df.columns else np.full(len(df), np.nan))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            # grid returns for drift
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)
            # bet detection
            side = 0
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            bet_side = np.zeros(n, dtype=int)
            for i in range(n):
                f = fc[i]
                s = int(np.sign(f))
                if s == 0:
                    side, low = 0, 0.0
                    continue
                a = abs(f)
                if s != side:
                    side, low = s, 0.0
                else:
                    low = min(low, a)
                if a - low >= BAND - 1e-12:
                    bet[i] = True
                    bet_side[i] = s
                    low = a
            # first bet per grid cell
            for start in range(0, n, H):
                for i in range(start, min(start + H, n)):
                    if bet[i]:
                        if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                            r = close[i + H] / close[i] - 1.0
                            coin_cases.append((coin, ts.iloc[i].normalize(), r, bet_side[i], post[i]))
                        break
        drift[coin] = float(np.mean(grid_rets)) if len(grid_rets) > 0 else np.nan
        cases.extend(coin_cases)

    rows = []
    for coin, day, r, d, pv in cases:
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        u = d * (r - drift[coin])
        rows.append((day, u, pv))
    cdf = pd.DataFrame(rows, columns=["day", "u", "post"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct case days": n_days}

    mean_u = float(cdf["u"].mean()) if n_cases else None
    t = None
    if n_cases >= 2:
        dev = cdf["u"] - mean_u
        s_day = dev.groupby(cdf["day"]).sum()
        se = np.sqrt(float((s_day ** 2).sum())) / n_cases
        if n_days >= 2 and se > 0:
            t = float(mean_u / se)

    slope = None
    sub = cdf.dropna(subset=["u", "post"])
    if len(sub) >= 3 and sub["post"].nunique() > 1:
        slope = float(stats.linregress(sub["post"].values, sub["u"].values).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day pooled", "value": t} if t is not None else None,
            "threshold": threshold}
    support = {"name": "OLS slope of unusual move on fall post_pipeline_value", "value": slope, "passed": slope_pass}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither confirm nor reject is met."
    elif mean_u > 0 and t >= 2 and slope_pass is True:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the slope on the fall's size is positive."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope check is at or below 0 (or not computable), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
