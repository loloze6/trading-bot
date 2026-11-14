import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    COMP = "debug_info.components.down_day.last_history_value"

    # ---------- pooled data ----------
    rows = []          # (coin, forecast, next_ret) for bars with forecast > 0
    hold_rets = {}     # coin -> list of all next-bar returns (holding)
    n_active = 0
    n_agree = 0

    for coin, wins in bars.items():
        hold_rets.setdefault(coin, [])
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0          # next-bar return, inside the window
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))

            # raw 1-day return of the down_day component; fallback to the price return
            price_r1 = close / close.shift(1) - 1.0
            if COMP in df.columns:
                r1 = pd.to_numeric(df[COMP], errors="coerce")
                r1 = r1.where(r1.notna(), price_r1)
            else:
                r1 = price_r1

            hold_rets[coin].extend(nxt.dropna().tolist())

            # situation check: active bars must be trending, a down day, and long
            active = fc.notna() & (fc != 0)
            situation = (regime == "trending") & (r1 < 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            sel = fc.notna() & (fc > 0) & nxt.notna()
            for f, r in zip(fc[sel].tolist(), nxt[sel].tolist()):
                rows.append((coin, float(f), float(r)))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    threshold = "confirm if mean > 0 with t >= 2.0; reject if mean < 0 with t <= -2.0; else inconclusive; at least 200 forecast > 0 bars"
    reading = ("The situation is checked as regime == 'trending' and a negative raw 1-day return (down_day component, price return as fallback) with forecast > 0; "
               "the holding mean is each coin's mean next-bar return over all bars of all its windows, the 200-bar minimum counts forecast > 0 bars with a valid next-bar return, "
               "and the supporting check (positive OLS slope of excess return on forecast) is reported without changing the status.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean excess next-bar return over holding mean", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": len(rows), "active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars are trending down-day bars with a long forecast "
                           "(the plan's situation: uptrend with 20/60-day returns > 0 and a 1-day drop, long side)."),
            "reading": reading,
        }

    hold_mean = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in hold_rets.items()}
    ex, fsz = [], []
    for coin, f, r in rows:
        hm = hold_mean.get(coin, np.nan)
        if np.isfinite(hm):
            ex.append(r - hm)
            fsz.append(f)
    ex = np.asarray(ex, float)
    fsz = np.asarray(fsz, float)
    n = len(ex)

    mean_ex = float(np.mean(ex)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(ex, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n))) if sd > 0 else None

    slope = None
    if n > 2 and np.std(fsz) > 0:
        slope = float(stats.linregress(fsz, ex).slope)
    supporting = {"name": "OLS slope of excess next-bar return on forecast size",
                  "value": slope, "passed": (None if slope is None else bool(slope > 0))}

    counts = {"bars with forecast > 0": int(n)}

    if n < 200:
        status = "not observable"
        decided = f"Only {n} bars with forecast > 0 pooled across coins and windows, below the plan's minimum of 200."
    elif t is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so no confirm or reject rule is met."
    elif mean_ex > 0 and t >= 2.0:
        status = "confirmed"
        decided = "The mean excess next-bar return is positive with t >= 2.0 (confirm rule)."
    elif mean_ex < 0 and t <= -2.0:
        status = "rejected"
        decided = "The mean excess next-bar return is negative with t <= -2.0 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2.0 and 2.0 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean excess next-bar return over holding mean",
                         "value": mean_ex,
                         "statistic": (None if t is None else {"name": "t of the mean", "value": t}),
                         "threshold": threshold},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
