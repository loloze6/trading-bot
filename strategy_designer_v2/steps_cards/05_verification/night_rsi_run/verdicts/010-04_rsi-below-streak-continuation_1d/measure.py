import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 14
    MIN_CASES = 100
    RAW = "debug_info.components.rsi_below_age.last_history_value"
    POS = "postRebalance_current_allocation"

    # ---------- 1. Situation check: active bars must be RSI-below-50 run bars, on the short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            situation = raw.notna() & (raw < 0)  # raw = -n while RSI has been below 50 for n bars
            agree = active & situation & (fc < 0)  # expected side: short (outcome is a lower return)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "pooled OLS slope of 14-bar excess forward return on run length below 50 (grid bars with forecast < 0)"
    threshold = "confirm if slope < 0 with t <= -2 and supporting check passes; reject if slope > 0 with t >= +2; else inconclusive"
    check_name = "mean 14-bar gain before costs: position x (14-bar return - coin mean 14-bar return), > 0"
    reading = ("Grid bars are positions 0, 14, 28, ... of each window with close[t+14] inside the window; each coin's mean 14-bar "
               "return is the mean over all its grid bars in all windows (not only forecast < 0 ones); the slope's t is from one "
               "ordinary least-squares regression on the pooled bars of the coins present in the record (BTC and ETH; BNB is absent); "
               "the plan's 'fewer is inconclusive' minimum of 100 is applied as 'not observable' per the workflow rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars during an RSI run below 50 "
                           "(raw component value < 0), so the config does not do what the plan's Fidelity says."
                           if n_active > 0 else "No bar has a non-zero forecast, so the plan's situation is never traded."),
            "reading": reading,
        }

    # ---------- 2. Non-overlapping 14-bar grid ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            raw = pd.to_numeric(d[RAW], errors="coerce").values if RAW in d.columns else np.full(len(d), np.nan)
            pos = pd.to_numeric(d[POS], errors="coerce").values if POS in d.columns else np.full(len(d), np.nan)
            for t in range(0, len(d) - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({"coin": coin, "window": w, "ret": c1 / c0 - 1.0,
                             "fc": fc[t], "raw": raw[t], "pos": pos[t]})

    g = pd.DataFrame(rows, columns=["coin", "window", "ret", "fc", "raw", "pos"])
    if len(g):
        coin_mean = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(coin_mean)
    else:
        g["excess"] = []

    sel = g[(g["fc"] < 0)].copy() if len(g) else g
    reg = sel.dropna(subset=["excess", "raw"])
    n_cases = int(len(reg))
    counts = {"independent grid cases with forecast < 0": n_cases}
    for coin in sorted(reg["coin"].unique()) if n_cases else []:
        counts[f"grid cases with forecast < 0, {coin}"] = int((reg["coin"] == coin).sum())

    slope = None
    t_stat = None
    if n_cases >= 3:
        x = -reg["raw"].values.astype(float)
        y = reg["excess"].values.astype(float)
        if np.std(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            t_stat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    chk = sel.dropna(subset=["excess", "pos"]) if len(sel) else sel
    gain_mean = float((chk["pos"] * chk["excess"]).mean()) if len(chk) else None
    check_passed = (gain_mean > 0) if gain_mean is not None else None
    counts["grid cases in supporting check"] = int(len(chk))

    main = {"name": main_name, "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_stat} if t_stat is not None else None,
            "threshold": threshold}
    support = {"name": check_name, "value": gain_mean, "passed": check_passed}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent grid cases with forecast < 0, below the plan's minimum of {MIN_CASES}."
    elif t_stat is None or slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in run length), so neither confirm nor reject is met."
    elif slope < 0 and t_stat <= -2 and check_passed:
        status = "confirmed"
        decided = "The slope is negative with t <= -2 and the mean gain of the position is above 0 (confirm rule)."
    elif slope > 0 and t_stat >= 2:
        status = "rejected"
        decided = "The slope is positive with t >= +2: longer runs below 50 are followed by higher excess returns (reject rule)."
    elif t_stat <= -2:
        status = "inconclusive"
        decided = "The slope has t <= -2 but the supporting check's mean gain is not above 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
