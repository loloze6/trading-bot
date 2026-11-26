import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    THRESH_TREND = -10.0  # veto: 60-day price evolution (percent) >= -10 -> chop; falling = below -10 %

    # ---------- per-coin mean daily return over all windows (within-window returns only) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = df["close"].astype(float).reset_index(drop=True)
            r = (c.shift(-1) / c - 1.0).dropna()
            rets.append(r.values)
        coin_mean[coin] = float(np.mean(np.concatenate(rets))) if rets else np.nan

    # ---------- situation check and case collection ----------
    n_active = 0
    n_active_checkable = 0
    n_agree = 0
    cases = []  # (day, |f|, short excess)
    for coin, wins in bars.items():
        mu = coin_mean.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            f = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            day_move = c / c.shift(1) - 1.0
            trend60 = (c / c.shift(60) - 1.0) * 100.0
            nxt = c.shift(-1) / c - 1.0
            ts = pd.to_datetime(d["timestamp"], utc=True)
            active = f != 0
            for i in np.where(active.values)[0]:
                n_active += 1
                dm = day_move.iloc[i]
                tr = trend60.iloc[i]
                if pd.isna(dm) or pd.isna(tr):
                    continue
                n_active_checkable += 1
                if (dm > 0) and (tr < THRESH_TREND) and (f.iloc[i] < 0):
                    n_agree += 1
            for i in np.where(active.values)[0]:
                r = nxt.iloc[i]
                if pd.isna(r) or pd.isna(mu):
                    continue
                x = -(float(r) - mu)
                cases.append((ts.iloc[i].floor("D"), abs(float(f.iloc[i])), x))

    agreement = (n_agree / n_active_checkable) if n_active_checkable > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading = ("The falling profile is recomputed from closes as a 60-bar price change below -10 % inside each window "
               "and active bars whose first 60 window bars do not allow it are left out of the agreement share; "
               "the plan's '100 case-days' is read as 100 (coin, day) cases with a nonzero forecast and a next-day "
               "return in the window, and the weighted t sums each day's weighted deviations into one piece.")

    main_name = "|forecast|-weighted mean short-direction excess next-day return"
    threshold = "confirm: > 0 with t >= 2 and rank correlation > 0; reject: < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars checkable": int(n_active_checkable)},
            "decided_by": ("Fewer than 90 % of active bars are up-close bars in a falling 60-day market with a short "
                           "forecast" if agreement is not None else
                           "No active bar could be checked against the plan's situation"),
            "reading": reading,
        }

    n_cases = len(cases)
    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "Spearman rank corr |forecast| vs short excess", "value": None, "passed": None},
            "counts": {"case-days": 0, "distinct days": 0},
            "decided_by": "Fewer than the plan's 100 case-days (none).",
            "reading": reading,
        }

    cdf = pd.DataFrame(cases, columns=["day", "w", "x"])
    wsum = cdf["w"].sum()
    m = float((cdf["w"] * cdf["x"]).sum() / wsum) if wsum > 0 else np.nan
    cdf["dev"] = cdf["w"] * (cdf["x"] - m)
    per_day = cdf.groupby("day")["dev"].sum()
    n_days = int(len(per_day))
    t = np.nan
    if n_days > 1 and wsum > 0:
        se = np.sqrt((per_day.values ** 2).sum() * n_days / (n_days - 1)) / wsum
        t = float(m / se) if se > 0 else np.nan

    rho = np.nan
    if n_cases > 2 and cdf["w"].nunique() > 1 and cdf["x"].nunique() > 1:
        rho = float(stats.spearmanr(cdf["w"], cdf["x"]).correlation)
    sup_pass = bool(rho > 0) if not np.isnan(rho) else None

    counts = {"case-days": int(n_cases), "distinct days": n_days}

    def _num(v):
        return None if (v is None or (isinstance(v, float) and np.isnan(v))) else float(v)

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} case-days, below the plan's minimum of 100."
    elif not np.isnan(t) and m > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Weighted mean short excess return above 0 with t >= 2 and rank correlation above 0 (confirm rule)."
    elif not np.isnan(t) and m < 0 and t <= -2:
        status = "rejected"
        decided = "Weighted mean short excess return below 0 with t <= -2 (reject rule)."
    elif not np.isnan(t) and m > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but rank correlation 0 or below (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": _num(m),
                         "statistic": {"name": "t of weighted mean, same-day cases summed", "value": _num(t)},
                         "threshold": threshold},
        "supporting_check": {"name": "Spearman rank corr |forecast| vs short excess", "value": _num(rho),
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
