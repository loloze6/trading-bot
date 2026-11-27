import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.run_break_fade.last_history_value"
    BAND = 2.0
    MIN_CASE_DAYS = 30
    TOL = 1e-6

    # ---------- coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    n_active = 0
    n_agree = 0
    cases = []  # (day, signed excess, |forecast|)

    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            if len(d) == 0:
                continue
            c = d["close"].astype(float).values
            f = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).values
            n = len(d)
            raw = (pd.to_numeric(d[RAW], errors="coerce").values
                   if RAW in d.columns else np.full(n, np.nan))
            regime = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * n)

            # daily returns inside window
            r1 = np.full(n, np.nan)
            r1[1:] = c[1:] / c[:-1] - 1.0

            # z20: 20-day return / (std of 20 daily returns * sqrt(20))
            rs = pd.Series(r1)
            sd1 = rs.rolling(20, min_periods=20).std(ddof=1).values
            sd0 = rs.rolling(20, min_periods=20).std(ddof=0).values
            ret20 = np.full(n, np.nan)
            ret20[20:] = c[20:] / c[:-20] - 1.0
            with np.errstate(divide="ignore", invalid="ignore"):
                z1 = ret20 / (sd1 * np.sqrt(20))
                z0 = ret20 / (sd0 * np.sqrt(20))

            for t in range(n):
                # ---- situation: run break (up day after >=2 down days) ----
                if t >= 3:
                    rb = (c[t] > c[t - 1]) and (c[t - 1] < c[t - 2]) and (c[t - 2] < c[t - 3])
                else:
                    rb = bool(np.isfinite(raw[t]) and raw[t] != 0)
                # ---- regime: z20 <= -1 ----
                if np.isfinite(z1[t]) or np.isfinite(z0[t]):
                    deep = bool((np.isfinite(z1[t]) and z1[t] <= -1.0 + TOL) or
                                (np.isfinite(z0[t]) and z0[t] <= -1.0 + TOL))
                else:
                    deep = regime[t] == "trending"
                if f[t] != 0:
                    n_active += 1
                    if rb and deep and f[t] < 0:
                        n_agree += 1

            # ---- cases: short forecast deepening by >= band ----
            ref = 0.0
            for t in range(n):
                if f[t] >= 0:
                    ref = 0.0
                    continue
                s = -f[t]
                if s - ref >= BAND - 1e-12:
                    ref = s
                    if t + 1 < n and np.isfinite(coin_mean[coin]):
                        nr = c[t + 1] / c[t] - 1.0
                        if np.isfinite(nr):
                            ex = -(nr - coin_mean[coin])
                            day = pd.Timestamp(d["timestamp"].iloc[t]).normalize()
                            cases.append((str(day), float(ex), float(abs(f[t]))))
                else:
                    ref = min(ref, s)

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    main_name = "mean short-side excess next-day return on case bars"
    thr = "confirm: mean > 0 with t >= 2.0 over >= 30 case-days; reject: mean < 0 with t <= -2.0 over >= 30 case-days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("fewer than 90% of active (non-zero forecast) bars are short bars on an up day ending "
                           ">=2 down days with the 20-day return at or below -1 usual 20-day move"),
            "reading": "situation recomputed from closes (z20 with ddof 0 or 1), falling back to the raw component and regime on bars without enough window history",
        }

    n_cases = len(cases)
    if n_cases > 0:
        cdf = pd.DataFrame(cases, columns=["day", "ex", "absf"])
        mean_ex = float(cdf["ex"].mean())
        daysum = cdf.groupby("day")["ex"].sum().values
        n_days = int(len(daysum))
        if n_days > 1 and np.std(daysum, ddof=1) > 0:
            tval = float(np.mean(daysum) / (np.std(daysum, ddof=1) / np.sqrt(n_days)))
        else:
            tval = None
        med = float(cdf["absf"].median())
        up = cdf.loc[cdf["absf"] > med, "ex"]
        lo = cdf.loc[cdf["absf"] <= med, "ex"]
        if len(up) > 0 and len(lo) > 0:
            diff = float(up.mean() - lo.mean())
            sup_pass = bool(diff > 0)
        else:
            diff, sup_pass = None, None
    else:
        mean_ex, tval, n_days, diff, sup_pass = None, None, 0, None, None

    counts = {"case-days": int(n_days), "cases": int(n_cases), "active bars": int(n_active)}

    if n_days < MIN_CASE_DAYS or tval is None:
        status = "not observable"
        decided = f"fewer than {MIN_CASE_DAYS} case-days ({n_days}), the plan's minimum count, so the data could not show the idea"
    elif mean_ex > 0 and tval >= 2.0 and sup_pass is True:
        status = "confirmed"
        decided = "mean short-side excess next-day return positive with t >= 2.0 over >= 30 case-days and the supporting check passes"
    elif mean_ex < 0 and tval <= -2.0:
        status = "rejected"
        decided = "mean short-side excess next-day return negative with t <= -2.0 over >= 30 case-days"
    elif mean_ex > 0 and tval >= 2.0:
        status = "inconclusive"
        decided = "a confirming t with a failed supporting check is inconclusive"
    else:
        status = "inconclusive"
        decided = "t between -2.0 and 2.0 (or sign and t disagree), meeting neither confirm nor reject"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean, same-day cases summed", "value": tval} if tval is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "upper-half minus lower-half mean excess, split at median |forecast|",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("cases are bars where the short forecast deepens by >= 2 points from its lowest short level since the last bet "
                    "(reset at flat), the mean is over cases and the t over day-summed cases, the upper half is |forecast| strictly "
                    "above the median, and fewer than 30 case-days is treated as not observable"),
    }
