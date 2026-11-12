import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    MOVE = "debug_info.components.move.last_history_value"

    # ---------- collect rows, per window, never crossing windows ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            vol = pd.to_numeric(d["volume"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            next_ret = close.shift(-1) / close - 1.0
            vol_mean = vol.rolling(20, min_periods=20).mean()
            if MOVE in d.columns:
                move = pd.to_numeric(d[MOVE], errors="coerce")
            else:
                move = close / close.shift(1) - 1.0
            out = pd.DataFrame({
                "coin": coin, "window": w,
                "forecast": fc, "next_ret": next_ret,
                "vol": vol, "vol_mean": vol_mean, "move": move,
            })
            rows.append(out)
    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"active bars": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }
    all_df = pd.concat(rows, ignore_index=True)

    # ---------- situation check ----------
    active = all_df[all_df["forecast"].notna() & (all_df["forecast"] != 0)]
    chk = active[active["vol_mean"].notna() & active["move"].notna() & active["vol"].notna()]
    if len(chk) > 0:
        in_sit = (chk["vol"] >= chk["vol_mean"]) & (chk["move"] > 0) & (chk["forecast"] > 0)
        agreement = float(in_sit.mean())
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation = volume at or above its 20-bar mean (including the current bar, computed inside each window, "
               "active bars without 20 bars of volume history left out of the check) and a positive one-bar move from "
               "the move component, side long; the excess return is next-bar return minus the mean next-bar return over "
               "all bars of all windows pooled; the t-statistic is the ordinary t of the per-bar contributions "
               "forecast x excess / mean(forecast) over active bars (whose mean equals the forecast-weighted mean); "
               "the 60-bar minimum counts active bars with a next-bar return; top and bottom fifths are the "
               "floor(n/5) active bars with the highest and lowest forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"active bars": int(len(active))},
            "decided_by": ("Fewer than 90% of active bars are long bars with volume at or above its 20-bar mean "
                           "and a positive one-bar move, so the config does not do what the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- main measure ----------
    valid_all = all_df[all_df["next_ret"].notna()]
    drift = float(valid_all["next_ret"].mean()) if len(valid_all) else np.nan
    act = all_df[all_df["forecast"].notna() & (all_df["forecast"] != 0) & all_df["next_ret"].notna()].copy()
    act["excess"] = act["next_ret"] - drift
    n_active = int(len(act))

    wmean = None
    tstat = None
    if n_active > 0 and act["forecast"].sum() != 0:
        f = act["forecast"].values.astype(float)
        x = act["excess"].values.astype(float)
        wmean = float(np.sum(f * x) / np.sum(f))
        y = f * x / np.mean(f)
        if n_active > 1 and np.std(y, ddof=1) > 0:
            tstat = float(np.mean(y) / (np.std(y, ddof=1) / np.sqrt(n_active)))

    # ---------- supporting check ----------
    sup_val = None
    sup_pass = None
    k = n_active // 5
    if k >= 1:
        srt = act.sort_values("forecast", kind="mergesort")
        bottom = srt.iloc[:k]["excess"].mean()
        top = srt.iloc[-k:]["excess"].mean()
        sup_val = float(top - bottom)
        sup_pass = bool(top > 0 and top > bottom)
        top_mean = float(top)
    else:
        top_mean = None

    counts = {"active bars": n_active}
    main = {
        "name": "forecast-weighted mean next-bar excess return over buy-and-hold drift",
        "value": wmean,
        "statistic": {"name": "t of the forecast-weighted mean", "value": tstat} if tstat is not None else None,
        "threshold": "confirm if above 0 with t >= 2; reject if below 0 with t <= -2; else inconclusive",
    }
    support = {
        "name": "top-fifth minus bottom-fifth mean excess return (top must be > 0 and > bottom)",
        "value": sup_val,
        "passed": sup_pass,
    }

    if n_active < 60:
        status = "not observable"
        decided = f"Only {n_active} active bars across the windows, below the plan's minimum of 60."
    elif wmean is None or tstat is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif wmean > 0 and tstat >= 2:
        status = "confirmed"
        decided = "The forecast-weighted mean excess next-bar return is above 0 with a t-statistic of 2 or more."
    elif wmean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess next-bar return is below 0 with a t-statistic of -2 or less."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
