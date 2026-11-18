import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.fall.last_history_value"

    # ---------- gather per-bar data, window by window ----------
    rows = []
    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp", kind="mergesort")
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce") if FC in df.columns else pd.Series(np.nan, index=df.index)
            # next-bar return inside the window only
            nxt = close.shift(-1) / close - 1.0
            # the 1-day return (situation's fall): recorded raw value, else recomputed inside the window
            prev_ret = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), prev_ret)
            else:
                raw = prev_ret
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            rows.append(pd.DataFrame({
                "coin": coin,
                "window": str(window),
                "forecast": fc.values,
                "next_ret": nxt.values,
                "raw_ret": raw.values,
                "regime": regime.values,
            }))

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean of (forecast/10) x next-day excess return on forecast > 0 bars",
                             "value": None, "statistic": None, "threshold": "t >= 2.0 confirms, t <= -2.0 rejects"},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": 0},
            "decided_by": "No bars in the record, so fewer than 30 bars with forecast > 0.",
            "reading": "none",
        }

    data = pd.concat(rows, ignore_index=True)

    # ---------- 1. situation check ----------
    active = data[data["forecast"].notna() & (data["forecast"] != 0)]
    n_active = int(len(active))
    in_situation = (
        (active["regime"] == "mean_reversion")
        & active["raw_ret"].notna()
        & (active["raw_ret"] < 0)
        & (active["forecast"] > 0)
    )
    agreement = float(in_situation.mean()) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation = regime 'mean_reversion' (the detector's recorded decision, since its 20-day/100-day "
               "volatility ratio is not recorded and windows are too short to rebuild it) and a negative 1-day return, "
               "side long; supporting split puts forecasts >= the median in the top half and < the median in the bottom "
               "half, with unweighted mean excess returns; the minimum of 30 counts forecast > 0 bars with a next-day "
               "return in the same window.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": int(in_situation.sum())},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars after a one-day fall in the "
                           "high-volatility (mean_reversion) regime, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin's mean daily return over all its windows
    coin_mean = data.dropna(subset=["next_ret"]).groupby("coin")["next_ret"].mean()
    data["excess"] = data["next_ret"] - data["coin"].map(coin_mean)

    pos = data[(data["forecast"] > 0) & data["excess"].notna()].copy()
    n_pos = int(len(pos))
    pos["val"] = (pos["forecast"] / 10.0) * pos["excess"]

    main_name = "mean of (forecast/10) x next-day excess return on forecast > 0 bars"
    threshold = "ordinary t >= 2.0 confirms (with top-minus-bottom > 0); t <= -2.0 rejects"

    mean_val = float(pos["val"].mean()) if n_pos > 0 else None
    t_val = None
    if n_pos >= 2:
        sd = float(pos["val"].std(ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_pos)))

    # supporting check
    diff = None
    n_top = n_bot = 0
    if n_pos > 0:
        med = float(pos["forecast"].median())
        top = pos[pos["forecast"] >= med]
        bot = pos[pos["forecast"] < med]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top > 0 and n_bot > 0:
            diff = float(top["excess"].mean() - bot["excess"].mean())
    sup_passed = None if diff is None else bool(diff > 0)

    counts = {
        "bars with forecast > 0": n_pos,
        "top half bars": n_top,
        "bottom half bars": n_bot,
    }

    main = {
        "name": main_name,
        "value": mean_val,
        "statistic": None if t_val is None else {"name": "ordinary t", "value": t_val},
        "threshold": threshold,
    }
    support = {"name": "top-half minus bottom-half mean excess next-day return (median forecast split)",
               "value": diff, "passed": sup_passed}
    sc = {"agreement": agreement, "passed": passed}

    if n_pos < 30:
        return {
            "status": "not observable",
            "situation_check": sc,
            "main_measure": main,
            "supporting_check": support,
            "counts": counts,
            "decided_by": f"Only {n_pos} bars with forecast > 0 pooled across coins and windows, below the plan's minimum of 30.",
            "reading": reading,
        }

    if t_val is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed (zero dispersion), so neither confirm nor reject rule is met."
    elif t_val >= 2.0 and sup_passed is True:
        status = "confirmed"
        decided = "The main measure's t is >= 2.0 and the top-minus-bottom difference is above 0."
    elif t_val >= 2.0:
        status = "inconclusive"
        decided = "The main measure's t is >= 2.0 but the top-minus-bottom difference is not above 0 (or not computable)."
    elif t_val <= -2.0:
        status = "rejected"
        decided = "The main measure's t is <= -2.0."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2.0 and 2.0."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
