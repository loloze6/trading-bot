import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.cross_spread.last_history_value"
    MIN_ACTIVE = 300

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce")
            else:
                lhv = pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0) & lhv.notna()
            n_active += int(active.sum())
            n_agree += int((active & (lhv > 0) & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else float("nan")
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation is bars where the raw SMA50-SMA200 spread (last_history_value) is > 0, "
               "on the long side, and bars with a missing spread are left out of the agreement; "
               "the next 1-bar return is taken on every bar inside its window, the coin's mean and "
               "up-share use all of its bars over all windows, and the supporting check compares "
               "the pooled up-share of forecast > 0 bars with the same bars' coin overall up-shares "
               "(mean of up minus the coin's share > 0).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if np.isnan(agreement) else agreement,
                                "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the "
                           "SMA50 is above the SMA200 (positive raw spread), as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin baselines over all windows
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_parts = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            nxt = np.full(len(close), np.nan)
            nxt[:-1] = close[1:] / close[:-1] - 1.0
            coin_rets.append(nxt[np.isfinite(nxt)])
            coin_parts.append((fc, nxt))
        if not coin_rets:
            continue
        allr = np.concatenate(coin_rets)
        if len(allr) == 0:
            continue
        mu = float(np.mean(allr))
        up_share = float(np.mean(allr > 0))
        for fc, nxt in coin_parts:
            m = np.isfinite(nxt) & np.isfinite(fc) & (fc > 0)
            for r in nxt[m]:
                rows.append((r - mu, (1.0 if r > 0 else 0.0) - up_share, 1.0 if r > 0 else 0.0, up_share))

    n = len(rows)
    counts = {"bars with forecast > 0": n}

    excess = np.array([r[0] for r in rows]) if n else np.array([])
    mean_ex = float(np.mean(excess)) if n else None
    if n >= 2:
        sd = float(np.std(excess, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n))) if sd > 0 else None
    else:
        t = None

    if n:
        up_on = float(np.mean([r[2] for r in rows]))
        base = float(np.mean([r[3] for r in rows]))
        up_diff = up_on - base
        sup_pass = bool(up_diff > 0)
    else:
        up_diff, sup_pass = None, None

    main = {"name": "mean next 1-bar return minus coin mean, on forecast > 0 bars",
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": "confirm t >= 2 (with up-share above coin's), reject t <= -2"}
    sup = {"name": "up-bar share on forecast > 0 bars minus coin overall up-share",
           "value": up_diff, "passed": sup_pass}

    if n < MIN_ACTIVE:
        status = "not observable"
        decided = f"Only {n} bars with forecast > 0, fewer than the plan's minimum of 300."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion)."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean excess return has t >= 2 and the up-bar share on forecast > 0 bars is above the coin's overall share."
    elif t <= -2:
        status = "rejected"
        decided = "The mean excess return has t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the up-bar share on forecast > 0 bars is not above the coin's overall share."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
