import numpy as np
import pandas as pd


def _component_series(df, comp_id, field):
    """Return a float Series of debug_info.components.<id>.<field>, NaN where missing."""
    col = f"debug_info.components.{comp_id}.{field}"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce").astype(float)
    if "debug_info.components" in df.columns:
        def get(v):
            try:
                if isinstance(v, dict):
                    c = v.get(comp_id)
                    if isinstance(c, dict):
                        x = c.get(field)
                        return float(x) if x is not None else np.nan
            except Exception:
                pass
            return np.nan
        return df["debug_info.components"].apply(get).astype(float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    H = 5
    PERIOD = 28

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float)
            # 28-day prior closing high, bar t excluded, inside the window only
            prior_high = close.shift(1).rolling(PERIOD, min_periods=PERIOD).max()
            dist = (close / prior_high - 1.0) * 100.0
            # fallback where the window does not hold 28 prior bars: recorded raw value, then regime
            raw = _component_series(df, "brk", "last_history_value")
            dist = dist.where(dist.notna(), raw)
            situ = dist > 0
            fallback = dist.isna()
            if fallback.any():
                reg = df["regime"].astype(str) == "trending"
                situ = situ.where(~fallback, reg)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ.astype(bool) & (fc > 0)).sum())

    if n_active == 0:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": 0.0, "passed": False},
            "main_measure": {"name": "slope t of excess 5-day return on breakout forecast",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms (with positive weighted mean excess), t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"breakout cases": 0, "distinct days": 0},
            "decided_by": "The plan expects a long forecast on every fresh 28-day closing high, but the record has no bar with a non-zero forecast (the config gives the 'trending' regime no strategy), so the situation is never traded.",
            "reading": "With no active bar the agreement share is taken as 0.",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "slope t of excess 5-day return on breakout forecast",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms (with positive weighted mean excess), t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"breakout cases": None, "distinct days": None},
            "decided_by": f"Only {agreement:.1%} of the active bars are long bars on a fresh 28-day closing high, below the 90 % the plan's situation requires.",
            "reading": "Situation recomputed from closes inside each window (28 prior closes, bar t excluded); recorded raw value or regime used where a window lacks 28 prior bars.",
        }

    # ---------- 2. criterion ----------
    # coin normal 5-day drift: mean of non-overlapping 5-bar returns over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").astype(float).to_numpy()
            for i in range(0, len(close) - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").astype(float).to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            mval = _component_series(df, "margin", "post_pipeline_value").to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df) - H, H):
                if reg[i] != "trending" or not (np.isfinite(fc[i]) and fc[i] > 0):
                    continue
                x = mval[i] if np.isfinite(mval[i]) else fc[i]
                r = close[i + H] / close[i] - 1.0
                if not (np.isfinite(r) and np.isfinite(x) and np.isfinite(drift[coin])):
                    continue
                rows.append({"day": ts.iloc[i].normalize(), "x": float(x),
                             "ex": r - drift[coin], "f": float(fc[i])})

    cases = pd.DataFrame(rows, columns=["day", "x", "ex", "f"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope = None
    t = None
    wmean = None
    if n_cases >= 3:
        x = cases["x"].to_numpy()
        y = cases["ex"].to_numpy()
        xd = x - x.mean()
        sxx = float(np.sum(xd ** 2))
        if sxx > 0:
            b = float(np.sum(xd * y) / sxx)
            a = y.mean() - b * x.mean()
            e = y - a - b * x
            score = pd.Series(xd * e).groupby(cases["day"].to_numpy()).sum().to_numpy()
            G = len(score)
            if G > 1:
                V = (G / (G - 1)) * float(np.sum(score ** 2)) / sxx ** 2
                slope = b
                t = float(b / np.sqrt(V)) if V > 0 else None
        fs = cases["f"].sum()
        if fs > 0:
            wmean = float((cases["f"] * cases["ex"]).sum() / fs)

    sup_pass = None if wmean is None else bool(wmean > 0)
    counts = {"breakout cases": n_cases, "distinct days": n_days}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = f"Minimum not reached: {n_cases} breakout cases (100 needed) on {n_days} distinct days (60 needed)."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed on the cases."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger margins are followed by smaller excess 5-day returns."
    elif t >= 2:
        status = "inconclusive"
        decided = "A positive slope (t >= 2) with a forecast-weighted mean excess return at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "slope of excess 5-day return on breakout forecast",
                         "value": slope,
                         "statistic": None if t is None else {"name": "slope t, day-clustered", "value": t},
                         "threshold": "t >= 2 confirms (with positive weighted mean excess), t <= -2 rejects"},
        "supporting_check": {"name": "forecast-weighted mean excess 5-day return > 0",
                             "value": wmean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "Cases are grid bars 0,5,10,... of each window with regime 'trending' and forecast > 0; the regressor is margin's post_pipeline_value (the forecast where it is not recorded); 'same day summed' is read as a day-clustered standard error of the OLS slope.",
    }
