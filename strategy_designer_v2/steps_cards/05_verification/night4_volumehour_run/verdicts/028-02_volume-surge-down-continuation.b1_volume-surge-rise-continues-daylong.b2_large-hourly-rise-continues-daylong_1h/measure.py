import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    BAND = 2.0
    VOL_PERIOD = 720
    RISE_COL = "debug_info.components.rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")

            # volume condition: volume >= mean of the prior 720 bars (bar excluded),
            # recomputed from the window's prices; where the prior 720 bars are not in
            # the window, the recorded regime decision of the detector is used.
            base = vol.shift(1).rolling(VOL_PERIOD, min_periods=VOL_PERIOD).mean()
            ratio = vol / base.replace(0, np.nan)
            vol_ok_px = ratio >= 1.0
            reg = df["regime"].astype(str).str.lower() if "regime" in df.columns else pd.Series([""] * len(df))
            vol_ok = np.where(ratio.notna().values, vol_ok_px.values, (reg == "trending").values)

            # rise condition: the hour's return (raw component sign) is positive
            if RISE_COL in df.columns:
                rise = pd.to_numeric(df[RISE_COL], errors="coerce")
            else:
                rise = pd.Series(np.nan, index=df.index)
            ret1 = close / close.shift(1) - 1.0
            rise = rise.where(rise.notna(), ret1)
            rise_ok = (rise > 0).fillna(False).values

            active = fc != 0
            situ = vol_ok.astype(bool) & rise_ok & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    main_name = "mean 24-bar excess return of forecast-rise cases (one per 24-bar grid cell)"
    thr = "confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("Situation = positive hourly return (raw 'rise' value, else close-to-close) on volume >= mean of prior 720 bars "
               "recomputed in-window (recorded regime used where 720 prior bars are absent), side long; a case is the first "
               "forecast rise of >= 2 points (from its lowest long level since the last bet, 0 after flat) in each 24-bar cell "
               "of each window, cases whose 24-bar return leaves the window are dropped, both coins pooled, each coin's drift "
               "from its non-overlapping 24-bar grid returns over all windows, and the plan's 'fewer than 30 cases' is reported "
               "as not observable.")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are positive-return, above-average-volume hours "
                           "with a positive forecast, so the config does not do what the Fidelity's situation and long side say."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_ret, case_fc, case_coin = [], [], []
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            # coin's drift: non-overlapping grid returns
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            # bets: rises of the long forecast of at least the band
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    bet[i] = True
                    ref = f
                else:
                    ref = min(ref, f)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                i = start + int(idx[0])
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    coin_cases.append((r, fc[i]))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        for r, f in coin_cases:
            if np.isfinite(drift[coin]):
                case_ret.append(r - drift[coin])
                case_fc.append(f)
                case_coin.append(coin)

    x = np.array(case_ret, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    n_cases = int(len(x))
    mean = float(x.mean()) if n_cases > 0 else None
    if n_cases >= 2 and x.std(ddof=1) > 0:
        t = float(mean / (x.std(ddof=1) / np.sqrt(n_cases)))
    else:
        t = None

    sup_val = None
    if n_cases > 0:
        med = np.median(fcs)
        hi = x[fcs > med]
        lo = x[fcs <= med]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
    sup_pass = (sup_val > 0) if sup_val is not None else None

    if n_cases < 30:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases is not reached ({n_cases} cases)."
    elif t is not None and mean > 0 and t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Mean excess return is positive with t >= 2 over at least 30 cases and the supporting check is positive."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess return is negative with t <= -2 over at least 30 cases."
    elif t is not None and mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "A confirming t with a supporting check that is not positive is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean excess return above-median forecast minus at-or-below-median",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
