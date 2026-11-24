import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    VOLC = "debug_info.components.vol20.post_pipeline_value"
    REG = "mean_reversion"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    frames = []
    coin_means = {}

    for coin, windows in bars.items():
        all_rets = []
        for wname, df in windows.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            low = d["low"].astype(float)

            # Situation recomputed from prices, inside the window only.
            r1 = close.pct_change(1)
            sd20 = r1.rolling(20, min_periods=20).std()
            fall = r1 / sd20.replace(0, np.nan)
            rng = (high - low).replace(0, np.nan)
            loc = (close - low) / rng
            computable = fall.notna() & loc.notna()
            sit = (fall <= -2.0) & (loc <= 0.25)
            # The first bars of a window have no 20-return history in the record.
            # On those bars, fall back to the detector's regime.
            regime_is = d["regime"].astype(str) == REG
            sit_full = np.where(computable, sit, regime_is)

            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(sit_full, index=d.index).astype(bool) & (fc > 0)).sum())

            # Next-bar return, inside the window only.
            nxt = close.shift(-1) / close - 1.0
            d["_next"] = nxt
            d["_coin"] = coin
            d["_win"] = wname
            all_rets.append(nxt.dropna().values)
            frames.append(d)
        if all_rets:
            allr = np.concatenate(all_rets)
            coin_means[coin] = float(np.mean(allr)) if len(allr) else np.nan

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation recomputed from prices as 1-bar return over the std (ddof 1) of the last 20 one-bar returns "
               "including bar t, with close location (close-low)/(high-low), falling back to the recorded regime on "
               "bars without 20 returns of history; cases are bars with regime mean_reversion and a next bar in the "
               "same window; the coin's mean is over all its 1-bar returns in all windows; the t clusters cases by "
               "UTC day (deviations summed per day); the median split puts cases above the median in the upper half "
               "and the rest in the lower half; fewer than 30 case-days is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean excess next-day return on mean_reversion bars",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 to confirm, t <= -2 to reject, over at least 30 case-days"},
            "supporting_check": None,
            "counts": {"case-days": None, "active bars": int(n_active)},
            "decided_by": ("Only {:.1%} of the active bars are deep (return <= -2 of 20-day volatility), "
                           "low-closing (lowest quarter) days on the long side, below the 90 % the plan's "
                           "situation requires.").format(agreement),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    if frames:
        allb = pd.concat(frames, ignore_index=True)
    else:
        allb = pd.DataFrame(columns=["regime", "_next", "_coin", "timestamp"])
    cases = allb[(allb["regime"].astype(str) == REG) & allb["_next"].notna()].copy()
    cases["_mean"] = cases["_coin"].map(coin_means)
    cases["_ex"] = cases["_next"] - cases["_mean"]
    cases = cases[cases["_ex"].notna()]
    cases["_day"] = cases["timestamp"].dt.floor("D")

    n_cases = int(len(cases))
    G = int(cases["_day"].nunique()) if n_cases else 0

    mean_ex = float(cases["_ex"].mean()) if n_cases else None
    t = None
    if n_cases and G >= 2:
        dev = (cases["_ex"] - mean_ex).groupby(cases["_day"]).sum().values
        var = (G / (G - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
        se = float(np.sqrt(var))
        t = float(mean_ex / se) if se > 0 else None

    # Supporting check
    diff = None
    sup_pass = None
    if n_cases and VOLC in cases.columns:
        v = pd.to_numeric(cases[VOLC], errors="coerce")
        sub = cases[v.notna()]
        vv = v[v.notna()]
        if len(sub) >= 2:
            med = float(vv.median())
            up = sub.loc[vv > med, "_ex"]
            lo = sub.loc[vv <= med, "_ex"]
            if len(up) > 0 and len(lo) > 0:
                diff = float(up.mean() - lo.mean())
                sup_pass = bool(diff > 0)

    if G < 30:
        status = "not observable"
        decided = "Fewer than 30 case-days ({}), the plan's minimum count, so the data cannot show the idea.".format(G)
    elif t is not None and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean excess next-day return has t >= 2 over at least 30 case-days and the high-volatility half beats the low-volatility half."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "The mean excess next-day return has t <= -2 over at least 30 case-days."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the high-volatility half does not beat the low-volatility half."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2 over at least 30 case-days."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean excess next-day return on mean_reversion bars",
                         "value": mean_ex,
                         "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t}
                                       if t is not None else None),
                         "threshold": "t >= 2 to confirm, t <= -2 to reject, over at least 30 case-days"},
        "supporting_check": {"name": "mean excess of upper vol20 half minus lower half",
                             "value": diff, "passed": sup_pass},
        "counts": {"case-days": G, "cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
