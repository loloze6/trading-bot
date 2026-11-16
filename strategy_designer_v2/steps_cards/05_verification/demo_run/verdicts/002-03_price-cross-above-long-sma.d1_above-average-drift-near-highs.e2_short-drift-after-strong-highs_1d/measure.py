import numpy as np
import pandas as pd
from scipy import stats


def _component_raw(df, comp_id, field="last_history_value"):
    """Return a Series with the component's recorded value (NaN where not recorded)."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        def _get(v):
            if isinstance(v, str):
                try:
                    import json
                    v = json.loads(v)
                except Exception:
                    return np.nan
            if isinstance(v, dict):
                c = v.get(comp_id)
                if isinstance(c, dict):
                    x = c.get(field)
                    try:
                        return float(x)
                    except Exception:
                        return np.nan
            return np.nan
        return df["debug_info.components"].apply(_get).astype(float)
    return pd.Series(np.nan, index=df.index)


def measure(bars):
    H = 5
    MIN_CASES = 100

    # ---------- 1. situation check ----------
    raw_all = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            raw_all.append(_component_raw(df, "range20").dropna().values)
    raw_all = np.concatenate(raw_all) if raw_all else np.array([])
    if raw_all.size and np.nanmin(raw_all) < -1e-9:
        mid = 0.0            # centred scale, e.g. [-1, 1]
    elif raw_all.size and np.nanmax(raw_all) > 1.5:
        mid = 50.0           # percent scale [0, 100]
    else:
        mid = 0.5            # fractional scale [0, 1]

    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            regime = df["regime"].astype(str)
            raw = _component_raw(df, "range20")
            # price fallback: position of close in its 20-bar closing range (0..1)
            hi = close.rolling(20, min_periods=20).max()
            lo = close.rolling(20, min_periods=20).min()
            rng = (hi - lo).replace(0, np.nan)
            pos_price = (close - lo) / rng
            upper = pd.Series(False, index=df.index)
            has_raw = raw.notna()
            upper[has_raw] = raw[has_raw] > mid
            has_px = (~has_raw) & pos_price.notna()
            upper[has_px] = pos_price[has_px] > 0.5
            situation = (regime == "trending") & upper
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "pooled OLS slope of coin-demeaned 5-bar forward return on forecast (trending, non-overlapping grid)"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive; at least 100 grid cases with regime trending and forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active_bars": n_active},
            "decided_by": ("No active bars: the forecast is never non-zero." if n_active == 0 else
                           f"Only {agreement:.1%} of active bars are long bars with regime trending (close >= 200-day SMA) "
                           "and the close in the upper half of its 20-day range, below the 90% required."),
            "reading": "The 200-day gate is read from the regime column (detector not recorded); the upper half of the 20-day range from range20's raw value above its scale's midpoint, else from closes.",
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    n_pos = 0
    for coin, wins in bars.items():
        rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((c1 / c0 - 1.0, fc[t], reg[t]))
        if not rows:
            continue
        rets = np.array([r[0] for r in rows])
        coin_mean = rets.mean()
        for r, f, g in rows:
            if g == "trending" and np.isfinite(f):
                xs.append(f)
                ys.append(r - coin_mean)
                if f > 0:
                    n_pos += 1

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n = len(x)
    counts = {"grid cases with regime trending and forecast > 0": n_pos,
              "grid cases with regime trending": n}

    slope, tstat = None, None
    if n >= 3 and np.var(x) > 0:
        X = np.column_stack([np.ones(n), x])
        beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        s2 = (resid @ resid) / (n - 2)
        cov = s2 * np.linalg.inv(X.T @ X)
        slope = float(beta[1])
        se = float(np.sqrt(cov[1, 1]))
        tstat = float(slope / se) if se > 0 else None

    if n_pos < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_pos} non-overlapping grid cases with regime trending and forecast > 0, fewer than the plan's minimum of 100."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided = "The pooled slope is positive with t >= 2 (confirm rule)."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The pooled slope is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t-statistic lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tstat} if tstat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": ("The coin's mean 5-bar return is taken over all grid bars of all its windows (every regime), the pooled regression is an OLS with intercept over all coins' trending grid bars, and the 200-day gate is read from the regime column since the detector's component is not recorded."),
    }
