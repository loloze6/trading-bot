import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LH_LOC = "debug_info.components.low_close.last_history_value"
    PP_LOC = "debug_info.components.low_close.post_pipeline_value"

    # ---------- pass 1: coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp")
            c = d["close"].astype(float).values
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check + case collection ----------
    n_active_eval = 0
    n_agree = 0
    n_active_total = 0
    case_rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            if len(d) == 0:
                continue
            h = d["high"].astype(float)
            l = d["low"].astype(float)
            c = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            ret1 = c.pct_change()
            vol = ret1.rolling(30, min_periods=30).std()
            rng = ((h - l) / c) / vol
            hl = (h - l).replace(0, np.nan)
            loc = (h - c) / hl
            if LH_LOC in d.columns:
                rec = pd.to_numeric(d[LH_LOC], errors="coerce")
                loc = rec.where(rec.notna(), loc)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            profile_ok = regime != "chop"
            situation = (rng >= 2.0 - 1e-9) & (loc >= 0.5 - 1e-9) & profile_ok
            computable = rng.notna() & loc.notna()
            active = fc != 0
            n_active_total += int(active.sum())
            ev = active & computable
            n_active_eval += int(ev.sum())
            n_agree += int((ev & situation & (fc > 0)).sum())

            # cases: forecast > 0, next-day return inside the window
            nxt = c.shift(-1) / c - 1.0
            mu = coin_mean.get(coin, np.nan)
            pp = pd.to_numeric(d[PP_LOC], errors="coerce") if PP_LOC in d.columns else pd.Series(np.nan, index=d.index)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in np.where((fc > 0).values & nxt.notna().values)[0]:
                case_rows.append({
                    "day": ts.iloc[i].strftime("%Y-%m-%d"),
                    "x": float(nxt.iloc[i] - mu),
                    "f": float(pp.iloc[i]) if np.isfinite(pp.iloc[i]) else np.nan,
                })

    reading = ("The rising-calm profile is taken from the recorded regime (not 'chop', since its components are not "
               "recorded and its 365-day lookback exceeds a window), range in usual moves is rebuilt from prices with a "
               "30-bar ddof-1 std of in-window daily returns (bars without 30 prior returns are left out of the "
               "agreement), close location uses the recorded raw value where present; the main t clusters cases by UTC "
               "day (per-day summed deviations, G/(G-1) correction); the 30-day minimum, when unmet, gives "
               "'not observable' per the workflow rule.")

    mm_name = "mean next-day excess return on forecast>0 bars"
    mm_thr = "confirm if mean > 0 with day-clustered t >= 2 and slope check passes; reject if mean < 0 with t <= -2"

    if n_active_eval == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": None,
            "counts": {"distinct days with cases": 0, "cases": 0, "active bars": n_active_total},
            "decided_by": "No active bars on which the situation could be evaluated, so nothing could be observed.",
            "reading": reading,
        }

    agreement = n_agree / n_active_eval
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": None,
            "counts": {"active bars evaluated": n_active_eval},
            "decided_by": ("Fewer than 90% of active bars are long bars of the plan's situation (range >= 2 usual moves, "
                           "close in lower half, rising calm profile): the config does not trade what the Fidelity says."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["day", "x", "f"])
    cases = cases[np.isfinite(cases["x"])]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"distinct days with cases": n_days, "cases": n_cases}

    mean_x = float(cases["x"].mean()) if n_cases else None
    t_main = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["x"] - mean_x
        D = dev.groupby(cases["day"]).sum().values
        G = len(D)
        var = np.sum(D ** 2) / n_cases ** 2 * G / (G - 1)
        if var > 0:
            t_main = float(mean_x / np.sqrt(var))

    slope = None
    t_slope = None
    sc = cases.dropna(subset=["f"])
    if len(sc) >= 3 and np.ptp(sc["f"].values) > 0:
        lr = stats.linregress(sc["f"].values, sc["x"].values)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    slope_pass = bool(slope is not None and t_slope is not None and slope > 0 and t_slope >= 1.0)

    main = {"name": mm_name, "value": mean_x,
            "statistic": {"name": "t of the mean, cases of one day summed", "value": t_main} if t_main is not None else None,
            "threshold": mm_thr}
    supp = {"name": "OLS slope of next-day excess return on low_close post_pipeline_value (t >= 1, positive)",
            "value": slope, "passed": slope_pass if slope is not None else None}
    sit = {"agreement": float(agreement), "passed": True}

    if n_days < 30:
        return {"status": "not observable", "situation_check": sit, "main_measure": main,
                "supporting_check": supp, "counts": counts,
                "decided_by": f"Only {n_days} distinct days with cases, below the plan's minimum of 30.",
                "reading": reading}

    if t_main is not None and mean_x > 0 and t_main >= 2:
        if slope_pass:
            status, why = "confirmed", "Mean next-day excess return above 0 with t >= 2 and the slope check passes."
        else:
            status, why = "inconclusive", "Main measure meets the confirm rule but the supporting slope check fails."
    elif t_main is not None and mean_x < 0 and t_main <= -2:
        status, why = "rejected", "Mean next-day excess return below 0 with t <= -2."
    else:
        status, why = "inconclusive", "The day-clustered t lies between -2 and 2."

    return {"status": status, "situation_check": sit, "main_measure": main,
            "supporting_check": supp, "counts": counts, "decided_by": why, "reading": reading}
