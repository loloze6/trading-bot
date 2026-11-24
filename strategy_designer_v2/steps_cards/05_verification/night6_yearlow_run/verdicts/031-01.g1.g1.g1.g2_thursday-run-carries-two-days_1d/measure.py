import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.ret14_scaled.last_history_value"
    H = 2

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True)
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            # Thursday's close: the bar starting Thursday (UTC), whose next bar is stamped Friday
            thursday = (ts.dt.dayofweek == 3).values
            active = fc != 0
            raw_sign = np.sign(np.where(np.isnan(raw), 0.0, raw))
            ok = active & thursday & (raw_sign != 0) & (np.sign(fc) == raw_sign)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x drift-removed 2-bar return on Thursday-close bars"
    main_thr = "t >= 2 confirms (with the check passing), t <= -2 rejects, otherwise inconclusive"
    check_name = "top third minus bottom third of forecasts, mean drift-removed 2-bar return, above 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are Thursday-close bars "
                           "(bar starting Thursday UTC) whose forecast sign matches the sign of the "
                           "volatility-scaled 14-day return."),
            "reading": "The situation is a bar starting on Thursday UTC (next bar Friday) and the side is the sign of the raw ret14_scaled value.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        # coin's mean 2-bar return over all its windows, non-overlapping grid 0,2,4,... per window
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(close)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            fc = pd.to_numeric(df[FC], errors="coerce").values
            for i in range(n - H):
                if ts.iloc[i].dayofweek != 3:
                    continue
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                coin_cases.append((coin, ts.iloc[i].normalize(), float(f), float(r)))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for (c, day, f, r) in coin_cases:
            rows.append({"coin": c, "day": day, "forecast": f, "ex": r - drift})

    cases = pd.DataFrame(rows, columns=["coin", "day", "forecast", "ex"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"Thursday cases with a nonzero forecast": n_cases, "distinct days": n_days}

    value = None
    t = None
    if n_cases > 0:
        prod = cases["forecast"].values / 10.0 * cases["ex"].values
        m = float(np.mean(prod))
        value = m
        dev = pd.Series(prod - m).groupby(cases["day"].values).sum().values
        G = len(dev)
        if G > 1:
            se = np.sqrt(np.sum(dev ** 2) * G / (G - 1)) / n_cases
            t = float(m / se) if se > 0 else None

    # supporting check
    chk_val = None
    chk_pass = None
    k = n_cases // 3
    if k >= 1:
        srt = cases.sort_values("forecast", kind="mergesort").reset_index(drop=True)
        bottom = srt["ex"].iloc[:k].mean()
        top = srt["ex"].iloc[n_cases - k:].mean()
        chk_val = float(top - bottom)
        chk_pass = bool(chk_val > 0)

    if n_cases < 200 or n_days < 100:
        status = "not observable"
        decided = (f"The plan's minimum of 200 Thursday cases with a nonzero forecast on at least 100 distinct days "
                   f"is not reached ({n_cases} cases, {n_days} days).")
    elif t is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and chk_pass:
        status = "confirmed"
        decided = "The main measure's t is >= 2 and the top-minus-bottom-third check is above 0 (confirm rule)."
    elif t <= -2:
        status = "rejected"
        decided = "The main measure's t is <= -2 (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main measure's t is >= 2 but the supporting check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": value,
            "statistic": ({"name": "t of the mean, cases of one day summed", "value": t} if t is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {"name": check_name, "value": chk_val, "passed": chk_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Thursday-close bars are bars starting Thursday UTC with a nonzero forecast and a full 2-bar "
                    "return inside the window (weekly spacing makes them non-overlapping), the drift is each coin's "
                    "mean 2-bar return on the non-overlapping grid 0,2,4,... of all its windows, and the thirds are "
                    "the floor(n/3) lowest and highest pooled forecasts."),
    }
