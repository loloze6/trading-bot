import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"

    def _raw_from_prices(close):
        r = close / close.shift(1) - 1.0
        sd = r.rolling(60, min_periods=60).std(ddof=1)
        return r / sd

    # ---------- collect per-bar rows ----------
    frames = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float).reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").reset_index(drop=True)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").reset_index(drop=True)
            else:
                raw = pd.Series(np.nan, index=close.index)
            # recompute only where the component is not recorded
            rec = _raw_from_prices(close)
            raw = raw.where(raw.notna(), rec)
            nxt = close.shift(-1) / close - 1.0  # inside the window only
            coin_rows.append(pd.DataFrame({
                "coin": coin,
                "window": w,
                "day": ts.dt.floor("D").reset_index(drop=True),
                "forecast": fc,
                "raw": raw,
                "ret_next": nxt,
            }))
        if not coin_rows:
            continue
        cdf = pd.concat(coin_rows, ignore_index=True)
        # coin's mean daily return over all its windows together
        cdf["drift"] = cdf["ret_next"].mean(skipna=True)
        frames.append(cdf)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean of (forecast/10) x next-day excess return",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2.0 confirms, t <= -2.0 rejects"},
            "supporting_check": None,
            "counts": {"distinct days with forecast > 0": 0},
            "decided_by": "No bars in the record: fewer than 300 distinct days with forecast > 0.",
            "reading": "none",
        }

    all_df = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    active = all_df[all_df["forecast"].notna() & (all_df["forecast"] != 0)]
    n_active = len(active)
    if n_active > 0:
        ok = (active["raw"] < 0) & (active["forecast"] > 0)
        agreement = float(ok.mean())
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("Situation = recorded raw scaled return < 0 (down day) with long side (forecast > 0); "
               "main t = mean over its standard error with case deviations summed per calendar day "
               "(K/(K-1) correction), all bars with a next-day return counted (zero forecasts add 0); "
               "thirds of forecast > 0 bars by forecast rank (ties broken by order), "
               "top = rank > 2n/3, bottom = rank <= n/3; minimum = distinct UTC days with any forecast > 0, "
               "and below it the status is 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean of (forecast/10) x next-day excess return",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2.0 confirms, t <= -2.0 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Only {:.1%} of bars with a non-zero forecast are down days (raw scaled return < 0) "
                           "held long, below the 90% the plan's situation requires.").format(agreement),
            "reading": reading,
        }

    # ---------- minimum count ----------
    pos = all_df[all_df["forecast"] > 0]
    n_days_pos = int(pos["day"].nunique())

    # ---------- main measure ----------
    m = all_df[all_df["forecast"].notna() & all_df["ret_next"].notna()].copy()
    m["excess"] = m["ret_next"] - m["drift"]
    m["x"] = (m["forecast"] / 10.0) * m["excess"]
    n_cases = len(m)
    main_value = float(m["x"].mean()) if n_cases > 0 else None
    t_main = None
    n_days_main = int(m["day"].nunique()) if n_cases > 0 else 0
    if n_cases > 1:
        dev = m["x"] - main_value
        D = dev.groupby(m["day"]).sum().values
        K = len(D)
        if K > 1:
            var_sum = float(np.sum(D ** 2)) * K / (K - 1)
            se = np.sqrt(var_sum) / n_cases
            t_main = float(main_value / se) if se > 0 else None

    # ---------- supporting check ----------
    s = m[m["forecast"] > 0].copy()
    sup_value = None
    sup_pass = None
    top_mean = bot_mean = None
    n_s = len(s)
    if n_s >= 3:
        s = s.reset_index(drop=True)
        rk = s["forecast"].rank(method="first")
        top = s.loc[rk > 2.0 * n_s / 3.0, "excess"]
        bot = s.loc[rk <= n_s / 3.0, "excess"]
        if len(top) > 0 and len(bot) > 0:
            top_mean = float(top.mean())
            bot_mean = float(bot.mean())
            sup_value = top_mean - bot_mean
            sup_pass = bool(sup_value > 0)

    counts = {
        "distinct days with forecast > 0": n_days_pos,
        "cases in main measure": int(n_cases),
        "days in main measure": n_days_main,
        "bars with forecast > 0 and next-day return": int(n_s),
    }

    main = {
        "name": "mean of (forecast/10) x (next-day return minus coin mean daily return)",
        "value": main_value,
        "statistic": ({"name": "t of the mean, cases summed per day", "value": t_main}
                      if t_main is not None else None),
        "threshold": "t >= 2.0 (with top third above bottom third) confirms; t <= -2.0 rejects",
    }
    sup = {
        "name": "top-third minus bottom-third mean excess next-day return (forecast > 0)",
        "value": sup_value,
        "passed": sup_pass,
    }

    if n_days_pos < 300:
        status = "not observable"
        decided = ("Only {} distinct days with forecast > 0, below the plan's minimum of 300."
                   .format(n_days_pos))
    elif t_main is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_main >= 2.0 and sup_pass is True:
        status = "confirmed"
        decided = ("The main measure has t = {:.2f} >= 2.0 and the top third's mean excess return "
                   "is above the bottom third's.").format(t_main)
    elif t_main <= -2.0:
        status = "rejected"
        decided = "The main measure has t = {:.2f} <= -2.0.".format(t_main)
    elif t_main >= 2.0:
        status = "inconclusive"
        decided = ("The main measure has t = {:.2f} >= 2.0 but the top third's mean excess return "
                   "is not above the bottom third's.").format(t_main)
    else:
        status = "inconclusive"
        decided = "The main measure's t = {:.2f} lies between -2.0 and 2.0.".format(t_main)

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
