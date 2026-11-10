import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    MOVE = "debug_info.components.move.last_history_value"

    # ---------- collect rows, per window, without crossing windows ----------
    frames = []
    for coin, wins in bars.items():
        for win, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["coin"] = coin
            d["window"] = win
            d["fc"] = pd.to_numeric(d[FC], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            vol = pd.to_numeric(d["volume"], errors="coerce")
            # next-bar return inside the same window only
            d["ret1"] = close.shift(-1) / close - 1.0
            # volume regime: volume at or above its 20-bar mean (mean includes the current bar)
            vmean = vol.rolling(20, min_periods=20).mean()
            d["vol_known"] = vmean.notna() & vol.notna()
            d["high_vol"] = (vol >= vmean) & d["vol_known"]
            # size of the current bar's one-day rise: raw move component, else close change
            if MOVE in d.columns:
                mv = pd.to_numeric(d[MOVE], errors="coerce")
            else:
                mv = pd.Series(np.nan, index=d.index)
            mv = mv.fillna(close / close.shift(1) - 1.0)
            d["move_raw"] = mv
            frames.append(d)

    if not frames:
        return {
            "status": "inconclusive",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"active bars": 0},
            "decided_by": "No data in the record.", "reading": "none",
        }

    all_df = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    active = all_df[all_df["fc"].notna() & (all_df["fc"] != 0)]
    checkable = active[active["vol_known"] & active["move_raw"].notna()]
    if len(checkable) > 0:
        ok = (checkable["high_vol"]
              & (checkable["move_raw"] > 0)
              & (checkable["fc"] > 0))
        agreement = float(ok.mean())
    else:
        agreement = float("nan")
    passed = bool(len(checkable) > 0 and agreement >= 0.90)

    reading = ("Volume regime taken as volume >= the rolling 20-bar mean of volume including the current bar, "
               "computed inside each window so the first 19 rows of each window (no full 20-bar history) are left "
               "out of the situation check; the up move is the raw 'move' component > 0; the drift is the mean "
               "next-bar return over all bars of all windows; the t-statistic is the weighted mean divided by its "
               "forecast-weighted (sandwich) standard error; the top/bottom fifths are the floor(n/5) active bars "
               "with the highest/lowest forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if np.isnan(agreement) else agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(len(active)), "checkable active bars": int(len(checkable))},
            "decided_by": ("Fewer than 90% of active bars are long bars with volume at or above its 20-bar mean "
                           "and a positive one-day move, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- main measure ----------
    valid = all_df[all_df["ret1"].notna()]
    drift = float(valid["ret1"].mean()) if len(valid) else np.nan
    act = valid[valid["fc"].notna() & (valid["fc"] != 0)].copy()
    act["excess"] = act["ret1"] - drift
    n = int(len(act))

    wmean = None
    tstat = None
    if n >= 2:
        w = act["fc"].to_numpy(dtype=float)
        x = act["excess"].to_numpy(dtype=float)
        sw = w.sum()
        m = float((w * x).sum() / sw)
        se = np.sqrt(np.sum(w ** 2 * (x - m) ** 2)) / sw * np.sqrt(n / (n - 1))
        wmean = m
        tstat = float(m / se) if se > 0 else None
    elif n == 1:
        wmean = float(act["excess"].iloc[0])

    # ---------- supporting check ----------
    sup_val = None
    sup_pass = None
    k = n // 5
    if k >= 1:
        srt = act.sort_values(["fc", "timestamp"], kind="mergesort")
        bottom = srt.head(k)["excess"].mean()
        top = srt.tail(k)["excess"].mean()
        sup_val = float(top - bottom)
        sup_pass = bool(top > 0 and top > bottom)

    # ---------- decision ----------
    if n < 60:
        status = "inconclusive"
        decided = "Fewer than 60 active bars across the 6 windows, so the result is inconclusive."
    elif tstat is None or wmean is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed, so the result is inconclusive."
    elif wmean > 0 and tstat >= 2:
        status = "confirmed"
        decided = "The forecast-weighted mean excess next-bar return is above 0 with a t-statistic of 2 or more."
    elif wmean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess next-bar return is below 0 with a t-statistic of -2 or less."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "forecast-weighted mean next-bar excess return over buy-and-hold drift",
            "value": wmean,
            "statistic": None if tstat is None else {"name": "t of the forecast-weighted mean", "value": tstat},
            "threshold": "above 0 with t >= 2 confirms; below 0 with t <= -2 rejects; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "top-fifth minus bottom-fifth mean next-bar excess return (top fifth must be > 0)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"active bars": n},
        "decided_by": decided,
        "reading": reading,
    }
