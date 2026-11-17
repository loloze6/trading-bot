import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.weekend_move.last_history_value"
    H = 2
    MIN_CASES = 300

    def to_time(s):
        if pd.api.types.is_numeric_dtype(s):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- coin mean 2-bar return (non-overlapping grid, all windows pooled) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            if len(idx) == 0:
                continue
            r = c[idx + H] / c[idx] - 1.0
            r = r[np.isfinite(r)]
            rets.extend(r.tolist())
        coin_mean[coin] = float(np.mean(rets)) if len(rets) else np.nan

    # ---------- situation check + case collection ----------
    n_active = 0
    n_agree = 0
    case_f = []
    case_x = []

    for coin, wins in bars.items():
        mu = coin_mean.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = to_time(df["timestamp"])
            is_sun = (ts.dt.dayofweek == 6).values
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            # raw 1-bar return: recorded value where present, else recomputed from prices
            price_ret = np.full(len(close), np.nan)
            if len(close) > 1:
                price_ret[1:] = close[1:] / close[:-1] - 1.0
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce").values
                raw = np.where(np.isfinite(lhv), lhv, price_ret)
            else:
                raw = price_ret
            regime = df["regime"].astype(str).values

            for t in range(len(df)):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                r = raw[t]
                if is_sun[t] and np.isfinite(r) and r != 0 and np.sign(f) == -np.sign(r):
                    n_agree += 1

            for t in range(len(df)):
                f = fc[t]
                if not is_sun[t] or regime[t] != "mean_reversion":
                    continue
                if not np.isfinite(f) or f == 0:
                    continue
                if t + H >= len(df):
                    continue
                r2 = close[t + H] / close[t] - 1.0
                if not np.isfinite(r2) or not np.isfinite(mu):
                    continue
                case_f.append(float(f))
                case_x.append(float(r2 - mu))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean of (forecast/10) x excess 2-bar return over coin mean, Sunday cases"
    threshold = "confirm if t >= 2 with tercile check passing; reject if t <= -2; at least 300 cases"
    reading = ("Sunday bar is the bar whose UTC start is a Sunday; side expected is opposite the sign of the Sunday "
               "1-bar return (recorded last_history_value, else close/prev close); cases require Sunday, regime "
               "mean_reversion, non-zero forecast and t+2 in window; coin mean 2-bar return from the non-overlapping "
               "grid of all windows pooled; terciles are three near-equal groups of cases sorted by |forecast| "
               "(stable sort), and the 300-case minimum is treated as the not-observable minimum.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": int(len(case_f)), "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are Sunday bars with a forecast opposite to the "
                           "Sunday 1-bar return, so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    f = np.array(case_f)
    x = np.array(case_x)
    n = len(f)
    counts = {"cases": int(n)}

    score = (f / 10.0) * x
    mean_score = float(np.mean(score)) if n > 0 else None
    t_stat = None
    if n > 1:
        sd = float(np.std(score, ddof=1))
        if sd > 0:
            t_stat = float(mean_score / (sd / np.sqrt(n)))

    sup_val = None
    sup_pass = None
    if n >= 3:
        order = np.argsort(np.abs(f), kind="mergesort")
        groups = np.array_split(order, 3)
        sx = np.sign(f) * x
        bottom = float(np.mean(sx[groups[0]]))
        top = float(np.mean(sx[groups[2]]))
        sup_val = top - bottom
        sup_pass = bool(sup_val > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 300 cases in total."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The main-measure t could not be computed, so it lies in neither the confirm nor the reject range."
    elif t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main-measure t is >= 2 and the top-minus-bottom tercile difference is > 0."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The main-measure t is <= -2: weekend moves continue into Monday and Tuesday."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "The main-measure t is >= 2 but the tercile difference is <= 0."
    else:
        status = "inconclusive"
        decided = "The main-measure t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_score,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "top minus bottom |forecast| tercile mean of sign(forecast) x excess 2-bar return",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
