import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    PERIOD = 20
    RAW = "debug_info.components.swings_above_high.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            prior_high = high.shift(1).rolling(PERIOD, min_periods=PERIOD).max()
            sit_price = close > prior_high
            known_price = prior_high.notna() & close.notna()
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            sit_raw = raw > 0
            situation = np.where(known_price, sit_price,
                                 np.where(raw.notna(), sit_raw, False)).astype(bool)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean 5-day excess return over the coin's mean 5-day return, cases with forecast > 0"
    thr = "confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2"
    reading = ("Situation recomputed from prices as close above the max high of the 20 prior bars in the window "
               "(falling back to the recorded raw component > 0 on the first 20 bars), expected side long; "
               "cases are grid bars 0,5,10,... of each window with forecast > 0 and a 5-bar return inside the window; "
               "the coin's mean 5-day return is taken on the same non-overlapping grids of all its windows; "
               "the day-clustered t sums deviations per calendar day (UTC) with a D/(D-1) correction; "
               "the plan's minimum of 100 cases on 60 days, when not reached, gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0, "distinct days": 0},
            "decided_by": ("Fewer than 90% of bars with a nonzero forecast are long bars with the close above the "
                           "prior 20-day high, as the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if fc[i] > 0:
                    rows.append((coin, ts.iloc[i].floor("D"), float(fc[i]), r))
        coin_rets[coin] = float(np.mean(allr)) if allr else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "day", "fc", "r"])
    if len(cases):
        cases["ex"] = cases["r"] - cases["coin"].map(coin_rets)
        cases = cases.dropna(subset=["ex"])
    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0

    mean_ex = float(cases["ex"].mean()) if n else None
    t = None
    if n >= 2 and n_days >= 2:
        dev = cases["ex"] - mean_ex
        S = dev.groupby(cases["day"]).sum().values
        var = (n_days / (n_days - 1.0)) * np.sum(S ** 2) / (n ** 2)
        se = float(np.sqrt(var))
        t = float(mean_ex / se) if se > 0 else None
    rho = None
    if n >= 3 and cases["fc"].nunique() > 1 and cases["ex"].nunique() > 1:
        rho = float(stats.spearmanr(cases["fc"], cases["ex"]).correlation)
    sup_pass = None if rho is None or not np.isfinite(rho) else bool(rho > 0)

    counts = {"cases": n, "distinct days": n_days, "active bars": int(n_active)}

    if n < 100 or n_days < 60:
        status = "not observable"
        decided = f"The plan's minimum of 100 cases on at least 60 distinct days is not reached ({n} cases, {n_days} days)."
    elif t is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean excess return above 0 with t >= 2 and Spearman correlation above 0 (confirm rule)."
    elif mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess return below 0 with t <= -2 (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the Spearman correlation is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean_ex,
                         "statistic": None if t is None else {"name": "t of the mean, cases of one day together", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "Spearman correlation forecast vs 5-day excess return > 0",
                             "value": rho, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
