import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.close_loc.last_history_value"
    MIN_ACTIVE = 500

    def raw_location(df):
        hi = df["high"].astype(float).values
        lo = df["low"].astype(float).values
        cl = df["close"].astype(float).values
        rng = hi - lo
        with np.errstate(divide="ignore", invalid="ignore"):
            from_prices = np.where(rng > 0, (hi - cl) / rng, np.nan)
        if RAW in df.columns:
            rec = pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
            return np.where(np.isfinite(rec), rec, from_prices)
        return from_prices

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp")
            raw = raw_location(df)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            s = pd.Series(np.abs(raw))
            # past mean size of the raw value, bar t left out, last 60 values, at least 20
            past = s.shift(1).rolling(60, min_periods=20).mean().values
            centre = np.where(np.isfinite(past) & (past > 0), past, 0.5)
            expected = np.sign(raw - centre)  # close lower in range than usual -> long (+1)
            for i in range(len(df)):
                if not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                n_active += 1
                if np.isfinite(expected[i]) and expected[i] != 0 and np.sign(fc[i]) == expected[i]:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The situation 'close lower in the range' is read as the raw location (high-close)/(high-low) above its "
               "mean over the last 60 recorded bars of the window (bar left out, at least 20; mid-range 0.5 before that), "
               "the expected side long there and short below; the slope is an OLS with intercept on every bar with a "
               "next-day return in its window (zero forecasts included), the minimum count is the non-zero-forecast bars "
               "of that sample, and the book's day is the mean over coins of each bar's position gain minus drift.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"bars with a non-zero forecast": int(n_active)},
            "decided_by": ("Only {:.1%} of the active bars have a forecast sign matching the plan's side (long when the "
                           "close is low in the day's range, short when high), below the 90 % required.").format(agreement),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin mean daily return over all windows
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            df = df.sort_values("timestamp")
            c = df["close"].astype(float).values
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        coin_mu[coin] = float(np.mean(np.concatenate(rets))) if rets and sum(len(x) for x in rets) > 0 else np.nan

    xs, ys = [], []
    timing_rows = []
    for coin, wins in bars.items():
        mu = coin_mu.get(coin, np.nan)
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            df = df.sort_values("timestamp")
            c = df["close"].astype(float).values
            fwd = np.full(len(c), np.nan)
            fwd[:-1] = c[1:] / c[:-1] - 1.0
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").values.astype(float)
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").values
            ok = np.isfinite(fwd) & np.isfinite(fc)
            xs.append(fc[ok])
            ys.append(fwd[ok] - mu)
            okp = np.isfinite(fwd) & np.isfinite(pos)
            for i in np.where(okp)[0]:
                timing_rows.append((ts[i], pos[i] * fwd[i] - pos[i] * mu))

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n = len(x)
    n_nonzero = int(np.sum(x != 0)) if n else 0

    slope = None
    tstat = None
    if n >= 3 and np.var(x) > 0:
        xm, ym = x.mean(), y.mean()
        sxx = np.sum((x - xm) ** 2)
        b = np.sum((x - xm) * (y - ym)) / sxx
        a = ym - b * xm
        resid = y - a - b * x
        s2 = np.sum(resid ** 2) / (n - 2)
        se = np.sqrt(s2 / sxx)
        slope = float(b)
        tstat = float(b / se) if se > 0 else None

    timing = None
    if timing_rows:
        tdf = pd.DataFrame(timing_rows, columns=["day", "g"])
        daily = tdf.groupby("day")["g"].mean()
        timing = float(daily.mean()) if len(daily) else None
    timing_pass = None if timing is None else bool(timing > 0)

    counts = {"bars with a non-zero forecast": n_nonzero, "bars in the regression": int(n)}
    main = {
        "name": "pooled OLS slope of next-day return minus coin mean on forecast",
        "value": slope,
        "statistic": {"name": "OLS t of the slope", "value": tstat} if tstat is not None else None,
        "threshold": "confirm: slope > 0 with t >= 2 and timing gain > 0; reject: slope < 0 with t <= -2",
    }
    support = {"name": "mean daily timing gain (position gain minus drift)", "value": timing, "passed": timing_pass}

    if n_nonzero < MIN_ACTIVE:
        status = "not observable"
        decided = "Fewer than 500 bars with a non-zero forecast ({}), the plan's minimum.".format(n_nonzero)
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        if timing_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the timing gain is above 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the timing gain is not above 0 (inconclusive rule)."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope has |t| < 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
