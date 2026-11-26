import numpy as np
import pandas as pd


def _to_day(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        unit = "ms" if s.abs().max() > 1e11 else "s"
        dt = pd.to_datetime(s, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.floor("D").dt.strftime("%Y-%m-%d").values


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    frames = []
    for coin in sorted(bars.keys()):
        coin_rets = []
        for window in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret1 = close / close.shift(1) - 1.0
            ret3 = close / close.shift(3) - 1.0
            computable = ret1.notna() & ret3.notna()
            situation = (ret1 > 0) & (ret3 < 0)
            active = fc != 0
            n_active_uncomputable += int((active & ~computable).sum())
            act_c = active & computable
            n_active += int(act_c.sum())
            n_agree += int((act_c & situation & (fc < 0)).sum())

            nxt = close.shift(-1) / close - 1.0
            coin_rets.append(nxt.dropna().values)
            frames.append(pd.DataFrame({
                "coin": coin,
                "day": _to_day(df["timestamp"]),
                "forecast": fc.values,
                "next_ret": nxt.values,
            }))
        bars_mu = np.concatenate(coin_rets).mean() if coin_rets and sum(len(r) for r in coin_rets) > 0 else np.nan
        for f in frames:
            if (f["coin"] == coin).all() and "mu" not in f.columns:
                f["mu"] = bars_mu

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual move per case in the short direction, 1 bar"
    threshold = "t >= 2 with supporting check passing confirms; t <= -2 rejects; at least 30 case-days"
    reading = ("Situation recomputed from closes inside each window (1-bar and 3-bar close returns), active bars whose "
               "3-bar return cannot be computed in the window are left out of the agreement share; the coin's mean daily "
               "return is over all its windows' 1-bar returns; the day-pooled t uses per-day sums of case deviations from "
               "the mean with a G/(G-1) small-sample factor; the supporting check compares cases strictly above and "
               "strictly below the median |forecast|, ties at the median left out.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active),
                       "active bars uncomputable": int(n_active_uncomputable)},
            "decided_by": ("Fewer than 90% of nonzero-forecast bars are short bars with a positive 1-day return and a "
                           "negative 3-day return, as the plan's Fidelity situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    allf = pd.concat(frames, ignore_index=True)
    cases = allf[(allf["forecast"] != 0) & allf["next_ret"].notna() & allf["mu"].notna()].copy()
    cases["u"] = -(cases["next_ret"] - cases["mu"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_val = None
    if n_cases > 0 and n_days > 1:
        dev = cases["u"] - mean_u
        D = dev.groupby(cases["day"]).sum().values
        G = len(D)
        var = (G / (G - 1.0)) * np.sum(D ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        absf = cases["forecast"].abs()
        med = absf.median()
        hi = cases.loc[absf > med, "u"]
        lo = cases.loc[absf < med, "u"]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    counts = {"case-days": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} case-days, fewer than the plan's minimum of 30, so no verdict."
    elif t_val is None:
        status = "inconclusive"
        decided = "The day-pooled t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The main t is 2 or more and the wider bounces fall more (supporting check passes)."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main t is -2 or less: after these bounces the coin rises more than its drift."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The main t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The main t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases pooled by day", "value": t_val}
                                       if t_val is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual move above-median |forecast| minus below-median",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
