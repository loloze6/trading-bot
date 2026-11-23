import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    MIN_CASES = 200

    def _ts(df):
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        if ts.isna().all():
            ts = pd.to_datetime(df["timestamp"], unit="ms", utc=True, errors="coerce")
        return ts

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            ts = _ts(df)
            # a bar's close is a settlement when the next bar starts at 00/08/16 UTC
            close_hour = (ts + pd.Timedelta(hours=1)).dt.hour
            settle = close_hour.isin([0, 8, 16])
            r2 = close / close.shift(2) - 1.0
            r24 = close / close.shift(24) - 1.0
            col = "debug_info.components.trend24.last_history_value"
            if col in df.columns:
                raw24 = pd.to_numeric(df[col], errors="coerce")
                r24 = raw24.where(raw24.notna(), r24)
            situation = settle & ((r2 * r24) < 0)
            side = np.sign(r24)
            active = fc != 0
            agree = active & situation & (np.sign(fc) == side) & (side != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of mean of forecast/10 x excess 2-bar return on regime cases"
    threshold = "confirm: mean > 0 with t >= 2 over >= 200 cases and correlation > 0; reject: mean < 0 with t <= -2 over >= 200 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of non-zero forecast bars are settlement-close bars where the 2h and 24h "
                           "returns have opposite signs with the forecast on the 24h trend's side "
                           f"(agreement {agreement:.3f})."),
            "reading": "Settlement bars are those whose next bar starts at 00/08/16 UTC; the 24h return is the trend24 raw value (recomputed from closes where missing) and the 2h return is close[t]/close[t-2]-1 within the window.",
        }

    # ---------- criterion ----------
    prods = []
    fcs = []
    excs = []
    for coin, wins in bars.items():
        # coin's mean 2-bar return over all windows, on a non-overlapping grid
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True).values
            if len(c) <= H:
                continue
            idx = np.arange(0, len(c) - H, H)
            r = c[idx + H] / c[idx] - 1.0
            grid_rets.append(r[np.isfinite(r)])
        if not grid_rets:
            continue
        allr = np.concatenate(grid_rets)
        if len(allr) == 0:
            continue
        mu = float(np.mean(allr))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            fwd = c.shift(-H) / c - 1.0
            fc = df["forecast"].astype(float).fillna(0.0)
            mask = (df["regime"].astype(str) == "mean_reversion") & (fc != 0) & fwd.notna()
            if mask.sum() == 0:
                continue
            e = (fwd[mask] - mu).values
            f = fc[mask].values
            fcs.append(f)
            excs.append(e)
            prods.append(f / 10.0 * e)

    if prods:
        p = np.concatenate(prods)
        f_all = np.concatenate(fcs)
        e_all = np.concatenate(excs)
    else:
        p = f_all = e_all = np.array([])
    n = int(len(p))

    mean_v = float(np.mean(p)) if n > 0 else None
    t_v = None
    if n > 1:
        sd = float(np.std(p, ddof=1))
        t_v = float(mean_v / (sd / np.sqrt(n))) if sd > 0 else 0.0
    corr = None
    if n > 2 and np.std(f_all) > 0 and np.std(e_all) > 0:
        corr = float(stats.pearsonr(f_all, e_all)[0])
    corr_pass = None if corr is None else bool(corr > 0)

    if n < MIN_CASES or t_v is None:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 200."
    elif mean_v > 0 and t_v >= 2 and corr_pass:
        status = "confirmed"
        decided = "The mean is positive with t >= 2 over at least 200 cases and the correlation is above 0."
    elif mean_v < 0 and t_v <= -2:
        status = "rejected"
        decided = "The mean is negative with t <= -2 over at least 200 cases."
    elif t_v >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the correlation is at or below 0."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_v,
            "statistic": None if t_v is None else {"name": "t of the mean", "value": t_v},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "Pearson correlation of forecast with excess 2-bar return",
            "value": corr,
            "passed": corr_pass,
        },
        "counts": {"cases": n, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": "Cases are all regime mean_reversion bars with non-zero forecast and a 2-bar forward close inside the window, each counted once, with the coin's mean 2-bar return taken on a non-overlapping grid (positions 0,2,4,...) pooled over all its windows; settlement bars are those whose next bar starts at 00/08/16 UTC.",
    }
