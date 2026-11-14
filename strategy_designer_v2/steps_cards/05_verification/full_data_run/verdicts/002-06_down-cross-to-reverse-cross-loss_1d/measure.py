import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.sma_cross_spread.last_history_value"
    threshold_words = ("confirm if weighted mean excess short return > 0 with t >= 2; "
                       "reject if < 0 with t <= -2; otherwise, or with fewer than 300 "
                       "pooled forecast<0 bars, inconclusive")
    main_name = "|forecast|-weighted mean excess short 1-bar return vs coin all-window mean"

    # ---------- 1. Situation check ----------
    active_total = 0
    active_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            # situation: 50-day SMA below the 200-day SMA -> raw spread < 0; expected side short
            situ = raw.notna() & (raw < 0)
            ok = active & situ & (fc < 0)
            active_total += int(active.sum())
            active_ok += int(ok.sum())

    agreement = float(active_ok / active_total) if active_total > 0 else 0.0
    passed = bool(active_total > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_words},
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars where the "
                           "50-day SMA is below the 200-day SMA (raw spread < 0), as the plan's situation requires."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    xs, ws, below = [], [], []
    for coin, wins in bars.items():
        coin_rets = []
        coin_sel = []  # (ret, forecast) on forecast<0 bars
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ret = np.full(len(close), np.nan)
            ret[:-1] = close[1:] / close[:-1] - 1.0
            valid = np.isfinite(ret)
            coin_rets.append(ret[valid])
            sel = valid & np.isfinite(fc) & (fc < 0)
            for r, f in zip(ret[sel], fc[sel]):
                coin_sel.append((r, f))
        if not coin_rets:
            continue
        allr = np.concatenate(coin_rets)
        if allr.size == 0 or not coin_sel:
            continue
        mu = float(np.mean(allr))
        for r, f in coin_sel:
            xs.append(-(r - mu))
            ws.append(abs(f))
            below.append(1 if r < mu else 0)

    x = np.asarray(xs, dtype=float)
    wt = np.asarray(ws, dtype=float)
    n = int(x.size)

    mean = None
    tval = None
    if n >= 2 and wt.sum() > 0:
        W = wt.sum()
        mean = float(np.sum(wt * x) / W)
        se = np.sqrt(np.sum(wt ** 2 * (x - mean) ** 2)) / W * np.sqrt(n / (n - 1))
        tval = float(mean / se) if se > 0 else (float("inf") * np.sign(mean) if mean != 0 else 0.0)
    elif n == 1:
        mean = float(x[0])

    # supporting check
    sup_val = None
    sup_z = None
    sup_pass = None
    if n > 0:
        k = int(np.sum(below))
        sup_val = float(k / n)
        sup_z = float((k - 0.5 * n) / np.sqrt(0.25 * n))
        sup_pass = bool(sup_z >= 2)

    # decision
    if n < 300:
        status = "inconclusive"
        decided = "Inconclusive: the pooled count of bars with forecast below 0 is under 300."
    elif tval is None:
        status = "inconclusive"
        decided = "Inconclusive: no t-statistic could be computed."
    elif mean > 0 and tval >= 2:
        status = "confirmed"
        decided = "Confirm: the weighted mean excess short return is above 0 with t >= 2."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject: the weighted mean excess short return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the t-statistic lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of weighted mean (heteroskedasticity-robust weighted SE)", "value": tval}
                          if tval is not None else None),
            "threshold": threshold_words,
        },
        "supporting_check": {
            "name": "share of forecast<0 bars with next return below coin mean (binomial z vs 50%)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"pooled bars with forecast below 0": n},
        "decided_by": decided,
        "reading": ("The situation is a raw spread below 0 with a negative forecast; the coin's mean is the mean of all its "
                    "within-window next-bar returns over all its windows; the weighted mean's t uses the robust weighted "
                    "standard error sqrt(sum w^2 (x-m)^2)/sum w with n/(n-1) correction; the supporting check passes when "
                    "its binomial z is at least 2 (z = %s)." % (None if sup_z is None else round(sup_z, 4))),
    }
