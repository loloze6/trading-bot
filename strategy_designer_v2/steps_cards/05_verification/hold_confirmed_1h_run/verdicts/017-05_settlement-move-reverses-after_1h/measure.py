import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.pre_move.last_history_value"
    SETTLE_HOURS = {0, 8, 16}
    H = 2

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close_time = ts + pd.Timedelta(hours=1)
            is_settle = close_time.dt.hour.isin(SETTLE_HOURS) & (close_time.dt.minute == 0)
            close = d["close"].astype(float)
            px_ret = close / close.shift(H) - 1.0
            if LHV in d.columns:
                raw = pd.to_numeric(d[LHV], errors="coerce")
                raw = raw.where(raw.notna(), px_ret)
            else:
                raw = px_ret
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            expected_sign = -np.sign(raw)
            agree = active & is_settle & raw.notna() & (raw != 0) & (np.sign(fc) == expected_sign)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x excess 2-bar forward return on settlement bars"
    main_thr = "confirm: mean > 0 with t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2"
    sup_name = "Welch t of forecast-signed excess 2-bar return, top third minus bottom third by |forecast|"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars on settlement and expected side": int(n_agree)},
            "decided_by": ("Fewer than 90% of active (non-zero forecast) bars are settlement-close bars with the "
                           "forecast opposite in sign to the pre-settlement 2-bar return, as the Fidelity requires."),
            "reading": "Settlement bars are bars whose close (start + 1h) falls at 00, 08 or 16 UTC; the expected side is minus the sign of the raw 2-bar return.",
        }

    # ---------- 2. criterion ----------
    rows = []  # (abs_fc, value)
    for coin, wins in bars.items():
        # coin's mean 2-bar return over all its windows: non-overlapping grid 0,2,4,... per window
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).to_numpy()
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.append(r[np.isfinite(r)])
        if not grid_rets:
            continue
        allg = np.concatenate(grid_rets)
        if len(allg) == 0:
            continue
        mu = float(np.mean(allg))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            sel = (d["regime"] == "mean_reversion") & fc.notna() & (fc != 0) & fwd.notna()
            for f, r in zip(fc[sel].to_numpy(), fwd[sel].to_numpy()):
                rows.append((abs(float(f)), float(f) / 10.0 * (float(r) - mu)))

    n = len(rows)
    vals = np.array([v for _, v in rows], dtype=float)
    absf = np.array([a for a, _ in rows], dtype=float)

    k = n // 3
    order = np.argsort(absf, kind="mergesort")
    bottom = vals[order[:k]] if k > 0 else np.array([])
    top = vals[order[n - k:]] if k > 0 else np.array([])
    n_mid = n - 2 * k

    mean_v = float(np.mean(vals)) if n > 0 else None
    t_main = None
    if n > 1:
        sd = float(np.std(vals, ddof=1))
        t_main = float(mean_v / (sd / np.sqrt(n))) if sd > 0 else None

    t_sup = None
    diff = None
    if len(top) > 1 and len(bottom) > 1:
        diff = float(np.mean(top) - np.mean(bottom))
        res = stats.ttest_ind(top, bottom, equal_var=False)
        t_sup = float(res.statistic) if np.isfinite(res.statistic) else None
    sup_pass = bool(t_sup is not None and t_sup >= 2)

    counts = {
        "settlement bars": int(n),
        "top third": int(len(top)),
        "middle third": int(n_mid),
        "bottom third": int(len(bottom)),
    }

    if n < 1000:
        status = "not observable"
        decided = f"Only {n} settlement bars, below the plan's minimum of 1000."
    elif min(len(top), n_mid, len(bottom)) < 300:
        status = "not observable"
        decided = "At least one third holds fewer than the plan's minimum of 300 settlement bars."
    elif t_main is None:
        status = "inconclusive"
        decided = "The main t could not be computed, which meets neither the confirm nor the reject rule."
    elif mean_v > 0 and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main mean is positive with t >= 2 and the top-minus-bottom third Welch t is >= 2."
    elif mean_v < 0 and t_main <= -2:
        status = "rejected"
        decided = "The main mean is negative with t <= -2."
    elif mean_v > 0 and t_main >= 2:
        status = "inconclusive"
        decided = "The main mean is positive with t >= 2 but the supporting check fails (Welch t < 2)."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_v,
            "statistic": {"name": "ordinary t of the mean", "value": t_main} if t_main is not None else None,
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": t_sup, "passed": sup_pass if t_sup is not None else None},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The coin's mean 2-bar return is taken on the non-overlapping grid (positions 0, 2, 4, ...) of "
                    "each window pooled over its windows, settlement bars without a full 2-bar forward return in "
                    "their window are left out, and the thirds are the pooled cases sorted by |forecast| split into "
                    "floor(n/3) bottom and top with the remainder in the middle, all three needing 300."),
    }
