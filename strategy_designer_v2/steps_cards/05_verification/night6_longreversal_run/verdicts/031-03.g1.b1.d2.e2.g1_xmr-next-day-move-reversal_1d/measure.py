import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    Z_COL = "debug_info.components.fade_move.last_history_value"
    POS_COL = "postRebalance_current_allocation"

    frames = []
    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys(), key=lambda w: int(str(w).lstrip("w") or 0)):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            next_ret = close.shift(-1) / close - 1.0  # inside the window only
            z = pd.to_numeric(df[Z_COL], errors="coerce") if Z_COL in df.columns else pd.Series(np.nan, index=df.index)
            out = pd.DataFrame({
                "coin": coin,
                "window": win,
                "forecast": pd.to_numeric(df["forecast"], errors="coerce"),
                "pos": pd.to_numeric(df[POS_COL], errors="coerce"),
                "z": z,
                "next_ret": next_ret,
            })
            frames.append(out)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean excess gain of position x (next-day return - XMR mean daily return)",
                             "value": None, "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"bars with a non-zero position": 0},
            "decided_by": "No bars in the record: the minimum of 500 bars with a non-zero position is not reached.",
            "reading": "none",
        }

    d = pd.concat(frames, ignore_index=True)

    # ---- 1. Situation check: reversal side = -sign(z), on every bar with a non-zero z
    active = d[(d["forecast"].notna()) & (d["forecast"] != 0)]
    n_active = int(len(active))
    if n_active > 0:
        zs = np.sign(active["z"].fillna(0.0).values)
        fs = np.sign(active["forecast"].values)
        agree = (zs != 0) & (fs == -zs)
        agreement = float(agree.mean())
    else:
        agreement = 0.0
    sit_passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("Every bar with a non-zero volatility-scaled return z (fade_move's raw value) is a bar of the situation, "
               "on the side opposite to z's sign; the excess gain is taken on every bar with a next-day return in its "
               "window, the coin's mean daily return is the mean of all next-day returns over all windows, the minimum "
               "count is of bars with a non-zero postRebalance_current_allocation, and the slopes are ordinary "
               "least-squares slopes of next-day return on raw z.")

    if not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean excess gain of position x (next-day return - XMR mean daily return)",
                             "value": None, "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active forecast bars": n_active},
            "decided_by": ("Fewer than 90% of the active forecast bars are long after a fall / short after a rise of "
                           "the volatility-scaled return, as the plan's reversal situation requires (agreement %.3f)."
                           % agreement),
            "reading": reading,
        }

    # ---- 2. Main measure
    valid_ret = d["next_ret"].notna()
    mu = float(d.loc[valid_ret, "next_ret"].mean())
    m = d[valid_ret & d["pos"].notna()].copy()
    m["excess"] = m["pos"] * (m["next_ret"] - mu)
    n_bars = int(len(m))
    n_nonzero = int((d["pos"].notna() & (d["pos"] != 0)).sum())

    if n_bars >= 2:
        mean_ex = float(m["excess"].mean())
        sd = float(m["excess"].std(ddof=1))
        t_main = float(mean_ex / (sd / np.sqrt(n_bars))) if sd > 0 else 0.0
    else:
        mean_ex = None
        t_main = None

    # ---- Supporting check: slopes of next-day return on z, on each side
    def slope(sub):
        sub = sub.dropna(subset=["z", "next_ret"])
        if len(sub) < 3 or np.ptp(sub["z"].values) == 0:
            return None, int(len(sub))
        res = stats.linregress(sub["z"].values, sub["next_ret"].values)
        return float(res.slope), int(len(sub))

    s_fall, n_fall = slope(d[d["z"] < 0])
    s_rise, n_rise = slope(d[d["z"] > 0])
    if s_fall is None or s_rise is None:
        sup_passed = None
        sup_value = None
    else:
        sup_passed = bool(s_fall < 0 and s_rise < 0 and abs(s_fall) > abs(s_rise))
        sup_value = float(abs(s_fall) - abs(s_rise))

    counts = {
        "bars with a non-zero position": n_nonzero,
        "bars in the main measure": n_bars,
        "bars with z < 0": n_fall,
        "bars with z > 0": n_rise,
    }

    main = {
        "name": "mean excess gain of position x (next-day return - XMR mean daily return)",
        "value": mean_ex,
        "statistic": {"name": "t of the mean", "value": t_main} if t_main is not None else None,
        "threshold": "t >= 2 (with the supporting check) confirms, t <= -2 rejects, otherwise inconclusive",
    }
    supporting = {
        "name": "fall-side slope larger in size than rise-side slope, both negative (|fall| - |rise|)",
        "value": sup_value,
        "passed": sup_passed,
        "fall_slope": s_fall,
        "rise_slope": s_rise,
    }

    if n_nonzero < 500 or t_main is None:
        status = "not observable"
        decided = "Fewer than 500 bars with a non-zero position (%d): the plan's minimum count is not reached." % n_nonzero
    elif t_main >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "The mean excess gain has t >= 2 (%.2f) and the fall-side reversal slope exceeds the rise-side one, both negative." % t_main
    elif t_main <= -2:
        status = "rejected"
        decided = "The mean excess gain has t <= -2 (%.2f): fading the moves loses against the coin's drift." % t_main
    elif t_main >= 2:
        status = "inconclusive"
        decided = "t >= 2 (%.2f) but the fall-side slope does not exceed the rise-side slope with both negative." % t_main
    else:
        status = "inconclusive"
        decided = "The mean excess gain's t (%.2f) lies between -2 and 2." % t_main

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": sit_passed},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
