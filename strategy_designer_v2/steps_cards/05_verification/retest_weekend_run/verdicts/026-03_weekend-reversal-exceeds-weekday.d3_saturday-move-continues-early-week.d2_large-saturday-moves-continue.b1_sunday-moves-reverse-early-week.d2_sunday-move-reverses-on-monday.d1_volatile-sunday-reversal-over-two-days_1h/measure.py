import numpy as np
import pandas as pd


def _ols_slope(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    if n < 3:
        return None, None, n
    xm = x.mean()
    sxx = np.sum((x - xm) ** 2)
    if sxx <= 0:
        return None, None, n
    b = np.sum((x - xm) * (y - y.mean())) / sxx
    a = y.mean() - b * xm
    resid = y - a - b * x
    s2 = np.sum(resid ** 2) / (n - 2)
    se = np.sqrt(s2 / sxx)
    t = b / se if se > 0 else None
    return float(b), (float(se) if se > 0 else None), n, t


def _fit(x, y):
    r = _ols_slope(x, y)
    if len(r) == 3:
        return None, None, r[2], None
    return r


def measure(bars):
    H = 48
    VOLN = 720
    RAW = "debug_info.components.sunday_move.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            nxt = ts + pd.Timedelta(hours=1)
            is_sit = ((nxt.dt.dayofweek == 0) & (nxt.dt.hour == 0) & (nxt.dt.minute == 0)).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
            else:
                raw = np.full(len(df), np.nan)
            # fallback recomputation from prices where the raw value is missing
            r24 = pd.Series(close).pct_change(24)
            denom = r24.abs().rolling(VOLN, min_periods=VOLN).mean()
            raw_re = (r24 / denom).values
            raw = np.where(np.isnan(raw), raw_re, raw)
            active = fc != 0
            n_active += int(active.sum())
            ok = active & is_sit & (np.sign(fc) == -np.sign(raw)) & (np.sign(raw) != 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are Sunday's last hourly bar with the forecast against the sign of Sunday's scaled 24h move, as the plan's situation and side require.",
            "reading": "none",
        }

    # ---------- cases ----------
    rows = []
    for coin in bars:
        drift_samples = []
        coin_rows = []
        for w in bars[coin]:
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            n = len(close)
            for i in range(0, n - H, H):
                if close[i] > 0 and np.isfinite(close[i]) and np.isfinite(close[i + H]):
                    drift_samples.append(close[i + H] / close[i] - 1.0)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            r1 = np.full(n, np.nan)
            r1[1:] = close[1:] / close[:-1] - 1.0
            idx = np.where((reg == "mean_reversion") & (fc != 0))[0]
            for i in idx:
                if i + H >= n:
                    continue
                ret = close[i + H] / close[i] - 1.0
                if not np.isfinite(ret):
                    continue
                if i >= VOLN:
                    seg = r1[i - VOLN + 1:i + 1]
                    vol = float(np.std(seg, ddof=1)) if np.all(np.isfinite(seg)) else np.nan
                else:
                    vol = np.nan
                coin_rows.append([coin, float(fc[i]), ret, vol])
        drift = float(np.mean(drift_samples)) if drift_samples else np.nan
        for r in coin_rows:
            rows.append({"coin": r[0], "fc": r[1], "ex": (r[2] - drift) * 100.0, "vol": r[3]})

    cases = pd.DataFrame(rows, columns=["coin", "fc", "ex", "vol"]).dropna(subset=["fc", "ex"])
    b_main, se_main, n_main, t_main = _fit(cases["fc"].values, cases["ex"].values) if len(cases) else (None, None, 0, None)

    top_parts, bot_parts = [], []
    for coin, g in cases.dropna(subset=["vol"]).groupby("coin"):
        g = g.sort_values("vol", kind="mergesort")
        k = len(g) // 3
        if k > 0:
            bot_parts.append(g.iloc[:k])
            top_parts.append(g.iloc[len(g) - k:])
    top = pd.concat(top_parts) if top_parts else pd.DataFrame(columns=cases.columns)
    bot = pd.concat(bot_parts) if bot_parts else pd.DataFrame(columns=cases.columns)
    bt, set_, nt, _ = _fit(top["fc"].values, top["ex"].values)
    bb, seb, nb, _ = _fit(bot["fc"].values, bot["ex"].values)
    diff, t_diff = None, None
    if bt is not None and bb is not None and set_ is not None and seb is not None:
        diff = bt - bb
        t_diff = float(diff / np.sqrt(set_ ** 2 + seb ** 2))

    counts = {"cases across all coins": int(len(cases)),
              "cases in top volatility third": int(len(top)),
              "cases in bottom volatility third": int(len(bot))}

    main = {"name": "pooled OLS slope of excess 48-bar return (%) on forecast",
            "value": b_main,
            "statistic": {"name": "t of slope", "value": t_main} if t_main is not None else None,
            "threshold": "confirm: positive with t >= 2; reject: negative with t <= -2"}
    sup_pass = None if t_diff is None else bool(diff > 0 and t_diff >= 2)
    sup = {"name": "top-third minus bottom-third volatility slope, Welch t",
           "value": diff, "passed": sup_pass, "welch_t": t_diff}

    reading = ("Situation = bar starting Sunday 23:00 UTC with forecast sign opposite to the raw scaled Sunday move; "
               "drift = coin's mean of non-overlapping 48-bar returns on each window's grid; volatility = std of the 720 "
               "one-bar returns ending at the entry close (cases with fewer bars in the window left out of the split); "
               "thirds = lowest and highest floor(n/3) cases per coin by volatility, pooled across coins; slopes by OLS "
               "with intercept, difference t = diff / sqrt(se_top^2 + se_bottom^2); too few cases gives 'not observable'.")

    if len(cases) < 300 or len(top) < 100 or len(bot) < 100:
        status = "not observable"
        decided = "A minimum count is not reached: at least 300 cases across all coins and 100 in each volatility third are required."
    elif t_main is None or t_diff is None:
        status = "inconclusive"
        decided = "A slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif (b_main < 0 and t_main <= -2) or (diff < 0 and t_diff <= -2):
        status = "rejected"
        decided = ("Reject rule: the main slope is negative with t <= -2" if (b_main < 0 and t_main <= -2)
                   else "Reject rule: the top-minus-bottom volatility slope difference is negative with t <= -2") + "."
    elif b_main > 0 and t_main >= 2 and diff > 0 and t_diff >= 2:
        status = "confirmed"
        decided = "Confirm rule: the main slope is positive with t >= 2 and the volatility slope difference is positive with t >= 2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the numbers meet neither the confirm nor the reject rule (t values between -2 and 2 or a failed supporting check)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
