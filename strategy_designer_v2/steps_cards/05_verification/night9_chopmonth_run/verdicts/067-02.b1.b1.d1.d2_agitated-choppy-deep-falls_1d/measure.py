import numpy as np
import pandas as pd


def measure(bars):
    H = 21
    LH = "debug_info.components.month_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if LH in df.columns:
                raw = pd.to_numeric(df[LH], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            recomputed = (close / close.shift(30) - 1.0) * 100.0
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            situ = (raw < 0) & (fc < 0)
            n_agree += int((active & situ).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = bool(agreement >= 0.9)
    else:
        agreement = None
        passed = None

    if passed is False:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars whose close "
                           "sits below its close of 30 days earlier, as the Fidelity's situation requires."),
            "reading": "The situation is a negative raw 30-day return (last_history_value, recomputed from closes where missing) with a negative forecast.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                coin_cases.append((r, fc[i], ts.iloc[i].floor("D")))
        if not coin_rets:
            continue
        drift = float(np.mean(coin_rets))
        for r, f, day in coin_cases:
            if not np.isfinite(f):
                continue
            rows.append({"coin": coin, "day": day, "f": f, "x": -(r - drift)})

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "x"])
    deep = cases[cases["f"] <= -10]
    shallow = cases[(cases["f"] < 0) & (cases["f"] > -10)]
    n_deep = int(len(deep))
    n_shallow = int(len(shallow))
    n_days = int(deep["day"].nunique()) if n_deep else 0

    mean_deep = float(deep["x"].mean()) if n_deep else None
    mean_shallow = float(shallow["x"].mean()) if n_shallow else None

    t = None
    if n_deep >= 2 and n_days >= 2:
        dev = deep["x"] - mean_deep
        S = dev.groupby(deep["day"]).sum().values
        K = len(S)
        var = (S ** 2).sum() / (n_deep ** 2) * (K / (K - 1))
        se = np.sqrt(var)
        t = float(mean_deep / se) if se > 0 else None

    if mean_deep is not None and mean_shallow is not None:
        sup_val = mean_deep - mean_shallow
        sup_pass = bool(sup_val > 0)
    else:
        sup_val = None
        sup_pass = None

    if n_deep < 20:
        status = "not observable"
        decided = f"Fewer than 20 deep cases (forecast -10 or below) on the 21-bar grid: {n_deep}."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the deep cases' mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_deep > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("Deep cases' mean short-direction excess move is above 0 with t of 2 or more, and it is larger "
                       "than the shallow cases' mean.")
        else:
            status = "inconclusive"
            decided = "A confirming t whose supporting check (deep mean larger than shallow mean) fails is inconclusive."
    elif mean_deep < 0 and t <= -2:
        status = "rejected"
        decided = ("Deep cases' mean short-direction excess move is below 0 with t of -2 or less: the coin rises "
                   "more than its drift after deep falls.")
    else:
        status = "inconclusive"
        decided = "The t of the deep cases' mean lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None),
                            "passed": passed},
        "main_measure": {
            "name": "mean short-direction 21-bar excess move of deep cases (forecast <= -10)",
            "value": mean_deep,
            "statistic": ({"name": "t of the mean, cases summed per day", "value": t} if t is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2; at least 20 deep cases",
        },
        "supporting_check": {
            "name": "deep mean minus shallow mean short-direction excess move (> 0 passes)",
            "value": (float(sup_val) if sup_val is not None else None),
            "passed": sup_pass,
        },
        "counts": {"deep cases": n_deep, "days of deep cases": n_days, "shallow cases": n_shallow,
                   "active bars": int(n_active)},
        "decided_by": decided,
        "reading": ("Grid bars are positions 0, 21, 42, ... of each window with a full 21-bar return inside it; "
                    "the coin's drift is the mean of all its grid returns over all its windows; the day t uses "
                    "per-day sums of deviations from the case mean with a K/(K-1) correction; the situation is a "
                    "negative raw 30-day return with a negative forecast; fewer than 20 deep cases is reported as "
                    "not observable."),
    }
