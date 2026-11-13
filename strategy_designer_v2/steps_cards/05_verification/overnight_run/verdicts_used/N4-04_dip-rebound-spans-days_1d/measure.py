import numpy as np
import pandas as pd


def measure(bars):
    DIP_COL = "debug_info.components.dip.last_history_value"
    H = 3
    MIN_CASES = 30

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if DIP_COL in df.columns:
                dip = pd.to_numeric(df[DIP_COL], errors="coerce")
                # fill missing raw values with the in-window one-bar return
                dip = dip.where(dip.notna(), close / close.shift(1) - 1)
            else:
                dip = close / close.shift(1) - 1
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            active = fc.notna() & (fc != 0)
            situ = (regime == "trending") & (dip < 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean excess return close t+1 to close t+3 after top-decile positive forecasts, vs coin mean 2-bar return"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; fewer than 30 non-overlapping cases is not observable"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "non-overlapping cases": 0},
            "decided_by": ("Fewer than 90% of active bars are trending-regime bars with a one-day drop and a long "
                           "forecast, so the config does not do what the plan's situation and side describe."),
            "reading": "Situation taken as regime == 'trending' and a negative one-bar return (dip raw value), expected side long.",
        }

    # ---------- 2. Criterion ----------
    # pooled positive forecasts -> top-decile cut
    pos = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            pos.append(fc[fc > 0].values)
    pos = np.concatenate(pos) if pos else np.array([])
    if len(pos) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean 3-bar excess return vs coin mean 3-bar return", "value": None, "passed": None},
            "counts": {"non-overlapping cases": 0},
            "decided_by": "No positive forecasts, so fewer than 30 non-overlapping cases.",
            "reading": "none",
        }
    cut = float(np.quantile(pos, 0.9))

    ex2_all = []
    ex3_all = []
    for coin, wins in bars.items():
        # coin mean 2-bar and 3-bar returns over all windows together (every bar, within windows)
        r2_list, r3_list = [], []
        frames = {}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            r2_list.append((close.shift(-2) / close - 1).dropna().values)
            r3_list.append((close.shift(-3) / close - 1).dropna().values)
            frames[w] = (df, close)
        r2c = np.concatenate(r2_list) if r2_list else np.array([])
        r3c = np.concatenate(r3_list) if r3_list else np.array([])
        if len(r2c) == 0 or len(r3c) == 0:
            continue
        m2 = float(np.mean(r2c))
        m3 = float(np.mean(r3c))

        for w, (df, close) in frames.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            r23 = close.shift(-3) / close.shift(-1) - 1
            r03 = close.shift(-3) / close - 1
            sel = (fc > 0) & (fc >= cut) & r23.notna() & r03.notna()
            idx = list(np.where(sel.values)[0])
            last = None
            for i in idx:
                if last is not None and i - last <= H:
                    last = i  # chain: same merged case
                    continue
                last = i
                ex2_all.append(float(r23.iloc[i]) - m2)
                ex3_all.append(float(r03.iloc[i]) - m3)

    n = len(ex2_all)
    counts = {"non-overlapping cases": int(n)}
    reading = ("Top decile = forecast >= 90th percentile of all pooled positive forecasts; coin mean 2-bar and 3-bar returns "
               "use every in-window bar of all windows; cases are merged within a window when within 3 bars of the previous "
               "case (chained), each merged case keeping its first bar's returns; cases lacking close t+3 in the window are dropped first.")

    if n == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean 3-bar excess return vs coin mean 3-bar return", "value": None, "passed": None},
            "counts": counts,
            "decided_by": "No non-overlapping cases, below the minimum of 30.",
            "reading": reading,
        }

    ex2 = np.array(ex2_all)
    ex3 = np.array(ex3_all)
    mean2 = float(np.mean(ex2))
    if n > 1:
        sd = float(np.std(ex2, ddof=1))
        t = float(mean2 / (sd / np.sqrt(n))) if sd > 0 else (0.0 if mean2 == 0 else float(np.sign(mean2) * np.inf))
    else:
        t = None
    mean3 = float(np.mean(ex3))
    sup = {"name": "mean 3-bar excess return vs coin mean 3-bar return", "value": mean3, "passed": bool(mean3 > 0)}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} non-overlapping cases, fewer than the plan's minimum of 30."
    elif mean2 > 0 and t is not None and t >= 2:
        status = "confirmed"
        decided = "The mean excess return over days 2-3 is above 0 with t >= 2."
    elif mean2 < 0 and t is not None and t <= -2:
        status = "rejected"
        decided = "The mean excess return over days 2-3 is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, which the plan calls inconclusive."

    t_out = None
    if t is not None:
        t_out = float(t) if np.isfinite(t) else (1e308 if t > 0 else -1e308)

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean2,
                         "statistic": {"name": "t of the mean", "value": t_out} if t_out is not None else None,
                         "threshold": threshold},
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
