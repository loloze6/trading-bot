import numpy as np
import pandas as pd
from scipy import stats


def _to_day(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        unit = "ms" if s.abs().max() > 1e11 else "s"
        t = pd.to_datetime(s, unit=unit, utc=True)
    else:
        t = pd.to_datetime(s, utc=True)
    return t.dt.floor("D").dt.strftime("%Y-%m-%d").values


def measure(bars):
    MIN_HIST = 20  # below this many past returns in a window, the engine's stored history (warm-up) is not visible

    # ---------- pass 1: coin mean daily return over all windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        rets = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(rets)) if len(rets) else np.nan

    # ---------- pass 2: situation check and cases ----------
    n_active = 0
    n_agree = 0
    case_x, case_f, case_day = [], [], []

    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)
            days = _to_day(df["timestamp"])

            ret1 = np.full(n, np.nan)
            if n > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0

            # situation: the day's return in the bottom 5 % of the coin's past daily returns
            situ = np.zeros(n, dtype=bool)
            for t in range(n):
                r = ret1[t]
                if not np.isfinite(r):
                    continue
                hist = ret1[1:t + 1]
                hist = hist[np.isfinite(hist)]
                if len(hist) - 1 >= MIN_HIST:
                    # negate_percentile: share of history (incl. current) with -x <= -r, i.e. x >= r
                    pct = np.mean(hist >= r)
                    situ[t] = pct >= 0.95
                else:
                    situ[t] = (r < 0) and (regime[t] == "mean_reversion")

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())

            # cases: forecast > 0 with a next close in the same window
            for t in range(n - 1):
                if fc[t] > 0 and np.isfinite(close[t]) and np.isfinite(close[t + 1]) and np.isfinite(mu):
                    x = close[t + 1] / close[t] - 1.0 - mu
                    if np.isfinite(x):
                        case_x.append(x)
                        case_f.append(fc[t])
                        case_day.append(days[t])

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    reading = ("The rank is recomputed from close-to-close returns inside each window over the past returns available "
               "(current included, share of returns at or above it >= 0.95), and where fewer than 20 past returns are "
               "visible the recorded regime plus a down day stands for it; the t is the case mean over a standard error "
               "with each day's deviations summed into one, and the mean daily return per coin is over all its windows.")

    main_name = "mean excess next-day return of forecast>0 cases"
    threshold = "> 0 with t >= 2 to confirm (slope > 0), t <= -2 to reject, over at least 30 distinct days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct case days": None},
            "decided_by": (f"Only {agreement:.1%} of the bars with a non-zero forecast are long bars on a day whose return "
                           "ranks in the bottom 5 % of the coin's past daily returns, below the 90 % needed."),
            "reading": reading,
        }

    x = np.array(case_x, dtype=float)
    f = np.array(case_f, dtype=float)
    d = np.array(case_day)
    n_cases = len(x)
    uniq_days = np.unique(d) if n_cases else np.array([])
    n_days = int(len(uniq_days))

    mean_x = float(np.mean(x)) if n_cases else None
    t_val = None
    if n_cases and n_days >= 2:
        dev = x - mean_x
        sums = pd.Series(dev).groupby(d).sum().values
        se = np.sqrt(np.sum(sums ** 2) * n_days / (n_days - 1)) / n_cases
        t_val = float(mean_x / se) if se > 0 else None

    slope = None
    if n_cases >= 2 and np.unique(f).size >= 2:
        slope = float(stats.linregress(f, x).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"distinct case days": n_days, "cases": int(n_cases)}

    if n_days < 30:
        status = "not observable"
        decided = f"The cases fall on {n_days} distinct days, fewer than the 30 the plan requires."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean excess cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_x > 0 and t_val >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The mean excess next-day return is > 0 with t >= 2 over at least 30 distinct days, and the slope on the forecast is > 0."
        else:
            status = "inconclusive"
            decided = "The mean excess is > 0 with t >= 2, but the supporting slope is not > 0, which the plan calls inconclusive."
    elif t_val <= -2:
        status = "rejected"
        decided = "The mean excess next-day return has t <= -2 over at least 30 distinct days."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess next-day return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_x,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day summed", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {"name": "OLS slope of excess next-day return on forecast", "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
