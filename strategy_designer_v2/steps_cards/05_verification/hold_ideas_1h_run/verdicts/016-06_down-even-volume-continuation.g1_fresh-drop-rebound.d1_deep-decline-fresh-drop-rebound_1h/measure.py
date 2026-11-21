import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    RAW3 = "debug_info.components.fall3d.last_history_value"

    # ---------- 1. Situation check: active bars must be r72 < 0 and long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            # 72-bar return recomputed from prices inside the window
            r72_px = np.full(len(df), np.nan)
            if len(df) > H:
                r72_px[H:] = close[H:] / close[:-H] - 1.0
            if RAW3 in df.columns:
                raw = pd.to_numeric(df[RAW3], errors="coerce").values
                r72 = np.where(np.isfinite(raw), raw, r72_px)
            else:
                r72 = r72_px
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            ok = active & np.isfinite(r72) & (r72 < 0) & (fc > 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of forward 72-bar excess return on forecast (forecast > 0 grid bars)"
    thr = "slope t >= 2 confirms (with supporting check), t <= -2 rejects; at least 100 grid cases with forecast > 0"
    sup_name = "mean excess 72-bar return of top third of forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars with a negative "
                           "72-bar return, the situation and side the plan's Fidelity states."),
            "reading": "The 72-bar return is read from fall3d's raw value where recorded, else recomputed from closes inside the window.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n:
                    ret = close[i + H] / close[i] - 1.0
                    if np.isfinite(ret):
                        coin_rows.append((fc[i], ret))
        if not coin_rows:
            continue
        rets = np.array([r for _, r in coin_rows])
        coin_mean = float(np.mean(rets))
        for f, r in coin_rows:
            if np.isfinite(f) and f > 0:
                rows.append((coin, float(f), r - coin_mean))

    n_cases = len(rows)
    counts = {"independent grid cases with a positive forecast": n_cases}

    if n_cases < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} independent grid cases with a positive forecast, fewer than the 100 the plan requires.",
            "reading": ("Grid is positions 0, 72, 144, ... of each window; the coin's mean 72-bar return is the mean over "
                        "all its grid bars in all windows; top third is forecast at or above its 2/3 quantile among the samples."),
        }

    x = np.array([r[1] for r in rows])
    y = np.array([r[2] for r in rows])
    if np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr > 0 else float("nan")
    else:
        slope, t = float("nan"), float("nan")

    q = np.quantile(x, 2.0 / 3.0)
    top = y[x >= q]
    top_mean = float(np.mean(top)) if len(top) else float("nan")
    sup_pass = bool(np.isfinite(top_mean) and top_mean > 0)
    counts["top third cases"] = int(len(top))

    if np.isfinite(t) and t >= 2 and sup_pass:
        status = "confirmed"
        decided = f"The slope's t is {t:.2f} (>= 2) and the top third's mean excess return is above 0."
    elif np.isfinite(t) and t <= -2:
        status = "rejected"
        decided = f"The slope's t is {t:.2f} (<= -2)."
    elif np.isfinite(t) and t >= 2:
        status = "inconclusive"
        decided = f"The slope's t is {t:.2f} (>= 2) but the supporting check fails (top third mean excess {top_mean:.5f} <= 0)."
    else:
        status = "inconclusive"
        decided = f"The slope's t is {t:.2f}, between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope if np.isfinite(slope) else None,
                         "statistic": {"name": "OLS slope t", "value": t if np.isfinite(t) else None},
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": top_mean if np.isfinite(top_mean) else None, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid is positions 0, 72, 144, ... of each window; the coin's mean 72-bar return is the mean over all "
                    "its grid bars in all windows; top third is forecast at or above its 2/3 quantile among the positive-forecast samples."),
    }
