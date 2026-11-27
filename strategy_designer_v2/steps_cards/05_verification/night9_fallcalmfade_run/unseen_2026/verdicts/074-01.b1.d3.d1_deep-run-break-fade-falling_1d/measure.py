import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    LHV = "debug_info.components.run_depth.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_det = 0
    n_agree = 0
    rows = []
    coin_rets = {}

    for coin in sorted(bars.keys()):
        allr = []
        wins = bars[coin]
        for w in sorted(wins.keys(), key=lambda s: int(str(s).lstrip("w")) if str(s).lstrip("w").isdigit() else str(s)):
            df = wins[w].copy()
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)

            # run of >= 2 down closes broken by an up close (needs 3 prior closes)
            up = close > close.shift(1)
            d1 = close.shift(1) < close.shift(2)
            d2 = close.shift(2) < close.shift(3)
            run_det = close.shift(3).notna() & close.notna()
            run_ok = up & d1 & d2

            # falling profile: 60-bar price evolution (percent) below -10
            evo = (close / close.shift(60) - 1.0) * 100.0
            prof_det = evo.notna()
            falling = evo < -10

            det = run_det & prof_det
            situ = run_ok & falling
            active = fc != 0
            n_active += int(active.sum())
            mask = active & det
            n_det += int(mask.sum())
            n_agree += int((mask & situ & (fc < 0)).sum())

            # forward 1-bar return inside window
            fwd = close.shift(-1) / close - 1.0
            allr.append(fwd.dropna().values)

            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce") if "timestamp" in df.columns else pd.Series([pd.NaT] * len(df))
            for i in range(len(df)):
                if fc.iloc[i] < 0 and np.isfinite(fwd.iloc[i]):
                    rows.append((coin, str(w), i, ts.iloc[i], float(fc.iloc[i]), float(fwd.iloc[i])))
        coin_rets[coin] = float(np.concatenate(allr).mean()) if allr and sum(len(a) for a in allr) > 0 else np.nan

    agreement = (n_agree / n_det) if n_det > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation bars are computed from prices (up close after at least 2 consecutive down closes, "
               "and 60-bar percent price change below -10) on active bars where both can be computed inside the window; "
               "the top and bottom thirds are the first and last round(n/3) cases sorted by |forecast| "
               "(stable order by coin, window, bar); the day-clustered t sums deviations per UTC day; "
               "fewer than 30 top-third cases or days is reported as not observable.")

    main_name = "mean next-day unusual short-side move, top third of cases by |forecast|"
    thr = "t >= 2 confirms (with top minus bottom > 0), t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement if agreement is not None else 0.0, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars checkable": int(n_det)},
            "decided_by": ("Fewer than 90% of the active (checkable) bars are short bars on an up close ending a run of "
                           "at least 2 down closes in a falling market (60-bar change below -10%)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = pd.DataFrame(rows, columns=["coin", "window", "i", "ts", "fc", "fwd"])
    cases["mu"] = cases["coin"].map(coin_rets)
    cases = cases.dropna(subset=["fwd", "mu"])
    cases["x"] = -(cases["fwd"] - cases["mu"])
    cases["day"] = cases["ts"].dt.floor("D")
    cases["abs"] = cases["fc"].abs()
    cases = cases.sort_values(["coin", "window", "i"], kind="mergesort").reset_index(drop=True)
    order = cases.sort_values("abs", ascending=False, kind="mergesort")
    n = len(order)
    k = int(round(n / 3.0))
    top = order.iloc[:k]
    bot = order.iloc[n - k:] if k > 0 else order.iloc[0:0]

    def clustered_t(g):
        m = len(g)
        if m < 2:
            return (float(g["x"].mean()) if m else None), None, int(g["day"].nunique())
        mean = g["x"].mean()
        S = (g["x"] - mean).groupby(g["day"]).sum()
        D = len(S)
        if D < 2:
            return float(mean), None, D
        se = np.sqrt(D / (D - 1.0) * float((S ** 2).sum())) / m
        t = float(mean / se) if se > 0 else None
        return float(mean), t, D

    top_mean, top_t, top_days = clustered_t(top)
    bot_mean = float(bot["x"].mean()) if len(bot) else None
    diff = (top_mean - bot_mean) if (top_mean is not None and bot_mean is not None) else None
    sup_pass = (diff > 0) if diff is not None else None

    counts = {"cases": int(n), "top-third cases": int(len(top)), "top-third distinct days": int(top_days),
              "bottom-third cases": int(len(bot))}

    if len(top) < 30 or top_days < 30:
        status = "not observable"
        decided = "The plan's minimum of 30 top-third cases on at least 30 distinct days is not reached."
    elif top_t is None:
        status = "inconclusive"
        decided = "The top-third t could not be computed, so neither the confirm nor the reject rule is met."
    elif top_t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The top-third mean unusual short-side move has t >= 2 and the top-minus-bottom difference is above 0."
    elif top_t <= -2:
        status = "rejected"
        decided = "The top-third mean unusual short-side move has t <= -2."
    elif top_t >= 2:
        status = "inconclusive"
        decided = "The top-third t is >= 2 but the top-minus-bottom difference is 0 or below."
    else:
        status = "inconclusive"
        decided = "The top-third t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": top_mean,
                         "statistic": ({"name": "t of the mean, cases of one day taken together", "value": top_t}
                                       if top_t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "top third minus bottom third mean unusual short-side move",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
