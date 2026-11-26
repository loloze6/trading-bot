import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.low_close_wide_range.last_history_value"
    POS = "postRebalance_current_allocation"

    # ---------- gather rows per coin, per window (never joined across windows) ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            d["ret_next"] = close.shift(-1) / close - 1.0  # inside the window only
            d["coin"] = coin
            d["window"] = w
            if RAW not in d.columns:
                d[RAW] = np.nan
            rows.append(d)
    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "drift-adjusted next-day return x position", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"position days": 0, "distinct days": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }
    all_df = pd.concat(rows, ignore_index=True)
    for c in ["forecast", POS, "high", "low", "close", RAW, "ret_next"]:
        all_df[c] = pd.to_numeric(all_df[c], errors="coerce")
    all_df["day"] = all_df["timestamp"].dt.floor("D")

    # ---------- situation check ----------
    # Situation: inside the agitated profile (regime 'unknown', the regime holding the strategy, i.e. not the
    # 'chop' veto), with the close sitting below the day's high (raw (high-close)/mean range > 0); side: long.
    regime = all_df["regime"].astype(str).str.lower()
    agitated = regime == "unknown"
    raw = all_df[RAW]
    raw_pos = np.where(raw.notna(), raw > 0, all_df["high"] > all_df["close"])
    raw_pos = pd.Series(raw_pos, index=all_df.index).astype(bool)
    active = all_df["forecast"].fillna(0) != 0
    n_active = int(active.sum())
    if n_active > 0:
        ok = active & agitated & raw_pos & (all_df["forecast"] > 0)
        agreement = float(ok.sum()) / n_active
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    threshold_txt = ("confirm: t >= 2 with supporting check > 0; reject: t <= -2; "
                     "otherwise inconclusive; minimum 300 position days on 150 distinct days")
    main_name = "mean of (next-day return - coin mean daily return) x position held, on non-zero positions"
    reading = ("Agitated profile read as regime 'unknown' (the non-chop regime carrying the strategy) and the "
               "situation as a raw value above 0 there, long; positions are postRebalance_current_allocation != 0 "
               "with a next-day return in the same window, every bar counted (1-bar horizon), the t uses per-day "
               "sums of the products across coins, the coin mean is over all its windows' daily returns, and the "
               "thirds are floor(n/3) lowest and highest non-zero forecasts pooled over all coins; fewer cases than "
               "the plan's minimums is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"position days": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the agitated "
                           "profile with a close below the day's high, as the Fidelity requires."
                           if n_active > 0 else "No bar has a non-zero forecast."),
            "reading": reading,
        }

    # ---------- coin drift: mean daily return over all windows ----------
    mu = all_df.groupby("coin")["ret_next"].mean()
    all_df["adj"] = all_df["ret_next"] - all_df["coin"].map(mu)

    # ---------- main measure ----------
    pos_mask = (all_df[POS].fillna(0) != 0) & all_df["adj"].notna()
    m = all_df.loc[pos_mask].copy()
    m["gain"] = m["adj"] * m[POS]
    n_cases = int(len(m))
    n_days = int(m["day"].nunique()) if n_cases else 0
    mean_val = float(m["gain"].mean()) if n_cases else None

    day_sums = m.groupby("day")["gain"].sum() if n_cases else pd.Series(dtype=float)
    t_val = None
    if len(day_sums) >= 2:
        sd = float(day_sums.std(ddof=1))
        if sd > 0:
            t_val = float(day_sums.mean() / (sd / np.sqrt(len(day_sums))))

    # ---------- supporting check ----------
    f = all_df.loc[(all_df["forecast"].fillna(0) != 0) & all_df["adj"].notna(), ["forecast", "adj"]]
    f = f.sort_values("forecast", kind="mergesort")
    k = len(f) // 3
    sup_val = None
    if k >= 1:
        sup_val = float(f["adj"].iloc[-k:].mean() - f["adj"].iloc[:k].mean())
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    counts = {"position days": n_cases, "distinct days": n_days}
    statistic = {"name": "t of the mean (cases of one day summed)", "value": t_val} if t_val is not None else None
    supporting = {"name": "top third minus bottom third of non-zero forecasts, drift-adjusted next-day return",
                  "value": sup_val, "passed": sup_pass}

    if n_cases < 300 or n_days < 150:
        status = "not observable"
        decided = (f"The plan's minimum of 300 position days on 150 distinct days is not reached "
                   f"({n_cases} position days on {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed (no variation), so neither rule is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure's t is 2 or more and the supporting check is above 0 (confirm rule)."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less (reject rule)."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The main measure's t is 2 or more but the supporting check is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The main measure's t is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_val, "statistic": statistic, "threshold": threshold_txt},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
