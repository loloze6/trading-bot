import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    FC = "forecast"
    RAW = "debug_info.components.vol_ratio.last_history_value"

    def ts_day(s):
        t = pd.to_datetime(s, utc=True, errors="coerce")
        return t.dt.floor("D")

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce")
            run6 = close / close.shift(6) - 1.0
            # where the 6-bar return cannot be computed inside the window, fall back to the recorded regime
            reg_tr = d["regime"].astype(str) == "trending" if "regime" in d.columns else pd.Series(False, index=d.index)
            situ = pd.Series(np.where(run6.notna(), run6 > 0, reg_tr), index=d.index).astype(bool)
            active = fc.notna() & (fc != 0)
            agree = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The 6-day rise is recomputed as close[t]/close[t-6]-1 > 0 inside each window (the recorded regime "
               "is used only for a window's first 6 bars), the long side is forecast > 0; the regime grid cases are "
               "rows with regime == 'trending' at positions 0,3,6,... of each window with a 3-bar forward return in the "
               "window, the coin's mean 3-bar return is taken over all grid bars of all its windows, and the slope's t "
               "uses OLS with standard errors clustered by UTC day (residual-score sums per day, G/(G-1) correction).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of 3-bar excess return on forecast, trending grid bars",
                             "value": None, "statistic": None,
                             "threshold": "slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars during a positive "
                           "6-day close-to-close return, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            reg = d["regime"].astype(str).values
            day = ts_day(d["timestamp"]).values
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_grid_rets.append(r)
                if reg[i] == "trending" and np.isfinite(fc[i]):
                    coin_rows.append((coin, day[i], fc[i], r))
        if len(coin_grid_rets) == 0:
            continue
        mu = float(np.mean(coin_grid_rets))
        for (c, dy, f, r) in coin_rows:
            rows.append({"coin": c, "day": dy, "f": float(f), "ex": r - mu})

    tab = pd.DataFrame(rows, columns=["coin", "day", "f", "ex"])
    n_cases = int(len(tab))
    n_pos = int((tab["f"] > 0).sum()) if n_cases else 0
    n_zero = int((tab["f"] == 0).sum()) if n_cases else 0
    n_days = int(tab["day"].nunique()) if n_cases else 0
    counts = {"regime grid cases": n_cases, "regime grid cases with forecast > 0": n_pos,
              "regime grid cases with forecast = 0": n_zero, "days": n_days}

    slope = None
    t = None
    if n_cases >= 3:
        x = tab["f"].values
        y = tab["ex"].values
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        if sxx > 0:
            slope = float(np.sum(xc * (y - y.mean())) / sxx)
            a = y.mean() - slope * x.mean()
            e = y - a - slope * x
            score = pd.Series(xc * e).groupby(tab["day"].values).sum().values
            G = len(score)
            if G > 1:
                var = (G / (G - 1)) * float(np.sum(score ** 2)) / sxx ** 2
                if var > 0:
                    t = float(slope / np.sqrt(var))

    diff = None
    if n_pos > 0 and n_zero > 0:
        diff = float(tab.loc[tab["f"] > 0, "ex"].mean() - tab.loc[tab["f"] == 0, "ex"].mean())
    sup_pass = None if diff is None else bool(diff > 0)

    if n_cases < 200:
        status = "not observable"
        decided = f"Only {n_cases} regime grid cases, below the plan's minimum of 200: no verdict."
    elif n_pos < 60:
        status = "not observable"
        decided = f"Only {n_pos} regime grid cases with forecast > 0, below the plan's minimum of 60: no verdict."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the heavy-minus-light excess difference is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the heavy-minus-light excess difference is not above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: more volume during a 6-day rise is followed by a smaller 3-day excess return."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "slope of 3-bar excess return on forecast, trending grid bars",
                         "value": slope,
                         "statistic": None if t is None else {"name": "slope t, cases of one day summed (day-clustered)", "value": t},
                         "threshold": "slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject"},
        "supporting_check": {"name": "mean excess 3-bar return, forecast > 0 minus forecast = 0",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
