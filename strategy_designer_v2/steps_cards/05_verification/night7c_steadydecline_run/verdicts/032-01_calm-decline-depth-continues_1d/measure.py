import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.fall28.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d[FC], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            calm = d["regime"].astype(str).str.strip().str.lower() == "trending"
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # fallback where the component is not recorded: the 28-bar return from prices
            price_ret = close / close.shift(28) - 1.0
            raw = raw.where(raw.notna(), price_ret)
            fell = raw < 0
            active = fc.notna() & (fc != 0)
            agree = active & calm & fell & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    threshold_txt = ("confirm: slope > 0 with t >= 2 and short-direction mean excess > 0; "
                     "reject: slope < 0 with t <= -2, or short-direction mean t <= -2; "
                     "fewer than 30 independent days: inconclusive")
    main_name = "slope of next 5-bar excess return on the forecast (forecast < 0 cells)"
    reading = ("Calm is read from the recorded regime 'trending' and the fall from fall28's raw value "
               "(28-bar price return where not recorded); the slope is pooled OLS of excess return on forecast "
               "with its t from a day-clustered standard error (case terms summed per day, G/(G-1) correction), "
               "the short-direction mean's t sums its deviations per day, the coin's mean 5-bar return is over "
               "its non-overlapping grid cells of all windows, and the 30-day minimum (stated as inconclusive by "
               "the plan) is applied as the minimum count, i.e. 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation on the short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are calm ('trending') bars after a "
                           "28-day fall with a short (negative) forecast, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append({"coin": coin, "day": ts.iloc[i].floor("D"),
                                  "ret": c1 / c0 - 1.0, "fc": fc[i]})
        if coin_rows:
            cdf = pd.DataFrame(coin_rows)
            cdf["excess"] = cdf["ret"] - cdf["ret"].mean()
            rows.append(cdf)

    if rows:
        allc = pd.concat(rows, ignore_index=True)
        cases = allc[allc["fc"].notna() & (allc["fc"] < 0) & allc["excess"].notna()].copy()
    else:
        cases = pd.DataFrame(columns=["coin", "day", "ret", "fc", "excess"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope = None
    t_slope = None
    short_mean = None
    t_short = None
    if n_cases >= 2 and n_days >= 2:
        x = cases["fc"].values.astype(float)
        y = cases["excess"].values.astype(float)
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        G = n_days
        if sxx > 0:
            b = float(np.sum(xc * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            e = y - a - b * x
            sc = pd.Series(xc * e).groupby(cases["day"].values).sum().values
            var_b = (G / (G - 1)) * float(np.sum(sc ** 2)) / sxx ** 2
            slope = b
            t_slope = b / np.sqrt(var_b) if var_b > 0 else None
        s = -y
        m = float(s.mean())
        dev = pd.Series(s - m).groupby(cases["day"].values).sum().values
        var_m = (G / (G - 1)) * float(np.sum(dev ** 2)) / n_cases ** 2
        short_mean = m
        t_short = m / np.sqrt(var_m) if var_m > 0 else None
    elif n_cases >= 1:
        short_mean = float(-cases["excess"].mean())

    sup_passed = None if short_mean is None else bool(short_mean > 0)
    counts = {"independent days of cases": n_days, "cases (coin-cells with forecast < 0)": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} independent days of cases, fewer than the plan's minimum of 30."
    elif (slope is not None and t_slope is not None and slope < 0 and t_slope <= -2) or \
         (t_short is not None and t_short <= -2):
        status = "rejected"
        if slope is not None and t_slope is not None and slope < 0 and t_slope <= -2:
            decided = "Reject rule: the slope is negative with t <= -2."
        else:
            decided = "Reject rule: the short-direction mean excess return has t <= -2."
    elif slope is not None and t_slope is not None and slope > 0 and t_slope >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Confirm rule: the slope is positive with t >= 2 and the short-direction mean excess return is above 0."
        else:
            status = "inconclusive"
            decided = "Inconclusive rule: a confirming slope whose short-direction mean excess return is not above 0."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope's t lies between -2 and 2 (or cannot be computed) and no reject rule is met."

    def f(v):
        return None if v is None or not np.isfinite(v) else float(v)

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {"name": main_name, "value": f(slope),
                         "statistic": None if t_slope is None else {"name": "slope t, day-clustered", "value": f(t_slope)},
                         "threshold": threshold_txt},
        "supporting_check": {"name": "mean short-direction excess 5-bar return > 0 (t summed per day: "
                                     + ("n/a" if t_short is None else f"{float(t_short):.3f}") + ")",
                             "value": f(short_mean), "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
