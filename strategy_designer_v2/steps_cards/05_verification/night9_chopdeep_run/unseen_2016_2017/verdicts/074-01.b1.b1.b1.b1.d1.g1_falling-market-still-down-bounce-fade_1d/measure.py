import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    LH = "debug_info.components.loss5.last_history_value"
    BAND = 2.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    case_rows = []      # (coin, day, direction, ret_next, abs_forecast)
    coin_rets = {}      # coin -> list of 1-bar returns over all windows

    for coin, wins in bars.items():
        rets_all = []
        for w in sorted(wins.keys(), key=lambda x: str(x)):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce").astype(float).fillna(0.0)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            in_regime = (regime == "mean_reversion").values

            # raw components, in percent, inside the window only
            ret1 = (close / close.shift(1) - 1.0) * 100.0
            ret5_px = (close / close.shift(5) - 1.0) * 100.0
            ret60 = (close / close.shift(60) - 1.0) * 100.0
            if LH in df.columns:
                lh = pd.to_numeric(df[LH], errors="coerce").astype(float)
                ret5 = lh.where(lh.notna(), ret5_px)
            else:
                ret5 = ret5_px

            def cond(series, fn):
                v = series.values
                out = np.zeros(len(v), dtype=bool)
                known = ~np.isnan(v)
                out[known] = fn(v[known])
                # where not computable from the window's own bars, use the detector's recorded decision
                out[~known] = in_regime[~known]
                return out

            c1 = cond(ret1, lambda x: x > 0.0)
            c5 = cond(ret5, lambda x: x < 0.0)
            c60 = cond(ret60, lambda x: x < -10.0)
            situation = c1 & c5 & c60

            active = fc.values != 0.0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc.values < 0)).sum())

            # ---------- returns ----------
            r_next = (close.shift(-1) / close - 1.0).values
            rets_all.extend([x for x in r_next if np.isfinite(x)])

            # ---------- cases: bets (rise of forecast on its side >= band), horizon 1 bar ----------
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            days = ts.dt.floor("D")
            side = 0
            ref = 0.0
            for i in range(len(df)):
                f = fc.values[i]
                if not np.isfinite(f) or f == 0.0:
                    side = 0
                    ref = 0.0
                    continue
                s = 1 if f > 0 else -1
                if s != side:
                    side = s
                    ref = 0.0
                mag = abs(f)
                if mag - ref >= BAND:
                    if np.isfinite(r_next[i]) and pd.notna(days.iloc[i]):
                        case_rows.append((coin, days.iloc[i], s, r_next[i], mag))
                    ref = mag
                else:
                    ref = min(ref, mag)
        coin_rets[coin] = rets_all

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean unusual 1-day move in the short direction (next-day return minus coin's normal 1-day drift)"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passing; reject: mean < 0 with t <= -2"
    sup_name = "deeper half minus shallower half of |forecast|, mean unusual move (Welch), above 0"
    reading = ("Situation = 1-day return > 0, 5-day return < 0 and 60-day return < -10 % (the falling-profile veto), "
               "with the recorded regime used where a return cannot be computed inside the window; cases are the "
               "workflow's bets (forecast rising on its side by >= 2 points) on every bar of the 1-bar grid; the "
               "day-clustered t uses per-day summed deviations with a G/(G-1) correction; the deeper half is the "
               "top floor(n/2) cases by |forecast| (stable sort), the rest is the shallower half; the plan's "
               "'fewer is inconclusive' is reported as 'not observable' per the workflow; values are fractions.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": (f"Only {agreement:.1%} of the {n_active} active bars are up days with a negative 5-day "
                           "return in a falling market (60-day return < -10 %) and short, below the 90 % needed."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in coin_rets.items()}
    cases = pd.DataFrame(case_rows, columns=["coin", "day", "dir", "ret", "absf"])
    if len(cases):
        cases["drift"] = cases["coin"].map(drift)
        cases = cases[np.isfinite(cases["drift"])]
        cases["u"] = cases["dir"] * (cases["ret"] - cases["drift"])
        cases = cases[np.isfinite(cases["u"])]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["u"] - mean_u
        sums = dev.groupby(cases["day"]).sum().values
        G = len(sums)
        var_mean = (sums ** 2).sum() * G / (G - 1) / (n_cases ** 2)
        if var_mean > 0:
            t_val = float(mean_u / np.sqrt(var_mean))

    sup_val, sup_pass, welch_t = None, None, None
    if n_cases >= 4:
        srt = cases.sort_values("absf", ascending=False, kind="mergesort")
        k = n_cases // 2
        deep = srt["u"].iloc[:k].values
        shallow = srt["u"].iloc[k:].values
        if len(deep) >= 2 and len(shallow) >= 2:
            sup_val = float(deep.mean() - shallow.mean())
            sup_pass = bool(sup_val > 0)
            tt = stats.ttest_ind(deep, shallow, equal_var=False)
            welch_t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    counts = {"cases": n_cases, "distinct days": n_days}
    main = {"name": main_name, "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_val}
                          if t_val is not None else None),
            "threshold": threshold}
    sup = {"name": sup_name + (f" (Welch t {welch_t:.3f})" if welch_t is not None else ""),
           "value": sup_val, "passed": sup_pass}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"The plan's minimum of 100 cases on 60 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the deeper half shows a larger mean than the shallower half."
        else:
            status = "inconclusive"
            decided = "The mean unusual move is positive with t >= 2 but the supporting check fails: a confirming t with the check failing is inconclusive."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
