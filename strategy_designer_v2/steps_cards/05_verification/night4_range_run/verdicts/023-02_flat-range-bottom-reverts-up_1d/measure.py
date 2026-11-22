import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.below_mid.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            # raw distance from midpoint of 30-bar high-low range (percent of close)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            hh = df["high"].rolling(30, min_periods=30).max()
            ll = df["low"].rolling(30, min_periods=30).min()
            mid = (hh + ll) / 2.0
            raw_px = (df["close"] - mid) / df["close"] * 100.0
            raw = raw.where(raw.notna(), raw_px)
            regime_ok = df["regime"].astype(str) == "mean_reversion"
            active = fc.notna() & (fc != 0)
            situ = regime_ok & (raw < 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean excess 5-bar forward return of cases with forecast > 0 (minus coin's normal 5-bar drift)"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; fewer than 30 independent cases is inconclusive/not observable"
    reading = ("Situation is taken as regime == 'mean_reversion' (the detector's recorded decision for NMR(30) <= 0.3) "
               "and raw below_mid value < 0 (close below the 30-bar midpoint), long side; the forecast halves split the "
               "cases sorted by forecast into the top and bottom floor(n/2), dropping the middle case when n is odd; "
               "normal drift is the mean of the coin's non-overlapping 5-bar grid returns over all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent cases": None},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the regime is "
                           "mean_reversion and the close is below the 30-bar range midpoint."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_ret, case_coin, case_fc = [], [], []
    drift = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[j]) and close[i] != 0):
                    continue
                r = close[j] / close[i] - 1.0
                all_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    case_ret.append(r)
                    case_coin.append(coin)
                    case_fc.append(float(fc[i]))
        drift[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    ex = np.array([r - drift[c] for r, c in zip(case_ret, case_coin)], dtype=float)
    fcs = np.array(case_fc, dtype=float)
    ok = np.isfinite(ex)
    ex, fcs = ex[ok], fcs[ok]
    n_cases = int(len(ex))

    mean_ex = float(np.mean(ex)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(ex, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val, sup_pass = None, None
    if n_cases >= 2:
        order = np.argsort(-fcs, kind="mergesort")
        half = n_cases // 2
        top = ex[order[:half]]
        bot = ex[order[n_cases - half:]]
        sup_val = float(np.mean(top) - np.mean(bot))
        sup_pass = bool(sup_val > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, fewer than the plan's minimum of 30."
    elif t is not None and mean_ex > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean excess 5-bar return above 0 with t >= 2 and the larger-forecast half beats the smaller half."
    elif t is not None and mean_ex > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the larger-forecast half does not beat the smaller-forecast half."
    elif t is not None and mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess 5-bar return below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (or could not be computed)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess return of larger-forecast half minus smaller-forecast half",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"independent cases": n_cases, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
