import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 21
    RAW = "debug_info.components.month_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            reg = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * len(d))
            raw = pd.to_numeric(d[RAW], errors="coerce").values if RAW in d.columns else np.full(len(d), np.nan)
            n = len(d)
            for i in range(n):
                if fc[i] == 0 or not np.isfinite(fc[i]):
                    continue
                n_active += 1
                # choppy regime: 60-day percent return in [-10, 10]
                if i >= 60 and np.isfinite(close[i]) and np.isfinite(close[i - 60]) and close[i - 60] != 0:
                    tr60 = (close[i] / close[i - 60] - 1.0) * 100.0
                    choppy = (-10.0 <= tr60 <= 10.0)
                else:
                    choppy = (reg[i] == "mean_reversion")
                # 30-day fall
                if np.isfinite(raw[i]):
                    fall = raw[i] < 0
                elif i >= 30 and np.isfinite(close[i]) and np.isfinite(close[i - 30]) and close[i - 30] != 0:
                    fall = (close[i] / close[i - 30] - 1.0) < 0
                else:
                    fall = False
                if choppy and fall and fc[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-direction 21-bar excess return of the deepest fifth of negative-forecast grid cases"
    main_thr = "mean above 0 with day-clustered t >= 2 confirms (with check); t <= -2 rejects"
    sup_name = "deepest fifth minus rest, short-direction excess return, Welch t >= 1"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are short bars in a choppy market "
                          "(60-day return between -10 % and +10 %) with the close below its close of 30 days earlier.",
            "reading": "Choppy regime recomputed from the 60-day close return where the window holds 60 prior bars, "
                       "otherwise taken from the recorded regime; the 30-day fall from the raw month_fall value.",
        }

    # ---------- 2. criterion ----------
    cases = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    coin_cases.append((coin, ts.iloc[i].floor("D"), float(fc[i]), r))
        if len(coin_rets) == 0:
            continue
        drift = float(np.mean(coin_rets))
        for (c, day, f, r) in coin_cases:
            cases.append({"coin": c, "day": day, "forecast": f, "excess": -(r - drift)})

    n_cases = len(cases)
    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"negative-forecast cases": 0, "deepest-fifth cases": 0, "distinct days among deepest-fifth cases": 0},
            "decided_by": "The minimum of 30 distinct days among the deepest-fifth cases is not reached (no cases).",
            "reading": "none",
        }

    cdf = pd.DataFrame(cases)
    cdf = cdf.sort_values(["forecast", "day", "coin"], kind="mergesort").reset_index(drop=True)
    k = int(np.ceil(n_cases / 5.0))
    deep = cdf.iloc[:k]
    rest = cdf.iloc[k:]

    n_days = int(deep["day"].nunique())
    mean_deep = float(deep["excess"].mean())

    # day-clustered t
    dev = deep["excess"] - mean_deep
    S = dev.groupby(deep["day"]).sum().values
    D = len(S)
    t_main = None
    if D >= 2 and k >= 2:
        var_sum = float(np.sum(S ** 2)) * D / (D - 1)
        se = np.sqrt(var_sum) / k
        if se > 0:
            t_main = float(mean_deep / se)

    # supporting check: Welch t deepest minus rest
    t_sup = None
    if len(deep) >= 2 and len(rest) >= 2:
        tt = stats.ttest_ind(deep["excess"].values, rest["excess"].values, equal_var=False)
        if np.isfinite(tt.statistic):
            t_sup = float(tt.statistic)
    sup_pass = (t_sup is not None and t_sup >= 1.0)

    counts = {
        "negative-forecast cases": int(n_cases),
        "deepest-fifth cases": int(k),
        "distinct days among deepest-fifth cases": n_days,
        "rest cases": int(len(rest)),
    }

    if n_days < 30:
        status = "not observable"
        decided = f"The minimum of 30 distinct days among the deepest-fifth cases is not reached ({n_days})."
    elif t_main is None:
        status = "inconclusive"
        decided = "The deepest fifth's t could not be computed; no confirm or reject rule is met."
    elif mean_deep > 0 and t_main >= 2.0 and sup_pass:
        status = "confirmed"
        decided = "Deepest fifth's mean short-direction excess return is above 0 with t >= 2 and the deepest-minus-rest Welch t is >= 1."
    elif t_main <= -2.0:
        status = "rejected"
        decided = "Deepest fifth's mean short-direction excess return has t <= -2: the deepest falls rise more than the coin's drift."
    elif mean_deep > 0 and t_main >= 2.0:
        status = "inconclusive"
        decided = "Confirming main measure (mean > 0, t >= 2) but the supporting check failed (Welch t < 1)."
    else:
        status = "inconclusive"
        decided = "The deepest fifth's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_deep,
            "statistic": None if t_main is None else {"name": "t of the mean, cases summed per day", "value": t_main},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": t_sup, "passed": bool(sup_pass) if t_sup is not None else None},
        "counts": counts,
        "decided_by": decided,
        "reading": "The deepest fifth is the ceil(n/5) negative-forecast grid cases with the most negative forecast "
                   "(ties broken by day then coin), the normal drift is each coin's mean non-overlapping 21-bar return "
                   "over all its windows, the supporting Welch t is on individual cases, and fewer than 30 days gives "
                   "'not observable'.",
    }
