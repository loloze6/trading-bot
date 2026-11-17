import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.fall.last_history_value"
    POS = "postRebalance_current_allocation"

    # ---------- per-coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) >= 2:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    reg_x, reg_y = [], []
    timing_rows = []

    for coin, wins in bars.items():
        mu = coin_mean[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            if n == 0:
                continue
            # today's return, inside the window
            r_today = np.full(n, np.nan)
            if n >= 2:
                r_today[1:] = close[1:] / close[:-1] - 1.0
            lhv = (pd.to_numeric(df[LHV], errors="coerce").to_numpy(dtype=float)
                   if LHV in df.columns else np.full(n, np.nan))
            # next-day return, inside the window
            r_next = np.full(n, np.nan)
            if n >= 2:
                r_next[:-1] = close[1:] / close[:-1] - 1.0

            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if np.isfinite(r_today[i]):
                    down = r_today[i] < 0
                elif np.isfinite(lhv[i]):
                    down = lhv[i] < 0
                else:
                    down = False
                if down and f > 0:
                    n_agree += 1

            # main measure rows
            for i in range(n):
                if np.isfinite(fc[i]) and fc[i] > 0 and np.isfinite(r_next[i]) and np.isfinite(mu):
                    reg_x.append(fc[i])
                    reg_y.append(r_next[i] - mu)

            # timing gain rows
            if POS in df.columns:
                pos = pd.to_numeric(df[POS], errors="coerce").to_numpy(dtype=float)
                ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
                day = ts.dt.floor("D")
                for i in range(n):
                    if np.isfinite(pos[i]) and np.isfinite(r_next[i]) and np.isfinite(mu) and pd.notna(day.iloc[i]):
                        timing_rows.append((w, day.iloc[i], coin, pos[i] * (r_next[i] - mu)))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "t of OLS slope of next-day excess return on forecast, forecast>0 bars"
    threshold = "confirm if slope t >= 2 with mean timing gain > 0; reject if slope t <= -2; at least 500 bars with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": int(len(reg_x)), "active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of active bars are one-day falls with a long forecast, "
                           "below the 90% needed for the plan's situation (a coin's one-day fall, long side)."),
            "reading": ("A bar is in the situation when close[t]/close[t-1]-1 < 0 inside its window, using the sign of "
                        "the fall component's last_history_value on a window's first bar."),
        }

    # ---------- main measure ----------
    x = np.asarray(reg_x, dtype=float)
    y = np.asarray(reg_y, dtype=float)
    n_cases = int(x.size)
    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- supporting check ----------
    tg_mean = None
    n_days = 0
    if timing_rows:
        tdf = pd.DataFrame(timing_rows, columns=["window", "day", "coin", "tg"])
        daily = tdf.groupby(["window", "day"])["tg"].mean()
        n_days = int(daily.size)
        tg_mean = float(daily.mean()) if n_days else None
    tg_pass = (tg_mean is not None and tg_mean > 0)

    counts = {"bars with forecast > 0": n_cases, "book days": n_days}

    if n_cases < 500:
        status = "not observable"
        decided = f"Only {n_cases} bars with forecast > 0 (with a next-day return), fewer than the plan's minimum of 500."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no variation in forecast), so it meets neither the confirm nor the reject rule."
    elif t_slope >= 2 and tg_pass:
        status = "confirmed"
        decided = "Slope t is 2 or more and the mean timing gain is above 0, meeting the confirm rule."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t is -2 or less, meeting the reject rule."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Slope t is 2 or more but the mean timing gain is 0 or less, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean daily timing gain of the book (position x (coin return - coin mean))",
            "value": tg_mean,
            "passed": bool(tg_pass) if tg_mean is not None else None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The 500-bar minimum counts forecast > 0 bars that have a next-day close in the same window, and the "
                    "daily book's timing gain is each day's mean over coins of postRebalance_current_allocation x "
                    "(next-day return - coin mean), averaged over all days."),
    }
