import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            reg = df["regime"].astype(str).values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            # 5-day return from prices inside the window (fallback where raw value is missing)
            r5 = np.full(len(df), np.nan)
            if len(df) > 5:
                r5[5:] = close[5:] / close[:-5] - 1.0
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                choppy = reg[i] == "unknown"
                if np.isfinite(raw[i]):
                    rise = raw[i] > 0
                elif np.isfinite(r5[i]):
                    rise = r5[i] > 0
                else:
                    rise = False
                if choppy and rise and fc[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess 3-bar forward return on cases (forecast > 0, non-overlapping 3-bar grid)"
    threshold = "confirm: mean > 0 with day-pooled t >= 2 and top-minus-bottom > 0; reject: mean < 0 with t <= -2"
    reading = ("Choppy profile taken as the bars whose regime is 'unknown' (neither 60-bar trend veto fired), "
               "the 5-day rise as raw scaled_rise > 0 (price 5-day return where missing); top half = cases with "
               "forecast above the cases' median, bottom half = at or below it; the day-pooled t sums the cases' "
               "deviations from the mean per UTC day; the plan's 'fewer than 100 cases or 60 days' is applied as "
               "'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars (forecast != 0) are long bars in the choppy profile "
                           "while the 5-day return is positive, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                coin_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    coin_cases.append((r, float(fc[i]), ts.iloc[i].floor("D")))
        if not coin_rets:
            continue
        mu = float(np.mean(coin_rets))
        for r, f, d in coin_cases:
            rows.append({"coin": coin, "excess": r - mu, "forecast": f, "day": d})

    cases = pd.DataFrame(rows, columns=["coin", "excess", "forecast", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_ex = float(cases["excess"].mean()) if n_cases else None
    t = None
    if n_cases > 0 and n_days > 1:
        dev = cases["excess"] - mean_ex
        s = dev.groupby(cases["day"]).sum().values
        var = (n_days / (n_days - 1.0)) * np.sum(s ** 2) / (n_cases ** 2)
        if var > 0:
            t = float(mean_ex / np.sqrt(var))

    diff = None
    sup_pass = None
    if n_cases > 1:
        med = cases["forecast"].median()
        top = cases.loc[cases["forecast"] > med, "excess"]
        bot = cases.loc[cases["forecast"] <= med, "excess"]
        if len(top) > 0 and len(bot) > 0:
            diff = float(top.mean() - bot.mean())
            sup_pass = bool(diff > 0)

    main = {"name": main_name, "value": mean_ex,
            "statistic": ({"name": "t of the mean, cases of a day pooled", "value": t} if t is not None else None),
            "threshold": threshold}
    support = {"name": "mean excess of top-half forecast cases minus bottom half",
               "value": diff, "passed": sup_pass}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (need 100) on {n_days} distinct days (need 60).")
    elif t is None:
        status = "inconclusive"
        decided = "The day-pooled t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean excess return positive with t >= 2 and top-minus-bottom half > 0 (confirm rule)."
    elif mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess return negative with t <= -2 (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "Main t >= 2 but the top-minus-bottom difference is not above 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "Main t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
