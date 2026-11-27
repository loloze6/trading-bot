import numpy as np
import pandas as pd
from scipy import stats
import json


def _recorded_r20(df):
    """Raw value of the strategy component fall20, if recorded (NaN elsewhere)."""
    col = "debug_info.components.fall20.last_history_value"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
    out = np.full(len(df), np.nan)
    if "debug_info.components" in df.columns:
        for i, v in enumerate(df["debug_info.components"].to_numpy()):
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get("fall20")
                if isinstance(c, dict):
                    x = c.get("last_history_value")
                    try:
                        out[i] = float(x)
                    except (TypeError, ValueError):
                        pass
    return out


def measure(bars):
    H = 10
    BAND = 2.0
    MIN_CASES = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = []  # (coin, window, df)
    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = bars[coin][win].copy().reset_index(drop=True)
            if len(df) == 0:
                continue
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).to_numpy()
            high = df["high"].astype(float).to_numpy()
            low = df["low"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            rng = high - low
            with np.errstate(divide="ignore", invalid="ignore"):
                loc = np.where(rng > 0, (close - low) / rng, np.nan)
            cs = pd.Series(close)
            r5 = (cs / cs.shift(5) - 1.0).to_numpy() * 100.0
            r20 = (cs / cs.shift(20) - 1.0).to_numpy() * 100.0
            rec = _recorded_r20(df)
            rec = np.where(np.abs(rec) <= 1.0, rec * 100.0, rec)
            r20 = np.where(np.isnan(r20), rec, r20)
            evaluable = ~np.isnan(r5) & ~np.isnan(r20)
            with np.errstate(invalid="ignore"):
                sit = (np.nan_to_num(loc, nan=0.0) > 0.5) & (r5 < 0.0) & (r20 < -10.0)
            active = (fc != 0) & evaluable
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc < 0)).sum())
            prepared.append((coin, win, df, close, fc))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Situation computed from prices (close location (close-low)/(high-low) > 0.5, 5-bar return < 0, "
               "20-bar return < -10 %, inside each window, the recorded fall20 raw value used where the window "
               "holds fewer than 20 prior bars) and active bars where it cannot be evaluated are left out; the "
               "profile is not part of the Fidelity situation; a case is the first short bet (rise of -forecast "
               "of >= 2 points from its low since the last bet, reset at flat) in each 10-bar grid cell of a window; "
               "the per-day t is the cluster-by-day t of the mean; forecast size is |forecast|; the plan's "
               "'fewer than 30 cases' is reported as not observable.")

    main_name = "mean short-direction unusual 10-bar move per case"
    threshold = "confirm: mean > 0 with t >= 2 on >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 on >= 30 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars with close location "
                           "above 0.5, 5-day return below 0 and 20-day return below -10 %, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean of non-overlapping 10-bar returns over all windows
    drift_samples = {}
    for coin, win, df, close, fc in prepared:
        idx = np.arange(0, len(close) - H, H)
        r = close[idx + H] / close[idx] - 1.0
        drift_samples.setdefault(coin, []).extend(list(r[np.isfinite(r)]))
    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in drift_samples.items()}

    cases = []  # (day, unusual, size)
    for coin, win, df, close, fc in prepared:
        s = np.maximum(-fc, 0.0)
        ref = 0.0
        bets = np.zeros(len(s), dtype=bool)
        for i in range(len(s)):
            if s[i] <= 0:
                ref = 0.0
                continue
            if s[i] - ref >= BAND:
                bets[i] = True
                ref = s[i]
            else:
                ref = min(ref, s[i])
        seen = set()
        for i in np.where(bets)[0]:
            cell = i // H
            if cell in seen:
                continue
            seen.add(cell)
            if i + H >= len(close) or not np.isfinite(drift.get(coin, np.nan)):
                continue
            ret = close[i + H] / close[i] - 1.0
            if not np.isfinite(ret):
                continue
            u = -(ret - drift[coin])
            day = df["timestamp"].iloc[i].floor("D")
            cases.append((day, u, abs(fc[i])))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)
    counts = {"cases": n_cases, "days": n_days}

    mean_u = None
    t_val = None
    rho = None
    if n_cases > 0:
        u = np.array([c[1] for c in cases])
        sz = np.array([c[2] for c in cases])
        mean_u = float(np.mean(u))
        if n_days >= 2:
            dser = pd.Series(u - mean_u, index=[c[0] for c in cases]).groupby(level=0).sum()
            var = float((dser.to_numpy() ** 2).sum()) / (n_cases ** 2) * n_days / (n_days - 1)
            if var > 0:
                t_val = float(mean_u / np.sqrt(var))
        if n_cases >= 3 and np.std(sz) > 0 and np.std(u) > 0:
            r, _ = stats.spearmanr(sz, u)
            rho = float(r) if np.isfinite(r) else None

    sup_pass = None if rho is None else bool(rho > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases is not reached ({n_cases} cases)."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean short-direction unusual move above 0 with t >= 2 on at least 30 cases and Spearman correlation above 0."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean short-direction unusual move below 0 with t <= -2 on at least 30 cases."
    elif mean_u > 0 and t_val >= 2:
        status = "inconclusive"
        decided = "A confirming t with a Spearman correlation at or below 0 (or not computable) is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, so neither the confirm nor the reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day together", "value": t_val}
                          if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": "Spearman(|forecast| at signal, short-direction unusual move) > 0",
                             "value": rho, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
