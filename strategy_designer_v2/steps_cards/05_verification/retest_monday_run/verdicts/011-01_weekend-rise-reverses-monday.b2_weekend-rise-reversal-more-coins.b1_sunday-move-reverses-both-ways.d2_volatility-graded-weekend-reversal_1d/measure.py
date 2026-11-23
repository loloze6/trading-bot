import numpy as np
import pandas as pd
from scipy import stats


def _to_time(ts):
    if pd.api.types.is_numeric_dtype(ts):
        v = pd.Series(ts).astype(float)
        mx = v.abs().max() if len(v) else 0
        unit = "ms" if mx > 1e11 else "s"
        if mx > 1e14:
            unit = "us"
        if mx > 1e17:
            unit = "ns"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(ts, utc=True)


def measure(bars):
    RAW = "debug_info.components.wkd_rev.last_history_value"
    H = 2

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            if len(d) == 0:
                continue
            d["_t"] = _to_time(d["timestamp"]).reset_index(drop=True)
            d["_sun"] = d["_t"].dt.dayofweek == 6
            close = d["close"].astype(float)
            d["_ret1"] = close / close.shift(1) - 1.0
            raw = d[RAW].astype(float) if RAW in d.columns else pd.Series(np.nan, index=d.index)
            move = d["_ret1"].copy()
            move = move.where(move.notna(), raw)  # first row of a window: use the raw component value
            d["_move"] = move
            fc = d["forecast"].astype(float).fillna(0.0)
            d["_fc"] = fc
            act = fc != 0
            exp_sign = -np.sign(d["_move"])
            ok = act & d["_sun"] & (np.sign(fc) == exp_sign) & (exp_sign != 0)
            n_active += int(act.sum())
            n_agree += int(ok.sum())
            prepared[coin][w] = d

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean signed excess 2-day return (Sunday close to Tuesday close) over Sunday cases, before costs"
    main_thr = "confirm: mean > 0 with t >= 2 (and slope t >= 2); reject: mean < 0 with t <= -2"
    sup_name = "slope of signed excess 2-day return on s20/s60 (recomputed from closes)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on expected side": n_agree},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are Sunday bars whose forecast sign is "
                          "against the Sunday bar's return, as the plan's Fidelity requires.",
            "reading": "Situation = bar whose start (UTC) is a Sunday; expected side = minus the sign of the Sunday bar's "
                       "close-to-close return (raw component value on a window's first row).",
        }

    # ---------- criterion ----------
    xs, ratios = [], []
    for coin, wins in prepared.items():
        # coin's mean 2-day return over all windows, non-overlapping grid 0,2,4,...
        grid = []
        for w, d in wins.items():
            c = d["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    grid.append(c[i + H] / c[i] - 1.0)
        if len(grid) == 0:
            continue
        mu = float(np.mean(grid))
        for w, d in wins.items():
            c = d["close"].astype(float)
            fwd = c.shift(-H) / c - 1.0
            r = d["_ret1"]
            s20 = r.rolling(20, min_periods=20).std()
            s60 = r.rolling(60, min_periods=60).std()
            ratio = s20 / s60
            cases = d.index[d["_sun"] & (d["_fc"] != 0)]
            for i in cases:
                f = fwd.iloc[i]
                if not np.isfinite(f):
                    continue
                x = (f - mu) * np.sign(d["_fc"].iloc[i])
                xs.append(float(x))
                q = ratio.iloc[i]
                ratios.append(float(q) if np.isfinite(q) else np.nan)

    xs = np.array(xs, dtype=float)
    ratios = np.array(ratios, dtype=float)
    n = len(xs)

    mean = float(np.mean(xs)) if n > 0 else None
    tval = None
    if n > 1:
        sd = float(np.std(xs, ddof=1))
        tval = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    m = np.isfinite(ratios)
    n_reg = int(m.sum())
    slope, slope_t = None, None
    if n_reg >= 3 and np.ptp(ratios[m]) > 0:
        lr = stats.linregress(ratios[m], xs[m])
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    sup_pass = None
    if slope is not None and slope_t is not None:
        sup_pass = bool(slope > 0 and slope_t >= 2)
    elif n_reg > 0:
        sup_pass = False

    counts = {"Sunday cases": n, "cases in slope regression": n_reg}

    if n < 300:
        status = "not observable"
        decided = f"Only {n} Sunday cases, below the plan's minimum of 300."
    elif tval is not None and mean > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Main mean positive with t >= 2 and the s20/s60 slope positive with t >= 2."
        else:
            status = "inconclusive"
            decided = "Main t >= 2 but the s20/s60 slope is not positive with t >= 2."
    elif tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Main mean negative with t <= -2: weekend moves continue rather than reverse."
    else:
        status = "inconclusive"
        decided = "Main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean", "value": tval} if tval is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": slope, "passed": sup_pass,
                             "slope_t": slope_t},
        "counts": counts,
        "decided_by": decided,
        "reading": "Cases are Sunday (UTC start) bars with nonzero forecast and a close two bars later in the same "
                   "window, the coin's mean 2-day return is pooled over a 0,2,4,... grid of all its windows, s20/s60 "
                   "uses within-window daily returns (std ddof 1, cases without 60 returns left out of the regression), "
                   "and the plan's 300-case minimum is applied as 'not observable'.",
    }
