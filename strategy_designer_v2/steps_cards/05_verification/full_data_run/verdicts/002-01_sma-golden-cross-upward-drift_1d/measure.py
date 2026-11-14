import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_BLOCKS = 100
    spread_col = "debug_info.components.sma_cross.last_history_value"

    # ---------- 1. Situation check: 50-SMA above 200-SMA (spread > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if spread_col in df.columns:
                sp = pd.to_numeric(df[spread_col], errors="coerce")
                situ = sp.notna() & (sp > 0)
            else:
                situ = pd.Series(False, index=df.index)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS slope of forward 10-bar return minus coin holding mean on forecast"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive"
    reading = ("Non-overlapping samples are positions 0,10,20,... of each window; holding is the coin's mean "
               "of those samples over all its windows; the regression is OLS with intercept on the pooled "
               "samples; the supporting check is pooled as the mean over forecast>0 samples of "
               "(positive indicator minus that coin's all-sample positive share) and passes if above zero; "
               "fewer than 100 forecast>0 blocks gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are bars where the 50-day SMA is "
                           "above the 200-day SMA with a long forecast, as the Fidelity's situation requires."),
            "reading": reading,
        }

    # ---------- 2. Non-overlapping 10-bar samples ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                rows.append((coin, w, c1 / c0 - 1.0, fc[p]))
    s = pd.DataFrame(rows, columns=["coin", "window", "ret", "fc"])

    if len(s) > 0:
        coin_mean = s.groupby("coin")["ret"].mean()
        coin_pos = s.groupby("coin")["ret"].apply(lambda r: float((r > 0).mean()))
        s["excess"] = s["ret"] - s["coin"].map(coin_mean)
        s["base_pos"] = s["coin"].map(coin_pos)
    reg = s.dropna(subset=["fc", "excess"]) if len(s) > 0 else s
    pos = reg[reg["fc"] > 0] if len(reg) > 0 else reg
    n_pos = int(len(pos))
    n_all = int(len(reg))

    # supporting check
    if n_pos > 0:
        sup_val = float(((pos["ret"] > 0).astype(float) - pos["base_pos"]).mean())
        sup_pass = bool(sup_val > 0)
    else:
        sup_val, sup_pass = None, None

    # regression
    slope, tval = None, None
    if n_all >= 3 and np.nanstd(reg["fc"].to_numpy(dtype=float)) > 0:
        res = stats.linregress(reg["fc"].to_numpy(dtype=float), reg["excess"].to_numpy(dtype=float))
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    counts = {"non-overlapping blocks with forecast > 0": n_pos,
              "non-overlapping blocks (all)": n_all}

    if n_pos < MIN_BLOCKS:
        status = "not observable"
        decided = f"Only {n_pos} non-overlapping blocks with forecast > 0, fewer than the plan's minimum of 100."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be estimated, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the supporting check is positive (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails, so the result is inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t of the slope lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "share of positive 10-bar returns when forecast > 0 minus coin's share over all bars",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
