import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    P = "debug_info.components."
    col_f = "forecast"
    mom_raw, mom_post = P + "mom28.last_history_value", P + "mom28.post_pipeline_value"
    hi_raw, hi_post = P + "high90.last_history_value", P + "high90.post_pipeline_value"
    off_post = P + "offset.post_pipeline_value"

    # ---------- 1. situation check ----------
    # Situation: equal-weight score of 28-day momentum and nearness to the 90-day high (+10 offset).
    # Expected side: long when the score is positive, short when negative.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df[col_f], errors="coerce")
            needed = [mom_raw, mom_post, hi_raw, hi_post]
            if not all(c in df.columns for c in needed):
                act = f.notna() & (f != 0)
                n_active += int(act.sum())
                continue
            mr = pd.to_numeric(df[mom_raw], errors="coerce")
            mp = pd.to_numeric(df[mom_post], errors="coerce")
            hr = pd.to_numeric(df[hi_raw], errors="coerce")
            hp = pd.to_numeric(df[hi_post], errors="coerce")
            if off_post in df.columns:
                op = pd.to_numeric(df[off_post], errors="coerce")
            else:
                op = pd.Series(10.0, index=df.index)
            # standardise scales without centring: the post value keeps the raw value's sign
            mom_ok = (np.sign(mp) == np.sign(mr)) | (mp == 0)
            hi_ok = (hr <= 1e-12) & (hp <= 1e-12)
            score = (mp + hp + op) / 3.0
            act = f.notna() & (f != 0)
            n_active += int(act.sum())
            agree = act & mom_ok & hi_ok & score.notna() & (np.sign(score) == np.sign(f))
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars have a forecast whose sign equals the sign of the "
                          "equal-weight momentum + nearness-to-high + offset score rebuilt from the components.",
            "reading": "The score is rebuilt from the recorded values after transforms, checked against the raw values' signs.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df[col_f], errors="coerce").to_numpy(dtype=float)
            for t in range(0, len(df) - H, H):
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                coin_rets.append(r)
                coin_rows.append((f[t], r))
        if not coin_rets:
            continue
        drift = float(np.mean(coin_rets))
        for fv, r in coin_rows:
            rows.append((coin, fv, r - drift))

    d = pd.DataFrame(rows, columns=["coin", "f", "x"])
    d = d[d["f"].notna() & (d["f"] != 0) & d["x"].notna()]
    n = int(len(d))
    counts = {"non-overlapping grid cases with a non-zero forecast": n}

    reading = ("The slope, its t and the fifths use the non-overlapping 5-bar grid bars (positions 0,5,10,... of each "
               "window) with a non-zero forecast, pooled; the drift is the coin's mean 5-bar grid return over all its "
               "windows; the fifths are the n//5 lowest and highest forecasts after sorting; the slope's t is the "
               "OLS t with an intercept.")

    main_name = "OLS slope of drift-removed 5-bar forward return on forecast"
    thr = "t >= 2 confirms (with top-minus-bottom fifth > 0); t <= -2 rejects"

    if n < 300:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": "top-minus-bottom fifth drift-removed 5-bar return", "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 300 non-overlapping grid cases with a non-zero forecast.",
            "reading": reading,
        }

    xf = d["f"].to_numpy(dtype=float)
    y = d["x"].to_numpy(dtype=float)
    lr = stats.linregress(xf, y)
    slope = float(lr.slope)
    t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else 0.0

    order = np.argsort(xf, kind="mergesort")
    k = n // 5
    bottom = y[order[:k]]
    top = y[order[-k:]]
    diff = float(np.mean(top) - np.mean(bottom))
    sup_pass = bool(diff > 0)
    counts["top fifth cases"] = int(k)
    counts["bottom fifth cases"] = int(k)

    if t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-minus-bottom-fifth difference is positive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-minus-bottom-fifth difference is 0 or less."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "OLS slope t", "value": t_slope},
                         "threshold": thr},
        "supporting_check": {"name": "top-minus-bottom fifth drift-removed 5-bar return",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
