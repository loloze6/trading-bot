import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    comp_col = "debug_info.components.sma_cross_down.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            if "forecast" not in df.columns or comp_col not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            sp = pd.to_numeric(df[comp_col], errors="coerce")
            ok = fc.notna() & sp.notna()
            fc = fc[ok]
            sp = sp[ok]
            active = fc != 0
            # Situation: short SMA below long SMA (spread < 0); expected side: short (forecast < 0)
            agree = active & (sp < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t-stat of mean of (forecast/10 x forward 24-bar excess return over window mean) on non-overlapping 24-bar blocks"
    threshold_txt = "confirm if t >= 2, reject if t <= -2, inconclusive otherwise or if fewer than 100 active (forecast < 0) blocks"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars where SMA50 sits below SMA200, so the config does not trade the plan's situation on its side.",
            "reading": "Situation taken as the raw SMA50-SMA200 spread being below 0, expected side short (forecast < 0).",
        }

    # ---------- 2. Criterion ----------
    products = []
    active_excess = []
    n_blocks = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            if n <= H:
                continue
            fwd = np.full(n, np.nan)
            fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            valid_all = np.isfinite(fwd)
            if not valid_all.any():
                continue
            win_mean = float(np.mean(fwd[valid_all]))
            for i in range(0, n, H):
                r = fwd[i]
                f = fc[i]
                if not (np.isfinite(r) and np.isfinite(f)):
                    continue
                ex = r - win_mean
                products.append((f / 10.0) * ex)
                n_blocks += 1
                if f < 0:
                    active_excess.append(ex)

    products = np.asarray(products, dtype=float)
    active_excess = np.asarray(active_excess, dtype=float)
    n_act_blocks = int(len(active_excess))

    mean_prod = float(np.mean(products)) if len(products) > 0 else None
    t_stat = None
    if len(products) > 1:
        sd = float(np.std(products, ddof=1))
        if sd > 0:
            t_stat = float(mean_prod / (sd / np.sqrt(len(products))))

    share_neg = float(np.mean(active_excess < 0)) if n_act_blocks > 0 else None
    sup_passed = (share_neg > 0.5) if share_neg is not None else None

    if n_act_blocks < 100:
        status = "inconclusive"
        decided = f"Only {n_act_blocks} non-overlapping active blocks (forecast < 0), fewer than the 100 the plan requires, so the result is inconclusive."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t-stat could not be computed, so neither the confirm nor the reject rule is met."
    elif t_stat >= 2:
        status = "confirmed"
        decided = "The main-measure t-stat is >= 2 with at least 100 active blocks, so short positions gain beyond the coin's drift (confirm rule)."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The main-measure t-stat is <= -2 with at least 100 active blocks, so moves after down-crosses reverse relative to drift (reject rule)."
    else:
        status = "inconclusive"
        decided = "The main-measure t-stat lies strictly between -2 and 2, which neither confirms nor rejects."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_prod,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "share of active blocks with negative forward 24-bar excess return (vs 50%)",
            "value": share_neg,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping active blocks (forecast < 0)": n_act_blocks,
            "non-overlapping blocks": int(n_blocks),
        },
        "decided_by": decided,
        "reading": "Each window's mean 24-bar return is the mean of the forward 24-bar returns from every bar of that window; all grid blocks (including forecast 0, whose product is 0) enter the t-stat; the supporting check passes when the share exceeds 50%.",
    }
