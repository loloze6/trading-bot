import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    MID = 24
    MIN_CASES = 100
    COMP = "debug_info.components.fall1d.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            # 72-bar price change recomputed from prices, inside the window
            fall3d = close / close.shift(H) - 1.0
            # where 72 bars of history are not in the window, use the detector's recorded decision
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            fell3d = pd.Series(np.where(fall3d.notna(), fall3d < 0.0,
                                        regime == "mean_reversion"), index=df.index)
            if COMP in df.columns:
                f1 = pd.to_numeric(df[COMP], errors="coerce")
            else:
                f1 = pd.Series(np.nan, index=df.index)
            f1_fallback = close / close.shift(MID) - 1.0
            f1 = f1.where(f1.notna(), f1_fallback)
            fell1d = (f1 < 0.0).fillna(False)
            situation = fell3d.astype(bool) & fell1d.astype(bool)
            active = fc != 0.0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0.0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "t of OLS slope of next-72-bar excess return on forecast (grid bars, forecast > 0)"
    threshold = "confirm if t >= 2 and supporting check > 0; reject if t <= -2; else inconclusive; at least 100 grid cases"
    reading = ("Situation = recomputed 72-bar close change < 0 (recorded regime where the window lacks 72 bars) "
               "and recorded fall1d raw value < 0, expected side long; the coin's mean 72-bar and 24-to-72-bar "
               "moves are taken over all grid bars of all its windows; the plan's 'below 100 cases' rule is "
               "reported as not observable per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the coin fell over "
                           "72 bars and over the last 24 bars, as the Fidelity's situation requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, cm, ch = close[t], close[t + MID], close[t + H]
                r72 = ch / c0 - 1.0 if (np.isfinite(c0) and np.isfinite(ch) and c0 != 0) else np.nan
                r2472 = ch / cm - 1.0 if (np.isfinite(cm) and np.isfinite(ch) and cm != 0) else np.nan
                rows.append((coin, w, fc[t], r72, r2472))

    g = pd.DataFrame(rows, columns=["coin", "window", "forecast", "r72", "r2472"])
    if len(g) > 0:
        g["mean72"] = g.groupby("coin")["r72"].transform("mean")
        g["mean2472"] = g.groupby("coin")["r2472"].transform("mean")
        g["ex72"] = g["r72"] - g["mean72"]
        g["ex2472"] = g["r2472"] - g["mean2472"]
        sel = g[(g["forecast"] > 0) & g["ex72"].notna()]
        sel_chk = g[(g["forecast"] > 0) & g["ex2472"].notna()]
    else:
        sel = pd.DataFrame(columns=["forecast", "ex72"])
        sel_chk = pd.DataFrame(columns=["forecast", "ex2472"])

    n_cases = int(len(sel))
    counts = {"grid cases with forecast > 0": n_cases}

    slope = None
    t_slope = None
    if n_cases >= 3 and np.ptp(sel["forecast"].to_numpy(dtype=float)) > 0:
        lr = stats.linregress(sel["forecast"].to_numpy(dtype=float), sel["ex72"].to_numpy(dtype=float))
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    chk_val = None
    if len(sel_chk) > 0 and sel_chk["forecast"].sum() > 0:
        chk_val = float((sel_chk["ex2472"] * sel_chk["forecast"]).sum() / sel_chk["forecast"].sum())
    chk_pass = None if chk_val is None else bool(chk_val > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with forecast > 0, below the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2:
        if chk_pass:
            status = "confirmed"
            decided = "The slope's t is 2 or more and the forecast-weighted 24-to-72-bar excess return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope's t is 2 or more but the supporting check fails (not above 0)."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope's t is strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": t_slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess return, bar t+24 to t+72",
            "value": chk_val,
            "passed": chk_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
