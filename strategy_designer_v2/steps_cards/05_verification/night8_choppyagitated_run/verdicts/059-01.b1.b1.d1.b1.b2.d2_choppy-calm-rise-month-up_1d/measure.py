import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    FC = "forecast"
    RAW = "debug_info.components.scaled_week.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).values
            reg = d["regime"].astype(str).values
            raw = (pd.to_numeric(d[RAW], errors="coerce").values
                   if RAW in d.columns else np.full(len(d), np.nan))
            n = len(d)
            # 30-day and 60-day returns in percent, from prices inside the window
            ret30 = np.full(n, np.nan)
            ret60 = np.full(n, np.nan)
            if n > 30:
                ret30[30:] = (close[30:] / close[:-30] - 1.0) * 100.0
            if n > 60:
                ret60[60:] = (close[60:] / close[:-60] - 1.0) * 100.0
            for i in range(n):
                if fc[i] == 0:
                    continue
                n_active += 1
                # choppy calm profile + 30-day rise: the detector's decision is `regime`
                ok = reg[i] == "trending"
                # 30-day return above 0, where it can be computed from the window's prices
                if ok and not np.isnan(ret30[i]):
                    ok = ret30[i] > 0
                # choppy profile: 60-day return within -10..+10 %, where computable
                if ok and not np.isnan(ret60[i]):
                    ok = (-10.0 <= ret60[i] <= 10.0)
                # the week rose (scaled 7-day return above 0)
                if ok:
                    ok = (not np.isnan(raw[i])) and raw[i] > 0
                # expected side: long
                if ok and fc[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "forecast-weighted mean excess 7-bar forward return (forecast > 0)"
    main_thr = "above 0 with day-clustered t >= 2 to confirm; below 0 with t <= -2 to reject"
    sup_name = "top third minus bottom third by forecast, mean excess 7-bar return (Welch t)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars in the plan's "
                           "situation (choppy calm profile, 30-day return above 0, a 7-day rise)."),
            "reading": ("The profile and regime are read from the recorded `regime` (trending), the 30- and 60-day "
                        "returns are recomputed from closes where the window allows, and the week's rise from the "
                        "scaled_week raw value."),
        }

    # ---------- 2. Criterion ----------
    grid_rets = {}
    cases = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                f = fc[i]
                if np.isfinite(f) and f > 0:
                    cases.append((coin, ts.iloc[i], float(f), float(r)))
        grid_rets[coin] = float(np.mean(allr)) if len(allr) else np.nan

    rows = []
    for coin, t, f, r in cases:
        mu = grid_rets.get(coin, np.nan)
        if np.isfinite(mu):
            rows.append((coin, t, f, r - mu))
    cdf = pd.DataFrame(rows, columns=["coin", "ts", "f", "x"])
    n_cases = int(len(cdf))
    n_days = int(cdf["ts"].dt.floor("D").nunique()) if n_cases else 0

    value = None
    tval = None
    diff = None
    sup_t = None
    if n_cases >= 2:
        f = cdf["f"].values
        x = cdf["x"].values
        sw = f.sum()
        m = float((f * x).sum() / sw)
        value = m
        dev = f * (x - m) / sw
        day = cdf["ts"].dt.floor("D").values
        g = pd.Series(dev).groupby(day).sum().values
        G = len(g)
        if G > 1:
            se = np.sqrt(G / (G - 1.0) * np.sum(g ** 2))
            tval = float(m / se) if se > 0 else None
        s = cdf.assign(_t=cdf["ts"].astype("int64")).sort_values(
            ["f", "coin", "_t"], kind="mergesort").reset_index(drop=True)
        k = n_cases // 3
        if k >= 2:
            bot = s["x"].values[:k]
            top = s["x"].values[-k:]
            diff = float(top.mean() - bot.mean())
            tt = stats.ttest_ind(top, bot, equal_var=False)
            sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    sup_pass = None if diff is None else bool(diff > 0)
    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = "Fewer than 30 cases or fewer than 30 distinct days with forecast > 0 on the 7-bar grid."
    elif value is None or tval is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif value > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("Forecast-weighted mean excess return above 0 with t >= 2 over at least 30 cases on 30 "
                       "days, and top-third minus bottom-third difference above 0.")
        else:
            status = "inconclusive"
            decided = ("A confirming main measure with a top-minus-bottom difference at or below 0 is "
                       "inconclusive.")
    elif value < 0 and tval <= -2:
        status = "rejected"
        decided = ("Forecast-weighted mean excess return below 0 with t <= -2 over at least 30 cases on 30 days.")
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and +2 (or its sign disagrees with the mean), which is inconclusive."

    sup = {"name": sup_name, "value": diff, "passed": sup_pass}
    if sup_t is not None:
        sup["welch_t"] = sup_t

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": value,
            "statistic": ({"name": "t of the weighted mean, cases of one day taken together", "value": tval}
                          if tval is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are grid bars (positions 0, 7, 14, ... of each window) with forecast > 0 and a 7-bar "
                    "forward close inside the window; the coin's mean is over all its windows' grid returns; "
                    "thirds are floor(n/3) cases sorted by forecast (ties by coin and time); the supporting check "
                    "passes on a difference above 0, with its Welch t reported."),
    }
