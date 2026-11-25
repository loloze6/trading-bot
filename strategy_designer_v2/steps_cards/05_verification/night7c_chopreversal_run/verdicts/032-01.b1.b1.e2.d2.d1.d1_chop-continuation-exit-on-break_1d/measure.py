import numpy as np
import pandas as pd


def measure(bars):
    # ---------- helpers ----------
    def _coin_returns(win_dict):
        rets = []
        for w, df in win_dict.items():
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            r = c.shift(-1) / c - 1.0
            rets.append(r.dropna())
        if not rets:
            return np.nan
        allr = pd.concat(rets)
        return float(allr.mean()) if len(allr) else np.nan

    # ---------- 1. situation check ----------
    n_active_eval = 0
    n_agree = 0
    n_active_total = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce")
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            net = (c - c.shift(30)).abs()
            path = c.diff().abs().rolling(30, min_periods=30).sum()
            er = net / path.replace(0.0, np.nan)
            r7 = c / c.shift(7) - 1.0
            r30 = c / c.shift(30) - 1.0
            active = f != 0
            n_active_total += int(active.sum())
            evaluable = active & er.notna() & r7.notna() & r30.notna()
            chop = (er < 0.3) & (((r7 > 0) & (r30 > 0)) | ((r7 < 0) & (r30 < 0)))
            side_ok = np.sign(f) == np.sign(r7)
            n_active_eval += int(evaluable.sum())
            n_agree += int((evaluable & chop & side_ok).sum())

    agreement = (n_agree / n_active_eval) if n_active_eval > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "t of the per-day sum of (forecast/10) x (next-day return - coin mean daily return) on chop-regime bars"
    threshold = "confirm: t >= 2 over >= 100 days with top-minus-bottom third > 0; reject: t <= -2 over >= 100 days"
    reading = ("Situation recomputed from closes inside each window (ER = |close[t]-close[t-30]| / sum of 30 absolute daily "
               "changes, 7- and 30-day returns), with active bars whose 30-day lookback lies before the window's first "
               "recorded bar left out of the agreement share; chop-regime bars are those whose recorded regime is 'chop' "
               "with a next-day close in the same window; terciles of |forecast| are cut by rank (ties in time order) "
               "over all chop-regime cases pooled, and a day is the UTC date of the bar's timestamp.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"days": None, "active bars checked": int(n_active_eval)},
            "decided_by": ("Fewer than 90% of active forecast bars are bars where the 30-day efficiency ratio is below 0.3 "
                           "and the 7- and 30-day returns share a sign, with the forecast on the 7-day move's side."
                           if agreement is not None else
                           "No active bar could be checked against the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        mu = _coin_returns(wins)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce")
            f = pd.to_numeric(df["forecast"], errors="coerce")
            nxt = c.shift(-1) / c - 1.0
            reg = df["regime"].astype(str)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            m = (reg == "chop") & nxt.notna() & f.notna()
            for i in np.where(m.values)[0]:
                ex = float(nxt.iloc[i]) - mu
                rows.append({
                    "day": ts.iloc[i].floor("D"),
                    "ts": ts.iloc[i],
                    "coin": coin,
                    "f": float(f.iloc[i]),
                    "val": float(f.iloc[i]) / 10.0 * ex,
                    "signed": float(np.sign(f.iloc[i])) * ex,
                })

    cases = pd.DataFrame(rows)
    n_cases = int(len(cases))
    if n_cases == 0:
        n_days = 0
    else:
        daily = cases.groupby("day")["val"].sum()
        n_days = int(len(daily))

    if n_days < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"days": n_days, "chop-regime cases": n_cases},
            "decided_by": "Fewer than 100 days with a chop-regime case, the plan's minimum.",
            "reading": reading,
        }

    mean_d = float(daily.mean())
    sd_d = float(daily.std(ddof=1))
    t = float(mean_d / (sd_d / np.sqrt(n_days))) if sd_d > 0 else float("nan")

    # supporting check: terciles of |forecast|
    cs = cases.sort_values(["ts", "coin"]).reset_index(drop=True)
    absf = cs["f"].abs()
    rk = absf.rank(method="first")
    n = len(cs)
    lo_cut = n / 3.0
    hi_cut = 2.0 * n / 3.0
    bottom = cs.loc[rk <= lo_cut, "signed"]
    top = cs.loc[rk > hi_cut, "signed"]
    if len(top) > 0 and len(bottom) > 0:
        diff = float(top.mean() - bottom.mean())
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = None

    if np.isfinite(t) and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The main t is 2 or more over at least 100 days and the top third minus the bottom third is above 0."
        else:
            status = "inconclusive"
            decided = "The main t is 2 or more but the top-minus-bottom third difference is not above 0."
    elif np.isfinite(t) and t <= -2:
        status = "rejected"
        decided = "The main t is -2 or less over at least 100 days."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_d,
            "statistic": {"name": "t of the mean over days", "value": t if np.isfinite(t) else None},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "top third minus bottom third of |forecast|, mean direction-signed excess next-day return",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": {"days": n_days, "chop-regime cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
