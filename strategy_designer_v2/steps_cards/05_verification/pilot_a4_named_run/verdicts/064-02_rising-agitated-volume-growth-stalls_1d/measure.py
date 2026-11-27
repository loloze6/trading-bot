import json
import numpy as np
import pandas as pd
from scipy import stats

H = 5
COMP = "vol_change"


def _raw_component(df, comp=COMP, field="last_history_value"):
    """Recorded value of a strategy component, NaN where it is not recorded."""
    flat = f"debug_info.components.{comp}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    out = pd.Series(np.nan, index=df.index, dtype=float)
    if "debug_info.components" in df.columns:
        vals = []
        for v in df["debug_info.components"].values:
            x = np.nan
            try:
                if isinstance(v, str):
                    v = json.loads(v)
                if isinstance(v, dict) and comp in v and isinstance(v[comp], dict):
                    y = v[comp].get(field)
                    if y is not None:
                        x = float(y)
            except Exception:
                x = np.nan
            vals.append(x)
        out = pd.Series(vals, index=df.index, dtype=float)
    return out


def _recompute_raw(df):
    """ln(mean volume of last 30 bars / mean volume of the 30 bars before), inside the window."""
    v = pd.to_numeric(df["volume"], errors="coerce")
    recent = v.rolling(30, min_periods=30).mean()
    prior = v.shift(30).rolling(30, min_periods=30).mean()
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.log(recent / prior)
    return r.replace([np.inf, -np.inf], np.nan)


def measure(bars):
    reading = ("The profile (rising agitated) is read from the recorded regime 'unknown' (the only regime with a "
               "strategy, the detector's vetoes sending the rest to 'chop'); the expected side is graded, i.e. the "
               "forecast's sign opposite to the raw log volume ratio (long on shrinkage, short on growth); the slope "
               "is the OLS slope (with intercept) of the excess 5-bar return on the forecast over the active grid "
               "cases, and its t uses standard errors clustered by UTC day, so cases on the same day are summed into "
               "one piece of evidence; the normal drift is each coin's mean 5-bar return over the non-overlapping "
               "grids of all its windows.")

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    cases = []  # (day, forecast, excess return)

    for coin, wins in bars.items():
        # coin's normal drift: mean non-overlapping 5-bar return over all windows
        all_grid_rets = []
        per_window = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = close[H:] / close[:n - H] - 1.0
            grid = np.zeros(n, dtype=bool)
            grid[::H] = True
            g_rets = fwd[grid]
            g_rets = g_rets[np.isfinite(g_rets)]
            all_grid_rets.extend(g_rets.tolist())
            per_window.append((df, fwd, grid))

            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            raw = _raw_component(df)
            rec = _recompute_raw(df)
            raw = raw.where(raw.notna(), rec).values
            regime = df["regime"].astype(str).values
            active = fc != 0
            in_profile = regime == "unknown"
            side_ok = np.sign(fc) == -np.sign(raw)
            side_ok = side_ok & np.isfinite(raw) & (raw != 0)
            n_active += int(active.sum())
            n_agree += int((active & in_profile & side_ok).sum())

        drift = float(np.mean(all_grid_rets)) if len(all_grid_rets) else np.nan

        for df, fwd, grid in per_window:
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D").values
            sel = grid & (fc != 0) & np.isfinite(fwd)
            for i in np.where(sel)[0]:
                if not np.isfinite(drift):
                    continue
                cases.append((day[i], float(fc[i]), float(fwd[i] - drift)))

    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive"
    mm_name = "slope of 5-bar forward return minus normal drift on the forecast"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"grid cases": 0, "distinct days": 0},
            "decided_by": "No bar has a nonzero forecast: fewer than 100 grid cases and fewer than 60 distinct days.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the active bars are rising-agitated profile bars whose forecast sign "
                           "is opposite to the volume growth (long on shrinkage, short on growth)."),
            "reading": reading,
        }

    # ---------- criterion ----------
    cdf = pd.DataFrame(cases, columns=["day", "x", "y"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days": n_days}

    if n_cases < 100 or n_days < 60:
        which = []
        if n_cases < 100:
            which.append(f"{n_cases} grid cases (< 100)")
        if n_days < 60:
            which.append(f"{n_days} distinct days (< 60)")
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "Minimum count not reached: " + " and ".join(which) + " with a nonzero forecast.",
            "reading": reading,
        }

    x = cdf["x"].values
    y = cdf["y"].values
    xm = x - x.mean()
    sxx = float(np.sum(xm ** 2))
    if sxx <= 0:
        return {
            "status": "inconclusive",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The forecast does not vary over the cases, so no slope can be measured.",
            "reading": reading,
        }
    slope = float(np.sum(xm * (y - y.mean())) / sxx)
    intercept = float(y.mean() - slope * x.mean())
    resid = y - intercept - slope * x
    cdf["score"] = xm * resid
    S = cdf.groupby("day")["score"].sum().values
    G = len(S)
    var = float(np.sum(S ** 2)) / sxx ** 2
    if G > 1:
        var *= G / (G - 1) * (n_cases - 1) / max(n_cases - 2, 1)
    se = np.sqrt(var) if var > 0 else np.nan
    t = float(slope / se) if np.isfinite(se) and se > 0 else float("nan")

    if np.isfinite(t) and slope > 0 and t >= 2:
        status = "confirmed"
        decided = f"The slope is positive ({slope:.3g}) with t = {t:.2f} >= 2 (no supporting check in the plan)."
    elif np.isfinite(t) and slope < 0 and t <= -2:
        status = "rejected"
        decided = f"The slope is negative ({slope:.3g}) with t = {t:.2f} <= -2."
    else:
        status = "inconclusive"
        decided = f"The t of the slope ({t:.2f}) lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": mm_name,
            "value": slope,
            "statistic": {"name": "t of the slope, day-clustered", "value": t if np.isfinite(t) else None},
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
