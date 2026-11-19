import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    FC = "forecast"
    PPV = "debug_info.components.vol_share.post_pipeline_value"

    # ---------- 1. Situation check: 72-bar return > 0, expected side short ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            rise = np.full(n, np.nan)
            if n > H:
                rise[H:] = close[H:] / close[:-H] - 1.0
            active = np.isfinite(fc) & (fc != 0) & np.isfinite(rise)
            n_active += int(active.sum())
            n_agree += int((active & (rise > 0) & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the active forecast bars are bars with a positive 72-bar return "
                           "carrying a short forecast, so the config does not do what the plan's situation and side say"
                           if n_active > 0 else
                           "No active forecast bars with a computable 72-bar return, so the plan's situation cannot be matched"),
            "reading": ("The 72-bar return is close[t]/close[t-72]-1 inside the window; active bars in a window's "
                        "first 72 rows, where it cannot be computed from the record, are left out of the agreement."),
        }

    # ---------- 2. Criterion ----------
    rows = []          # (coin, fwd_ret, size) for risen-regime grid samples
    coin_all = {}      # coin -> list of all grid forward returns (all windows)
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            regime = df["regime"].astype(str).to_numpy()
            ppv = (pd.to_numeric(df[PPV], errors="coerce").to_numpy(dtype=float)
                   if PPV in df.columns else np.full(n, np.nan))
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if regime[t] == "mean_reversion" and np.isfinite(ppv[t]):
                    rows.append((coin, r, abs(ppv[t])))
        coin_all[coin] = allr

    coin_mean = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in coin_all.items()}
    if rows:
        d = pd.DataFrame(rows, columns=["coin", "r", "size"])
        d["excess"] = d["r"] - d["coin"].map(coin_mean)
        d = d[np.isfinite(d["excess"])].sort_values("size", kind="mergesort").reset_index(drop=True)
    else:
        d = pd.DataFrame(columns=["coin", "r", "size", "excess"])

    N = len(d)
    k = N // 3
    bottom = d["excess"].iloc[:k].to_numpy(dtype=float)
    top = d["excess"].iloc[N - k:].to_numpy(dtype=float) if k > 0 else np.array([])
    middle_n = N - 2 * k

    counts = {
        "grid samples in top third": int(len(top)),
        "grid samples in middle third": int(middle_n),
        "grid samples in bottom third": int(len(bottom)),
    }
    reading = ("Risen-regime bars are grid bars with regime 'mean_reversion' and a recorded post_pipeline_value; "
               "the coin's mean 72-bar return is the mean of its forward returns on all grid bars of all windows; "
               "thirds are cut by rank of |post_pipeline_value| pooled over coins and windows (N//3 lowest and highest); "
               "situation-check bars in a window's first 72 rows are left out.")

    t_val = None
    diff = None
    top_mean = None
    if len(top) >= 2 and len(bottom) >= 2:
        t_val = float(stats.ttest_ind(top, bottom, equal_var=False).statistic)
        diff = float(top.mean() - bottom.mean())
    if len(top) > 0:
        top_mean = float(top.mean())

    main = {
        "name": "excess fwd 72-bar return, top third minus bottom third of |post_pipeline_value|",
        "value": diff,
        "statistic": {"name": "Welch t", "value": t_val} if t_val is not None else None,
        "threshold": "confirm t <= -2 (with top-third mean < 0); reject t >= +2",
    }
    sup_pass = (top_mean < 0) if top_mean is not None else None
    sup = {"name": "top third mean excess fwd 72-bar return < 0", "value": top_mean, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if len(top) < 100 or len(bottom) < 100 or middle_n < 100 or t_val is None or not np.isfinite(t_val):
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": "Fewer than 100 grid samples in at least one third, pooled over coins and windows.",
                "reading": reading}

    if t_val <= -2 and sup_pass:
        status, dec = "confirmed", "Welch t <= -2 and the top third's mean excess return is below 0."
    elif t_val >= 2:
        status, dec = "rejected", "Welch t >= +2: more concentrated rises do better over the next 72 bars."
    elif t_val <= -2:
        status, dec = "inconclusive", "Welch t <= -2 but the top third's mean excess return is at or above 0."
    else:
        status, dec = "inconclusive", "Welch t lies between -2 and +2."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": dec, "reading": reading}
