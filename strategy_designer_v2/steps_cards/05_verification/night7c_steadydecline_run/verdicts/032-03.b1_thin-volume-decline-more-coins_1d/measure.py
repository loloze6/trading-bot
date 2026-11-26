import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    FC = "forecast"
    REG = "regime"
    TREND = "trending"

    # ---------- 1. Situation check: active bars must be 28-bar declines, on the short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            ret28 = close / close.shift(28) - 1.0
            # where the 28-bar return is not computable inside the window, use the detector's recorded decision
            situ = np.where(ret28.notna(), ret28 < 0, d[REG].astype(str) == TREND)
            active = (fc != 0).values
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0).values).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of 5-bar excess return (return minus coin drift) on forecast, in-regime grid cases"
    main_thr = "slope t >= 2 confirms (with supporting check and >=100 cases on >=60 days); t <= -2 rejects"
    reading = ("Situation recomputed as close below its close 28 bars earlier inside each window, falling back to the "
               "recorded regime on a window's first 28 bars; expected side short; in-regime cases are grid bars with "
               "regime 'trending'; drift is the coin's mean 5-bar return over its non-overlapping grid of all windows; "
               "the slope's t uses day-clustered (cases summed per day) standard errors with a G/(G-1) correction; "
               "the supporting check uses in-regime grid cases with forecast <= -2.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars inside a 28-bar decline: "
                           "the config's forecast does not follow the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. Grid cases ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            reg = d[REG].astype(str).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in range(0, len(d), H):
                if i + H >= len(d):
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                coin_rows.append({
                    "coin": coin, "ret": r, "fc": fc[i],
                    "inreg": reg[i] == TREND, "day": ts.iloc[i].floor("D"),
                })
        if coin_rows:
            cdf = pd.DataFrame(coin_rows)
            drift = cdf["ret"].mean()
            cdf["ex"] = cdf["ret"] - drift
            rows.append(cdf)

    if rows:
        g = pd.concat(rows, ignore_index=True)
    else:
        g = pd.DataFrame(columns=["coin", "ret", "fc", "inreg", "day", "ex"])

    cases = g[g["inreg"].astype(bool)].copy()
    cases = cases[np.isfinite(cases["fc"].astype(float)) & np.isfinite(cases["ex"].astype(float))]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope, t = None, None
    if n_cases >= 3:
        x = cases["fc"].astype(float).values
        y = cases["ex"].astype(float).values
        xc = x - x.mean()
        sxx = float((xc ** 2).sum())
        if sxx > 0:
            b = float((xc * y).sum() / sxx)
            a = y.mean() - b * x.mean()
            e = y - a - b * x
            s = pd.Series(xc * e).groupby(cases["day"].values).sum().values
            G = len(s)
            var = float((s ** 2).sum()) / sxx ** 2
            if G > 1:
                var *= G / (G - 1)
            se = np.sqrt(var)
            slope = b
            t = float(b / se) if se > 0 else None

    # supporting check
    sup = cases[cases["fc"].astype(float) <= -2.0]
    n_sup = int(len(sup))
    sup_val = float(sup["ex"].mean()) if n_sup > 0 else None
    sup_pass = (sup_val < 0) if sup_val is not None else None

    counts = {"in-regime cases": n_cases, "distinct days": n_days, "cases with forecast <= -2": n_sup}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"Minimum not reached: {n_cases} in-regime cases on {n_days} distinct days "
                   "(the plan needs at least 100 cases on at least 60 days).")
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Slope t >= 2, the supporting check holds, with at least 100 cases on at least 60 days: confirm rule."
    elif t >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but the supporting check fails (or has no cases): inconclusive by the plan's rule."
    elif t <= -2:
        status = "rejected"
        decided = "Slope t <= -2 with at least 100 cases on at least 60 days: reject rule."
    else:
        status = "inconclusive"
        decided = "Slope t between -2 and 2: inconclusive by the plan's rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": None if slope is None else float(slope),
            "statistic": None if t is None else {"name": "slope t, cases of a day taken together", "value": float(t)},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "mean 5-bar excess return on cases with forecast <= -2 below 0",
            "value": sup_val,
            "passed": None if sup_pass is None else bool(sup_pass),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
