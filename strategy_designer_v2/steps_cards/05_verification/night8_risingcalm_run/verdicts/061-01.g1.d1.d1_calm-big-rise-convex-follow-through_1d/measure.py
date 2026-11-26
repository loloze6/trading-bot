import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    VSR_COL = "debug_info.components.big_day.last_history_value"

    def prep(df):
        df = df.sort_values("timestamp").reset_index(drop=True).copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
        return df

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = prep(df)
            prepared[(coin, w)] = df
            # Raw vsr: the recorded value of the same component, else recomputed from prices
            ret = df["close"].pct_change()
            vsr_re = ret / ret.shift(1).rolling(30, min_periods=30).std()
            if VSR_COL in df.columns:
                vsr = pd.to_numeric(df[VSR_COL], errors="coerce")
                vsr = vsr.where(vsr.notna(), vsr_re)
            else:
                vsr = vsr_re
            active = df["forecast"] != 0
            n_active += int(active.sum())
            agree = active & (vsr >= 1.0 - 1e-9) & (df["forecast"] > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("The situation is checked as the raw volatility-scaled 1-day return (recorded big_day value, "
               "recomputed from closes where missing) at least 1.0 with a positive forecast, the choppy-calm "
               "profile not being recomputable from the record; a case is the first long bet (forecast rise of at "
               "least 2 points from its low on the long side) in each non-overlapping 5-bar grid cell of a window, "
               "its forecast is the signal bar's forecast, and the t clusters cases by UTC day with a G/(G-1) correction.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean excess 5-day return of long cases", "value": None,
                             "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject, over at least 30 cases"},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with a one-day rise "
                           "of at least 1 std (vsr >= 1), the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. coin's mean 5-day return over all windows ----------
    coin_rets = {}
    for (coin, w), df in prepared.items():
        c = df["close"].values
        for p in range(0, len(c) - H, H):
            if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                coin_rets.setdefault(coin, []).append(c[p + H] / c[p] - 1.0)
    coin_mean = {k: float(np.mean(v)) for k, v in coin_rets.items() if len(v) > 0}

    # ---------- cases ----------
    cases = []  # (day, excess, forecast)
    for (coin, w), df in prepared.items():
        if coin not in coin_mean:
            continue
        f = df["forecast"].values
        c = df["close"].values
        bet = np.zeros(len(f), dtype=bool)
        low = 0.0
        prev_side = 0
        for i in range(len(f)):
            fi = f[i]
            side = 1 if fi > 0 else (-1 if fi < 0 else 0)
            if side != prev_side:
                low = 0.0
            if side == 1:
                if fi - low >= BAND:
                    bet[i] = True
                    low = fi
                else:
                    low = min(low, fi)
            elif side == -1:
                if (-fi) - low >= BAND:
                    low = -fi
                else:
                    low = min(low, -fi)
            else:
                low = 0.0
            prev_side = side
        n = len(f)
        for start in range(0, n, H):
            idx = [i for i in range(start, min(start + H, n)) if bet[i]]
            if not idx:
                continue
            t = idx[0]
            if t + H >= n:
                continue
            if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                continue
            r = c[t + H] / c[t] - 1.0
            cases.append((df["timestamp"].iloc[t].floor("D"), r - coin_mean[coin], float(f[t])))

    n_cases = len(cases)
    mean_ex = None
    tstat = None
    n_days = 0
    slope = None
    if n_cases > 0:
        cd = pd.DataFrame(cases, columns=["day", "ex", "fc"])
        mean_ex = float(cd["ex"].mean())
        n_days = int(cd["day"].nunique())
        dev = cd["ex"] - mean_ex
        D = dev.groupby(cd["day"]).sum().values
        G = len(D)
        if G > 1:
            var = (G / (G - 1)) * float(np.sum(D ** 2)) / (n_cases ** 2)
            if var > 0:
                tstat = float(mean_ex / np.sqrt(var))
        if n_cases >= 2 and cd["fc"].nunique() >= 2:
            x = cd["fc"].values
            y = cd["ex"].values
            xm = x - x.mean()
            slope = float(np.sum(xm * (y - y.mean())) / np.sum(xm ** 2))

    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n_cases}), the plan's minimum count, so the data could not show the idea."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t of the mean excess return could not be computed, so neither confirm nor reject is met."
    elif mean_ex > 0 and tstat >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "Mean excess 5-day return above 0 with t >= 2 over at least 30 cases, and the slope above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t with a slope at or below 0 (or not computable) is inconclusive."
    elif mean_ex < 0 and tstat <= -2:
        status = "rejected"
        decided = "Mean excess 5-day return below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "mean excess 5-day return of long cases over the coin's mean 5-day return",
            "value": mean_ex,
            "statistic": None if tstat is None else {"name": "t of the mean, cases of one day together", "value": tstat},
            "threshold": "above 0 with t >= 2 to confirm, below 0 with t <= -2 to reject, over at least 30 cases",
        },
        "supporting_check": {"name": "least-squares slope of excess 5-day return on forecast",
                             "value": slope, "passed": slope_pass},
        "counts": {"cases": int(n_cases), "days": int(n_days)},
        "decided_by": decided,
        "reading": reading,
    }
