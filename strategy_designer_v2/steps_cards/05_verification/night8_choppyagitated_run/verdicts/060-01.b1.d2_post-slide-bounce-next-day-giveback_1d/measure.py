import numpy as np
import pandas as pd


def measure(bars):
    RAW_RISE = "debug_info.components.scaled_rise.last_history_value"
    MIN_ACTIVE = 100
    MIN_DAYS = 50

    # ---------- coin drift: mean 1-day return over all windows together ----------
    coin_drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.sort_values("timestamp")
            c = d["close"].astype(float).values
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        rets = np.concatenate(rets) if rets else np.array([])
        coin_drift[coin] = float(np.mean(rets)) if rets.size else np.nan

    # ---------- collect bars ----------
    n_active_all = 0
    n_agree = 0
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        drift = coin_drift.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            prev_ret = close / close.shift(1) - 1.0
            raw = pd.to_numeric(d[RAW_RISE], errors="coerce") if RAW_RISE in d.columns \
                else pd.Series(np.nan, index=d.index)
            # rise: today's 1-day return above 0 (from prices; on the window's first bar, from the raw component)
            rise = np.where(prev_ret.notna(), prev_ret > 0, raw > 0)
            rise = pd.Series(rise, index=d.index).astype(bool)
            regime = d["regime"].astype(str).str.strip().str.lower()
            in_profile = regime == "trending"  # the detector's decision: rise rule passed, falling/agitated vetoes not fired
            active = fc != 0
            n_active_all += int(active.sum())
            n_agree += int((active & rise & in_profile & (fc < 0)).sum())

            # measure rows: forecast below 0, next bar inside the window
            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(d["timestamp"], utc=True)
            m = (fc < 0) & nxt.notna() & np.isfinite(drift)
            if m.any():
                xs.append((-fc[m]).values.astype(float))
                ys.append((nxt[m] - drift).values.astype(float))
                days.append(ts[m].dt.floor("D").astype("int64").values)

    agreement = (n_agree / n_active_all) if n_active_all > 0 else 0.0
    passed = bool(n_active_all > 0 and agreement >= 0.90)

    main_name = "slope of drift-adjusted next 1-day return on short size (-forecast), active bars"
    thr = "confirm: slope < 0 with t <= -2 and mean drift-adjusted return < 0; reject: slope > 0 with t >= +2"
    reading = ("Situation checked as rise bar (prior close-to-close return > 0, raw scaled_rise sign on a window's first bar) "
               "with regime 'trending' as the profile (detector components not recorded, its vetoes encode falling/agitated) "
               "and short side; slope by OLS with intercept, t from day-clustered (CR1) standard errors, drift is each coin's "
               "mean daily return over all its windows, and the plan's minimum counts unmet give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active_all), "distinct days": None},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars on a rise day inside the "
                           "falling agitated profile (agreement %.3f)." % agreement),
            "reading": reading,
        }

    if xs:
        x = np.concatenate(xs); y = np.concatenate(ys); g = np.concatenate(days)
        ok = np.isfinite(x) & np.isfinite(y)
        x, y, g = x[ok], y[ok], g[ok]
    else:
        x = y = g = np.array([])

    n = int(x.size)
    n_days = int(np.unique(g).size) if n else 0
    counts = {"active bars": n, "distinct days": n_days}

    slope = None; t = None; mean_y = None
    if n >= 3:
        xm = x.mean(); ym = y.mean()
        dx = x - xm
        sxx = float(np.sum(dx * dx))
        if sxx > 0:
            slope = float(np.sum(dx * (y - ym)) / sxx)
            a = ym - slope * xm
            e = y - a - slope * x
            sc = pd.Series(dx * e).groupby(g).sum().values
            G = sc.size
            var = float(np.sum(sc ** 2)) / sxx ** 2
            if G > 1 and n > 2:
                var *= (G / (G - 1.0)) * ((n - 1.0) / (n - 2.0))
            se = np.sqrt(var)
            t = float(slope / se) if se > 0 else None
        mean_y = float(ym)

    sup_pass = (mean_y < 0) if mean_y is not None else None
    stat = {"name": "slope t, day-clustered SE", "value": t} if t is not None else None
    main = {"name": main_name, "value": slope, "statistic": stat, "threshold": thr}
    sup = {"name": "mean drift-adjusted next-day return on active bars < 0", "value": mean_y,
           "passed": sup_pass}

    if n < MIN_ACTIVE or n_days < MIN_DAYS:
        status = "not observable"
        decided = "The plan's minimum of 100 active bars on at least 50 distinct days is not reached (%d bars, %d days)." % (n, n_days)
    elif t is None or slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope < 0 and t <= -2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is negative with t <= -2 and the mean drift-adjusted next-day return is below 0."
        else:
            status = "inconclusive"
            decided = "A confirming slope (t <= -2) with a mean drift-adjusted return at or above 0 is inconclusive."
    elif slope > 0 and t >= 2:
        status = "rejected"
        decided = "The slope is positive with t >= +2: larger shorts are followed by higher returns than the drift."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
