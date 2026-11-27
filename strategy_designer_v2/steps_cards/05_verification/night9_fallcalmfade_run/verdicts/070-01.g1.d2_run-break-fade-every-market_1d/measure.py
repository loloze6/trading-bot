import numpy as np
import pandas as pd


def _to_day(ts):
    s = pd.Series(ts)
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        if mx > 1e14:
            unit = "us"
        elif mx > 1e11:
            unit = "ms"
        else:
            unit = "s"
        dt = pd.to_datetime(s, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.floor("D")


def _clustered_t(values, days):
    values = np.asarray(values, dtype=float)
    n = len(values)
    if n < 2:
        return None, 0
    m = values.mean()
    dev = pd.Series(values - m).groupby(np.asarray(days)).sum()
    g = len(dev)
    if g < 2:
        return None, g
    var = (dev.values ** 2).sum() / (n ** 2) * (g / (g - 1.0))
    if not np.isfinite(var) or var <= 0:
        return None, g
    return float(m / np.sqrt(var)), g


def measure(bars):
    fc_col = "forecast"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    frames = []
    coin_rets = {}
    for coin, wins in bars.items():
        all_r = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            prev = close.shift(1)
            prev2 = close.shift(2)
            up = close > prev
            prev_down = prev < prev2
            situ = (up & prev_down)
            known = prev.notna() & prev2.notna()
            # where price history inside the window is too short, the detector's own decision is used
            reg_mr = df["regime"].astype(str) == "mean_reversion"
            situ = situ.where(known, reg_mr).astype(bool)

            fc = pd.to_numeric(df[fc_col], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

            r = close.shift(-1) / close - 1.0
            all_r.append(r.dropna())
            frames.append(pd.DataFrame({
                "coin": coin,
                "day": _to_day(df["timestamp"]).values,
                "fc": fc.values,
                "r": r.values,
            }))
        coin_rets[coin] = float(pd.concat(all_r).mean()) if all_r else np.nan

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed_situ = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-direction unusual 1-day move on bars with forecast <= -2"
    thr = "confirm: mean > 0 with day-clustered t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2; at least 100 case-days"
    reading = ("Situation from prices: close up on the bar and the previous close down (strict), using the regime column only on a window's first two bars; "
               "the next-day return stays inside the window and the coin's mean is over all its 1-bar returns in all windows; the day-clustered t sums "
               "deviations per UTC day with a G/(G-1) correction; case-days are distinct UTC days with a case; the shorter-run group is -8 < forecast <= -2.")

    if not passed_situ:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active (non-zero forecast) bars are short bars on an up close right after a down close, "
                           "the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    data = pd.concat(frames, ignore_index=True)
    data["mu"] = data["coin"].map(coin_rets)
    data = data.dropna(subset=["r", "mu"])
    data["u"] = -(data["r"] - data["mu"])

    cases = data[data["fc"] <= -2]
    n_cases = int(len(cases))
    case_days = int(cases["day"].nunique()) if n_cases else 0
    mean_u = float(cases["u"].mean()) if n_cases else None
    t_u, _ = _clustered_t(cases["u"].values, cases["day"].values) if n_cases else (None, 0)

    longer = cases[cases["fc"] <= -8]["u"]
    shorter = cases[(cases["fc"] > -8) & (cases["fc"] <= -2)]["u"]
    if len(longer) > 0 and len(shorter) > 0:
        diff = float(longer.mean() - shorter.mean())
        sup_passed = bool(diff > 0)
    else:
        diff = None
        sup_passed = None

    counts = {
        "case-days": case_days,
        "cases": n_cases,
        "cases with forecast <= -8": int(len(longer)),
        "cases with forecast between -8 and -2": int(len(shorter)),
    }

    if case_days < 100:
        status = "not observable"
        decided = f"Only {case_days} case-days, below the plan's minimum of 100 case-days."
    elif mean_u is not None and t_u is not None and mean_u > 0 and t_u >= 2:
        if sup_passed is True:
            status = "confirmed"
            decided = "Mean short-direction unusual move above 0 with t >= 2 and longer runs show a larger move: the confirm rule."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (mean > 0, t >= 2) but the supporting check fails: the inconclusive rule."
    elif mean_u is not None and t_u is not None and mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "Mean short-direction unusual move below 0 with t <= -2: the reject rule."
    else:
        status = "inconclusive"
        decided = "The mean unusual move has |t| < 2: the inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": float(t_u)}
                          if t_u is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean unusual move, runs of 3+ (forecast <= -8) minus runs of 2 (-8 < forecast <= -2), above 0",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
