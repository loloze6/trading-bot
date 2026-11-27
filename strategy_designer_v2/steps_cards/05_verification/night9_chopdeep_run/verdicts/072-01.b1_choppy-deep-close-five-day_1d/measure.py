import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    DEPTH = "debug_info.components.depth.last_history_value"
    ACTIVE_REGIME = "unknown"  # the regime holding the depth component (choppy profile, by the config)

    def to_days(ts):
        if np.issubdtype(ts.dtype, np.number):
            unit = "ms" if ts.abs().max() > 1e11 else "s"
            t = pd.to_datetime(ts, unit=unit, utc=True)
        else:
            t = pd.to_datetime(ts, utc=True)
        return t.dt.strftime("%Y-%m-%d")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if DEPTH in df.columns:
                depth = pd.to_numeric(df[DEPTH], errors="coerce")
            else:
                depth = pd.Series(np.nan, index=df.index)
            choppy = df["regime"].astype(str) == ACTIVE_REGIME
            situation = choppy & depth.notna() & (depth < 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS slope of 5-bar excess return on forecast (grid cells with forecast < 0)"
    thr = "confirm: slope t >= 2 with supporting check; reject: slope t <= -2"
    sup_name = "mean 5-bar excess return, deepest third minus shallowest third of forecasts (must be < 0)"
    reading = ("Choppy profile read as the bars where regime is the config's active regime 'unknown' "
               "(|60-day trend| <= 10, the depth component's regime), situation as depth raw value < 0 there; "
               "normal drift is the coin's mean 5-bar return on all grid cells of all its windows; slope from pooled "
               "OLS over all coins; thirds are the lowest and highest n//3 forecasts by rank; the plan's minimum "
               "counts, if not reached, give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars in the choppy profile "
                           "with the close below its 20-day high, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            days = to_days(df["timestamp"]).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(f[i]) and f[i] < 0:
                    coin_rows.append((coin, days[i], float(f[i]), r))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for (c, d, fv, r) in coin_rows:
            rows.append({"coin": c, "day": d, "forecast": fv, "excess": r - drift})

    cases = pd.DataFrame(rows, columns=["coin", "day", "forecast", "excess"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases with a nonzero forecast": n_cases, "distinct days": n_days}

    slope = None
    t_slope = None
    if n_cases >= 3 and cases["forecast"].nunique() > 1:
        res = stats.linregress(cases["forecast"].values, cases["excess"].values)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        s = cases.sort_values("forecast", kind="mergesort").reset_index(drop=True)
        k = n_cases // 3
        deep = s.iloc[:k]["excess"].mean()
        shallow = s.iloc[n_cases - k:]["excess"].mean()
        sup_val = float(deep - shallow)
        sup_pass = bool(deep < shallow)

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": thr}
    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_cases < 100 or n_days < 60:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": (f"The plan's minimum of 100 grid cases on at least 60 distinct days is not reached "
                               f"({n_cases} cases on {n_days} days)."),
                "reading": reading}

    if t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t >= 2 and the deepest third's mean excess return is below the shallowest third's: confirm rule."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but the supporting check fails: a confirming t whose supporting check fails is inconclusive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t <= -2: deeper closes are followed by relatively larger rises (reject rule)."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2: inconclusive rule."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": decided, "reading": reading}
