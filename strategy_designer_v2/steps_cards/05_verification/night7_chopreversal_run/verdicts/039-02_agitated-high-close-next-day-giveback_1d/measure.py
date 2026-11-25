import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.close_loc.last_history_value"
    POST = "debug_info.components.close_loc.post_pipeline_value"

    def _num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        return np.full(len(df), np.nan)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = _num(df, FC)
            hi = _num(df, "high")
            lo = _num(df, "low")
            cl = _num(df, "close")
            raw = _num(df, RAW)
            post = _num(df, POST)
            reg = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                x_price = np.where(rng > 0, (hi - cl) / rng, np.nan)
            # rebuild of the usual level from in-window raw values, when post is missing
            raw_s = pd.Series(raw)
            mean_abs_past = raw_s.abs().shift(1).rolling(60, min_periods=20).mean().to_numpy()
            for i in range(len(df)):
                if not np.isfinite(f[i]) or f[i] == 0:
                    continue
                n_active += 1
                # situation: the agitated profile (detector not in "chop")
                in_profile = reg[i] == "unknown"
                # close location measured as stated: 0 at the high, 1 at the low
                if not np.isfinite(raw[i]):
                    orient_ok = False
                elif np.isfinite(x_price[i]):
                    orient_ok = abs(raw[i] - x_price[i]) < 1e-4
                else:
                    orient_ok = True
                # expected side: long when close lower in range than usual, short when higher
                if np.isfinite(post[i]):
                    d = post[i] - 10.0
                elif np.isfinite(raw[i]) and np.isfinite(mean_abs_past[i]) and mean_abs_past[i] > 0:
                    d = min(max(raw[i] * 10.0 / mean_abs_past[i], -20.0), 20.0) - 10.0
                else:
                    d = np.nan
                if not np.isfinite(d) or d == 0:
                    side_ok = False
                else:
                    side_ok = np.sign(d) == np.sign(f[i])
                if in_profile and orient_ok and side_ok:
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of next-day return minus coin mean daily return on forecast"
    threshold = "confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are agitated-profile bars "
                           "with the forecast short when the close is higher in its range than usual and long "
                           "when lower (close location 0 at the high)."),
            "reading": "The agitated profile is read as regime 'unknown' (not 'chop'); the expected side is the sign of the standardised close location minus 10.",
        }

    # ---------- 2. criterion ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = _num(df.sort_values("timestamp"), "close")
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    F, Y, D = [], [], []
    for coin, wins in bars.items():
        mu = coin_mean.get(coin, np.nan)
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = _num(df, FC)
            c = _num(df, "close")
            reg = df["regime"].astype(str).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.floor("D").astype("int64").to_numpy()
            for i in range(len(df) - 1):
                if reg[i] != "unknown" or not np.isfinite(f[i]) or f[i] == 0:
                    continue
                r = c[i + 1] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                F.append(f[i]); Y.append(r - mu); D.append(days[i])

    F = np.asarray(F, float); Y = np.asarray(Y, float); D = np.asarray(D)
    n = int(len(F))
    n_days = int(len(np.unique(D))) if n else 0
    counts = {"bars in the profile": n, "distinct days": n_days}

    slope = None
    tval = None
    if n >= 3:
        fm = F - F.mean()
        sxx = float(np.sum(fm ** 2))
        if sxx > 0:
            b = float(np.sum(fm * (Y - Y.mean())) / sxx)
            a = float(Y.mean() - b * F.mean())
            e = Y - a - b * F
            s = pd.Series(fm * e).groupby(D).sum().to_numpy()
            G = len(s)
            if G > 1:
                corr = (G / (G - 1.0)) * ((n - 1.0) / (n - 2.0))
                var = corr * float(np.sum(s ** 2)) / sxx ** 2
                if var > 0:
                    tval = float(b / np.sqrt(var))
            slope = b

    stat = {"name": "slope t, day-clustered", "value": tval} if tval is not None else None
    main = {"name": main_name, "value": slope, "statistic": stat, "threshold": threshold}
    reading = ("The agitated profile is read as regime 'unknown' (not 'chop'); the slope is an OLS slope with "
               "intercept on all profile bars with a non-zero forecast and a next bar in the same window, its t "
               "day-clustered (CR1); the plan's minimums (500 bars, 250 days) are applied as 'not observable'.")

    if n < 500 or n_days < 250:
        status = "not observable"
        decided = (f"Minimum count not reached: {n} bars in the profile (need 500) and "
                   f"{n_days} distinct days (need 250).")
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2: the higher the close, the larger the next-day fall."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: a high close is followed by a stronger next day."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
