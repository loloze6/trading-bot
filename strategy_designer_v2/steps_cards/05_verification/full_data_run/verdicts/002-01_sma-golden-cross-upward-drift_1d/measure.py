import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.sma_cross.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            ok = f.notna() & raw.notna()
            active = ok & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of excess forward 10-bar return on forecast (non-overlapping, pooled)"
    main_thr = "confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is the 50-day SMA above the 200-day SMA (raw spread > 0) with a long "
                           "position, but fewer than 90% of the bars with a non-zero forecast are long bars with a "
                           "positive raw spread."),
            "reading": "Situation taken as raw sma_cross spread > 0 and side long (forecast > 0).",
        }

    # ---------- 2. Non-overlapping samples ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 != 0):
                    continue
                rows.append((coin, f[t], c1 / c0 - 1.0))
    s = pd.DataFrame(rows, columns=["coin", "forecast", "ret"])

    if len(s) == 0:
        return {
            "status": "inconclusive",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"non-overlapping blocks with forecast > 0": 0},
            "decided_by": "No non-overlapping 10-bar blocks, so fewer than 100 blocks with forecast > 0: inconclusive.",
            "reading": "none",
        }

    # holding: coin mean 10-bar return over all windows (same grid), and share positive
    coin_mean = s.groupby("coin")["ret"].mean()
    coin_pos = s.groupby("coin")["ret"].apply(lambda r: float((r > 0).mean()))
    s["excess"] = s["ret"] - s["coin"].map(coin_mean)

    reg = s.dropna(subset=["forecast", "excess"])
    n_pos_blocks = int((reg["forecast"] > 0).sum())

    slope, tval = None, None
    if len(reg) >= 3 and reg["forecast"].nunique() > 1:
        x = reg["forecast"].to_numpy(float)
        y = reg["excess"].to_numpy(float)
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    # supporting check
    pos = reg[reg["forecast"] > 0]
    if len(pos) > 0:
        sup_val = float(((pos["ret"] > 0).astype(float) - pos["coin"].map(coin_pos)).mean())
        sup_pass = bool(sup_val > 0)
    else:
        sup_val, sup_pass = None, None

    # decision
    if n_pos_blocks < 100:
        status = "inconclusive"
        decided = "Fewer than 100 non-overlapping blocks with forecast > 0, so the result is inconclusive."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t-statistic could not be estimated, so it is not beyond +/-2: inconclusive."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 over non-overlapping blocks: confirmed."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: rejected (gains fall as the position grows)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "share positive fwd 10-bar returns when forecast > 0 minus coin's share positive",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping blocks with forecast > 0": n_pos_blocks,
            "non-overlapping blocks": int(len(reg)),
        },
        "decided_by": decided,
        "reading": ("Blocks start at positions 0, 10, 20, ... of each window, the forecast is taken at the block's "
                    "first bar, the coin's holding mean and positive share use the same non-overlapping grid over "
                    "all its windows, the slope t is the ordinary OLS t, and the supporting check averages, over "
                    "blocks with forecast > 0, the positive indicator minus that coin's positive share."),
    }
