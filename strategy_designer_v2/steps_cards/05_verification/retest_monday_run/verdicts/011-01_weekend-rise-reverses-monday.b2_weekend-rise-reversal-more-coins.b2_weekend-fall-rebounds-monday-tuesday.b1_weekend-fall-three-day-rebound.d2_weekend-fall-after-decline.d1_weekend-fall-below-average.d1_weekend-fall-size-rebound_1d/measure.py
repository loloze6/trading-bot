import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    MIN_CASES = 100
    FC = "forecast"
    RAW = "debug_info.components.weekend_fall.last_history_value"

    n_active = 0
    n_agree = 0
    n_unverifiable = 0

    coin_frames = {}  # coin -> list of prepared window frames
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["close"] = pd.to_numeric(d["close"], errors="coerce")
            d[FC] = pd.to_numeric(d[FC], errors="coerce")
            frames.append(d)
        coin_frames[coin] = frames

    # ---------- situation check ----------
    for coin, frames in coin_frames.items():
        for d in frames:
            close = d["close"]
            sma50 = close.rolling(50, min_periods=50).mean()
            prev_close = close.shift(1)
            prev_ts = d["ts"].shift(1)
            consecutive = (d["ts"] - prev_ts) == pd.Timedelta(days=1)
            ret1 = (close / prev_close - 1).where(consecutive)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # fall sign: raw component value where recorded, else the Sat->Sun close return
            fall_val = raw.where(raw.notna(), ret1)
            is_sunday = d["ts"].dt.dayofweek == 6  # bar opening Sunday: coming bar is Monday
            active = d[FC].fillna(0) != 0
            for i in np.where(active.values)[0]:
                sm = sma50.iloc[i]
                fv = fall_val.iloc[i]
                if not bool(is_sunday.iloc[i]):
                    n_active += 1
                    continue
                if pd.isna(sm) or pd.isna(fv):
                    n_unverifiable += 1
                    continue
                n_active += 1
                in_sit = (close.iloc[i] < sm) and (fv < 0)
                if in_sit and d[FC].iloc[i] > 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The situation is a bar opening on Sunday UTC whose close is below the 50-bar SMA of closes "
               "computed inside its window and whose one-bar return (the recorded raw component, else the close "
               "versus the previous day's close) is negative, active Sunday bars whose SMA50 cannot be computed "
               "inside the window are left out of the agreement; the coin's mean 3-bar return is taken on the "
               "non-overlapping grid (positions 0, 3, 6, ...) of all its windows pooled, cases without 3 bars left "
               "in their window are left out, and t is the ordinary t of the mean of the products.")

    main_name = "mean of (excess 3-bar return x forecast / 10) over Sunday cases with forecast > 0"
    threshold = "confirm: mean > 0 with t >= 2 and correlation > 0; reject: mean < 0 with t <= -2; at least 100 cases"

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree),
                       "unverifiable active bars": int(n_unverifiable)},
            "decided_by": ("Only {:.1%} of active bars are Sunday bars with a fall below the 50-day average "
                           "carrying a long forecast, under the 90 % required.").format(agreement),
            "reading": reading,
        }

    # ---------- criterion ----------
    products = []
    fcs = []
    excess_all = []
    for coin, frames in coin_frames.items():
        grid_rets = []
        for d in frames:
            c = d["close"].values
            n = len(c)
            for p in range(0, n - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1)
        if len(grid_rets) == 0:
            continue
        mean3 = float(np.mean(grid_rets))
        for d in frames:
            c = d["close"].values
            f = d[FC].values
            dow = d["ts"].dt.dayofweek.values
            n = len(c)
            for i in range(n):
                if dow[i] != 6 or not np.isfinite(f[i]) or f[i] <= 0:
                    continue
                if i + H >= n or not np.isfinite(c[i]) or not np.isfinite(c[i + H]) or c[i] == 0:
                    continue
                ex = c[i + H] / c[i] - 1 - mean3
                products.append(ex * f[i] / 10.0)
                fcs.append(f[i])
                excess_all.append(ex)

    n_cases = len(products)
    counts = {"cases": int(n_cases)}

    mean_p = float(np.mean(products)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(products, ddof=1))
        t = float(mean_p / (sd / np.sqrt(n_cases))) if sd > 0 else None
    corr = None
    if n_cases > 2 and np.std(fcs) > 0 and np.std(excess_all) > 0:
        corr = float(stats.pearsonr(fcs, excess_all)[0])
    corr_pass = None if corr is None else bool(corr > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = "The plan needs at least 100 cases and only {} were found.".format(n_cases)
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean of the products could not be computed, so neither rule is met."
    elif mean_p > 0 and t >= 2 and corr_pass:
        status = "confirmed"
        decided = "The mean of the products is above 0 with t >= 2 and the correlation is above 0."
    elif mean_p < 0 and t <= -2:
        status = "rejected"
        decided = "The mean of the products is below 0 with t <= -2."
    elif mean_p > 0 and t >= 2:
        status = "inconclusive"
        decided = "The t confirms (>= 2) but the correlation is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {"name": main_name, "value": mean_p,
                         "statistic": None if t is None else {"name": "t of the mean", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "correlation of forecast with excess 3-bar return across cases",
                             "value": corr, "passed": corr_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
