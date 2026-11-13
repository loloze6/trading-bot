import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    NH = "debug_info.components.near_high.last_history_value"

    # ---------- per-coin mean 10-bar return over all its test windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            r = c.shift(-H) / c - 1.0
            rets.append(r.dropna().values)
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- situation check + collect cases ----------
    n_active = 0
    n_agree = 0
    hi_all = []          # excess returns, all bars with forecast >= 10
    hi_nonov = []        # excess returns, non-overlapping grid bars with forecast >= 10
    tr_fc = []
    tr_ex = []

    for coin, wins in bars.items():
        mu = coin_mean.get(coin, np.nan)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            reg = df["regime"].astype(str).str.strip().str.lower() if "regime" in df.columns \
                else pd.Series([""] * len(df))
            nh = pd.to_numeric(df[NH], errors="coerce") if NH in df.columns \
                else pd.Series([np.nan] * len(df))

            active = fc.notna() & (fc != 0)
            situ = (reg == "trending") & nh.notna() & (nh > 0)
            agree = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            c = df["close"].astype(float)
            fwd = c.shift(-H) / c - 1.0
            ex = fwd - mu
            pos = np.arange(len(df))
            grid = (pos % H) == 0

            m_hi = fc.notna() & (fc >= 10) & ex.notna()
            hi_all.extend(ex[m_hi].tolist())
            hi_nonov.extend(ex[m_hi & grid].tolist())

            m_tr = (reg == "trending") & fc.notna() & ex.notna()
            tr_fc.extend(fc[m_tr].tolist())
            tr_ex.extend(ex[m_tr].tolist())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("The situation is checked as regime == 'trending' (the detector's 200-SMA and 60-bar rules) "
               "with the raw 20-bar Donchian range position above 0 (upper half of the range) and a positive "
               "forecast; the coin's usual move is the mean of all its in-window 10-bar returns over all windows; "
               "the main value is the mean excess return over all bars with forecast >= 10, its t is the ordinary "
               "t of the mean over the non-overlapping grid bars (positions 0, 10, 20, ... of each window) with "
               "forecast >= 10, which are also the counted cases.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are trending bars in the upper "
                           "half of the 20-bar range with a long forecast, as the plan's situation requires."),
            "reading": reading,
        }

    hi_all = np.array(hi_all, dtype=float)
    hi_nonov = np.array(hi_nonov, dtype=float)
    n_cases = int(hi_nonov.size)

    mean_all = float(np.mean(hi_all)) if hi_all.size else None
    t_val = None
    if n_cases >= 2:
        sd = np.std(hi_nonov, ddof=1)
        if sd > 0:
            t_val = float(np.mean(hi_nonov) / (sd / np.sqrt(n_cases)))

    rho = None
    if len(tr_fc) >= 3 and np.std(tr_fc) > 0 and np.std(tr_ex) > 0:
        r, _ = stats.spearmanr(tr_fc, tr_ex)
        rho = float(r) if np.isfinite(r) else None
    sup = {"name": "Spearman rank correlation, forecast vs forward 10-bar excess return, trending bars",
           "value": rho, "passed": (None if rho is None else bool(rho > 0))}

    if n_cases < 30:
        status = "not observable"
        decided = (f"Only {n_cases} non-overlapping cases with forecast >= 10, below the plan's minimum of 30.")
    elif mean_all is not None and t_val is not None and mean_all > 0 and t_val >= 2:
        status = "confirmed"
        decided = "The mean excess 10-bar return after forecasts >= 10 is above 0 with t >= 2 and at least 30 non-overlapping cases."
    elif mean_all is not None and t_val is not None and mean_all < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean excess 10-bar return after forecasts >= 10 is below 0 with t <= -2 and at least 30 non-overlapping cases."
    else:
        status = "inconclusive"
        decided = "With at least 30 non-overlapping cases, the t-statistic lies between -2 and 2 (or does not agree with the mean's sign), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean forward 10-bar excess return after forecast >= 10",
            "value": mean_all,
            "statistic": (None if t_val is None else {"name": "t of the mean, non-overlapping samples", "value": t_val}),
            "threshold": "confirm if mean > 0 with t >= 2, reject if mean < 0 with t <= -2, at least 30 non-overlapping cases",
        },
        "supporting_check": sup,
        "counts": {
            "non-overlapping cases with forecast >= 10": n_cases,
            "bars with forecast >= 10": int(hi_all.size),
            "trending bars": int(len(tr_fc)),
        },
        "decided_by": decided,
        "reading": reading,
    }
