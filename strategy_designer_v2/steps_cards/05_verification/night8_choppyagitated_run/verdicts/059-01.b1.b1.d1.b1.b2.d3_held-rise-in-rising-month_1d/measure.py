import numpy as np
import pandas as pd
from scipy import stats


def _component_col(df, comp_id, field="last_history_value"):
    """Return a float Series of a strategy component's recorded value (NaN where not recorded)."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce").astype(float)
    if "debug_info.components" in df.columns:
        def _get(v):
            try:
                if isinstance(v, str):
                    import json
                    v = json.loads(v)
                if isinstance(v, dict):
                    c = v.get(comp_id)
                    if isinstance(c, dict):
                        x = c.get(field)
                        return float(x) if x is not None else np.nan
            except Exception:
                return np.nan
            return np.nan
        return df["debug_info.components"].apply(_get).astype(float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    H = 7
    MIN_CASES = 30
    EPS = 1e-9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            high = pd.to_numeric(df["high"], errors="coerce").astype(float)
            low = pd.to_numeric(df["low"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)

            # weekly high-low position, stochastic convention, current bar included
            hh = high.rolling(7, min_periods=7).max()
            ll = low.rolling(7, min_periods=7).min()
            rng = hh - ll
            pos = (close - ll) / rng.replace(0, np.nan)
            ret30 = close / close.shift(30) - 1.0

            scaled = _component_col(df, "scaled_rise", "last_history_value")

            top = pos >= 0.8 - EPS
            up30 = ret30 > 0
            # where the detector's inputs cannot be rebuilt from this window's bars, use its decision
            regime_ok = regime == "trending"
            cond_top = np.where(pos.isna(), regime_ok, top)
            cond_up = np.where(ret30.isna(), regime_ok, up30)
            situation = cond_top & cond_up & (scaled > 0).values

            active = (fc != 0).values
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0).values).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation rebuilt as: recorded scaled_rise raw value > 0, close in the top 20 % of the 7-bar "
               "high-low range (current bar included) and close/close[-30]-1 > 0, long side, using the recorded "
               "regime 'trending' where a window's first bars cannot rebuild those inputs; the coin's mean 7-bar "
               "return is taken over its 0,7,14,... grid of all windows; the slope's t is the OLS slope over its "
               "standard error; the weighted mean's t uses the standard error sqrt(sum w^2 (x-m)^2)/sum w.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars of the plan's situation "
                           "(positive scaled 7-day rise, close in the top fifth of the week's range, 30-day rise)."
                           if n_active > 0 else "No bar has a non-zero forecast, so the config never takes the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []  # (coin, forecast, fwd)
    coin_grid_rets = {}
    for coin in sorted(bars.keys()):
        allr = []
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    rows.append((coin, float(fc[i]), r))
        coin_grid_rets[coin] = float(np.mean(allr)) if allr else np.nan

    f = np.array([r[1] for r in rows], dtype=float)
    x = np.array([r[2] - coin_grid_rets[r[0]] for r in rows], dtype=float)
    ok = np.isfinite(f) & np.isfinite(x)
    f, x = f[ok], x[ok]
    n_cases = int(len(f))

    slope = slope_t = None
    if n_cases >= 3 and np.std(f) > 0:
        lr = stats.linregress(f, x)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    wmean = wmean_t = None
    if n_cases >= 2 and f.sum() > 0:
        wmean = float(np.sum(f * x) / np.sum(f))
        se = float(np.sqrt(np.sum(f ** 2 * (x - wmean) ** 2)) / np.sum(f))
        wmean_t = float(wmean / se) if se > 0 else None

    supp_pass = None
    if wmean is not None and wmean_t is not None:
        supp_pass = bool(wmean > 0 and wmean_t >= 2)

    main = {
        "name": "OLS slope of excess forward 7-bar return on forecast (grid bars, forecast > 0)",
        "value": slope,
        "statistic": {"name": "slope t", "value": slope_t} if slope_t is not None else None,
        "threshold": "confirm: slope t >= 2 (with weighted mean > 0, t >= 2); reject: slope t <= -2 or weighted mean t <= -2; at least 30 cases",
    }
    supporting = {
        "name": "forecast-weighted mean excess forward 7-bar return (t)",
        "value": wmean,
        "t": wmean_t,
        "passed": supp_pass,
    }
    counts = {"cases": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with forecast > 0, fewer than the plan's minimum of 30."
    else:
        st = slope_t if slope_t is not None else 0.0
        wt = wmean_t if wmean_t is not None else 0.0
        if st <= -2 or wt <= -2:
            status = "rejected"
            decided = "Reject rule: the slope's t is -2 or less, or the forecast-weighted mean excess return has t of -2 or less, over at least 30 cases."
        elif st >= 2 and supp_pass:
            status = "confirmed"
            decided = "Confirm rule: the slope's t is 2 or more and the forecast-weighted mean excess return is above 0 with t of 2 or more, over at least 30 cases."
        else:
            status = "inconclusive"
            decided = "Inconclusive rule: neither the confirm nor the reject rule is met by the slope's t and the weighted mean's t, over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
