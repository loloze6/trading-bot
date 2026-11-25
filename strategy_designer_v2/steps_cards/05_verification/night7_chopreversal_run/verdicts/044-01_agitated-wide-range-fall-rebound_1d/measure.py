import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.fall_range.last_history_value"

    # ---------- 1. Situation check: agitated profile, day closed lower, long side ----------
    n_active = 0
    n_agree = 0
    case_frames = []

    for coin, wins in bars.items():
        # coin's mean daily return over all its windows (pooled, within-window returns only)
        all_rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            r = c.shift(-1) / c - 1.0
            all_rets.append(r.dropna().values)
        all_rets = np.concatenate(all_rets) if len(all_rets) else np.array([])
        coin_mean = float(np.mean(all_rets)) if all_rets.size else np.nan

        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            f = pd.to_numeric(d["forecast"], errors="coerce")
            regime = d["regime"].astype(str)

            # down day: the component's raw value > 0 where recorded, else close below previous close
            if LHV in d.columns:
                raw = pd.to_numeric(d[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            close_down = (c < c.shift(1))
            down = np.where(raw.notna(), raw > 0, close_down.fillna(False))
            down = pd.Series(down, index=d.index).astype(bool)

            agitated = regime == "unknown"
            situation = agitated & down

            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (f > 0)).sum())

            # cases for the criterion
            nxt = c.shift(-1) / c - 1.0
            sel = f.notna() & (f > 0) & nxt.notna()
            if sel.any():
                ts = pd.to_datetime(d.loc[sel, "timestamp"], utc=True)
                case_frames.append(pd.DataFrame({
                    "f": f[sel].values,
                    "y": (nxt[sel] - coin_mean).values,
                    "day": ts.dt.floor("D").values,
                }))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of next-day excess return on forecast (forecast > 0 bars)"
    thr = "confirm: slope > 0 with day-clustered t >= 2 (and weighted mean > 0); reject: slope < 0 with t <= -2"
    reading = ("Agitated profile read as regime == 'unknown' (not vetoed to chop), a down day as the recorded raw "
               "component > 0 (close below previous close where not recorded); cases are forecast > 0 bars with a "
               "next close in the same window; the clustered t uses the standard CR1 small-sample correction "
               "G/(G-1)*(N-1)/(N-K); the plan's 'fewer is inconclusive' minimum is reported as 'not observable' per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": (f"Only {agreement:.1%} of active bars are agitated down days with a long forecast "
                           "(below 90%): the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    if case_frames:
        cases = pd.concat(case_frames, ignore_index=True)
    else:
        cases = pd.DataFrame({"f": [], "y": [], "day": []})
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases with forecast > 0": n_cases, "distinct days": n_days}

    slope = None
    t = None
    wmean = None
    if n_cases >= 3 and cases["f"].nunique() > 1:
        X = np.column_stack([np.ones(n_cases), cases["f"].values.astype(float)])
        y = cases["y"].values.astype(float)
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ (X.T @ y)
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in cases.groupby("day").indices.items():
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        G = n_days
        K = 2
        corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - K)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t = float(slope / se) if se and np.isfinite(se) and se > 0 else None
    if n_cases > 0 and cases["f"].sum() > 0:
        wmean = float((cases["y"] * cases["f"]).sum() / cases["f"].sum())

    wm_pass = None if wmean is None else bool(wmean > 0)

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"Minimum not reached: {n_cases} cases with forecast > 0 (needs 100) on {n_days} distinct days "
                   "(needs 60).")
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2 and wm_pass:
        status = "confirmed"
        decided = "Confirm: the slope is positive with t >= 2 and the forecast-weighted mean excess return is above 0."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "Inconclusive: positive slope with t >= 2 but the forecast-weighted mean excess return is <= 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "Reject: the slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope's day-clustered t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t is None else {"name": "t clustered by day", "value": t},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "forecast-weighted mean next-day excess return > 0",
            "value": wmean,
            "passed": wm_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
