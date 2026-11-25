import numpy as np
import pandas as pd

RAW = "debug_info.components.scaled_rise.last_history_value"
H = 5
BAND = 2.0


def _prep(df):
    df = df.sort_values("timestamp").reset_index(drop=True).copy()
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
    if RAW in df.columns:
        df["_raw"] = pd.to_numeric(df[RAW], errors="coerce")
    else:
        df["_raw"] = np.nan
    c = df["close"].values
    n = len(df)
    fwd = np.full(n, np.nan)
    prior = np.full(n, np.nan)
    if n > H:
        fwd[: n - H] = c[H:] / c[: n - H] - 1.0
    if n > 3:
        prior[3:] = c[3:] / c[:-3] - 1.0
    df["_fwd"] = fwd
    df["_prior3"] = prior
    # raw sign: recorded raw value, else the 3-day return from prices (same sign)
    df["_rawsign"] = df["_raw"].where(df["_raw"].notna(), df["_prior3"])
    return df


def _short_bets(forecast):
    """Bars where the short-side forecast deepens by >= BAND from its lowest
    size on that side since the last bet (reset to 0 after flat / other side)."""
    bets = np.zeros(len(forecast), dtype=bool)
    ref = 0.0
    for i, f in enumerate(forecast):
        m = -f if f < 0 else 0.0
        if m <= 0:
            ref = 0.0
            continue
        if m - ref >= BAND - 1e-12:
            bets[i] = True
            ref = m
        else:
            ref = min(ref, m)
    return bets


def _clustered_t(values, days):
    values = np.asarray(values, dtype=float)
    n = len(values)
    if n < 2:
        return None
    m = values.mean()
    dev = pd.Series(values - m).groupby(np.asarray(days)).sum().values
    D = len(dev)
    if D < 2:
        return None
    var_sum = (D / (D - 1.0)) * np.sum(dev ** 2)
    se = np.sqrt(var_sum) / n
    if se <= 0 or not np.isfinite(se):
        return None
    return float(m / se)


def measure(bars):
    prepped = {}
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            prepped[(coin, w)] = _prep(df)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for (coin, w), df in prepped.items():
        act = df["forecast"] != 0
        n_active += int(act.sum())
        in_profile = df["regime"].astype(str) == "unknown"
        rise = df["_rawsign"] > 0
        short = df["forecast"] < 0
        n_agree += int((act & in_profile & rise & short).sum())

    reading_sit = ("the falling agitated profile is read as the detector's regime 'unknown' "
                   "(both chop vetoes off), since its 60- and 365-bar inputs cannot be rebuilt from the recorded windows")
    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean short-direction unusual 5-day move of the cases",
                             "value": None, "statistic": None,
                             "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2"},
            "supporting_check": None,
            "counts": {"active bars": 0, "cases": 0, "distinct days carrying cases": 0},
            "decided_by": "no active bar in the record, so neither the situation nor the criterion can be read",
            "reading": reading_sit,
        }
    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": (f"only {agreement:.1%} of active bars are short bars after a 3-day rise inside the "
                           "falling agitated profile, below the 90 % the plan's Fidelity requires"),
            "reading": reading_sit,
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean of non-overlapping 5-day returns over all its windows
    drift = {}
    for coin in sorted(bars):
        rets = []
        for (c, w), df in prepped.items():
            if c != coin:
                continue
            r = df["_fwd"].values[::H]
            rets.extend([x for x in r if np.isfinite(x)])
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []
    for (coin, w), df in prepped.items():
        bets = _short_bets(df["forecast"].values)
        cell = np.arange(len(df)) // H
        seen = set()
        for i in np.where(bets)[0]:
            if cell[i] in seen:
                continue
            seen.add(cell[i])
            fwd = df["_fwd"].iat[i]
            d = drift.get(coin, np.nan)
            if not (np.isfinite(fwd) and np.isfinite(d)):
                continue
            adj = fwd - d
            ts = pd.to_datetime(df["timestamp"].iat[i], utc=True)
            cases.append({
                "coin": coin, "window": w,
                "day": ts.strftime("%Y-%m-%d"),
                "move": -adj,
                "adj": adj,
                "raw": df["_raw"].iat[i],
                "prior3": df["_prior3"].iat[i],
            })

    cdf = pd.DataFrame(cases, columns=["coin", "window", "day", "move", "adj", "raw", "prior3"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_move = float(cdf["move"].mean()) if n_cases else None
    t = _clustered_t(cdf["move"].values, cdf["day"].values) if n_cases else None

    # supporting check
    sup_val = None
    sup_pass = None
    n_top = n_bot = 0
    s = cdf.dropna(subset=["raw", "prior3"])
    s = s[s["prior3"] > 0]
    if len(s) >= 2:
        s = s.assign(share=-s["adj"] / s["prior3"])
        med = s["raw"].median()
        top = s[s["raw"] > med]
        bot = s[s["raw"] <= med]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top > 0 and n_bot > 0:
            sup_val = float(top["share"].mean() - bot["share"].mean())
            sup_pass = bool(sup_val > 0)

    counts = {"distinct days carrying cases": n_days, "cases": n_cases,
              "supporting top half cases": n_top, "supporting bottom half cases": n_bot}

    if n_days < 30:
        status = "not observable"
        decided = f"fewer than 30 distinct days carry cases ({n_days}), the plan's minimum count"
    elif t is None or mean_move is None:
        status = "inconclusive"
        decided = "the t of the mean move could not be computed, so neither confirm nor reject is met"
    elif mean_move > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("mean short-direction unusual move above 0 with t >= 2 and a larger give-back share "
                       "in the top half of scaled rises")
        else:
            status = "inconclusive"
            decided = "the main measure meets the confirm rule but the supporting check fails"
    elif mean_move < 0 and t <= -2:
        status = "rejected"
        decided = "mean short-direction unusual move below 0 with t <= -2: the scaled rises go on rising"
    else:
        status = "inconclusive"
        decided = "the t of the mean short-direction unusual move lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean short-direction unusual 5-day move of the cases",
            "value": mean_move,
            "statistic": ({"name": "t of the mean, cases of one day summed", "value": float(t)}
                          if t is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "give-back share, top minus bottom half of raw scaled rise",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": (reading_sit + "; a case is the first short bet (forecast deepening >= 2 points from its lowest "
                    "short level since the last bet) in each 5-bar cell counted from each window's first row; the t "
                    "uses a day-clustered standard error with a D/(D-1) factor; the supporting split puts raw values "
                    "above the median in the top half and the rest in the bottom, leaving out cases whose prior "
                    "3-day return is not a rise; the plan's 'fewer than 30 distinct days' is taken as its minimum "
                    "count, hence 'not observable'."),
    }
