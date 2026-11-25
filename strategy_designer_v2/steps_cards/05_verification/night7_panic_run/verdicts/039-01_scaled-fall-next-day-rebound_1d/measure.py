import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- collect per-bar data ----------
    frames = []
    coin_rets = {}
    for coin, wins in bars.items():
        all_r = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0          # inside the window only
            prev_r = close / close.shift(1) - 1.0
            all_r.append(nxt.dropna().values)
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            # sign of raw value = sign of the 1-day return; recompute from prices where not recorded
            raw_sign = np.sign(raw).where(raw.notna(), np.sign(prev_r))
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            frames.append(pd.DataFrame({
                "coin": coin,
                "window": w,
                "day": ts.dt.floor("D"),
                "forecast": pd.to_numeric(d["forecast"], errors="coerce"),
                "raw_sign": raw_sign,
                "next_ret": nxt,
            }))
        coin_rets[coin] = np.concatenate(all_r) if all_r else np.array([])

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"down-day cases": 0, "distinct days": 0},
            "decided_by": "No bars in the record.", "reading": "none",
        }

    data = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    active = data[data["forecast"].notna() & (data["forecast"] != 0)]
    n_active = len(active)
    if n_active > 0:
        ok = (active["raw_sign"] < 0) & (active["forecast"] > 0)
        agreement = float(ok.mean())
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are down days (raw scaled return < 0) with a long "
                           "forecast, so the config does not take the plan's situation on its expected long side."),
            "reading": "Situation = raw component value < 0 (recomputed from the close-to-close return where not recorded); expected side long.",
        }

    # ---------- cases ----------
    coin_mean = {c: (float(np.mean(r)) if len(r) else np.nan) for c, r in coin_rets.items()}
    cases = data[(data["forecast"] > 0) & data["next_ret"].notna() & data["day"].notna()].copy()
    cases["excess"] = cases["next_ret"] - cases["coin"].map(coin_mean)
    cases = cases[cases["excess"].notna()]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique())
    counts = {"down-day cases": n_cases, "distinct days": n_days}

    # ---------- main measure: slope with day-clustered t ----------
    slope = None
    t_slope = None
    if n_cases >= 3:
        x = cases["forecast"].values.astype(float)
        y = cases["excess"].values.astype(float)
        X = np.column_stack([np.ones_like(x), x])
        XtX_inv = np.linalg.pinv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        slope = float(beta[1])
        scores = pd.DataFrame(X * e[:, None], columns=["a", "b"])
        scores["day"] = cases["day"].values
        S = scores.groupby("day")[["a", "b"]].sum().values
        G = S.shape[0]
        meat = S.T @ S
        k = 2
        corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - k)) if G > 1 else np.nan
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if np.isfinite(V[1, 1]) and V[1, 1] > 0 else np.nan
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None

    # ---------- supporting check: top fifth by coin ----------
    tops = []
    for c, g in cases.groupby("coin"):
        if len(g) == 0:
            continue
        q = np.quantile(g["forecast"].values, 0.8)
        tops.append(g[g["forecast"] >= q])
    top = pd.concat(tops) if tops else cases.iloc[0:0]
    top_mean = float(top["excess"].mean()) if len(top) else None
    top_pass = (top_mean is not None) and (top_mean > 0)
    counts["top-fifth cases"] = int(len(top))

    main = {
        "name": "slope of next-day excess return on forecast (forecast > 0)",
        "value": slope,
        "statistic": {"name": "slope t, residuals summed per day (day-clustered)", "value": t_slope} if t_slope is not None else None,
        "threshold": "confirm if t >= 2 (with top-fifth mean > 0); reject if t <= -2",
    }
    support = {"name": "mean next-day excess return, top fifth of forecast by coin",
               "value": top_mean, "passed": bool(top_pass) if top_mean is not None else None}

    reading = ("Excess = next-day close-to-close return minus the coin's mean 1-day return over all its windows; "
               "the slope's t uses day-clustered standard errors (each day's score summed across coins); "
               "the top fifth is the coin's cases with forecast at or above its 80th percentile, pooled across coins; "
               "a 'down-day case' is a bar with forecast > 0 and a next-day return in the same window.")

    # ---------- decision ----------
    if n_cases < 300 or n_days < 200:
        status = "not observable"
        decided_by = (f"Minimum counts not reached: {n_cases} down-day cases (need 300) on "
                      f"{n_days} distinct days (need 200).")
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and top_pass:
        status = "confirmed"
        decided_by = "Confirm: the slope's t is 2 or more and the top-fifth mean excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "Reject: the slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "Inconclusive: a confirming slope (t >= 2) whose top-fifth mean excess return is not above 0."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
