import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.dip.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan situation: trending regime (20- and 60-bar changes both > 0) and a
    # one-day drop of any size (graded). The expected side is long.
    active_total = 0
    active_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            r1_price = close / close.shift(1) - 1.0
            if LHV in df.columns:
                r1 = pd.to_numeric(df[LHV], errors="coerce")
                r1 = r1.where(r1.notna(), r1_price)
            else:
                r1 = r1_price
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            active = fc.notna() & (fc != 0)
            situ = (regime == "trending") & (r1 < 0) & (fc > 0)
            active_total += int(active.sum())
            active_ok += int((active & situ).sum())

    agreement = float(active_ok / active_total) if active_total > 0 else 0.0
    passed = active_total > 0 and agreement >= 0.9
    threshold_words = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; at least 30 non-overlapping cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean excess return close t+1 to close t+3 after top-decile forecasts",
                             "value": None, "statistic": None, "threshold": threshold_words},
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": "Fewer than 90% of active bars are long bars in the trending regime after a one-day drop, as the Fidelity situation requires.",
            "reading": "Situation checked as regime == 'trending', a negative one-bar return (dip raw value, or price if missing) and a positive forecast.",
        }

    # ---------- 2. Criterion ----------
    # coin mean 2-bar and 3-bar returns, pooled over all windows of the coin
    coin_mean2, coin_mean3 = {}, {}
    pos_fc = []
    for coin, wins in bars.items():
        r2_all, r3_all = [], []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            r2_all.append((close.shift(-2) / close - 1.0).dropna())
            r3_all.append((close.shift(-3) / close - 1.0).dropna())
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            pos_fc.extend(fc[fc > 0].dropna().tolist())
        r2c = pd.concat(r2_all) if r2_all else pd.Series(dtype=float)
        r3c = pd.concat(r3_all) if r3_all else pd.Series(dtype=float)
        coin_mean2[coin] = float(r2c.mean()) if len(r2c) else np.nan
        coin_mean3[coin] = float(r3c.mean()) if len(r3c) else np.nan

    n_pos = len(pos_fc)
    cut = float(np.quantile(pos_fc, 0.9)) if n_pos > 0 else np.inf

    main_cases, sup_cases = [], []
    n_top = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ex23 = (close.shift(-3) / close.shift(-1) - 1.0) - coin_mean2[coin]
            ex3 = (close.shift(-3) / close - 1.0) - coin_mean3[coin]
            idx = [i for i in range(len(df)) if fc.iloc[i] > 0 and fc.iloc[i] >= cut]
            n_top += len(idx)
            idx = [i for i in idx if np.isfinite(ex23.iloc[i])]
            # merge cases within 3 bars of each other (chained), inside the window
            clusters = []
            for i in idx:
                if clusters and i - clusters[-1][-1] <= 3:
                    clusters[-1].append(i)
                else:
                    clusters.append([i])
            for cl in clusters:
                main_cases.append(float(np.mean([ex23.iloc[i] for i in cl])))
                v3 = [ex3.iloc[i] for i in cl if np.isfinite(ex3.iloc[i])]
                if v3:
                    sup_cases.append(float(np.mean(v3)))

    n_cases = len(main_cases)
    mean_ex = float(np.mean(main_cases)) if n_cases else None
    if n_cases >= 2:
        sd = float(np.std(main_cases, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else (float(np.sign(mean_ex)) * np.inf if mean_ex != 0 else 0.0)
    else:
        t = None
    sup_val = float(np.mean(sup_cases)) if sup_cases else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases, fewer than the plan's minimum of 30."
    elif mean_ex > 0 and t is not None and t >= 2:
        status = "confirmed"
        decided = "The mean excess return over days 2-3 is above 0 with t >= 2."
    elif mean_ex < 0 and t is not None and t <= -2:
        status = "rejected"
        decided = "The mean excess return over days 2-3 is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, which the plan calls inconclusive."

    if t is not None and not np.isfinite(t):
        t = float(np.sign(t) * 1e12)

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean excess return close t+1 to close t+3 after top-decile forecasts",
                         "value": mean_ex,
                         "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
                         "threshold": threshold_words},
        "supporting_check": {"name": "mean 3-bar excess return close t to t+3 vs coin mean 3-bar return",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"non-overlapping cases": int(n_cases), "top-decile bars": int(n_top),
                   "positive forecasts": int(n_pos)},
        "decided_by": decided,
        "reading": "Top decile is forecast >= the 90th percentile of all pooled positive forecasts (ties included); coin mean 2- and 3-bar returns use every bar of every window of the coin; cases on the same coin and window are chained into one case when within 3 bars of the previous case, and the case value is the mean of its members' excess returns.",
    }
