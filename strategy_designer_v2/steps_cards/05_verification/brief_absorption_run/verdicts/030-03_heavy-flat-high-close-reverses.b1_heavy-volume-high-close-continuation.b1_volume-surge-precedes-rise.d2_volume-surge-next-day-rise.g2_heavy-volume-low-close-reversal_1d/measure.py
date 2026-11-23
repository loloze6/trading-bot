import numpy as np
import pandas as pd
from scipy import stats


def _ols_slope_t(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    n = len(x)
    if n < 3:
        return None, None, n
    xm = x - x.mean()
    sxx = float(np.sum(xm ** 2))
    if sxx <= 0:
        return None, None, n
    slope = float(np.sum(xm * (y - y.mean())) / sxx)
    intercept = y.mean() - slope * x.mean()
    resid = y - (intercept + slope * x)
    s2 = float(np.sum(resid ** 2) / (n - 2))
    se = np.sqrt(s2 / sxx) if s2 > 0 else 0.0
    t = float(slope / se) if se > 0 else (float(np.inf) * np.sign(slope) if slope != 0 else 0.0)
    return slope, t, n


def measure(bars):
    RAW = "debug_info.components.absorb.last_history_value"
    POST = "debug_info.components.absorb.post_pipeline_value"

    # ---------- collect per coin/window ----------
    frames = []
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp")
            d = d.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            vol = pd.to_numeric(d["volume"], errors="coerce")
            out = pd.DataFrame({
                "coin": coin,
                "window": w,
                "forecast": pd.to_numeric(d["forecast"], errors="coerce") if "forecast" in d.columns else np.nan,
                "raw": pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else np.nan,
                "post": pd.to_numeric(d[POST], errors="coerce") if POST in d.columns else np.nan,
            })
            # next-day return inside the window only
            out["ret1"] = (close.shift(-1) / close - 1.0).values
            rng = (high - low)
            cl = (high - close) / rng.where(rng > 0)
            prior_mean = vol.shift(1).rolling(20, min_periods=20).mean()
            vr = vol / prior_mean.where(prior_mean > 0)
            out["cl"] = cl.values
            out["vr"] = vr.values
            # price-based recomputation of the raw component, used only where raw is not recorded
            out["raw_price"] = (cl * vr).values
            frames.append(out)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "t of pooled slope of excess next-day return on forecast",
                             "value": None, "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"bars with forecast > 2": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    all_df = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    raw_used = all_df["raw"].where(all_df["raw"].notna(), all_df["raw_price"])
    fc = all_df["forecast"]
    active = fc.notna() & (fc != 0)
    n_active = int(active.sum())
    situation = raw_used > 0  # graded situation: close below the high with volume, product > 0
    agree = active & situation & (fc > 0)
    agreement = float(agree.sum() / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation bars are those whose recorded raw absorb value (close-location x volume ratio, recomputed "
               "from prices where not recorded) is > 0, with the expected side long; the coin's mean daily return is the "
               "mean of all its in-window next-day returns pooled over windows; the supporting check's volume ratio is "
               "recomputed inside each window from the prior 20 recorded bars (first 20 bars of each window left out), "
               "ordinary OLS slopes are used, and 'bars with forecast > 2' counts the recorded forecast column.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "t of pooled slope of excess next-day return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 (with check > 0) confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"bars with forecast > 2": int((fc > 2).sum()), "active bars": n_active},
            "decided_by": ("The plan's situation (a long on bars closing below the high, sized by close location x "
                           "volume ratio) holds on only %s of the bars with a non-zero forecast, below 90 %%."
                           % (None if agreement is None else round(agreement, 4))),
            "reading": reading,
        }

    # ---------- excess next-day return ----------
    coin_mean = all_df.groupby("coin")["ret1"].transform(lambda s: s.dropna().mean())
    all_df["exret"] = all_df["ret1"] - coin_mean

    # ---------- main measure ----------
    slope, t_slope, n_reg = _ols_slope_t(all_df["post"], all_df["exret"])

    # ---------- supporting check ----------
    hi = all_df[(all_df["vr"] >= 1)]
    lo = all_df[(all_df["vr"] < 1)]
    s_hi, _, n_hi = _ols_slope_t(hi["cl"], hi["exret"])
    s_lo, _, n_lo = _ols_slope_t(lo["cl"], lo["exret"])
    diff = (s_hi - s_lo) if (s_hi is not None and s_lo is not None) else None
    check_pass = (diff > 0) if diff is not None else None

    n_fc2 = int((fc > 2).sum())
    counts = {
        "bars with forecast > 2": n_fc2,
        "regression bars": int(n_reg),
        "heavy-volume days (ratio >= 1)": int(n_hi),
        "light-volume days (ratio < 1)": int(n_lo),
    }

    # ---------- decision ----------
    if n_fc2 < 1000:
        status = "not observable"
        decided_by = "Fewer than the plan's minimum of 1,000 bars with forecast > 2 across the coins (%d)." % n_fc2
    elif t_slope is None or not np.isfinite(t_slope) and t_slope is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed."
    elif t_slope >= 2 and check_pass is True:
        status = "confirmed"
        decided_by = "The slope t is >= 2 and the supporting check's difference is > 0."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope t is <= -2."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope t is >= 2 but the supporting check's difference is not > 0."
    else:
        status = "inconclusive"
        decided_by = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "t of pooled slope of excess next-day return on forecast (absorb post_pipeline_value)",
            "value": None if t_slope is None else float(t_slope),
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": float(t_slope)},
            "threshold": "t >= 2 (with check difference > 0) confirms, t <= -2 rejects, between is inconclusive",
        },
        "supporting_check": {
            "name": "slope on close location, volume ratio >= 1 minus ratio < 1",
            "value": None if diff is None else float(diff),
            "passed": None if check_pass is None else bool(check_pass),
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
