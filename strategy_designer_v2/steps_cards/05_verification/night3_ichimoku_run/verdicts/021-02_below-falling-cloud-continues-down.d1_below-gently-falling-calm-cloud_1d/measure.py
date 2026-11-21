import numpy as np
import pandas as pd


def measure(bars):
    H = 26
    MIN_CASES = 30
    FC = "forecast"
    SLOPE_COL = "debug_info.components.cloud_fall.last_history_value"

    def ichimoku_situation(df):
        """Return (pos_below, slope_neg) as arrays of True/False/NaN (NaN = not computable)."""
        high = df["high"].astype(float)
        low = df["low"].astype(float)
        close = df["close"].astype(float)
        tenkan = (high.rolling(9, min_periods=9).max() + low.rolling(9, min_periods=9).min()) / 2.0
        kijun = (high.rolling(26, min_periods=26).max() + low.rolling(26, min_periods=26).min()) / 2.0
        span_a_raw = (tenkan + kijun) / 2.0
        span_b_raw = (high.rolling(52, min_periods=52).max() + low.rolling(52, min_periods=52).min()) / 2.0
        span_a = span_a_raw.shift(26)
        span_b = span_b_raw.shift(26)
        bottom = np.minimum(span_a, span_b)
        mid = (span_a + span_b) / 2.0
        pos_below = pd.Series(np.where(bottom.notna(), (close < bottom).astype(float), np.nan), index=df.index)
        slope = mid - mid.shift(26)
        slope_neg = pd.Series(np.where(slope.notna(), (slope < 0).astype(float), np.nan), index=df.index)
        return pos_below, slope_neg

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True) if "timestamp" in df.columns else df.reset_index(drop=True)
            f = pd.to_numeric(df[FC], errors="coerce")
            pos_c, slope_c = ichimoku_situation(df)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            if SLOPE_COL in df.columns:
                slope_raw = pd.to_numeric(df[SLOPE_COL], errors="coerce")
            else:
                slope_raw = pd.Series(np.nan, index=df.index)
            for i in range(len(df)):
                fi = f.iloc[i]
                if pd.isna(fi) or fi == 0:
                    continue
                n_active += 1
                # slope: recorded raw value of the slope component, else recomputed, else regime
                if not pd.isna(slope_raw.iloc[i]):
                    s_ok = slope_raw.iloc[i] < 0
                elif not pd.isna(slope_c.iloc[i]):
                    s_ok = bool(slope_c.iloc[i])
                else:
                    s_ok = regime.iloc[i] == "trending"
                # position: recomputed from prices, else the detector's regime
                if not pd.isna(pos_c.iloc[i]):
                    p_ok = bool(pos_c.iloc[i])
                else:
                    p_ok = regime.iloc[i] == "trending"
                if s_ok and p_ok and fi < 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "|forecast|-weighted mean drift-adjusted 26-bar short gain"
    threshold = "confirm: mean > 0 with t >= 2 on >= 30 cases and check passes; reject: mean < 0 with t <= -2 on >= 30 cases"
    reading = ("Situation = close below the lower edge of the 9/26/52/26 cloud (recomputed from the window's prices, "
               "the detector's 'trending' regime where too few bars exist) and the cloud_fall raw slope < 0, side short; "
               "drift = each coin's mean non-overlapping 26-bar return over all its windows; the t of the weighted mean "
               "uses the weighted standard error sqrt(sum w^2 (x-m)^2)/sum w; the larger half is |forecast| above the "
               "median, the smaller half at or below it.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars where the close is below "
                           "the falling cloud, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rets_all = {}
    cells = []  # (coin, ret, forecast)
    for coin, wins in bars.items():
        rets_all.setdefault(coin, [])
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True) if "timestamp" in df.columns else df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df[FC], errors="coerce").values
            for t in range(0, len(df), H):
                if t + H >= len(df):
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                rets_all[coin].append(r)
                if np.isfinite(f[t]) and f[t] < 0:
                    cells.append((coin, r, float(f[t])))
    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in rets_all.items()}

    adj = np.array([r - drift[c] for c, r, _ in cells], dtype=float)
    wts = np.array([abs(fv) for _, _, fv in cells], dtype=float)
    ok = np.isfinite(adj) & np.isfinite(wts) & (wts > 0)
    adj, wts = adj[ok], wts[ok]
    gains = -adj
    n = int(len(gains))

    mean_gain, tstat = None, None
    if n >= 2 and wts.sum() > 0:
        m = float(np.sum(wts * gains) / np.sum(wts))
        se = float(np.sqrt(np.sum(wts ** 2 * (gains - m) ** 2)) / np.sum(wts))
        mean_gain = m
        tstat = float(m / se) if se > 0 else None
    elif n == 1:
        mean_gain = float(gains[0])

    diff, check_pass = None, None
    n_large = n_small = 0
    if n >= 2:
        med = float(np.median(wts))
        large = wts > med
        small = ~large
        n_large, n_small = int(large.sum()), int(small.sum())
        if n_large > 0 and n_small > 0:
            diff = float(np.mean(adj[large]) - np.mean(adj[small]))
            check_pass = bool(diff < 0)

    counts = {"cases": n, "active bars": int(n_active),
              "larger half": n_large, "smaller half": n_small}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} independent cases with a negative forecast, fewer than the plan's minimum of 30."
    elif mean_gain is not None and tstat is not None and mean_gain > 0 and tstat >= 2:
        if check_pass:
            status = "confirmed"
            decided = "Weighted mean short gain > 0 with t >= 2 on at least 30 cases, and the larger-|forecast| half returned less than the smaller half."
        else:
            status = "inconclusive"
            decided = "A confirming t (mean > 0, t >= 2) but the supporting check failed, which the plan calls inconclusive."
    elif mean_gain is not None and tstat is not None and mean_gain < 0 and tstat <= -2:
        status = "rejected"
        decided = "Weighted mean short gain < 0 with t <= -2 on at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the weighted mean short gain lies between -2 and 2 on at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_gain,
                         "statistic": ({"name": "t of the weighted mean", "value": tstat} if tstat is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean drift-adjusted return, larger minus smaller |forecast| half (< 0)",
                             "value": diff, "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
