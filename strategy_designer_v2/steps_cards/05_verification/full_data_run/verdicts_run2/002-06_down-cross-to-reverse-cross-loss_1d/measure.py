import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.sma_cross_spread.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            sub = df[["forecast", RAW]].dropna()
            f = sub["forecast"].astype(float).values
            raw = sub[RAW].astype(float).values
            active = f != 0
            n_active += int(active.sum())
            # Situation: 50-day SMA below 200-day SMA (raw spread < 0); expected side: short.
            n_agree += int((active & (raw < 0) & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (
                "Fewer than 90% of the bars with a non-zero forecast are short bars where the raw "
                "50/200 SMA spread is below 0, so the config does not trade the plan's below-cross "
                "situation on the short side."
            ),
            "reading": "Active bars with a missing raw spread are left out of the agreement share.",
        }

    # ---------- 2. Criterion ----------
    xs, ws, below = [], [], []
    for coin, wins in bars.items():
        # Coin mean 1-bar return over all bars of all its windows (returns within windows only).
        all_r = []
        per_window = []
        for w, df in wins.items():
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values if "forecast" in df.columns else np.full(len(df), np.nan)
            r = np.full(len(df), np.nan)
            if len(df) > 1:
                r[:-1] = close[1:] / close[:-1] - 1.0
            all_r.append(r[np.isfinite(r)])
            per_window.append((fc, r))
        all_r = np.concatenate(all_r) if all_r else np.array([])
        if all_r.size == 0:
            continue
        mu = float(np.mean(all_r))
        for fc, r in per_window:
            m = np.isfinite(fc) & np.isfinite(r) & (fc < 0)
            if not m.any():
                continue
            ex = r[m] - mu
            xs.append(-ex)
            ws.append(np.abs(fc[m]))
            below.append(r[m] < mu)

    if xs:
        x = np.concatenate(xs)
        wt = np.concatenate(ws)
        b = np.concatenate(below)
    else:
        x = wt = b = np.array([])
    n = int(x.size)

    wmean = None
    tstat = None
    if n >= 2 and wt.sum() > 0:
        W = wt.sum()
        wmean = float(np.sum(wt * x) / W)
        se = np.sqrt(np.sum(wt ** 2 * (x - wmean) ** 2)) / W * np.sqrt(n / (n - 1))
        if se > 0:
            tstat = float(wmean / se)

    share = None
    z = None
    sup_passed = None
    if n > 0:
        k = int(b.sum())
        share = float(k / n)
        z = float((k - 0.5 * n) / np.sqrt(0.25 * n))
        sup_passed = bool(z >= 2.0)

    if n < 300:
        status = "inconclusive"
        decided = "Inconclusive: the pooled count of bars with forecast below 0 is below 300."
    elif tstat is None:
        status = "inconclusive"
        decided = "Inconclusive: the t-statistic of the weighted mean could not be computed."
    elif wmean > 0 and tstat >= 2:
        status = "confirmed"
        decided = "Confirm: the weighted mean excess short return is above 0 with t >= 2."
    elif wmean < 0 and tstat <= -2:
        status = "rejected"
        decided = "Reject: the weighted mean excess short return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the t-statistic lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "|forecast|-weighted mean excess short 1-bar return vs coin all-window mean",
            "value": wmean,
            "statistic": {"name": "t of the weighted mean", "value": tstat} if tstat is not None else None,
            "threshold": "above 0 with t >= 2 confirms; below 0 with t <= -2 rejects; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "share of short bars with next return below coin all-window mean (binomial z vs 50%)",
            "value": share,
            "passed": sup_passed,
        },
        "counts": {"pooled bars with forecast below 0": n},
        "decided_by": decided,
        "reading": (
            "The coin's mean is the mean of all within-window next-bar returns pooled over all its windows, every "
            "bar with forecast below 0 and a next-bar return counts once, the t of the weighted mean uses the "
            "weighted standard error sqrt(sum w^2 (x - m)^2) / sum w with an n/(n-1) correction, and the supporting "
            "check counts as passed when the binomial z is at least 2 (it does not enter the decision)."
        ),
    }
