import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    DIP = "debug_info.components.dip.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan situation: regime trending (20- and 60-day returns both > 0) and a daily drop
    # (graded size, so any negative one-day return); outcome is a rise, so the side is long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df[FC], errors="coerce")
            ret1 = df["close"].astype(float).pct_change()
            if DIP in df.columns:
                drop = pd.to_numeric(df[DIP], errors="coerce").fillna(ret1)
            else:
                drop = ret1
            active = fc.notna() & (fc != 0)
            trending = df["regime"].astype(str).str.lower() == "trending"
            ok = active & trending & (drop < 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess return close t+1 to close t+3 after top-decile positive forecasts"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; fewer than 30 non-overlapping cases is not observable"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars are long forecasts on trending-regime bars with a negative one-day return, so the config does not do what the plan's situation says.",
            "reading": "Situation taken as regime == 'trending' and a negative dip component value (one-bar return), side long.",
        }

    # ---------- 2. Coin means over all windows together ----------
    coin_m2, coin_m3 = {}, {}
    for coin, wins in bars.items():
        r2_all, r3_all = [], []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            r2_all.append((c.shift(-2) / c - 1).dropna())
            r3_all.append((c.shift(-3) / c - 1).dropna())
        r2 = pd.concat(r2_all) if r2_all else pd.Series(dtype=float)
        r3 = pd.concat(r3_all) if r3_all else pd.Series(dtype=float)
        coin_m2[coin] = float(r2.mean()) if len(r2) else np.nan
        coin_m3[coin] = float(r3.mean()) if len(r3) else np.nan

    # ---------- 3. Top decile of positive forecasts, pooled ----------
    pos = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df[FC], errors="coerce")
            pos.append(fc[fc > 0].values)
    pos = np.concatenate(pos) if pos else np.array([])
    if len(pos) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping cases": 0},
            "decided_by": "There are no positive forecasts, so fewer than 30 non-overlapping cases.",
            "reading": "none",
        }
    q90 = float(np.quantile(pos, 0.9))

    cases_23, cases_3 = [], []
    n_raw = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce")
            r23 = c.shift(-3) / c.shift(-1) - 1
            r3 = c.shift(-3) / c - 1
            idx = [i for i in range(len(df))
                   if pd.notna(fc.iloc[i]) and fc.iloc[i] > 0 and fc.iloc[i] >= q90
                   and pd.notna(r23.iloc[i]) and pd.notna(r3.iloc[i])]
            n_raw += len(idx)
            # merge cases within 3 bars of each other (chained) into one case
            clusters = []
            for i in idx:
                if clusters and i - clusters[-1][-1] <= 3:
                    clusters[-1].append(i)
                else:
                    clusters.append([i])
            for cl in clusters:
                e23 = float(np.mean([r23.iloc[i] for i in cl])) - coin_m2[coin]
                e3 = float(np.mean([r3.iloc[i] for i in cl])) - coin_m3[coin]
                if np.isfinite(e23):
                    cases_23.append(e23)
                if np.isfinite(e3):
                    cases_3.append(e3)

    n = len(cases_23)
    a = np.array(cases_23)
    mean = float(a.mean()) if n > 0 else None
    if n > 1 and a.std(ddof=1) > 0:
        t = float(a.mean() / (a.std(ddof=1) / np.sqrt(n)))
    else:
        t = None
    b = np.array(cases_3)
    sup_val = float(b.mean()) if len(b) > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    reading = ("Top decile = positive forecasts at or above the pooled 90th percentile of positive forecasts; "
               "the coin's mean 2-bar (and 3-bar) return is taken over every bar of all its windows pooled, each return inside one window; "
               "cases on the same coin and window whose bars are at most 3 apart are chained into one case whose value is the mean of its members' excess returns; "
               "t is the ordinary t of the mean.")

    if n < 30:
        status = "not observable"
        decided = f"Only {n} non-overlapping cases, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so it does not meet confirm or reject."
    elif mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean excess return over days 2-3 is above 0 with t >= 2."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean excess return over days 2-3 is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean 3-bar excess return close t to t+3 vs coin mean 3-bar return, > 0",
            "value": sup_val,
            "passed": None if sup_pass is None else bool(sup_pass),
        },
        "counts": {"non-overlapping cases": int(n), "top-decile bars before merging": int(n_raw)},
        "decided_by": decided,
        "reading": reading,
    }
