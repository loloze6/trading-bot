import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    COMP = "debug_info.components.fall24.last_history_value"
    H = 2

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True)

    # ---------- 1. Situation check ----------
    # Situation (adapted): bars stamped 21:00 and 22:00 UTC, with a 24-bar fall read at that bar; side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = _ts(df)
            hour = ts.dt.hour.values
            close = df["close"].astype(float)
            recomputed = (close / close.shift(24) - 1.0).values
            if COMP in df.columns:
                raw = pd.to_numeric(df[COMP], errors="coerce").values
                raw = np.where(np.isnan(raw), recomputed, raw)
            else:
                raw = recomputed
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            active = (~np.isnan(fc)) & (fc != 0)
            situation = np.isin(hour, [21, 22]) & (~np.isnan(raw)) & (raw < 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of 21:00 excess 2-bar return on forecast, pooled"
    main_thr = "slope t >= 2 to confirm (with supporting mean t >= 2); slope t <= -2 rejects"
    sup_name = "mean excess 2-bar return on 21:00 bars with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": (f"Only {agreement:.1%} of the active bars are 21:00/22:00 UTC bars after a 24-bar fall "
                           f"with a long forecast, below the 90% the plan's situation requires."),
            "reading": "Situation taken as bars stamped 21:00 or 22:00 UTC with the raw 24-bar change below 0 "
                       "(recomputed from closes where not recorded), side long.",
        }

    # ---------- 2. Coin mean 2-bar return over all windows (non-overlapping grid) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = df["close"].astype(float).reset_index(drop=True).values
            idx = np.arange(0, len(c) - H, H)
            r = c[idx + H] / c[idx] - 1.0
            r = r[np.isfinite(r)]
            rets.append(r)
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- 3. Cases: one per day, the bar stamped 21:00 ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        m = coin_mean.get(coin, np.nan)
        if not np.isfinite(m):
            continue
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            df = df.reset_index(drop=True)
            ts = _ts(df)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            pos = np.where(ts.dt.hour.values == 21)[0]
            pos = pos[pos + H < len(c)]
            if len(pos) == 0:
                continue
            r = c[pos + H] / c[pos] - 1.0 - m
            f = fc[pos]
            ok = np.isfinite(r) & np.isfinite(f)
            xs.append(f[ok])
            ys.append(r[ok])

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n_cases = int(len(x))
    pos_mask = x > 0
    n_pos = int(pos_mask.sum())

    slope = None
    slope_t = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    sup_mean = None
    sup_t = None
    if n_pos >= 2:
        yp = y[pos_mask]
        sup_mean = float(np.mean(yp))
        sd = float(np.std(yp, ddof=1))
        sup_t = float(sup_mean / (sd / np.sqrt(n_pos))) if sd > 0 else None

    counts = {"days with forecast > 0 across coins": n_pos, "21:00 cases": n_cases}

    # ---------- 4. Decision ----------
    sup_passed = None if sup_t is None else bool(sup_mean > 0 and sup_t >= 2)
    if n_pos < 300:
        status = "not observable"
        decided = f"Only {n_pos} days with forecast > 0 across coins, fewer than the plan's minimum of 300."
    elif slope_t is None or sup_t is None:
        status = "inconclusive"
        decided = "The slope or the supporting mean's t could not be computed, so neither confirm nor reject is met."
    elif slope_t <= -2 or sup_t <= -2:
        status = "rejected"
        decided = f"Reject rule met: slope t = {slope_t:.2f}, supporting mean t = {sup_t:.2f} (one at -2 or lower)."
    elif slope_t >= 2 and sup_t >= 2:
        status = "confirmed"
        decided = f"Confirm rule met: slope t = {slope_t:.2f} >= 2 and supporting mean t = {sup_t:.2f} >= 2."
    else:
        status = "inconclusive"
        decided = (f"Neither rule met: slope t = {slope_t:.2f}, supporting mean t = {sup_t:.2f}, "
                   f"not both at least 2 and neither at -2 or lower.")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if slope_t is None else {"name": "OLS slope t", "value": slope_t},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_mean, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are every bar stamped 21:00 UTC with a row two positions later in the same window "
                    "(close[t+2] by row position), the coin mean is the mean 2-bar return on the non-overlapping "
                    "grid of all its windows pooled, the slope t is the OLS slope over its standard error, the "
                    "supporting check passes when its mean is above 0 with t >= 2, and the 300-day minimum counts "
                    "21:00 cases with forecast > 0 and a valid return, its shortfall giving 'not observable'."),
    }
