import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.fall24.last_history_value"
    POST = "debug_info.components.fall24.post_pipeline_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}  # coin -> list of per-window frames
    for coin, wins in bars.items():
        prepared[coin] = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            d["_hour"] = ts.dt.hour.values
            close = pd.to_numeric(d["close"], errors="coerce")
            d["_close"] = close
            # raw 24-bar return: recorded value, else recomputed from prices inside the window
            recomputed = close / close.shift(H) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            d["_raw"] = raw
            d["_fwd"] = close.shift(-H) / close - 1.0
            d["_post"] = pd.to_numeric(d[POST], errors="coerce") if POST in d.columns else np.nan
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            d["_fc"] = fc
            prepared[coin].append(d)

            active = fc != 0
            # bar closing at 20:00 UTC = bar starting 19:00; situation = 24h fall; side = long
            situ = (d["_hour"] == 19) & (d["_raw"] < 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "pooled OLS slope of next-24-bar excess return on fall24 post_pipeline_value at 20:00 UTC bars"
    thr = "slope t >= +2 confirms (with supporting check); t <= -2 rejects; otherwise inconclusive"
    reading = ("The 20:00 UTC bar is the bar stamped 19:00; the coin's mean 24-bar return is the mean of the "
               "non-overlapping 24-bar returns (positions 0, 24, 48, ... of each window) pooled over all its windows; "
               "the slope's t is the ordinary OLS t with an intercept; the 300-bar minimum counts 20:00 bars with "
               "forecast > 0 and a next-24-bar return inside the window, and a shortfall is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars closing at 20:00 UTC "
                           "after a 24-hour fall, so the config does not trade the plan's situation and side."
                           if n_active > 0 else
                           "The forecast is never non-zero, so the config never takes the plan's long after a 24-hour fall at 20:00 UTC."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, frames in prepared.items():
        grid_rets = []
        for d in frames:
            c = d["_close"].values
            idx = np.arange(0, len(d) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.append(r[np.isfinite(r)])
        if not grid_rets:
            continue
        allr = np.concatenate(grid_rets)
        if len(allr) == 0:
            continue
        mu = float(np.mean(allr))
        for d in frames:
            s = d[(d["_hour"] == 19)]
            s = s[np.isfinite(s["_fwd"]) & np.isfinite(s["_post"])]
            xs.append(s["_post"].values.astype(float))
            ys.append(s["_fwd"].values.astype(float) - mu)

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n_total = int(len(x))
    pos = x > 0
    n_pos = int(pos.sum())

    counts = {"bars at 20:00 with forecast > 0": n_pos, "bars at 20:00 in regression": n_total}

    slope = None
    t = None
    if n_total >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    sup_val = float(np.mean(y[pos])) if n_pos > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
            "threshold": thr}
    supporting = {"name": "mean next-24-bar excess return on 20:00 bars with forecast > 0",
                  "value": sup_val, "passed": sup_pass}

    if n_pos < 300:
        status = "not observable"
        decided = f"Only {n_pos} bars at 20:00 with forecast > 0, below the plan's minimum of 300."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is +2 or more and the mean excess return on forecast > 0 bars is positive."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is +2 or more but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
