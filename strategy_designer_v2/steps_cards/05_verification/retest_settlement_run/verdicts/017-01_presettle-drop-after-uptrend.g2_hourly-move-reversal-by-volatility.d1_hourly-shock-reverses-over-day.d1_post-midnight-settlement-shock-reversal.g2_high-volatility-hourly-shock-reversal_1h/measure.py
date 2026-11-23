import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.fade.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            r1 = close.pct_change()
            sd24 = r1.rolling(24, min_periods=24).std()
            sd720 = r1.rolling(720, min_periods=720).std()
            volratio = sd24 / sd720
            regime_mr = (df["regime"].astype(str) == "mean_reversion")
            # Use the recomputed vol ratio where enough in-window history exists, else the detector's recorded decision.
            hv = pd.Series(np.where(volratio.notna(), volratio > 1.0, regime_mr), index=df.index).astype(bool)
            # Raw fade value: recorded where present, else recomputed from prices.
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw_re = r1 / sd24
            raw = raw.where(raw.notna(), raw_re)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            expected_sign = -np.sign(raw)
            ok = hv & (np.sign(fc) == expected_sign) & (expected_sign != 0)
            n_active += int(active.sum())
            n_agree += int((ok & active).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of excess 24-bar return on forecast (grid cases, pooled)"
    threshold = "confirm: slope > 0 with t >= 2 and support passes; reject: slope < 0 with t <= -2; else inconclusive; minimum 300 grid cases"
    reading = ("Situation bars use the 24/720-bar return-std ratio recomputed from in-window closes (falling back to the "
               "recorded regime where fewer than 720 prior returns exist) and the expected side is minus the sign of the "
               "raw fade value; the coin's mean 24-bar return is taken over all grid bars of all its windows; the "
               "plan's 'fewer than 300 grid cases' minimum is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are high-volatility (24/720 std ratio > 1) "
                           "bars with the forecast opposite to the 1-hour scaled return, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                ret = close[i + H] / close[i] - 1.0
                if not np.isfinite(ret):
                    continue
                all_rets.append(ret)
                if reg[i] == "mean_reversion" and fc[i] != 0:
                    coin_rows.append((ret, fc[i]))
        if len(all_rets) == 0:
            continue
        mu = float(np.mean(all_rets))
        for ret, f in coin_rows:
            rows.append((ret - mu, f))

    n_cases = len(rows)
    counts = {"grid cases": n_cases}

    if n_cases < 300:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean of excess return x sign(forecast) > 0", "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} grid cases, fewer than the plan's minimum of 300.",
            "reading": reading,
        }

    arr = np.array(rows, dtype=float)
    ex, f = arr[:, 0], arr[:, 1]
    lr = stats.linregress(f, ex)
    slope = float(lr.slope)
    t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else 0.0
    sup = float(np.mean(ex * np.sign(f)))
    sup_pass = bool(sup > 0)

    if slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean signed excess return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check (mean signed excess return > 0) fails."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: sharp hourly moves continue rather than reverse."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "OLS slope t", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "mean of excess return x sign(forecast) > 0", "value": sup, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
