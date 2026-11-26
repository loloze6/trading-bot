import numpy as np
import pandas as pd


def measure(bars):
    RET_COL = "debug_info.components.ret14.last_history_value"
    H = 2

    def _prep(df):
        df = df.copy().reset_index(drop=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
        return df

    def _std14(close):
        raw = close / close.shift(14) - 1.0
        out = pd.Series(np.nan, index=close.index)
        vals = raw.values
        for i in range(len(vals)):
            if np.isnan(vals[i]):
                continue
            past = vals[max(0, i - 60):i]
            past = past[~np.isnan(past)]
            if len(past) < 20:
                out.iloc[i] = 0.0
                continue
            m = np.mean(np.abs(past))
            out.iloc[i] = 0.0 if m == 0 else float(np.clip(vals[i] * 10.0 / m, -20, 20))
        return raw, out

    def _ols(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        n = len(x)
        if n < 3 or np.var(x) == 0:
            return None, None, n
        xm, ym = x.mean(), y.mean()
        sxx = np.sum((x - xm) ** 2)
        b = np.sum((x - xm) * (y - ym)) / sxx
        a = ym - b * xm
        res = y - a - b * x
        s2 = np.sum(res ** 2) / (n - 2)
        se = np.sqrt(s2 / sxx)
        return float(b), float(se), n

    # ---- coin mean 2-bar return over all windows (non-overlapping grid) ----
    prepared = {}
    mu2 = {}
    for coin, wins in bars.items():
        rets = []
        prepared[coin] = {}
        for w, df in wins.items():
            d = _prep(df)
            prepared[coin][w] = d
            c = d["close"].values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        mu2[coin] = float(np.mean(rets)) if rets else np.nan

    # ---- situation check + collection ----
    n_active = 0
    n_agree = 0
    cases = []  # (date, gain)
    hi_x, hi_y, lo_x, lo_y = [], [], [], []

    for coin, wins in prepared.items():
        for w, d in wins.items():
            close = d["close"]
            r = close.pct_change()
            vol = r.rolling(20, min_periods=20).std()
            volr = vol / vol.rolling(60, min_periods=60).mean()
            raw14, std14 = _std14(close)
            next_wd = (d["timestamp"] + pd.Timedelta(days=1)).dt.dayofweek
            is_fri = (next_wd == 5).values
            regime = d["regime"].astype(str).values if "regime" in d else np.array([""] * len(d))
            raw_rec = pd.to_numeric(d[RET_COL], errors="coerce") if RET_COL in d else pd.Series(np.nan, index=d.index)
            fc = d["forecast"].values
            c = close.values
            n = len(d)
            for i in range(n):
                f = fc[i]
                if f != 0:
                    n_active += 1
                    vr = volr.iloc[i]
                    vol_ok = (vr > 1.0) if np.isfinite(vr) else (regime[i] == "trending")
                    rv = raw_rec.iloc[i]
                    if not np.isfinite(rv):
                        rv = raw14.iloc[i]
                    side_ok = np.isfinite(rv) and rv != 0 and np.sign(rv) == np.sign(f)
                    if is_fri[i] and vol_ok and side_ok:
                        n_agree += 1
                if not is_fri[i] or i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                ex = c[i + H] / c[i] - 1.0 - mu2[coin]
                if not np.isfinite(ex):
                    continue
                hi = regime[i] == "trending"
                if hi and f != 0:
                    cases.append((d["timestamp"].iloc[i].normalize(), (f / 10.0) * ex))
                sx = std14.iloc[i]
                if np.isfinite(sx):
                    if hi:
                        hi_x.append(sx); hi_y.append(ex)
                    else:
                        lo_x.append(sx); lo_y.append(ex)

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    sit = {"agreement": agreement, "passed": bool(passed)}

    main_name = "t of the mean per-Friday summed gain (forecast/10 x excess 2-bar return)"
    main_thr = "confirm if t >= 2 over >= 100 distinct Fridays; reject if t <= -2"
    reading = ("Friday bars are those whose next bar starts on Saturday (UTC); high-volatility Fridays are read "
               "from the recorded regime 'trending'; the situation check recomputes the 20/60 volatility ratio "
               "from window closes and falls back to the recorded regime where the window is too short; the "
               "coin's mean 2-bar return uses a non-overlapping grid over all its windows; slopes are pooled "
               "OLS over coins and their Welch t is (b_high - b_other)/sqrt(se_high^2 + se_other^2).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": ("Fewer than 90% of nonzero-forecast bars are high-volatility Friday bars with the "
                           "forecast in the 14-day return's direction, as the Fidelity's situation requires."),
            "reading": reading,
        }

    # ---- main measure ----
    if cases:
        cdf = pd.DataFrame(cases, columns=["day", "g"])
        daily = cdf.groupby("day")["g"].sum()
        n_days = int(len(daily))
        mean_g = float(daily.mean())
        sd = float(daily.std(ddof=1)) if n_days > 1 else np.nan
        t_main = float(mean_g / (sd / np.sqrt(n_days))) if n_days > 1 and sd > 0 else None
    else:
        n_days, mean_g, t_main = 0, None, None

    # ---- supporting check ----
    b_hi, se_hi, n_hi = _ols(hi_x, hi_y)
    b_lo, se_lo, n_lo = _ols(lo_x, lo_y)
    if b_hi is not None and b_lo is not None:
        diff = b_hi - b_lo
        den = np.sqrt(se_hi ** 2 + se_lo ** 2)
        t_diff = float(diff / den) if den > 0 else None
    else:
        diff, t_diff = None, None
    sup_pass = None if diff is None else bool(diff > 0)

    counts = {"distinct Fridays with cases": n_days,
              "cases": int(len(cases)),
              "high-volatility Fridays in slope": int(n_hi),
              "other Fridays in slope": int(n_lo)}

    if n_days < 100:
        status = "not observable"
        decided = f"Only {n_days} distinct Fridays with cases, below the plan's minimum of 100."
    elif (t_main is not None and t_main <= -2) or (t_diff is not None and t_diff <= -2):
        status = "rejected"
        decided = ("Reject: over at least 100 distinct Fridays, the main t is at most -2 or the slope "
                   "difference has a t of at most -2.")
    elif t_main is not None and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: main t at least 2 over at least 100 distinct Fridays and slope difference above 0."
    else:
        status = "inconclusive"
        if t_main is not None and t_main >= 2:
            decided = ("Inconclusive: main t of 2 or more but the slope difference is at or below 0 "
                       "with a t above -2.")
        else:
            decided = "Inconclusive: main t strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {"name": main_name,
                         "value": mean_g,
                         "statistic": None if t_main is None else {"name": "t of the mean over days", "value": t_main},
                         "threshold": main_thr},
        "supporting_check": {"name": "high-vol minus other-Fridays slope of excess weekend return on standardised 14-day return"
                                     + ("" if t_diff is None else f" (Welch t {t_diff:.3f})"),
                             "value": diff,
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
