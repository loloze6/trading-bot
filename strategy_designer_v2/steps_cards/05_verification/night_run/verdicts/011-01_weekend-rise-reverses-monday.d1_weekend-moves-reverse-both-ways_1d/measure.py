import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.weekend_move.last_history_value"
    HORIZON = 2
    MIN_CASES = 200

    def to_ts(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            mx = np.nanmax(np.abs(v.values)) if len(v) else 0
            unit = "ns" if mx > 1e17 else ("us" if mx > 1e14 else ("ms" if mx > 1e11 else "s"))
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = to_ts(df["timestamp"])
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fall back to the bar's own one-bar return (same sign as the vol-scaled return)
            ret1 = close / close.shift(1) - 1
            raw = raw.where(raw.notna(), ret1)
            active = fc.notna() & (fc != 0)
            sunday = ts.dt.dayofweek == 6
            expected_side = -np.sign(raw)
            ok = active & sunday & (np.sign(fc) == expected_side) & (expected_side != 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of mean of (forecast/10) x 2-bar excess return on Sunday bars"
    threshold = "mean > 0 with t >= 2 (confirm, with supporting check); mean < 0 with t <= -2 (reject)"
    reading_base = ("Cases are Sunday bars (timestamp day of week = Sunday) with regime mean_reversion and a close two bars "
                    "later in the same window, including any with forecast 0; the coin's mean 2-bar return is taken on the "
                    "non-overlapping grid (positions 0,2,4,... of each window) pooled over all its windows; thirds are "
                    "floor(n/3) cases at each end after sorting by |forecast|.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are Sunday-close bars with a forecast opposite "
                           "in sign to the weekend move, so the config does not do what the plan's situation and side say."),
            "reading": "Situation is a Sunday bar; expected side is opposite the sign of the weekend_move raw value (or the bar's return when missing).",
        }

    # ---------- 2. criterion ----------
    vals, excs, fcs = [], [], []
    for coin, wins in bars.items():
        # coin mean 2-bar return over all windows, non-overlapping grid
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(close)
            for i in range(0, n - HORIZON, HORIZON):
                r = close[i + HORIZON] / close[i] - 1
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append(df)
        if not grid_rets:
            continue
        coin_mean = float(np.mean(grid_rets))
        for df in prepared:
            ts = to_ts(df["timestamp"])
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            regime = df["regime"].astype(str).values
            sunday = (ts.dt.dayofweek == 6).values
            n = len(df)
            for t in range(n - HORIZON):
                if not sunday[t] or regime[t] != "mean_reversion":
                    continue
                r = close[t + HORIZON] / close[t] - 1
                f = fc[t]
                if not (np.isfinite(r) and np.isfinite(f)):
                    continue
                ex = r - coin_mean
                vals.append((f / 10.0) * ex)
                excs.append(ex)
                fcs.append(f)

    n_cases = len(vals)
    vals = np.array(vals, dtype=float)
    excs = np.array(excs, dtype=float)
    fcs = np.array(fcs, dtype=float)

    mean_val = float(np.mean(vals)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        t_stat = float(mean_val / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    sup_val = None
    sup_pass = None
    k = n_cases // 3
    if k >= 1:
        order = np.argsort(np.abs(fcs), kind="mergesort")
        bottom = order[:k]
        top = order[-k:]
        sx = np.sign(fcs) * excs
        sup_val = float(np.mean(sx[top]) - np.mean(sx[bottom]))
        sup_pass = bool(sup_val > 0)

    counts = {"Sunday cases with a full 2-bar outcome": int(n_cases), "active bars": int(n_active)}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} Sunday cases with a full 2-bar outcome, fewer than the plan's minimum of 200."
    elif t_stat is not None and mean_val > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean value is positive with t >= 2 and the top third by |forecast| beats the bottom third."
    elif t_stat is not None and mean_val > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails (top third by |forecast| does not beat the bottom third)."
    elif t_stat is not None and mean_val < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean value is negative with t <= -2: weekend moves continue into Monday and Tuesday."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "ordinary t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "top-third minus bottom-third mean of sign(forecast) x excess, by |forecast|",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
