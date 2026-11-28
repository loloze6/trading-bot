import json
import numpy as np
import pandas as pd


VSR_THRESHOLD = 1.1547
HORIZON = 3
MIN_CASE_DAYS = 30


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        unit = "ms" if np.nanmax(np.abs(v.values)) > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _component_raw(df, comp_id):
    """Raw value (last_history_value) of a strategies component, NaN where not recorded."""
    col = "debug_info.components.%s.last_history_value" % comp_id
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce").reset_index(drop=True)
    out = pd.Series(np.nan, index=range(len(df)))
    if "debug_info.components" in df.columns:
        vals = df["debug_info.components"].reset_index(drop=True)
        for i, v in enumerate(vals):
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(comp_id)
                if isinstance(c, dict) and c.get("last_history_value") is not None:
                    try:
                        out.iloc[i] = float(c.get("last_history_value"))
                    except Exception:
                        pass
    return out


def _vsr_from_prices(close, period=3, vol_period=30):
    r1 = close.pct_change()
    std = r1.rolling(vol_period, min_periods=vol_period).std()
    ret = close / close.shift(period) - 1.0
    return ret / (std * np.sqrt(period))


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            vsr = _component_raw(df, "push")
            vsr_px = _vsr_from_prices(close)
            vsr = vsr.where(vsr.notna(), vsr_px)
            regime = df["regime"].astype(str).str.lower()
            # profile (rising agitated) vetoes and the vsr rule both lead to "trending"
            situation = (regime == "trending") & (vsr >= VSR_THRESHOLD - 1e-9)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess 3-bar forward return (vs coin's mean 3-bar return) on forecast>0 grid bars"
    threshold = "confirm: mean > 0 with day-pooled t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are long bars of the plan's "
                           "situation (regime 'trending' in the rising agitated profile with 3-day scaled "
                           "return >= 1.1547)" if n_active > 0 else "no bar has a non-zero forecast"),
            "reading": "the situation is read as regime 'trending' (profile vetoes passed) with the recorded "
                       "push raw value (or its price recomputation) >= 1.1547, on the long side.",
        }

    # ---------- 2. criterion ----------
    coin_grid = {}
    cases = []
    for coin in sorted(bars):
        all_rets = []
        coin_cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = _to_utc(df["timestamp"]).values
            for p in range(0, len(df), HORIZON):
                if p + HORIZON >= len(df):
                    break
                c0, c1 = close[p], close[p + HORIZON]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if fc[p] > 0:
                    day = pd.Timestamp(ts[p]).tz_localize(None).normalize() if pd.Timestamp(ts[p]).tzinfo is None \
                        else pd.Timestamp(ts[p]).tz_convert("UTC").tz_localize(None).normalize()
                    coin_cases.append((day, r, float(fc[p])))
        if all_rets:
            coin_grid[coin] = float(np.mean(all_rets))
            for day, r, f in coin_cases:
                cases.append((coin, day, r - coin_grid[coin], f))

    n_cases = len(cases)
    days = sorted(set(c[1] for c in cases))
    n_days = len(days)
    counts = {"independent case-days": n_days, "cases": n_cases}

    mean_ex = None
    t_val = None
    slope = None
    if n_cases > 0:
        ex = np.array([c[2] for c in cases], dtype=float)
        fcs = np.array([c[3] for c in cases], dtype=float)
        mean_ex = float(ex.mean())
        dev = pd.Series(ex - mean_ex, index=[c[1] for c in cases])
        s_day = dev.groupby(level=0).sum().values
        D = len(s_day)
        if D > 1:
            var_mean = (s_day ** 2).sum() * D / (D - 1) / (n_cases ** 2)
            if var_mean > 0:
                t_val = float(mean_ex / np.sqrt(var_mean))
        if n_cases >= 2 and np.var(fcs) > 0:
            slope = float(np.polyfit(fcs, ex, 1)[0])

    slope_passed = None if slope is None else bool(slope > 0)
    reading = ("cases are grid bars (positions 0,3,6,... of each window) with forecast > 0 and a full 3-bar "
               "forward return inside the window; the coin's mean 3-bar return is over the same grids of all its "
               "windows; the t is the mean over a day-clustered standard error (deviations summed per UTC day, "
               "D/(D-1) correction); the plan's 30 case-days minimum, when unmet, is reported as not observable.")

    main = {"name": main_name, "value": mean_ex,
            "statistic": None if t_val is None else {"name": "t pooling the cases of one day", "value": t_val},
            "threshold": threshold}
    supp = {"name": "least-squares slope of excess 3-bar return on forecast", "value": slope,
            "passed": slope_passed}
    sit = {"agreement": agreement, "passed": True}

    if n_days < MIN_CASE_DAYS:
        status = "not observable"
        decided = "fewer than 30 independent case-days (%d), the plan's minimum." % n_days
    elif mean_ex is not None and t_val is not None and mean_ex > 0 and t_val >= 2 and slope_passed:
        status = "confirmed"
        decided = "the mean excess return is above 0 with t >= 2 and the slope is above 0 (confirm rule)."
    elif mean_ex is not None and t_val is not None and mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "the mean excess return is below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        if mean_ex is not None and t_val is not None and mean_ex > 0 and t_val >= 2:
            decided = "the mean excess return meets the confirm rule but the slope is not above 0 (inconclusive rule)."
        else:
            decided = "the t is between -2 and 2 (or undefined), meeting neither confirm nor reject (inconclusive rule)."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
