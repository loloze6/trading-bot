import numpy as np
import pandas as pd


def _ols_slope_t(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    if n < 3:
        return None, None, n
    xm = x.mean()
    ym = y.mean()
    sxx = np.sum((x - xm) ** 2)
    if sxx <= 0:
        return None, None, n
    slope = np.sum((x - xm) * (y - ym)) / sxx
    intercept = ym - slope * xm
    resid = y - intercept - slope * x
    s2 = np.sum(resid ** 2) / (n - 2)
    se = np.sqrt(s2 / sxx) if s2 > 0 else np.nan
    t = slope / se if se and np.isfinite(se) and se > 0 else None
    return float(slope), (float(t) if t is not None else None), n


def measure(bars):
    RAW = "debug_info.components.fade_1h.last_history_value"
    POST = "debug_info.components.fade_1h.post_pipeline_value"

    frames = []
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        coin_rets = []
        parts = []
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            ret_prev = close / close.shift(1) - 1.0          # last hour's return, inside window
            ret_next = close.shift(-1) / close - 1.0          # next hour's return, inside window
            vol24 = ret_prev.rolling(24, min_periods=24).std()
            vol_mean720 = vol24.rolling(720, min_periods=720).mean()
            high = pd.Series(np.where(vol24.notna() & vol_mean720.notna(),
                                      (vol24 >= vol_mean720).astype(float), np.nan))
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            post = pd.to_numeric(df[POST], errors="coerce") if POST in df.columns else pd.Series(np.nan, index=df.index)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            coin_rets.append(ret_prev.dropna().values)
            parts.append(pd.DataFrame({
                "coin": coin, "window": w,
                "raw": raw.values, "post": post.values, "forecast": fc.values,
                "ret_prev": ret_prev.values, "ret_next": ret_next.values,
                "high": high.values,
            }))
        if not parts:
            continue
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        mu = float(np.mean(allr)) if len(allr) else np.nan
        cdf = pd.concat(parts, ignore_index=True)
        cdf["excess_next"] = cdf["ret_next"] - mu
        frames.append(cdf)

    if not frames:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": {"name": "pooled slope of next-hour excess return on fade_1h forecast",
                                 "value": None, "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
                "supporting_check": None,
                "counts": {"bars in total": 0, "bars with high 24h volatility": 0, "bars with low 24h volatility": 0},
                "decided_by": "No bars in the record.",
                "reading": "none"}
    d = pd.concat(frames, ignore_index=True)

    # ---- situation check: forecast must fade last hour's move ----
    active = d[d["forecast"].notna() & (d["forecast"] != 0)]
    move = active["raw"].where(active["raw"].notna(), active["ret_prev"])
    expected = -np.sign(move)
    ok = (expected != 0) & move.notna() & (np.sign(active["forecast"]) == expected)
    n_active = len(active)
    agreement = float(ok.sum() / n_active) if n_active > 0 else None
    passed_sit = agreement is not None and agreement >= 0.9

    reading = ("The situation is any bar with a non-zero last-hour move (raw fade_1h value, or the close-to-close "
               "return where it is missing) and the expected side is opposite to that move; the regression uses every "
               "bar with a recorded post_pipeline_value and a next-hour return inside its window (zero forecasts "
               "included), and the volatility groups use the 24-bar standard deviation of hourly returns against its "
               "full 720-bar rolling mean computed inside each window, bars without that mean left out of the groups.")

    if not passed_sit:
        return {"status": "mismatch",
                "situation_check": {"agreement": agreement, "passed": False},
                "main_measure": {"name": "pooled slope of next-hour excess return on fade_1h forecast",
                                 "value": None, "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
                "supporting_check": None,
                "counts": {"active bars": int(n_active)},
                "decided_by": ("Fewer than 90% of active bars have a forecast opposite in sign to last hour's move, "
                               "as the plan's fade situation requires."),
                "reading": reading}

    # ---- main measure ----
    m = d[d["post"].notna() & d["excess_next"].notna()]
    slope, t, n_total = _ols_slope_t(m["post"].values, m["excess_next"].values)

    # ---- supporting check ----
    g = m[m["high"].notna()]
    hi = g[g["high"] == 1.0]
    lo = g[g["high"] == 0.0]
    s_hi, _, n_hi = _ols_slope_t(hi["post"].values, hi["excess_next"].values)
    s_lo, _, n_lo = _ols_slope_t(lo["post"].values, lo["excess_next"].values)
    diff = (s_hi - s_lo) if (s_hi is not None and s_lo is not None) else None
    sup_pass = (diff > 0) if diff is not None else None

    counts = {"bars in total": int(n_total),
              "bars with high 24h volatility": int(len(hi)),
              "bars with low 24h volatility": int(len(lo))}

    main = {"name": "pooled slope of next-hour excess return on fade_1h forecast",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": "t >= 2 with supporting check passing confirms; t <= -2 rejects; otherwise inconclusive"}
    sup = {"name": "slope on high-vol bars minus slope on low-vol bars",
           "value": diff, "passed": (bool(sup_pass) if sup_pass is not None else None)}

    if n_total < 5000 or len(hi) < 1000 or len(lo) < 1000:
        status = "not observable"
        decided = "A minimum count is not reached: at least 5000 bars in total and 1000 in each volatility group."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so it meets neither the confirm nor the reject rule."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the high-vol slope exceeds the low-vol slope."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {"status": status,
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main,
            "supporting_check": sup,
            "counts": counts,
            "decided_by": decided,
            "reading": reading}
