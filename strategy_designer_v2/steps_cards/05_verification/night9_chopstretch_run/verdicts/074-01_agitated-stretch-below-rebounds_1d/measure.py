import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.stretch_below.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: agitated profile (regime not vetoed to "chop") and close below its 20-day SMA (raw distance < 0).
    # Expected side: long (forecast > 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            agitated = df["regime"].notna() & (regime.str.lower() != "chop")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            below = raw.notna() & (raw < 0)
            situ = agitated & below & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 1.0
    passed = bool(agreement >= 0.9)

    reading = ("Agitated profile read as a regime other than 'chop' (the config's veto of volatility percentile <= 0.5), "
               "below the average as raw distance < 0; slope from an OLS of each grid case's unusual 10-bar return on its "
               "forecast pooled over coins and windows, with a t from standard errors clustered by calendar day; drift is "
               "each coin's mean non-overlapping 10-bar return over all its windows; the plan's minimum of 30 cases is "
               "applied as 'not observable' per the workflow's rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars in the agitated profile "
                           "with the close below its 20-day average, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []  # (coin, day, forecast, ret)
    drift = {}
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0 and not pd.isna(ts.iloc[i]):
                    coin_cases.append((coin, ts.iloc[i].floor("D"), float(fc[i]), r))
        if coin_rets:
            drift[coin] = float(np.mean(coin_rets))
            for (c, d, f, r) in coin_cases:
                rows.append((c, d, f, r - drift[coin]))

    n_cases = len(rows)
    days = sorted(set(r[1] for r in rows))
    n_days = len(days)

    slope = None
    t_slope = None
    mean_unusual = None
    if n_cases >= 3:
        f = np.array([r[2] for r in rows], dtype=float)
        y = np.array([r[3] for r in rows], dtype=float)
        mean_unusual = float(np.mean(y))
        X = np.column_stack([np.ones(n_cases), f])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            bread = np.linalg.inv(XtX)
            beta = bread @ X.T @ y
            e = y - X @ beta
            slope = float(beta[1])
            day_idx = {d: k for k, d in enumerate(days)}
            g = np.array([day_idx[r[1]] for r in rows])
            G = len(days)
            meat = np.zeros((2, 2))
            for k in range(G):
                m = g == k
                s = X[m].T @ e[m]
                meat += np.outer(s, s)
            if G > 1 and n_cases > 2:
                corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - 2.0))
                V = corr * bread @ meat @ bread
                se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
                t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None
    elif n_cases > 0:
        mean_unusual = float(np.mean([r[3] for r in rows]))

    support_passed = None if mean_unusual is None else bool(mean_unusual > 0)

    counts = {"non-overlapping grid cases with a forecast above 0": int(n_cases),
              "days the cases fall on": int(n_days)}

    if n_cases < 30:
        status = "not observable"
        decided_by = (f"Only {n_cases} non-overlapping grid cases with a forecast above 0, below the plan's minimum of 30.")
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed (degenerate forecasts or a single day), so neither rule is met."
    elif t_slope >= 2 and support_passed:
        status = "confirmed"
        decided_by = "The slope has t >= 2 and the mean unusual move is above 0 (confirm rule)."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope has t >= 2 but the mean unusual move is at or below 0 (inconclusive rule)."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope has t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided_by = "The slope has t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "slope of 10-bar unusual forward return on forecast, grid bars with forecast > 0",
            "value": slope,
            "statistic": None if t_slope is None else {"name": "t of slope, same-day cases pooled (clustered by day)",
                                                       "value": t_slope},
            "threshold": "confirm if t >= 2 (with mean unusual move > 0); reject if t <= -2; else inconclusive",
        },
        "supporting_check": {"name": "mean unusual 10-bar move over the same grid bars above 0",
                             "value": mean_unusual, "passed": support_passed},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
