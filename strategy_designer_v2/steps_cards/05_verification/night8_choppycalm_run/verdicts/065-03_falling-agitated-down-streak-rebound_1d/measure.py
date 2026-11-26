import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.down_streak.last_history_value"
    rows = []        # (coin, day, forecast, next_ret)
    coin_rets = {}   # coin -> list of all in-window 1-bar returns
    active_total = 0
    active_ok = 0

    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).astype(float)
            nxt = close.shift(-1) / close - 1.0
            rets_all.extend(nxt.dropna().tolist())

            # Situation check: profile (regime "unknown" = the regime with a strategy,
            # i.e. both vetoes off: falling and agitated), on a down-close streak, long side.
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            in_profile = regime.str.lower().eq("unknown")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            price_down = close < close.shift(1)
            streak_on = raw.gt(0) | (raw.isna() & price_down)
            active = fc != 0
            ok = active & in_profile & streak_on & (fc > 0)
            active_total += int(active.sum())
            active_ok += int(ok.sum())

            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D")
            sel = (fc > 0) & nxt.notna() & day.notna()
            for i in np.where(sel.values)[0]:
                rows.append((coin, day.iloc[i], fc.iloc[i], nxt.iloc[i]))
        coin_rets[coin] = float(np.mean(rets_all)) if rets_all else np.nan

    agreement = (active_ok / active_total) if active_total > 0 else 0.0
    passed = active_total > 0 and agreement >= 0.9
    situation = {"agreement": float(agreement), "passed": bool(passed)}

    main_name = "slope of next-day excess return on forecast, bars with forecast > 0"
    threshold = "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"
    reading = ("The profile is read from the recorded regime ('unknown' = both vetoes off, the falling agitated profile) "
               "and the streak from the raw down_streak value (> 0, price down-close if missing); the slope's t uses "
               "day-clustered errors (x-deviation times residual summed per day); the 100-day minimum counts distinct "
               "UTC days of bars with forecast > 0 and a next-day return, and below it the status is 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "active bars in situation on long side": int(active_ok)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars inside the falling agitated "
                           "profile on a down-close streak, as the Fidelity requires."),
            "reading": reading,
        }

    df = pd.DataFrame(rows, columns=["coin", "day", "x", "r"])
    if len(df):
        df["mu"] = df["coin"].map(coin_rets)
        df["y"] = df["r"] - df["mu"]
        df = df.dropna(subset=["x", "y"])
    n_days = int(df["day"].nunique()) if len(df) else 0
    n_bars = int(len(df))
    counts = {"distinct days with forecast > 0": n_days, "bars with forecast > 0": n_bars}

    slope = None
    tval = None
    support_val = None
    support_pass = None
    if n_bars >= 3:
        x = df["x"].values.astype(float)
        y = df["y"].values.astype(float)
        xd = x - x.mean()
        sxx = float(np.sum(xd ** 2))
        support_val = float(np.mean(y))
        support_pass = bool(support_val > 0)
        if sxx > 0:
            b = float(np.sum(xd * (y - y.mean())) / sxx)
            a = float(y.mean() - b * x.mean())
            e = y - a - b * x
            score = pd.Series(xd * e).groupby(df["day"].values).sum().values
            var_b = float(np.sum(score ** 2)) / sxx ** 2
            slope = b
            tval = float(b / np.sqrt(var_b)) if var_b > 0 else None

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "t (deviations summed per day)", "value": tval} if tval is not None else None),
            "threshold": threshold}
    supp = {"name": "mean next-day return minus coin mean, forecast > 0", "value": support_val,
            "passed": support_pass}

    if n_days < 100:
        status = "not observable"
        decided = f"The plan's minimum of 100 distinct days with forecast > 0 is not reached ({n_days})."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed (no variation in the forecast), so no rule is met."
    elif slope > 0 and tval >= 2 and support_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the supporting check passes (confirm rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    elif tval >= 2 and not support_pass:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "|t| < 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": situation,
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
