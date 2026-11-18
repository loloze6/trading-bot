import numpy as np
import pandas as pd


def measure(bars):
    H = 2
    MIN_CASES = 100

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    # ---------------- 1. Situation check ----------------
    # Situation: the coming bar is Monday or Tuesday. The bar just closed is a Sunday bar
    # (the coming bar is Monday) or a Monday bar (the coming bar is Tuesday). The Sunday
    # close-to-close return must be a fall. The expected side is long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = _ts(df)
            wd = ts.dt.weekday.values  # Monday=0 ... Sunday=6
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            raw_mon = pd.to_numeric(
                df.get("debug_info.components.sun_drop_mon.last_history_value",
                       pd.Series(np.nan, index=df.index)), errors="coerce").values
            raw_tue = pd.to_numeric(
                df.get("debug_info.components.sun_drop_tue.last_history_value",
                       pd.Series(np.nan, index=df.index)), errors="coerce").values
            for i in range(len(df)):
                if fc[i] == 0 or not np.isfinite(fc[i]):
                    continue
                n_active += 1
                ok = False
                if wd[i] == 6:  # Sunday bar, the coming bar is Monday
                    sun_ret = np.nan
                    if i >= 1 and np.isfinite(close[i]) and np.isfinite(close[i - 1]):
                        sun_ret = close[i] / close[i - 1] - 1
                    if not np.isfinite(sun_ret):
                        sun_ret = raw_mon[i]
                    ok = np.isfinite(sun_ret) and sun_ret < 0 and fc[i] > 0
                elif wd[i] == 0:  # Monday bar, the coming bar is Tuesday
                    sun_ret = np.nan
                    if i >= 2 and wd[i - 1] == 6 and np.isfinite(close[i - 1]) and np.isfinite(close[i - 2]):
                        sun_ret = close[i - 1] / close[i - 2] - 1
                    if not np.isfinite(sun_ret):
                        sun_ret = raw_tue[i]
                    ok = np.isfinite(sun_ret) and sun_ret < 0 and fc[i] > 0
                if ok:
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of mean forecast/10 x excess 2-bar return over Sunday cases, pooled"
    thr = "confirm if t >= 2 with the check passing; reject if t <= -2; at least 100 cases with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are Sunday or Monday closes after a Sunday fall "
                           "with a long forecast, so the config does not hold the plan's situation and side."),
            "reading": "Sunday and Monday bars are identified from the bar's UTC start timestamp; the Sunday fall is "
                       "taken from closes, or from the component's raw value when closes are unavailable.",
        }

    # ---------------- 2. Criterion ----------------
    # Each coin's mean 2-bar return over all windows, on the 2-bar grid.
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    rets.append(c[i + H] / c[i] - 1)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    prods, fcs, excs = [], [], []
    for coin, wins in bars.items():
        m = coin_mean.get(coin, np.nan)
        if not np.isfinite(m):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            for i in range(len(df) - H):
                if reg[i] != "trending" or not np.isfinite(fc[i]) or fc[i] <= 0:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                ex = c[i + H] / c[i] - 1 - m
                prods.append(fc[i] / 10.0 * ex)
                fcs.append(fc[i])
                excs.append(ex)

    n = len(prods)
    prods = np.asarray(prods, dtype=float)
    mean_p = float(np.mean(prods)) if n > 0 else None
    t = None
    if n >= 2:
        sd = float(np.std(prods, ddof=1))
        t = float(mean_p / (sd / np.sqrt(n))) if sd > 0 else None

    # Supporting check: the top third minus the bottom third by forecast.
    sup_val, sup_pass = None, None
    k = n // 3
    if k >= 1:
        order = np.argsort(np.asarray(fcs), kind="mergesort")
        ex_arr = np.asarray(excs)
        bottom = ex_arr[order[:k]]
        top = ex_arr[order[-k:]]
        sup_val = float(np.mean(top) - np.mean(bottom))
        sup_pass = bool(sup_val > 0)

    counts = {"cases with forecast > 0": int(n)}
    reading = ("Cases are bars with regime 'trending' and forecast > 0 whose t+2 close lies in the same window; "
               "thirds are n//3 cases each, ranked by forecast; the plan's 'fewer than 100 cases' is treated as "
               "the minimum count (not observable); the situation check identifies days from the UTC start timestamp.")

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases with forecast > 0, below the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The main t could not be computed (zero dispersion), so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main t is 2 or more and the top-minus-bottom-third excess return is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The main t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The main t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_p,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "top third minus bottom third mean excess 2-bar return",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
