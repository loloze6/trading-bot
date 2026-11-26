import numpy as np
import pandas as pd


def measure(bars):
    CL_RAW = "debug_info.components.close_loc.last_history_value"
    CL_POST = "debug_info.components.close_loc.post_pipeline_value"

    sit_rows = []
    sample_rows = []
    book_rows = []

    # Each coin's mean daily return, taken over all its windows together (never across two windows).
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        allr = np.concatenate(rets) if rets else np.array([])
        allr = allr[np.isfinite(allr)]
        coin_mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            day = ts.dt.floor("D")
            h = df["high"].astype(float).values
            l = df["low"].astype(float).values
            c = df["close"].astype(float).values
            rng = h - l
            with np.errstate(divide="ignore", invalid="ignore"):
                raw = np.where(rng > 0, (h - c) / rng, np.nan)
            if CL_RAW in df.columns:
                rec = df[CL_RAW].astype(float).values
                raw = np.where(np.isfinite(rec), rec, raw)

            # Rebuild standardise(60, 20) from the raw values: x * 10 / mean|past 60|, bar t left out, cap +-20.
            # Use the rebuild where 60 past bars exist inside the window; else the recorded post-pipeline value.
            s = pd.Series(raw)
            past_mean = s.abs().shift(1).rolling(60, min_periods=60).mean().values
            with np.errstate(divide="ignore", invalid="ignore"):
                std_rebuilt = np.clip(raw * 10.0 / past_mean, -20, 20)
            post = df[CL_POST].astype(float).values if CL_POST in df.columns else np.full(len(df), np.nan)
            std_val = np.where(np.isfinite(std_rebuilt) & np.isfinite(past_mean) & (past_mean > 0),
                               std_rebuilt, post)
            # Close lower in its range than usual (standardised value above the -10 offset's +10) -> long.
            exp_side = np.sign(std_val - 10.0)
            exp_side = np.where(np.isfinite(exp_side), exp_side, 0.0)

            regime = df["regime"].astype(str).values
            agitated = regime != "chop"
            fc = df["forecast"].astype(float).values
            alloc = df["postRebalance_current_allocation"].astype(float).values

            nxt = np.full(len(df), np.nan)
            if len(df) > 1:
                nxt[:-1] = c[1:] / c[:-1] - 1.0

            for i in range(len(df)):
                if np.isfinite(fc[i]) and fc[i] != 0:
                    ok = bool(agitated[i] and exp_side[i] != 0 and np.sign(fc[i]) == exp_side[i])
                    sit_rows.append(ok)
                    if np.isfinite(nxt[i]) and np.isfinite(mu):
                        sample_rows.append((day.iloc[i], fc[i], nxt[i] - mu))
                if np.isfinite(nxt[i]) and np.isfinite(alloc[i]) and np.isfinite(mu):
                    book_rows.append((day.iloc[i], coin, alloc[i] * nxt[i], alloc[i] * mu))

    n_active = len(sit_rows)
    agreement = float(np.mean(sit_rows)) if n_active else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "pooled OLS slope of next-day excess return on forecast"
    threshold = "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects"
    reading = ("The agitated situation is every bar whose regime is not 'chop'; the expected side is long when "
               "the standardised close location (rebuilt from raw values with 60 past bars inside the window, else the "
               "recorded post-pipeline value) exceeds 10; the slope's t uses day-clustered standard errors with a "
               "G/(G-1) correction; the book's daily return before costs is the position after each bar's trade times "
               "the next-day return, averaged over the coins each day; and the minimum counts are applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with a non-zero forecast": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are agitated bars on the side the "
                           "Fidelity expects (long when the close sits lower in its range than usual, short when higher)."),
            "reading": reading,
        }

    sm = pd.DataFrame(sample_rows, columns=["day", "f", "r"])
    n_bars = int(len(sm))
    n_days = int(sm["day"].nunique()) if n_bars else 0

    slope, tval = None, None
    if n_bars >= 3:
        f = sm["f"].values
        r = sm["r"].values
        fbar = f.mean()
        fd = f - fbar
        sxx = float(np.sum(fd ** 2))
        if sxx > 0:
            b = float(np.sum(fd * (r - r.mean())) / sxx)
            a = r.mean() - b * fbar
            e = r - a - b * f
            sc = pd.Series(fd * e).groupby(sm["day"].values).sum().values
            G = len(sc)
            var_b = float(np.sum(sc ** 2)) / sxx ** 2
            if G > 1:
                var_b *= G / (G - 1.0)
            slope = b
            tval = float(b / np.sqrt(var_b)) if var_b > 0 else None

    bk = pd.DataFrame(book_rows, columns=["day", "coin", "gain", "mkt"])
    timing = None
    if len(bk):
        daily = bk.groupby("day")[["gain", "mkt"]].mean()
        timing = float(daily["gain"].mean() - daily["mkt"].mean())
    sup_pass = None if timing is None else bool(timing > 0)

    counts = {"bars with a non-zero forecast": n_bars, "distinct days": n_days}

    if n_bars < 300 or n_days < 150:
        status = "not observable"
        decided_by = (f"The minimum count is not reached: {n_bars} bars with a non-zero forecast (300 needed) "
                      f"on {n_days} distinct days (150 needed).")
    elif slope is None or tval is None:
        status = "inconclusive"
        decided_by = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided_by = "The slope is positive with t >= 2 and the timing part is above 0."
        else:
            status = "inconclusive"
            decided_by = "The slope is positive with t >= 2 but the timing part is at or below 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided_by = "The slope is negative with t <= -2: the next day rises more after higher closes."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tval is None else {"name": "day-clustered t of the slope", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book mean daily return before costs minus market-rise part (timing)",
            "value": timing,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
