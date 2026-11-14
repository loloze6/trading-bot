import numpy as np
import pandas as pd


def measure(bars):
    DIP = "debug_info.components.dip.last_history_value"
    H = 3

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            price_ret = close / close.shift(1) - 1.0
            if DIP in df.columns:
                r1 = pd.to_numeric(df[DIP], errors="coerce").where(
                    lambda s: s.notna(), price_ret)
            else:
                r1 = price_ret
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            active = fc.notna() & (fc != 0)
            situation = (regime == "trending") & (r1 < 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess return close t+1 to close t+3 after top-decile positive forecasts"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; at least 30 non-overlapping cases"
    reading = ("Situation = regime 'trending' and a negative one-bar return (dip raw value, else close-to-close) with a long forecast; "
               "top decile = positive forecasts >= the 90th percentile of all positive forecasts pooled (ties included); "
               "coin mean 2-bar and 3-bar returns are over every bar of all its windows, inside windows; "
               "cases on the same coin and window whose bars are <= 3 apart are chained into one case whose excess is the mean of its members.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are trending-regime down-day bars with a long forecast, "
                           "so the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. Coin mean returns ----------
    coin_m2, coin_m3 = {}, {}
    for coin, wins in bars.items():
        r2s, r3s = [], []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            r2s.append((c.shift(-2) / c - 1.0).dropna())
            r3s.append((c.shift(-3) / c - 1.0).dropna())
        r2 = pd.concat(r2s) if r2s else pd.Series(dtype=float)
        r3 = pd.concat(r3s) if r3s else pd.Series(dtype=float)
        coin_m2[coin] = float(r2.mean()) if len(r2) else np.nan
        coin_m3[coin] = float(r3.mean()) if len(r3) else np.nan

    # ---------- 3. Top-decile threshold ----------
    pos = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            pos.append(fc[fc > 0].dropna())
    pos = pd.concat(pos) if pos else pd.Series(dtype=float)
    if len(pos) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean 3-bar excess return, close t to t+3", "value": None, "passed": None},
            "counts": {"non-overlapping cases": 0},
            "decided_by": "No positive forecasts, so fewer than 30 non-overlapping cases.",
            "reading": reading,
        }
    q90 = float(np.quantile(pos.values, 0.9))

    # ---------- 4. Cases ----------
    ex23_cases, ex3_cases = [], []
    n_raw = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            c = pd.to_numeric(df["close"], errors="coerce")
            r23 = c.shift(-3) / c.shift(-1) - 1.0
            r3 = c.shift(-3) / c - 1.0
            sel = (fc > 0) & (fc >= q90) & r23.notna() & r3.notna()
            idx = list(np.where(sel.values)[0])
            n_raw += len(idx)
            clusters = []
            for i in idx:
                if clusters and i - clusters[-1][-1] <= H:
                    clusters[-1].append(i)
                else:
                    clusters.append([i])
            for cl in clusters:
                ex23_cases.append(float(np.mean([r23.iloc[i] - coin_m2[coin] for i in cl])))
                ex3_cases.append(float(np.mean([r3.iloc[i] - coin_m3[coin] for i in cl])))

    ex23 = np.array([x for x in ex23_cases if np.isfinite(x)])
    ex3 = np.array([x for x in ex3_cases if np.isfinite(x)])
    n = int(len(ex23))

    mean23 = float(ex23.mean()) if n > 0 else None
    t23 = None
    if n > 1:
        sd = float(ex23.std(ddof=1))
        t23 = float(mean23 / (sd / np.sqrt(n))) if sd > 0 else None
    mean3 = float(ex3.mean()) if len(ex3) > 0 else None
    sup_pass = (mean3 > 0) if mean3 is not None else None

    counts = {"non-overlapping cases": n, "top-decile bars before merging": int(n_raw)}

    if n < 30:
        status = "not observable"
        decided = f"Only {n} non-overlapping cases, fewer than the plan's minimum of 30."
    elif t23 is not None and mean23 > 0 and t23 >= 2:
        status = "confirmed"
        decided = "The mean excess return over days 2-3 is above 0 with t >= 2."
    elif t23 is not None and mean23 < 0 and t23 <= -2:
        status = "rejected"
        decided = "The mean excess return over days 2-3 is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic of the days 2-3 excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean23,
            "statistic": {"name": "t of the mean", "value": t23} if t23 is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean 3-bar excess return (close t to t+3) vs coin mean 3-bar return, should be > 0",
            "value": mean3,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
