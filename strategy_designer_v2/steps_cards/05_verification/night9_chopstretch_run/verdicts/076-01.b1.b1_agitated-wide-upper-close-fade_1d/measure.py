import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    WHC = "debug_info.components.wide_high_close.last_history_value"
    BAND = 2.0
    H = 1

    # ---------- drift per coin: mean 1-bar return over all windows (non-overlapping grid, h=1) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                rets.append(c[idx + H] / c[idx] - 1.0)
        allr = np.concatenate(rets) if rets else np.array([])
        allr = allr[np.isfinite(allr)]
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check and cases ----------
    n_active = 0
    n_agree = 0
    cases = []  # (day, unusual_move, |forecast|)
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            hi = d["high"].astype(float).values
            lo = d["low"].astype(float).values
            cl = d["close"].astype(float).values
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).values
            reg = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * len(d))
            whc = pd.to_numeric(d[WHC], errors="coerce").values if WHC in d.columns else np.full(len(d), np.nan)
            rng = hi - lo
            mean_prior = pd.Series(rng).rolling(20, min_periods=20).mean().shift(1).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            days = ts.dt.floor("D").values

            # situation per bar
            for i in range(len(d)):
                if fc[i] == 0:
                    continue
                n_active += 1
                mp = mean_prior[i]
                if not np.isfinite(mp) or mp <= 0:
                    if np.isfinite(whc[i]) and whc[i] > 0:
                        mp = (cl[i] - lo[i]) / whc[i]
                    else:
                        mp = np.nan
                width = rng[i] / mp if (np.isfinite(mp) and mp > 0) else np.nan
                loc = (cl[i] - lo[i]) / rng[i] if rng[i] > 0 else np.nan
                in_sit = (np.isfinite(width) and width >= 1.0 and np.isfinite(loc) and loc >= 0.5
                          and reg[i] != "chop")
                if in_sit and fc[i] < 0:
                    n_agree += 1

            # bets on the short side: rise of |forecast| of at least the band from its lowest level since the last bet
            ref = 0.0
            for i in range(len(d)):
                f = fc[i]
                if f >= 0:
                    ref = 0.0
                    continue
                lvl = -f
                if lvl - ref >= BAND:
                    ref = lvl
                    if i + H < len(d) and (i % H == 0) and np.isfinite(drift[coin]):
                        r = cl[i + H] / cl[i] - 1.0
                        if np.isfinite(r):
                            cases.append((days[i], -(r - drift[coin]), lvl))
                else:
                    ref = min(ref, lvl)

    agreement = (n_agree / n_active) if n_active else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("Profile taken from the recorded regime (not 'chop', the veto's result) since the 365-bar volatility "
               "percentile cannot be rebuilt inside a window; range multiple against the prior 20 bars' mean range "
               "(from prices, or from the recorded component when the window lacks 20 prior bars); cases are short "
               "bets (rise of |forecast| >= 2) on every bar (1-bar grid); day-clustered t with deviations summed per "
               "UTC day; median split: larger half = |forecast| above the median, smaller half = at or below; fewer "
               "than 30 case-days gives 'not observable' per the workflow rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "case-days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on an agitated day with "
                           "range at or above its prior 20-day mean and a close in the upper half."),
            "reading": reading,
        }

    threshold = "confirm: mean > 0 with t >= 2 over >= 30 case-days and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 case-days"
    if not cases:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": "mean short-side unusual 1-day move", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean unusual move, larger minus smaller |forecast| half",
                                 "value": None, "passed": None},
            "counts": {"case-days": 0, "cases": 0},
            "decided_by": "Fewer than 30 case-days (none).",
            "reading": reading,
        }

    cdf = pd.DataFrame(cases, columns=["day", "x", "absf"])
    n = len(cdf)
    m = float(cdf["x"].mean())
    dev = cdf["x"] - m
    day_sums = dev.groupby(cdf["day"]).sum()
    n_days = int(len(day_sums))
    se = float(np.sqrt(np.sum(day_sums.values ** 2)) / n)
    t = float(m / se) if se > 0 else float("nan")

    med = float(cdf["absf"].median())
    big = cdf.loc[cdf["absf"] > med, "x"]
    small = cdf.loc[cdf["absf"] <= med, "x"]
    if len(big) and len(small):
        diff = float(big.mean() - small.mean())
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = None

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} case-days, fewer than the plan's minimum of 30."
    elif np.isfinite(t) and m > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean short-side unusual move above 0 with t >= 2 over at least 30 case-days, and the larger-|forecast| half beats the smaller half."
        else:
            status = "inconclusive"
            decided = "Confirm-level t but the supporting check (larger minus smaller half > 0) fails."
    elif np.isfinite(t) and m < 0 and t <= -2:
        status = "rejected"
        decided = "Mean short-side unusual move below 0 with t <= -2 over at least 30 case-days."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 over at least 30 case-days."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean short-side unusual 1-day move",
                         "value": m,
                         "statistic": {"name": "t of the mean, cases of one day clustered",
                                       "value": t if np.isfinite(t) else None},
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual move, larger minus smaller |forecast| half",
                             "value": diff, "passed": sup_pass},
        "counts": {"case-days": n_days, "cases": int(n)},
        "decided_by": decided,
        "reading": reading,
    }
