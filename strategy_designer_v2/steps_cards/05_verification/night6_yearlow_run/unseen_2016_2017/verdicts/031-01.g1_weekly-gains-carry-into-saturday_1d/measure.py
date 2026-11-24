import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.week_ret.last_history_value"
    rows = []
    for coin, wins in bars.items():
        # coin's mean daily return over all windows together (returns stay inside a window)
        all_r = []
        prepared = []
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            d["ret1"] = close.shift(-1) / close - 1.0
            # 5-bar raw value: recorded where present, else recomputed from prices in the window
            rec = d[RAW].astype(float) if RAW in d.columns else pd.Series(np.nan, index=d.index)
            recomputed = close / close.shift(5) - 1.0
            d["raw5"] = rec.where(rec.notna(), recomputed)
            d["coin"] = coin
            d["window"] = w
            all_r.append(d["ret1"].dropna().values)
            prepared.append(d)
        r = np.concatenate(all_r) if all_r else np.array([])
        mu = float(np.mean(r)) if len(r) else np.nan
        for d in prepared:
            d["excess"] = d["ret1"] - mu
            rows.append(d)

    reading = ("The coming bar is the bar opening at timestamp + 1 day, so the situation is a Friday-UTC bar with a "
               "positive 5-bar return (recorded raw value, else recomputed in-window), expected long; Friday bars for "
               "the supporting check are those same bars; the top third is above the 2/3 quantile of positive Friday "
               "forecasts pooled over coins; the day-clustered t sums deviations per UTC date with a D/(D-1) correction; "
               "distinct days with a positive forecast count UTC dates of any bar with forecast > 0.")

    if not rows:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": {"name": "mean forecast/10 x next-bar excess return", "value": None,
                                 "statistic": None, "threshold": "above 0 with t >= 2"},
                "supporting_check": None,
                "counts": {"distinct days with a positive forecast": 0},
                "decided_by": "No bars in the record.", "reading": reading}

    a = pd.concat(rows, ignore_index=True)
    a["forecast"] = a["forecast"].astype(float)
    coming = a["timestamp"] + pd.Timedelta(days=1)
    a["is_fri"] = coming.dt.weekday == 5  # coming bar is Saturday (UTC)
    a["day"] = a["timestamp"].dt.floor("D")

    # ---- situation check
    active = a["forecast"].fillna(0) != 0
    n_active = int(active.sum())
    ok = active & a["is_fri"] & (a["raw5"] > 0) & (a["forecast"] > 0)
    agreement = float(ok.sum() / n_active) if n_active else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": agreement, "passed": False},
                "main_measure": {"name": "mean forecast/10 x next-bar excess return", "value": None,
                                 "statistic": None, "threshold": "above 0 with t >= 2"},
                "supporting_check": None,
                "counts": {"active bars": n_active},
                "decided_by": (f"Only {agreement:.1%} of active bars are long on Friday-UTC bars (coming bar Saturday) "
                               "after a positive 5-bar return, below 90%."),
                "reading": reading}

    # ---- main measure
    m = a[(a["regime"] == "trending") & (a["forecast"] > 0) & a["excess"].notna()].copy()
    m["x"] = m["forecast"] / 10.0 * m["excess"]
    N = len(m)
    mean = float(m["x"].mean()) if N else np.nan
    tstat = np.nan
    n_days_cases = int(m["day"].nunique()) if N else 0
    if N > 1 and n_days_cases > 1:
        dev = m["x"] - mean
        S = dev.groupby(m["day"]).sum().values
        D = len(S)
        var = (D / (D - 1)) * np.sum(S ** 2) / N ** 2
        se = np.sqrt(var)
        tstat = float(mean / se) if se > 0 else np.nan

    # ---- supporting check
    fri = a[a["is_fri"] & a["excess"].notna() & a["forecast"].notna()]
    pos = fri[fri["forecast"] > 0]
    zero = fri[fri["forecast"] == 0]
    sup_val = None
    sup_pass = None
    n_top = 0
    if len(pos) > 0 and len(zero) > 0:
        cut = pos["forecast"].quantile(2.0 / 3.0)
        top = pos[pos["forecast"] > cut]
        if len(top) == 0:
            top = pos[pos["forecast"] >= cut]
        n_top = len(top)
        sup_val = float(top["excess"].mean() - zero["excess"].mean())
        sup_pass = bool(sup_val > 0)

    n_pos_days = int(a.loc[a["forecast"] > 0, "day"].nunique())
    counts = {"distinct days with a positive forecast": n_pos_days,
              "main measure cases": int(N),
              "days of main measure cases": n_days_cases,
              "top-third Friday bars": int(n_top),
              "zero-forecast Friday bars": int(len(zero))}

    mm = {"name": "mean of forecast/10 x (next-bar return - coin mean daily return), trending bars with forecast > 0",
          "value": None if np.isnan(mean) else mean,
          "statistic": None if np.isnan(tstat) else {"name": "t of the mean, cases of one day summed", "value": tstat},
          "threshold": "confirm: above 0 with t >= 2 (and supporting check positive); reject: below 0 with t <= -2"}
    sc = {"name": "Saturday excess return, top third of positive Friday forecasts minus Friday forecast 0",
          "value": sup_val, "passed": sup_pass}

    if n_pos_days < 300:
        status = "not observable"
        decided = f"Only {n_pos_days} distinct days with a positive forecast, below the plan's minimum of 300."
    elif np.isnan(tstat) or np.isnan(mean):
        status = "inconclusive"
        decided = "The main measure's t could not be computed, which meets neither the confirm nor the reject rule."
    elif mean > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The main measure is above 0 with t >= 2 and the supporting check is positive."
        else:
            status = "inconclusive"
            decided = "The main measure is above 0 with t >= 2 but the supporting check failed, which the plan calls inconclusive."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The main measure is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2, which the plan calls inconclusive."

    return {"status": status,
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": mm,
            "supporting_check": sc,
            "counts": counts,
            "decided_by": decided,
            "reading": reading}
