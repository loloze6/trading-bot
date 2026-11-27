import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.depth_sw.last_history_value"

    # Per coin: the mean one-bar return over all windows together (never across two windows)
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp")
            c = pd.to_numeric(d["close"], errors="coerce").values
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if allr.size else np.nan

    n_active = 0
    n_agree = 0
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce") if FC in d else pd.Series(np.nan, index=d.index)
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d else pd.Series(np.nan, index=d.index)
            day_ret = close / close.shift(1) - 1.0
            next_ret = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")

            # Situation check: up day (1-day return > 0) and close below the 20-day high (raw depth < 0), short side
            active = fc.notna() & (fc != 0) & day_ret.notna()
            situ = (day_ret > 0) & (raw < 0)
            agree = active & situ & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            up = (day_ret > 0) & fc.notna() & next_ret.notna()
            for i in np.where(up.values)[0]:
                rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].floor("D") if pd.notna(ts.iloc[i]) else pd.NaT,
                    "absf": abs(float(fc.iloc[i])),
                    "excess": float(next_ret.iloc[i]) - coin_mu[coin],
                })

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("Up days are bars whose close is above the prior close in the same window (each window's first bar, "
               "with no prior close, is left out); the top and bottom quintiles are the up-day bars with |forecast| at "
               "or above the pooled 80th percentile and at or below the pooled 20th percentile; the main mean is over "
               "cases and its t is the ordinary t over per-day sums of the short-signed excess returns; the supporting "
               "check uses the unsigned excess returns, top minus bottom.")
    main_name = "mean next-day excess return of top-|forecast|-quintile up days, short-signed"
    threshold = "confirm t >= 2 with supporting check < 0; reject t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are up days below the 20-day high with a short forecast, "
                           "so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    t = pd.DataFrame(rows)
    sup_name = "next-day excess return, top-quintile minus bottom-quintile up days"
    if t.empty:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"top-quintile cases": 0, "distinct days": 0},
            "decided_by": "No up-day cases: the minimum of 200 top-quintile cases on 100 distinct days is not reached.",
            "reading": reading,
        }

    t = t.dropna(subset=["absf", "excess"])
    q80 = float(np.quantile(t["absf"].values, 0.8))
    q20 = float(np.quantile(t["absf"].values, 0.2))
    top = t[t["absf"] >= q80].copy()
    bot = t[t["absf"] <= q20].copy()

    top["signed"] = -top["excess"]
    n_top = int(len(top))
    days = top.dropna(subset=["day"]).groupby("day")["signed"].sum()
    n_days = int(len(days))
    mean_val = float(top["signed"].mean()) if n_top else None
    if n_days >= 2:
        sd = float(days.std(ddof=1))
        tstat = float(days.mean() / (sd / np.sqrt(n_days))) if sd > 0 else None
    else:
        tstat = None

    sup_val = None
    sup_pass = None
    if len(top) and len(bot):
        sup_val = float(top["excess"].mean() - bot["excess"].mean())
        sup_pass = bool(sup_val < 0)

    counts = {"top-quintile cases": n_top, "distinct days": n_days, "bottom-quintile cases": int(len(bot))}
    stat = {"name": "t of the mean (per-day sums)", "value": tstat} if tstat is not None else None

    if n_top < 200 or n_days < 100 or tstat is None:
        status = "not observable"
        decided = (f"The minimum is not reached: {n_top} top-quintile cases (need 200) on {n_days} "
                   f"distinct days (need 100).")
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure has t >= 2 and the top-minus-bottom excess return is below 0."
    elif tstat <= -2:
        status = "rejected"
        decided = "The main measure has t <= -2: the deepest up days rise more than the drift the next day."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The main measure has t >= 2 but the supporting check fails (top minus bottom not below 0)."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_val, "statistic": stat, "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
