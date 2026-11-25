import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    LB = 20
    RAW = "debug_info.components.range_pos.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: the close's place in its 20-close range, graded. Above the middle means long, below means short.
    # The side of the range comes from the raw component value. Where that value is missing, it comes from the
    # close against the midpoint of the last 20 closes of the same window.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            hi = close.rolling(LB, min_periods=LB).max()
            lo = close.rolling(LB, min_periods=LB).min()
            mid = (hi + lo) / 2.0
            price_pos = np.sign(close - mid)
            pos_sign = np.sign(raw).where(raw.notna(), price_pos)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & pos_sign.notna() & (pos_sign != 0) & (np.sign(fc) == pos_sign)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    threshold_txt = ("confirm: slope > 0 with t >= 2 and supporting check passes; "
                     "reject: slope < 0 with t <= -2; else inconclusive; "
                     "minimum 500 grid cases on 100 distinct days")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": "pooled OLS slope of 5-bar excess return on forecast",
                             "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars have a forecast whose sign matches the close's side "
                           "of its 20-close range (long upper half, short lower half), as the Fidelity requires."),
            "reading": "The side of the range is the sign of the raw range_pos value, or the close against the "
                       "20-close midpoint where that value is missing.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append({"coin": coin, "ret": c1 / c0 - 1.0, "fc": fc[i],
                                  "day": ts.iloc[i].strftime("%Y-%m-%d")})
        if not coin_rows:
            continue
        cdf = pd.DataFrame(coin_rows)
        drift = cdf["ret"].mean()  # the coin's normal drift: its mean 5-bar return over all windows
        cdf["ex"] = cdf["ret"] - drift
        rows.append(cdf)

    if rows:
        allc = pd.concat(rows, ignore_index=True)
    else:
        allc = pd.DataFrame(columns=["coin", "ret", "fc", "day", "ex"])
    allc = allc[np.isfinite(allc["fc"].astype(float)) & np.isfinite(allc["ex"].astype(float))]

    n_cases = int(len(allc))
    n_days = int(allc["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days": n_days}

    slope = None
    tstat = None
    if n_cases >= 3:
        x = allc["fc"].astype(float).values
        y = allc["ex"].astype(float).values
        xm = x.mean()
        ym = y.mean()
        sxx = np.sum((x - xm) ** 2)
        if sxx > 0:
            slope = float(np.sum((x - xm) * (y - ym)) / sxx)
            a = ym - slope * xm
            e = y - a - slope * x
            score = pd.Series((x - xm) * e).groupby(allc["day"].values).sum().values
            G = len(score)
            if G > 1:
                var = (G / (G - 1)) * np.sum(score ** 2) / sxx ** 2
                if var > 0:
                    tstat = float(slope / np.sqrt(var))

    hi_grp = allc.loc[allc["fc"] > 10, "ex"].astype(float)
    lo_grp = allc.loc[allc["fc"] < -10, "ex"].astype(float)
    if len(hi_grp) > 0 and len(lo_grp) > 0:
        sup_val = float(hi_grp.mean() - lo_grp.mean())
        sup_pass = bool(sup_val > 0)
    else:
        sup_val = None
        sup_pass = False

    if n_cases < 500 or n_days < 100:
        status = "not observable"
        decided = (f"The minimum of 500 grid cases on 100 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the high-minus-low supporting check is above 0."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif slope > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2, but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "pooled OLS slope of 5-bar excess return on forecast",
            "value": slope,
            "statistic": None if tstat is None else {"name": "t, same-day cases summed (day-clustered)",
                                                     "value": tstat},
            "threshold": threshold_txt,
        },
        "supporting_check": {"name": "mean excess return, forecast > +10 minus forecast < -10",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Every grid bar (positions 0, 5, 10, ... of each window that have a close 5 bars later) "
                    "with a forecast is a case. The slope is OLS with an intercept, and its t uses residual "
                    "scores summed per UTC day with a G/(G-1) correction. The drift is each coin's mean grid "
                    "5-bar return over all its windows. A supporting check with an empty group fails."),
    }
