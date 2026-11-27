import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    rows = []          # case rows for the criterion
    n_active = 0
    n_agree = 0
    coin_drift = {}

    # ---- coin drift: mean 1-day return over all windows together ----
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_drift[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---- situation check and case collection ----
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").astype(float)
            f = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).astype(float)
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

            prev = c.shift(1)
            up = c > prev
            up_known = prev.notna() & c.notna()
            ret60 = (c / c.shift(60) - 1.0) * 100.0
            ret60_known = ret60.notna()
            falling = ret60 < -10.0
            not_chop = reg != "chop"
            trending = reg == "trending"

            # situation: up day (from prices) in a falling market (60-bar return below -10 %, from prices);
            # where the needed past prices are not inside the window, the regime detector's record stands in
            up_s = np.where(up_known, up, trending)
            fall_s = np.where(ret60_known, falling, not_chop)
            situation = up_s & fall_s

            active = (f != 0).to_numpy()
            n_active += int(active.sum())
            n_agree += int((active & situation & (f < 0).to_numpy()).sum())

            nxt = c.shift(-1) / c - 1.0
            drift = coin_drift.get(coin, np.nan)
            for i in range(len(df)):
                if f.iloc[i] < 0 and np.isfinite(nxt.iloc[i]) and np.isfinite(drift) and pd.notna(ts.iloc[i]):
                    unusual = -(float(nxt.iloc[i]) - drift)
                    rows.append((coin, w, ts.iloc[i].strftime("%Y-%m-%d"), float(abs(f.iloc[i])), unusual))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    threshold = "mean unusual move positive with day-clustered t >= 2 confirms; negative with t <= -2 rejects"
    main_name = "mean next-day unusual move in the short direction over forecast < 0 bars"
    reading = ("Falling market = 60-bar close return below -10 % and up day = close above prior close, from the window's prices, "
               "using the recorded regime where the window lacks the past prices; cases are all bars with forecast < 0 and a next close "
               "in the window; the larger half is abs(forecast) above the cases' median, the smaller half at or below it; "
               "the day-clustered t uses the per-day summed deviations with a G/(G-1) correction.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": len(rows), "distinct days": len(set(r[2] for r in rows))},
            "decided_by": ("Fewer than 90 % of the active bars are short bars on up days in a falling market "
                           "(close above prior close with 60-bar return below -10 %): the config's forecast does not follow the plan's situation and side."),
            "reading": reading,
        }

    cases = pd.DataFrame(rows, columns=["coin", "window", "day", "absf", "u"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = float(cases["u"].mean()) if n_cases else None
    t = None
    if n_cases >= 2 and n_days >= 2:
        d = cases["u"] - mean_u
        D = d.groupby(cases["day"]).sum().to_numpy()
        G = len(D)
        var = (G / (G - 1)) * float(np.sum(D ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        t = float(mean_u / se) if se > 0 else None

    diff = None
    if n_cases >= 2:
        med = float(cases["absf"].median())
        big = cases.loc[cases["absf"] > med, "u"]
        small = cases.loc[cases["absf"] <= med, "u"]
        if len(big) > 0 and len(small) > 0:
            diff = float(big.mean() - small.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": None if t is None else {"name": "t of the mean, cases of one day taken together", "value": t},
            "threshold": threshold}
    sup = {"name": "larger-half minus smaller-half mean unusual move (split at median abs(forecast))",
           "value": diff, "passed": sup_pass}

    if n_cases < 200 or n_days < 100:
        status = "not observable"
        decided = (f"The plan's minimum of 200 cases on 100 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t is None or mean_u is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the larger-half minus smaller-half difference is above 0."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: up days in falling markets are followed by rises beyond the drift."
    elif mean_u > 0 and t >= 2:
        status = "inconclusive"
        decided = "The t confirms, but the size check fails (larger-half minus smaller-half difference not above 0)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
