import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FALL_COL = "debug_info.components.fall10.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            high = df["high"].astype(float)
            low = df["low"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            hh = high.rolling(30, min_periods=30).max()
            ll = low.rolling(30, min_periods=30).min()
            rng = hh - ll
            net = (close - close.shift(29)).abs()
            ratio = net / rng.replace(0, np.nan)
            mid = (hh + ll) / 2.0
            flat = ratio <= 0.5 + 1e-12
            below = close < mid
            if FALL_COL in df.columns:
                fall_raw = pd.to_numeric(df[FALL_COL], errors="coerce")
            else:
                fall_raw = pd.Series(np.nan, index=df.index)
            fall_px = close / close.shift(10) - 1.0
            fall = fall_raw.where(fall_raw.notna(), fall_px)
            computable = ratio.notna() & mid.notna() & fall.notna()
            active = fc.notna() & (fc != 0)
            n_active_uncomputable += int((active & ~computable).sum())
            act_c = active & computable
            n_active += int(act_c.sum())
            ok = act_c & flat & below & (fall < 0) & (fc < 0)
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS slope of next-5-bar return minus coin drift on forecast, mean_reversion grid bars"
    thr = "confirm if slope t >= 2 and check passes; reject if slope t <= -2; inconclusive otherwise"
    reading = ("Situation computed from prices as |close[t]-close[t-29]| / (30-bar max high - min low) <= 0.5 and "
               "close < 30-bar high-low midpoint, with the 10-bar fall from fall10's raw value (prices when missing), "
               "active bars lacking 30 bars of in-window history left out of the agreement; drift is the coin's mean "
               "5-bar return on the 0,5,10,... grid of all its windows; the regression pools all coins and windows with "
               "an intercept; the minimum count is the grid bars with forecast < 0 and a valid next-5-bar return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars checked": n_active, "active bars agreeing": n_agree,
                       "active bars without history": n_active_uncomputable},
            "decided_by": ("Fewer than 90% of active (non-zero forecast) bars are flat (ratio <= 0.5), below the "
                           "30-bar midpoint, after a 10-bar fall, with a short forecast"
                           if agreement is not None else
                           "No active bar could be checked against the plan's situation"),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    drift = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n:
                    r = close[i + H] / close[i] - 1.0
                    if np.isfinite(r):
                        all_rets.append(r)
                        fcv = pd.to_numeric(pd.Series([df["forecast"].iloc[i]]), errors="coerce").iloc[0]
                        rows.append((coin, w, str(df["regime"].iloc[i]), float(fcv), r))
        drift[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    g = pd.DataFrame(rows, columns=["coin", "w", "regime", "fc", "r"])
    if len(g):
        g["d"] = g["r"] - g["coin"].map(drift)
        g = g[np.isfinite(g["fc"]) & np.isfinite(g["d"])]
    mr = g[g["regime"] == "mean_reversion"] if len(g) else g

    n_neg = int((g["fc"] < 0).sum()) if len(g) else 0
    n_mr = int(len(mr))
    cases = g[g["fc"] <= -2] if len(g) else g
    n_cases = int(len(cases))

    slope = None
    tval = None
    if n_mr >= 3 and mr["fc"].nunique() > 1:
        lr = stats.linregress(mr["fc"].values, mr["d"].values)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    check_val = float((-cases["d"]).mean()) if n_cases > 0 else None
    check_pass = (check_val is not None and check_val > 0)

    counts = {"grid bars with forecast < 0": n_neg,
              "mean_reversion grid bars": n_mr,
              "cases (grid bars with forecast <= -2)": n_cases}

    if n_neg < 30:
        status = "not observable"
        decided = f"Fewer than 30 grid bars with forecast < 0 exist across coins and windows ({n_neg})."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t is at least 2 and the short-direction mean of the forecast <= -2 cases is above 0."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is at least 2 but the supporting check fails, so the plan calls it inconclusive."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is at most -2: larger falls are followed by relative rises."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
                         "threshold": thr},
        "supporting_check": {"name": "mean next-5-bar return minus drift, short direction, forecast <= -2 grid bars",
                             "value": check_val,
                             "passed": None if check_val is None else bool(check_pass)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
