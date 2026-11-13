import numpy as np
import pandas as pd
from scipy import stats

H = 20


def _component(df, cid, field="last_history_value"):
    col = f"debug_info.components.{cid}.{field}"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        def get(x):
            try:
                if isinstance(x, dict):
                    v = x.get(cid, {})
                    if isinstance(v, dict):
                        return v.get(field, np.nan)
            except Exception:
                pass
            return np.nan
        return pd.to_numeric(df["debug_info.components"].map(get), errors="coerce")
    return pd.Series(np.nan, index=df.index)


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            d = _component(df, "dist200")
            m = _component(df, "mom20")
            act = fc.notna() & (fc != 0)
            sit = (d >= 0) & (m >= 0)
            n_active += int(act.sum())
            n_agree += int((act & sit & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold = "confirm if mean excess > 0 with t >= 2; reject if mean excess < 0 with t <= -2; otherwise inconclusive"
    mm_name = "mean forward 20-bar return after forecast > 0 minus coin's mean 20-bar return"
    reading = ("The coin's mean 20-bar return is the mean of every bar's in-window forward 20-bar return across all its "
               "windows; cases are bars with forecast > 0 at grid positions 0, 20, 40, ... of each window, pooled across "
               "coins; the minimum of 30 such cases is treated as an observability minimum; the supporting slope is an OLS "
               "of excess return on forecast over those same cases and passes if positive.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are long bars with close at or above its 200-day SMA and a "
                           "non-negative 20-bar return, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    excess = []
    fsize = []
    for coin in sorted(bars):
        frames = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            n = len(c)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = c[H:] / c[: n - H] - 1.0
            frames.append((fwd, fc))
        allfwd = np.concatenate([f for f, _ in frames]) if frames else np.array([])
        allfwd = allfwd[np.isfinite(allfwd)]
        if allfwd.size == 0:
            continue
        coin_mean = float(allfwd.mean())
        for fwd, fc in frames:
            for i in range(0, len(fwd), H):
                if np.isfinite(fwd[i]) and np.isfinite(fc[i]) and fc[i] > 0:
                    excess.append(fwd[i] - coin_mean)
                    fsize.append(fc[i])

    excess = np.array(excess, dtype=float)
    fsize = np.array(fsize, dtype=float)
    n_cases = int(excess.size)

    mean_ex = float(excess.mean()) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = excess.std(ddof=1)
        if sd > 0:
            t = float(mean_ex / (sd / np.sqrt(n_cases)))

    slope = None
    sup_pass = None
    if n_cases >= 3 and np.std(fsize) > 0:
        lr = stats.linregress(fsize, excess)
        slope = float(lr.slope)
        sup_pass = bool(slope > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping active 20-bar cases pooled, fewer than the plan's minimum of 30."
    elif t is not None and mean_ex > 0 and t >= 2:
        status = "confirmed"
        decided = "Mean excess forward 20-bar return is above 0 with t >= 2 (confirm rule)."
    elif t is not None and mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess forward 20-bar return is below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t-stat lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": mm_name,
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of excess forward 20-bar return on forecast, non-overlapping active cases",
            "value": slope,
            "passed": sup_pass,
        },
        "counts": {"non-overlapping active 20-bar cases pooled": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
