import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.vol_surge.last_history_value"
    PERIOD = 20
    MIN_POS = 300
    T_THR = 2.0

    # ---------- collect per-window frames, next-day returns, situation ----------
    per_coin = {}
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp")
            d = d.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            vol = pd.to_numeric(d["volume"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            # next-day return inside the window only
            nxt = close.shift(-1) / close - 1.0
            # raw component value: recorded, else recomputed from volume in-window
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            prior_mean = vol.shift(1).rolling(PERIOD, min_periods=PERIOD).mean()
            recomputed = vol / prior_mean - 1.0
            raw = raw.where(raw.notna(), recomputed)
            frames.append(pd.DataFrame({"fc": fc, "ret": nxt, "raw": raw}))
        if frames:
            per_coin[coin] = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    active_total = 0
    active_ok = 0
    for coin, d in per_coin.items():
        act = d["fc"].notna() & (d["fc"] != 0)
        active_total += int(act.sum())
        ok = act & (d["raw"] > 0) & (d["fc"] > 0)
        active_ok += int(ok.sum())
    agreement = (active_ok / active_total) if active_total > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "t-statistic of pooled OLS slope of next-day excess return on forecast"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 bars with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": active_total},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where today's volume "
                           "is above its prior 20-day mean (raw centred volume ratio > 0), as the Fidelity's situation requires."),
            "reading": "The situation is a raw centred volume ratio above 0 (volume above the prior 20-day mean) with a positive forecast; raw values recomputed from in-window volume where not recorded.",
        }

    # ---------- main measure: pooled OLS ----------
    xs, ys = [], []
    for coin, d in per_coin.items():
        rets = d["ret"].dropna()
        if len(rets) == 0:
            continue
        coin_mean = float(rets.mean())  # coin's mean daily return over all its windows
        sub = d[d["ret"].notna() & d["fc"].notna()]
        xs.append(sub["fc"].to_numpy(dtype=float))
        ys.append(sub["ret"].to_numpy(dtype=float) - coin_mean)
    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n = int(len(x))
    n_pos = int((x > 0).sum())

    slope = None
    t = None
    if n >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    counts = {"bars with a forecast above 0": n_pos, "bars in the fit": n}
    reading = ("Every bar with a next-day close in the same window enters the fit (zero-forecast bars included), "
               "the coin's mean daily return is the mean of all its in-window next-day returns, and the t is the ordinary OLS "
               "slope t with an intercept; the situation is a raw centred volume ratio above 0 with a positive forecast.")

    if n_pos < MIN_POS or t is None:
        status = "not observable"
        decided = f"The fit has {n_pos} bars with a forecast above 0, fewer than the plan's minimum of 300 (or no slope could be fitted)."
    elif slope > 0 and t >= T_THR:
        status = "confirmed"
        decided = "Confirm rule: the slope is positive with t >= 2, on at least 300 bars with a forecast above 0."
    elif slope < 0 and t <= -T_THR:
        status = "rejected"
        decided = "Reject rule: the slope is negative with t <= -2, on at least 300 bars with a forecast above 0."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t,
            "statistic": None if t is None else {"name": "OLS slope t", "value": t},
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
