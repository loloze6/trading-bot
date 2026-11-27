import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30

    def comp_value(df, cid, field="last_history_value"):
        col = f"debug_info.components.{cid}.{field}"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        out = np.full(len(df), np.nan)
        if "debug_info.components" in df.columns:
            for i, v in enumerate(df["debug_info.components"].to_numpy()):
                d = v
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(cid)
                    if isinstance(c, dict) and c.get(field) is not None:
                        try:
                            out[i] = float(c.get(field))
                        except Exception:
                            pass
        return out

    n_active = 0
    n_agree = 0
    cases = []  # dicts: coin, day, ret, absf

    for coin, wins in bars.items():
        drift_samples = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            high = pd.to_numeric(df["high"], errors="coerce").to_numpy(dtype=float)
            low = pd.to_numeric(df["low"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.floor("D").astype(str).to_numpy()
            n = len(df)
            raw_cf = comp_value(df, "calm_fall")

            # ---- situation check ----
            for t in range(n):
                if fc[t] == 0:
                    continue
                n_active += 1
                ok = regime[t] == "mean_reversion"
                # close in upper half of the day's range
                rng = high[t] - low[t]
                if np.isfinite(rng) and rng > 0:
                    loc = (close[t] - low[t]) / rng
                    if not loc > 0.5:
                        ok = False
                # 5-day return below 0
                if t >= 5 and np.isfinite(close[t - 5]) and close[t - 5] > 0:
                    if not (close[t] / close[t - 5] - 1.0) < 0:
                        ok = False
                elif np.isfinite(raw_cf[t]):
                    if not raw_cf[t] < 0:
                        ok = False
                # 60-day return within +-10 %
                if t >= 60 and np.isfinite(close[t - 60]) and close[t - 60] > 0:
                    r60 = (close[t] / close[t - 60] - 1.0) * 100.0
                    if not (-10.0 <= r60 <= 10.0):
                        ok = False
                # expected side: short
                if not fc[t] < 0:
                    ok = False
                if ok:
                    n_agree += 1

            # ---- drift samples: non-overlapping grid ----
            for t in range(0, n - H, H):
                if np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0:
                    drift_samples.append(close[t + H] / close[t] - 1.0)

            # ---- bets on the short side ----
            bet = np.zeros(n, dtype=bool)
            lowm = 0.0
            prev_short = False
            for t in range(n):
                f = fc[t]
                if f < 0:
                    m = -f
                    if not prev_short:
                        lowm = 0.0
                    if m - lowm >= BAND:
                        bet[t] = True
                        lowm = m
                    else:
                        lowm = min(lowm, m)
                    prev_short = True
                else:
                    prev_short = False
                    lowm = 0.0

            # ---- one case per 5-bar grid cell ----
            for start in range(0, n, H):
                idx = [t for t in range(start, min(start + H, n)) if bet[t]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                coin_cases.append({"day": days[t], "ret": close[t + H] / close[t] - 1.0,
                                   "absf": abs(fc[t])})
        if coin_cases:
            drift = float(np.mean(drift_samples)) if drift_samples else np.nan
            for c in coin_cases:
                if np.isfinite(drift):
                    c["x"] = -(c["ret"] - drift)
                    cases.append(c)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = (agreement is not None and agreement >= 0.9)

    main_name = "mean short-direction unusual 5-bar move (minus (5-bar return - coin's normal 5-bar drift))"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    reading = ("Situation bars are those the engine labelled mean_reversion, with the close-location, 5-day-return "
               "and 60-day-return conditions re-checked from prices where the window's bars allow (the 365-day "
               "swing percentile cannot be rebuilt inside a window, so the regime label stands for it); a case is "
               "the first short bet in each 5-bar grid cell of a window with its 5-bar return from that bet's close; "
               "the top half of the split is |forecast| strictly above the median; the plan's 'fewer than 30 cases' "
               "rule is applied as 'not observable' per the workflow.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": int(len(cases)), "active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars inside the plan's "
                           "regime (60-day return within +-10 %, high 30-day swing, close in upper half, "
                           "negative 5-day return)."),
            "reading": reading,
        }

    N = len(cases)
    days_set = sorted(set(c["day"] for c in cases))
    D = len(days_set)
    counts = {"cases": int(N), "days": int(D)}
    sc_agree = {"agreement": (float(agreement) if agreement is not None else None), "passed": bool(passed)}

    if N < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": sc_agree,
            "main_measure": {"name": main_name,
                             "value": (float(np.mean([c["x"] for c in cases])) if N else None),
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"The plan needs at least {MIN_CASES} cases; only {N} were found.",
            "reading": reading,
        }

    x = np.array([c["x"] for c in cases], dtype=float)
    mean = float(np.mean(x))
    dev = x - mean
    day_arr = np.array([c["day"] for c in cases])
    sums = pd.Series(dev).groupby(day_arr).sum().to_numpy()
    t_stat = None
    if D > 1:
        var = np.sum(sums ** 2) * D / (D - 1)
        se = np.sqrt(var) / N
        if se > 0:
            t_stat = float(mean / se)

    absf = np.array([c["absf"] for c in cases], dtype=float)
    med = float(np.median(absf))
    top = x[absf > med]
    bot = x[absf <= med]
    if len(top) > 0 and len(bot) > 0:
        diff = float(np.mean(top) - np.mean(bot))
        sup_pass = bool(diff >= 0)
    else:
        diff = None
        sup_pass = False

    if t_stat is not None and mean > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and the top |forecast| half at least the bottom half: confirm rule."
    elif t_stat is not None and mean < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: reject rule."
    elif t_stat is not None and mean > 0 and t_stat >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "Confirming t but the supporting check failed: inconclusive rule."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (or not computable): inconclusive rule."

    return {
        "status": status,
        "situation_check": sc_agree,
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean, cases of the same day taken together",
                                        "value": t_stat} if t_stat is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual move, top half minus bottom half at median |forecast|",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
