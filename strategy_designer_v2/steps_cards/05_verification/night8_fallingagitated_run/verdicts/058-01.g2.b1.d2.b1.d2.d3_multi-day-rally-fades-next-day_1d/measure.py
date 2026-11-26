import numpy as np
import pandas as pd


def _to_day(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype("float64")
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0.0
        unit = "ms" if med > 1e11 else "s"
        dt = pd.to_datetime(v, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.strftime("%Y-%m-%d").values


def _clustered_t(x, days):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return None, None
    m = float(np.mean(x))
    dev = pd.Series(x - m).groupby(pd.Series(days)).sum().values
    D = len(dev)
    if D < 2:
        return m, None
    var = (D / (D - 1.0)) * float(np.sum(dev ** 2)) / (n ** 2)
    se = np.sqrt(var)
    if not np.isfinite(se) or se == 0:
        return m, None
    return m, float(m / se)


def measure(bars):
    RALLY = "debug_info.components.rally.last_history_value"
    active_total = 0
    active_ok = 0
    case_rows = []  # (coin, day, next_ret, |forecast|)
    coin_means = {}

    for coin in sorted(bars.keys()):
        all_rets = []
        per_window = []
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float)
            nxt = close.shift(-1) / close - 1.0
            prev_ret = close / close.shift(1) - 1.0
            all_rets.append(nxt.dropna().values)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            rally = (pd.to_numeric(df[RALLY], errors="coerce") if RALLY in df.columns
                     else pd.Series([np.nan] * len(df)))
            days = _to_day(df["timestamp"])

            # situation check
            act = fc != 0
            in_profile_up = regime == "mean_reversion"  # profile vetoes passed and up-day rule passed
            up_day_price = prev_ret.isna() | (prev_ret > 0)  # first bar of window: rely on regime
            rising = rally > 0
            short_side = fc < 0
            ok = act & in_profile_up & up_day_price & rising.fillna(False) & short_side
            active_total += int(act.sum())
            active_ok += int(ok.sum())
            per_window.append((days, nxt, fc))
        coin_means[coin] = float(np.mean(np.concatenate(all_rets))) if all_rets and sum(len(a) for a in all_rets) else np.nan
        for days, nxt, fc in per_window:
            sel = (fc < 0) & nxt.notna()
            for i in np.where(sel.values)[0]:
                case_rows.append((coin, days[i], float(nxt.iloc[i]), float(abs(fc.iloc[i]))))

    agreement = (active_ok / active_total) if active_total > 0 else None
    passed = agreement is not None and agreement >= 0.9
    threshold = "confirm if t >= 2 (and size check > 0); reject if t <= -2; else inconclusive"
    reading = ("The falling-agitated profile and the up-day rule are taken from the recorded regime "
               "('mean_reversion', since the detector's components are not recorded and their 60/365-day "
               "lookbacks exceed the window), plus the up day from prices and a positive raw rally, short side; "
               "cases are all bars with forecast below 0 with a next close in the window, the coin's mean daily "
               "return is over all its windows, t is clustered by UTC day, the larger half is |forecast| strictly "
               "above the median and the 30 distinct case days minimum is treated as the plan's minimum count.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean short-direction unusual next-day move", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": active_total, "active bars in situation": active_ok},
            "decided_by": ("Fewer than 90% of active bars are short bars of a falling-agitated, up-day, "
                           "rising-5-day situation, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    if case_rows:
        cdf = pd.DataFrame(case_rows, columns=["coin", "day", "ret", "absf"])
        cdf["mu"] = cdf["coin"].map(coin_means)
        cdf = cdf[cdf["mu"].notna()]
        cdf["unusual"] = -(cdf["ret"] - cdf["mu"])
    else:
        cdf = pd.DataFrame(columns=["coin", "day", "ret", "absf", "mu", "unusual"])

    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0
    mean_u, t = (None, None)
    if n_cases:
        mean_u, t = _clustered_t(cdf["unusual"].values, cdf["day"].values)

    diff = None
    n_large = n_small = 0
    if n_cases:
        med = float(np.median(cdf["absf"].values))
        large = cdf[cdf["absf"] > med]["unusual"]
        small = cdf[cdf["absf"] <= med]["unusual"]
        n_large, n_small = int(len(large)), int(len(small))
        if n_large > 0 and n_small > 0:
            diff = float(large.mean() - small.mean())
    size_pass = (diff > 0) if diff is not None else None

    counts = {"distinct case days": n_days, "cases": n_cases,
              "larger half cases": n_large, "smaller half cases": n_small}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither confirm nor reject is met."
    elif t >= 2 and size_pass:
        status = "confirmed"
        decided = "The mean short-direction unusual move has t >= 2 and the larger-half minus smaller-half difference is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The mean short-direction unusual move has t <= -2: the coin rose more than usual after these rallies."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the larger-half minus smaller-half difference is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean short-direction unusual next-day move",
                         "value": float(mean_u) if mean_u is not None else None,
                         "statistic": ({"name": "t of the mean, cases pooled by day", "value": float(t)}
                                       if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "larger-half minus smaller-half mean unusual move (|forecast| median split)",
                             "value": diff, "passed": size_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
