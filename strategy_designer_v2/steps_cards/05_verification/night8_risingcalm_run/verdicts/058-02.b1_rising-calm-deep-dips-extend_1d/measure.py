import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.scaled_pullback.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            # scaled pullback raw value; recompute the sign from prices where not recorded
            high5 = close.rolling(H, min_periods=H).max()
            dist_px = close / high5 - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                dist = raw.where(raw.notna(), dist_px)
            else:
                dist = dist_px
            pullback = dist < 0
            rising_calm = d["regime"].astype(str) == "unknown"
            fc = pd.to_numeric(d[FC], errors="coerce")
            active = fc.notna() & (fc != 0)
            agree = active & rising_calm & pullback & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of 5-bar forward excess return on forecast (forecast < 0, non-overlapping grid)"
    thr = "confirm: slope t >= 2 with supporting check passing; reject: slope t <= -2"
    reading = ("Rising calm is the detector's own decision (regime 'unknown', i.e. neither veto fired, since the "
               "detector's components are not recorded and warm-up bars are absent), the pullback is "
               "last_history_value < 0 (price recompute where missing); the slope's t uses a day-clustered "
               "sandwich standard error with a G/(G-1) correction; the deepest third is the floor(n/3) cases with "
               "the most negative forecast; drift is the coin's mean 5-bar grid return over all its windows; "
               "the plan's minimum counts, when not reached, give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "agreeing bars": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are rising-calm bars below the "
                           "5-day closing high with a short forecast, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_grid = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_grid.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    rows.append({"coin": coin, "fc": float(fc[i]), "ret": r,
                                 "day": ts.iloc[i].strftime("%Y-%m-%d")})
        drift = float(np.mean(coin_grid)) if coin_grid else np.nan
        for r_ in rows:
            if r_["coin"] == coin and "ex" not in r_:
                r_["ex"] = r_["ret"] - drift

    cases = pd.DataFrame(rows)
    if len(cases):
        cases = cases[np.isfinite(cases["ex"])]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"non-overlapping cases": n_cases, "distinct days": n_days}

    slope = None
    t = None
    if n_cases >= 3 and cases["fc"].var() > 0:
        x = cases["fc"].values
        y = cases["ex"].values
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        slope = float(np.sum(xc * (y - y.mean())) / sxx)
        a = y.mean() - slope * x.mean()
        e = y - a - slope * x
        s = pd.Series(xc * e).groupby(cases["day"].values).sum().values
        G = len(s)
        if G > 1:
            var = (G / (G - 1)) * float(np.sum(s ** 2)) / sxx ** 2
            t = float(slope / np.sqrt(var)) if var > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        k = n_cases // 3
        deep = cases.sort_values("fc", kind="mergesort").iloc[:k]
        sup_val = float(np.mean(-deep["ex"].values))
        sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": slope,
            "statistic": {"name": "slope t, day-clustered", "value": t} if t is not None else None,
            "threshold": thr}
    sup = {"name": "deepest third: mean short-side 5-bar excess return > 0", "value": sup_val, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_cases < 30 or n_days < 20:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": "The plan's minimum of 30 non-overlapping cases on at least 20 distinct days is not reached.",
                "reading": reading}

    if t is None:
        status, dec = "inconclusive", "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status, dec = "confirmed", "Slope t >= 2 and the deepest third's short excess return is above 0."
    elif t >= 2:
        status, dec = "inconclusive", "Slope t >= 2 but the supporting check fails: a confirming slope with a failed check is inconclusive."
    elif t <= -2:
        status, dec = "rejected", "Slope t <= -2: deeper scaled pullbacks are followed by larger excess rises."
    else:
        status, dec = "inconclusive", "Slope t lies between -2 and 2."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": dec, "reading": reading}
