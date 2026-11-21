import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    C_RAW = "debug_info.components.combined.last_history_value"
    C_POST = "debug_info.components.combined.post_pipeline_value"
    B_POST = "debug_info.components.best.post_pipeline_value"

    def fnum(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        return None if not np.isfinite(x) else x

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = (pd.to_numeric(df[C_RAW], errors="coerce")
                   if C_RAW in df.columns else pd.Series(np.nan, index=df.index))
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            sit = raw.notna() & (raw != 0)
            agree = active & sit & (np.sign(raw) == np.sign(fc))
            n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of y x (combined - best post_pipeline_value) / 10 over non-overlapping 5-bar cases"
    threshold = "t >= 2 (with combined correlation > 0, >= 300 cases) confirms; t <= -2 rejects"
    support_name = "Pearson correlation of y with combined post_pipeline_value > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "non-overlapping cases": 0},
            "decided_by": ("Fewer than 90% of active bars have a forecast sign equal to the sign of the "
                           "combined score's raw value, so the config does not trade the plan's situation on its side."),
            "reading": "The expected side on each bar is the sign of the combined component's raw value (long when the learned combination points up).",
        }

    # ---------- 2. criterion ----------
    # grid returns per coin, and drift per coin over all windows
    per_coin = {}
    for coin in sorted(bars.keys()):
        rows = []
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            c = (pd.to_numeric(df[C_POST], errors="coerce").values
                 if C_POST in df.columns else np.full(len(df), np.nan))
            b = (pd.to_numeric(df[B_POST], errors="coerce").values
                 if B_POST in df.columns else np.full(len(df), np.nan))
            for t in range(0, len(df) - H, H):
                r = close[t + H] / close[t] - 1.0
                if np.isfinite(r):
                    rows.append((r, c[t], b[t]))
        per_coin[coin] = rows

    ys, cs, bs = [], [], []
    for coin, rows in per_coin.items():
        if not rows:
            continue
        rets = np.array([r[0] for r in rows], dtype=float)
        drift = float(np.mean(rets))
        for r, c, b in rows:
            if np.isfinite(c) and np.isfinite(b):
                ys.append(r - drift)
                cs.append(c)
                bs.append(b)
    ys = np.array(ys, dtype=float)
    cs = np.array(cs, dtype=float)
    bs = np.array(bs, dtype=float)
    n = int(len(ys))

    vals = ys * (cs - bs) / 10.0
    mean = float(np.mean(vals)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(vals, ddof=1))
        if sd > 0:
            t = mean / (sd / np.sqrt(n))
    corr = None
    if n > 2 and np.std(ys) > 0 and np.std(cs) > 0:
        corr = float(np.corrcoef(ys, cs)[0, 1])
    support_pass = None if corr is None else bool(corr > 0)

    if n < 300:
        status = "not observable"
        decided = f"Only {n} non-overlapping cases, fewer than the plan's minimum of 300."
    elif t is None or not np.isfinite(t):
        status = "inconclusive"
        decided = "The t of the main mean could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and support_pass:
        status = "confirmed"
        decided = "The main mean's t is 2 or more, the combined correlation is above 0, on at least 300 cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main mean's t is 2 or more but the combined correlation is at or below 0, which the plan calls inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "The main mean's t is -2 or less: the best single signal lines up with the coming 5-day return more closely than the combination."
    else:
        status = "inconclusive"
        decided = "The main mean's t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": fnum(mean),
            "statistic": None if fnum(t) is None else {"name": "ordinary t of the mean", "value": fnum(t)},
            "threshold": threshold,
        },
        "supporting_check": {"name": support_name, "value": fnum(corr), "passed": support_pass},
        "counts": {"non-overlapping cases": n, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": ("Cases are grid bars 0,5,10,... of each window with a full 5-bar return inside the window, the drift is "
                    "each coin's mean over all its grid returns, cases missing either score are left out, and fewer than 300 "
                    "cases is reported as not observable per the workflow's minimum-count rule."),
    }
