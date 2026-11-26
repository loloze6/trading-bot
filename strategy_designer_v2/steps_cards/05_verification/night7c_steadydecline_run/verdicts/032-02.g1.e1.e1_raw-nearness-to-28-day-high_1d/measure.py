import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.high_prox.last_history_value"
    POST = "debug_info.components.high_prox.post_pipeline_value"

    # ---------- 1. Situation check ----------
    # Situation: nearness to the 28-day closing high, whatever the 28-day return,
    # so it holds on every bar where the raw proximity 1/(1+D) is defined (finite, in (0, 1]).
    # Expected side: long, so an active bar should have a positive forecast.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            active = np.isfinite(fc) & (fc != 0)
            situ = np.isfinite(raw) & (raw > 0) & (raw <= 1 + 1e-9)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of 5-bar excess return on the high_prox forecast (pooled OLS)"
    main_thr = "slope t >= 2 confirms (with top-minus-bottom third > 0); t <= -2 rejects"
    sup_name = "mean excess 5-bar return, top third of forecasts minus bottom third"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are bars of the plan's situation on its long side: "
                           "the forecast is not a positive nearness to the 28-day high on its active bars."),
            "reading": "The situation was taken as holding wherever the raw proximity value is defined, since the plan keeps it whatever the 28-day return.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            x = (pd.to_numeric(df[POST], errors="coerce").to_numpy(dtype=float)
                 if POST in df.columns else np.full(len(df), np.nan))
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D").astype("int64").to_numpy() if hasattr(ts, "dt") else np.zeros(len(df))
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                rows.append((coin, c1 / c0 - 1.0, x[i], day[i]))

    if rows:
        cases = pd.DataFrame(rows, columns=["coin", "ret", "x", "day"])
        coin_mean = cases.groupby("coin")["ret"].mean()
        cases["exc"] = cases["ret"] - cases["coin"].map(coin_mean)
        cases = cases[np.isfinite(cases["x"]) & np.isfinite(cases["exc"])].reset_index(drop=True)
    else:
        cases = pd.DataFrame(columns=["coin", "ret", "x", "day", "exc"])

    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0
    counts = {"grid cases across coins and windows": n, "days": n_days}

    slope = None
    t = None
    diff = None
    if n >= 3:
        xv = cases["x"].to_numpy(dtype=float)
        yv = cases["exc"].to_numpy(dtype=float)
        xc = xv - xv.mean()
        sxx = float(np.sum(xc ** 2))
        if sxx > 0:
            b = float(np.sum(xc * (yv - yv.mean())) / sxx)
            a = yv.mean() - b * xv.mean()
            e = yv - a - b * xv
            score = pd.Series(xc * e).groupby(cases["day"].to_numpy()).sum().to_numpy()
            G = len(score)
            var = float(np.sum(score ** 2)) / sxx ** 2
            if G > 1:
                var *= G / (G - 1)
            slope = b
            t = float(b / np.sqrt(var)) if var > 0 else None
        k = n // 3
        if k >= 1:
            order = np.argsort(xv, kind="mergesort")
            bottom = yv[order[:k]]
            top = yv[order[-k:]]
            diff = float(top.mean() - bottom.mean())

    sup_pass = None if diff is None else bool(diff > 0)
    reading = ("The slope's t uses a day-clustered standard error (cases summed per calendar day, with a G/(G-1) "
               "correction), the coin's mean 5-bar return is the mean of its grid returns over all windows, and the "
               "thirds are the n//3 lowest and highest cases by post_pipeline_value (stable sort).")

    base = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t, day-clustered", "value": t} if t is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "reading": reading,
    }

    if n < 300:
        base["status"] = "not observable"
        base["decided_by"] = f"Only {n} grid cases across coins and windows, below the plan's minimum of 300."
        return base
    if t is None:
        base["status"] = "inconclusive"
        base["decided_by"] = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
        return base
    if t >= 2 and diff is not None and diff > 0:
        base["status"] = "confirmed"
        base["decided_by"] = "The slope's t is at least 2 and the top-minus-bottom-third difference is positive."
    elif t <= -2:
        base["status"] = "rejected"
        base["decided_by"] = "The slope's t is -2 or less."
    elif t >= 2:
        base["status"] = "inconclusive"
        base["decided_by"] = "The slope's t is 2 or more but the top-minus-bottom-third difference is at or below 0."
    else:
        base["status"] = "inconclusive"
        base["decided_by"] = "The slope's t lies between -2 and 2."
    return base
