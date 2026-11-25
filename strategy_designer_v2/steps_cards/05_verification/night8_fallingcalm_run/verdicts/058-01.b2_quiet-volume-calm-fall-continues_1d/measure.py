import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.quiet_vol.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret30 = close / close.shift(30) - 1.0
            reg = df["regime"].astype(str)
            # 30-day fall: from prices when 30 prior bars exist in the window,
            # otherwise from the regime (trending requires fall30 < 0 by the config)
            fall = np.where(ret30.notna(), ret30 < 0, reg == "trending")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            quiet = (raw < 0).fillna(False).values
            active = (fc != 0).values
            ok = active & fall & quiet & (fc < 0).values
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars with a 30-day return below 0 "
                           "and recent volume below the prior year's (raw log ratio < 0)."
                           if n_active > 0 else "No active bars: the config never takes the plan's short."),
            "reading": "none",
        }

    # ---------- 2. grid cases ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                f = pd.to_numeric(pd.Series([df["forecast"].iloc[i]]), errors="coerce").iloc[0]
                rows.append({
                    "coin": coin, "window": w,
                    "day": pd.to_datetime(df["timestamp"].iloc[i], utc=True).floor("D"),
                    "ret": r, "forecast": f, "regime": str(df["regime"].iloc[i]),
                })
    g = pd.DataFrame(rows)
    if len(g) == 0:
        g = pd.DataFrame(columns=["coin", "window", "day", "ret", "forecast", "regime"])
    g["coin_mean"] = g.groupby("coin")["ret"].transform("mean") if len(g) else []
    g["excess"] = g["ret"] - g["coin_mean"]

    neg = g[(g["forecast"] < 0)].dropna(subset=["forecast", "excess"]).copy()
    neg["val"] = (-neg["forecast"] / 10.0) * neg["excess"]
    n_cases = int(len(neg))
    n_days = int(neg["day"].nunique()) if n_cases else 0

    mean_val = float(neg["val"].mean()) if n_cases else None
    t_val = None
    if n_cases > 0 and n_days > 1:
        dev = neg["val"] - mean_val
        S = dev.groupby(neg["day"]).sum().values
        var = (S ** 2).sum() / (n_cases ** 2) * n_days / (n_days - 1)
        se = np.sqrt(var)
        t_val = float(mean_val / se) if se > 0 else None

    # supporting check
    tr = g[(g["regime"] == "trending")].dropna(subset=["forecast", "excess"])
    tr_neg = tr[tr["forecast"] < 0]
    heavy = tr[tr["forecast"] == 0]
    n_heavy = int(len(heavy))
    diff = None
    check_pass = None
    if len(tr_neg) > 0 and n_heavy > 0:
        med = tr_neg["forecast"].median()
        quiet_half = tr_neg[tr_neg["forecast"] < med]
        if len(quiet_half) > 0:
            diff = float(quiet_half["excess"].mean() - heavy["excess"].mean())
            check_pass = bool(diff < 0)

    counts = {"grid cases with forecast < 0": n_cases,
              "days of those cases": n_days,
              "heavy-volume cases for the check": n_heavy}

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 grid cases with forecast < 0 ({n_cases})."
    elif n_heavy < 10:
        status = "not observable"
        decided = f"Fewer than 10 heavy-volume cases for the check ({n_heavy})."
    elif t_val is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed, so neither confirm nor reject is met."
    elif mean_val > 0 and t_val >= 2:
        if check_pass:
            status = "confirmed"
            decided = "Main measure positive with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "Main measure positive with t >= 2 but the supporting check fails."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "Main measure negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The main measure's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean of (-forecast/10) x 5-bar excess return on grid bars with forecast < 0",
            "value": mean_val,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_val}
                          if t_val is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2 and check passing; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "trending grid cases: excess return of quieter half minus heavy-volume (forecast 0) cases < 0",
            "value": diff, "passed": check_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The 30-day fall is taken from closes when 30 prior bars exist in the window and from "
                    "regime 'trending' otherwise; the coin's mean 5-bar return is the mean of its grid returns "
                    "over all windows; the check's excess return is unweighted and the median is over negative "
                    "forecasts of trending grid cases; the day-clustered t uses a n_days/(n_days-1) correction."),
    }
