import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    PROFILE_REGIME = "unknown"   # the only regime with a strategy; the vetoes send everything else to "chop"
    CL_RAW = "debug_info.components.close_loc.last_history_value"
    CL_PP = "debug_info.components.close_loc.post_pipeline_value"
    STD_WINDOW, STD_MINP = 60, 20
    MIN_DAYS = 100

    def close_loc_from_prices(df):
        rng = (df["high"] - df["low"]).astype(float)
        x = (df["high"] - df["close"]).astype(float) / rng
        return x.where(rng > 0)  # 0 at the high, 1 at the low; undefined on a zero range

    def standardise_in_window(raw):
        # value(t) * 10 / mean(|raw| over the last `window` values, t excluded), capped to -20..+20.
        # Only trusted once a full window of past values exists inside the window (warm-up is not recorded).
        past_abs = raw.abs().shift(1)
        denom = past_abs.rolling(STD_WINDOW, min_periods=STD_WINDOW).mean()
        z = (raw * 10.0 / denom).clip(-20, 20)
        z[(denom == 0)] = 0.0
        return z

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    # mean daily return per coin over all windows
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp")
            c = df["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        coin_mu[coin] = float(np.mean(np.concatenate(rets))) if rets else np.nan

    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = df["forecast"].astype(float)
            in_profile = df["regime"].astype(str) == PROFILE_REGIME

            raw = close_loc_from_prices(df)
            z = standardise_in_window(raw)
            if CL_PP in df.columns:
                z = z.where(z.notna(), df[CL_PP].astype(float))
            near_low = z > 10.0  # nearer the low than its usual level

            active = fc.notna() & (fc != 0)
            situation_long = in_profile & near_low & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situation_long).sum())

            # ---------- main measure rows ----------
            c = df["close"].astype(float)
            r_next = c.shift(-1) / c - 1.0
            sel = in_profile & active & r_next.notna()
            if sel.any():
                ts = pd.to_datetime(df.loc[sel, "timestamp"], utc=True)
                contrib = (fc[sel] / 10.0) * (r_next[sel] - coin_mu[coin])
                rows.append(pd.DataFrame({"day": ts.dt.floor("D").values,
                                          "v": contrib.values}))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean over days of the daily sum of (forecast/10) x (next-day return minus coin mean daily return), in-profile nonzero-forecast bars"
    threshold = "confirm: mean > 0 with t >= 2 over at least 100 days; reject: mean < 0 with t <= -2 over at least 100 days"
    reading = ("The profile is read from the recorded regime (the only regime with a strategy, 'unknown', is the falling-agitated profile, the detector's components being unrecorded); "
               "the situation is close location (high-close)/(high-low) standardised above 10 recomputed in-window when 60 past bars exist (else the recorded post_pipeline value), on the long side; "
               "days are UTC calendar days of the bar timestamps, the coin mean is over all its bars' next-day returns across windows, and the plan's 100-day minimum is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of nonzero-forecast bars are in-profile bars with the close nearer the low than usual and a long forecast"
                           if n_active > 0 else "No bar with a nonzero forecast, so the config never takes the plan's position."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    if rows:
        allrows = pd.concat(rows, ignore_index=True)
        daily = allrows.groupby("day")["v"].sum()
    else:
        daily = pd.Series(dtype=float)
    n_days = int(len(daily))
    mean = float(daily.mean()) if n_days > 0 else None
    if n_days > 1:
        sd = float(daily.std(ddof=1))
        t = float(mean / (sd / np.sqrt(n_days))) if sd > 0 else None
    else:
        t = None

    counts = {"in-profile days with a nonzero forecast": n_days}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided_by = f"Only {n_days} in-profile days with a nonzero forecast, below the plan's minimum of 100."
    elif t is not None and mean > 0 and t >= 2:
        status = "confirmed"
        decided_by = "The mean is above 0 with t >= 2 over at least 100 days (no supporting check in the plan)."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided_by = "The mean is below 0 with t <= -2 over at least 100 days."
    else:
        status = "inconclusive"
        decided_by = "The t lies between -2 and +2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
