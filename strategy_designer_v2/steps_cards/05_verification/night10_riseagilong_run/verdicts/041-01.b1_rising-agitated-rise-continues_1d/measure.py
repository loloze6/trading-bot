import json
import numpy as np
import pandas as pd


def _component_raw(df, comp_id="scaled_rise"):
    """Return the raw value (last_history_value) of a strategy component, NaN where not recorded."""
    flat = f"debug_info.components.{comp_id}.last_history_value"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce").astype(float)
    out = pd.Series(np.nan, index=df.index, dtype=float)
    if "debug_info.components" in df.columns:
        for idx, v in df["debug_info.components"].items():
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(comp_id)
                if isinstance(c, dict) and "last_history_value" in c:
                    try:
                        out.at[idx] = float(c["last_history_value"])
                    except (TypeError, ValueError):
                        pass
    return out


def _recompute_raw(close):
    """Today's 1-day return divided by the std (ddof 1) of the last 30 daily returns, inside one window."""
    r = close / close.shift(1) - 1.0
    sd = r.rolling(30, min_periods=30).std(ddof=1)
    return r / sd


def measure(bars):
    # ---------- gather rows ----------
    rows = []
    coin_rets = {}
    for coin in sorted(bars.keys()):
        allr = []
        for w in sorted(bars[coin].keys(), key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").astype(float)
            nxt = close.shift(-1) / close - 1.0
            allr.append(nxt.dropna().values)
            raw = _component_raw(df)
            rec = _recompute_raw(close)
            raw = raw.where(raw.notna(), rec)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            rows.append(pd.DataFrame({
                "coin": coin, "window": str(w), "day": ts.dt.floor("D"),
                "forecast": fc, "raw": raw, "next_ret": nxt,
            }))
        coin_rets[coin] = float(np.mean(np.concatenate(allr))) if allr and sum(len(a) for a in allr) else np.nan

    if not rows:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": {"name": "day-clustered t of slope of next-day excess return on forecast",
                                 "value": None, "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
                "supporting_check": {"name": "mean next-day excess return over forecast > 0 bars",
                                     "value": None, "passed": None},
                "counts": {"bars with forecast > 0": 0},
                "decided_by": "No bars in the record: fewer than 100 bars with forecast > 0.",
                "reading": "none"}
    data = pd.concat(rows, ignore_index=True)

    # ---------- situation check ----------
    active = data[data["forecast"].fillna(0) != 0]
    n_active = len(active)
    if n_active > 0:
        ok = (active["raw"] > 0) & (active["forecast"] > 0)
        agreement = float(ok.sum()) / n_active
    else:
        agreement = None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The situation is a positive raw scaled one-day rise (recorded last_history_value, recomputed from "
               "closes inside the window where missing) with a long forecast; the slope's t uses OLS with "
               "standard errors clustered by UTC day (scores summed per day, G/(G-1) correction); the coin's mean "
               "daily return is over all its bars' next-day returns in all windows; the 100-bar minimum counts "
               "forecast > 0 bars with a next-day return.")

    mm_name = "day-clustered t of the slope of next-day excess return on forecast (forecast > 0 bars, pooled)"
    thr = "t >= 2 with positive mean excess return confirms; t <= -2 rejects; otherwise inconclusive; min 100 bars"

    if not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": agreement, "passed": False},
                "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
                "supporting_check": None,
                "counts": {"active bars": int(n_active)},
                "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on a positive "
                               "scaled one-day rise, so the config does not trade the plan's situation on its side."
                               if n_active > 0 else "The record has no active bars to compare with the situation."),
                "reading": reading}

    # ---------- main measure ----------
    s = data[(data["forecast"] > 0) & data["next_ret"].notna()].copy()
    s["excess"] = s["next_ret"] - s["coin"].map(coin_rets)
    s = s[s["excess"].notna() & s["day"].notna()]
    n = int(len(s))
    n_days = int(s["day"].nunique()) if n else 0

    slope = None
    tstat = None
    mean_ex = float(s["excess"].mean()) if n else None
    if n >= 3 and s["forecast"].nunique() > 1 and n_days > 1:
        X = np.column_stack([np.ones(n), s["forecast"].values])
        y = s["excess"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        scores = pd.DataFrame(X * e[:, None], index=s.index)
        scores["day"] = s["day"].values
        g = scores.groupby("day").sum().values
        G = g.shape[0]
        meat = g.T @ g
        V = XtX_inv @ meat @ XtX_inv * (G / (G - 1.0))
        se = float(np.sqrt(V[1, 1]))
        slope = float(beta[1])
        tstat = float(slope / se) if se > 0 else None

    sup_pass = (mean_ex > 0) if mean_ex is not None else None

    if n < 100:
        status = "not observable"
        decided = f"Only {n} bars with forecast > 0, fewer than the plan's minimum of 100."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, which meets neither the confirm nor the reject rule."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean next-day excess return is positive."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger scaled rises are followed by smaller next-day excess returns."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean next-day excess return is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": mm_name,
                         "value": slope,
                         "statistic": ({"name": "day-clustered OLS slope t", "value": tstat}
                                       if tstat is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean next-day excess return over forecast > 0 bars",
                             "value": mean_ex, "passed": sup_pass},
        "counts": {"bars with forecast > 0": n, "days": n_days},
        "decided_by": decided,
        "reading": reading,
    }
